# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include("apps.users.urls", namespace="users")),
    url(r'^$', include("apps.products.urls", namespace="products")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
