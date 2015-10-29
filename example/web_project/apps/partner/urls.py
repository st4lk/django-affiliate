# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = patterns('',
    url(r'^$',
        login_required(views.AffiliateView.as_view()), name='affiliate'),
)
