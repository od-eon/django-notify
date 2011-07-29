from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Notification(models.Model):
    user = models.ForeignKey(User)
    subject = models.TextField()
    context = models.TextField() # pickled dict
    template = models.TextField()
    date = models.DateField(auto_now_add=True)

class UserNotification(models.Model):
    user = models.ForeignKey(User)
    type = models.TextField()
    name = models.TextField()
    name_plural = models.TextField()
    link = models.TextField(blank=True)
    link_aggregated = models.TextField(blank=True)
    aggregate = models.BooleanField(default=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey()
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        str = u''
        if self.user:
            str += self.user.username + u' '
        str += u'[%s] "%s" <%s>' % (self.type, self.name, self.link)
        return str
