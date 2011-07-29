from models import *
from django.conf import settings
from textprocessors.html2plaintext import html2plaintext
try:
    import cPickle as pickle
except ImportError:
    import pickle
import base64
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from misc.lib import *

def notify(users, subject, context, template='notify/default.html', from_email=settings.DEFAULT_FROM_EMAIL, queue=False):
    """
        users = User object / email or list of User objects / emails
        subject = string
        context = dictionary for use in the template
                  (it will be updated with {'user': user} if user objects are passed to the function)
        template = alternative email template
        from_email
        queue = True if email is sent right away, otherwise it's stored in the db

        returns False if an error occured when sending the email
    """
    from massmail.models import Queue, QueueEmail # to avoid a circular import


    if type(users) is not list:
        if type(users) is not tuple:
            users = [users]


    for user in users:
        # make some context variables available in the template
        # !!! the context preprocessors are not run since this is not a view function !!!
        # this is done inside the loop to avoid pickling and storing unneeded data
        #new_context = context.copy()
        new_context = context
        new_context.update({
            'MEDIA_URL': settings.MEDIA_URL,
            'hostname': settings.SITE_ATTRIBUTES['hostname'],
            'sitename': settings.SITE_ATTRIBUTES['name']
        })
        
        if new_context['hostname'] == 'http://localhost':
            dbg("Localhost debug:")
            dbg(settings.SITE_ATTRIBUTES)

        if type(user) in (str, unicode):
            # it's an email, not a User object
            email = user
        else:
            # add the user to the context
            new_context.update({
                'user': user,
            })
            email = user.email

        # construct and send the multi-part text/html email
        html = render_to_string(template, new_context)

        # if queued, store the email in the db
        if queue:
            q, created = Queue.objects.get_or_create(subject = subject, body = html, status = '1', hostname=new_context['hostname'])
            qe = QueueEmail(to_email = email, queue = q)
            qe.save()

        else:
            #q, created = Queue.objects.get_or_create(subject = subject, body = html, status = '4', hostname=new_context['hostname'])
            
            # for local development define it in local_settings.py
            if hasattr(settings, 'DBG_EMAIL'):
                email = settings.DBG_EMAIL

            text = html2plaintext(html)
            msg = EmailMultiAlternatives(subject, text, from_email, [email])
            msg.attach_alternative(html, "text/html")
            try:
                msg.send()
            except Exception, e:
                print e
                return False

        # store in the db if it's an user
        if type(user) not in (str, unicode):
            n = Notification(user=user, subject=subject, context=base64.b64encode(pickle.dumps(context, -1)), template=template)
            # the contex dict can be retrieved like this: pickle.loads(base64.b64decode(log_obj.msg)) where log_obj is a Log instance
            n.save()

    return True

def set_user_notification(user, type, name, name_plural='', link='', link_aggregated='', aggregate=True, model=None, object=None):
    """
    user = User object
    type = string describing the notification's type (used for aggregation)
    name = displayed name
    name_plural = displayed name if aggregated (defaults to name + 's')
    link = the notification's link, if any
    link_aggregated = if you need a different link for agregated notifications use this
    aggregate =  boolean, defaults to True
    model = associate the notification with this model (so we can identify and delete it later)
    object = associate the notification with this object (so we can identify and delete it later)
    """

    if not isinstance(user, User):
        return

    content_type = None # derived from model or object
    object_id = None # derived from object
    if model:
        content_type = ContentType.objects.get_for_model(model)
    if object:
        object_id = object.id
        content_type = ContentType.objects.get_for_model(object)

    if not name_plural:
        name_plural = '%ss' % name

    UserNotification.objects.create(user=user, type=type, name=name, name_plural=name_plural, link=link, link_aggregated=link_aggregated, aggregate=aggregate, content_type=content_type, object_id=object_id)

def delete_user_notification(user, type, model=None, object=None):
    """
    user = User object
    type = string describing the notification's type
    model = model associated with this notification
    object = object associated with this notification
    """
    content_type = None # derived from model or object
    object_id = None # derived from object
    if model:
        content_type = ContentType.objects.get_for_model(model)
    if object:
        object_id = object.id
        content_type = ContentType.objects.get_for_model(object)
    
    for un in UserNotification.objects.filter(user=user, type=type, content_type=content_type, object_id=object_id).all():
        un.delete()

