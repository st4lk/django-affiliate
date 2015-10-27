# -*- coding: utf-8 -*-
import urlparse
import urllib
from . import settings as affiliate_settings
try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model as django_get_model

    def get_model(self, app_label, model_name=None):
        if model_name is None:
            app_label, model_name = app_label.split('.')
        return django_get_model(app_label, model_name)


def get_affiliate_model():
    return get_model(affiliate_settings.AFFILIATE_MODEL)


def add_affiliate_code(url, aid_code):
    parsed = urlparse.urlparse(str(url))
    query = dict(urlparse.parse_qsl(parsed.query))
    query.update({affiliate_settings.PARAM_NAME: str(aid_code)})
    url_parts = list(parsed)
    url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(url_parts)


def remove_affiliate_code(url):
    parsed = urlparse.urlparse(str(url))
    query = dict(urlparse.parse_qsl(parsed.query))
    query.pop(affiliate_settings.PARAM_NAME, None)
    url_parts = list(parsed)
    url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(url_parts)
