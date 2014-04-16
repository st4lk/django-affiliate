# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from apps.news import views

urlpatterns = patterns('',
    url(r'^$', views.NewsListView.as_view(), name='list'),
)
