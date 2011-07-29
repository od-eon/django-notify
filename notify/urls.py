from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'notify.views',
    url(r'^(?P<template>[^/]+)/$', 'show_template'),
)

