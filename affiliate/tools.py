# -*- coding: utf-8 -*-
from urlparse import urlparse, parse_qs
from urllib import urlencode
from datetime import datetime
from django.conf import settings
from django.db.models.loading import get_model


AFFILIATE_MODEL = settings.AFFILIATE_MODEL
AFFILIATE_COUNT_MODEL = settings.AFFILIATE_COUNT_MODEL


def get_affiliate_model():
    return get_model(*AFFILIATE_MODEL.split("."))


def get_affiliatestats_model():
    return get_model(*AFFILIATE_COUNT_MODEL.split("."))


def get_affiliate_param_name():
    return getattr(settings, "AFFILIATE_PARAM_NAME", 'aid')


def add_affiliate_code(url, aid_code):
    parsed = urlparse(str(url))
    params = parse_qs(parsed.query)
    aff_param_name = get_affiliate_param_name()
    params.update({aff_param_name: [str(aid_code)]})
    return "?".join((parsed.path, urlencode(params, doseq=True)))


def remove_affiliate_code(url):
    parsed = urlparse(str(url))
    params = parse_qs(parsed.query)
    aff_param_name = get_affiliate_param_name()
    params.pop(aff_param_name)
    return "?".join((parsed.path, urlencode(params, doseq=True)))


def get_seconds_day_left(now=None):
    now = now or datetime.now()
    end_day = datetime(year=now.year, month=now.month, day=now.day, hour=23,
        minute=59, second=59)
    return (end_day-now).seconds
