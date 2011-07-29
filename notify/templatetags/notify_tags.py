from django import template
from notify.models import *

register = template.Library()

@register.inclusion_tag('notify/profile_notifications.html')
def notifications(user):
    """
    shows all the current notifications for the given user
    {% profile_notifications %}
    """
    result = []
    types = {}
    for pn in ProfileNotification.objects.filter(user=user).order_by('-date').all():
        types[pn.type] = True
    for type in types.keys():
        # single entries
        for pn in ProfileNotification.objects.filter(user=user, type=type, aggregate=False).all():
            result.append({
                'type': pn.type,
                'name': pn.name,
                'link': pn.link,
            })
        # do the aggregation
        pn_aggr = ProfileNotification.objects.filter(user=user, type=type, aggregate=True).all()
        if pn_aggr:
            result.append({
                'type': pn_aggr[0].type,
                'name': '%d %s' % (len(pn_aggr), pn_aggr[0].name) if len(pn_aggr) == 1 else '%d %s' % (len(pn_aggr), pn_aggr[0].name_plural),
                'link': pn_aggr[0].link_aggregated if pn_aggr[0].link_aggregated and len(pn_aggr) > 1 else pn_aggr[0].link,
            })

    return {'notifications': result}


@register.inclusion_tag('notify/profile_notifications.html')
def notifications_listing(notifications_list):
    """
    Display 'notifications_listing'.
    """
    return {'notifications': notifications_list}
