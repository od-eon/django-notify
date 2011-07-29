from models import *
from django.contrib import admin

class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ['id', '__unicode__', 'date'] 
#    list_filter = ['type', 'content_type']
    list_filter = ['type', 'content_type', 'user']


class NotificationAdmin(admin.ModelAdmin):
    list_filter = ['date', 'user']
    list_display = ['subject', 'date', 'user'] 

admin.site.register(Notification, NotificationAdmin)
admin.site.register(UserNotification, UserNotificationAdmin)

