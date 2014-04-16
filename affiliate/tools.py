# -*- coding: utf-8 -*-
from urlparse import urlparse, parse_qs
from urllib import urlencode
from django.conf import settings


def get_affiliate_param_name():
    return getattr(settings, "AFFILIATE_PARAM_NAME", 'aid')


def add_affiliate_code(url, aid):
    parsed = urlparse(str(url))
    params = parse_qs(parsed.query)
    aff_param_name = get_affiliate_param_name()
    params.update({aff_param_name: [str(aid)]})
    return "?".join((parsed.path, urlencode(params, doseq=True)))


def remove_affiliate_code(url):
    parsed = urlparse(str(url))
    params = parse_qs(parsed.query)
    aff_param_name = get_affiliate_param_name()
    params.pop(aff_param_name)
    return "?".join((parsed.path, urlencode(params, doseq=True)))
