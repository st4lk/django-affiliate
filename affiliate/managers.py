# -*- coding: utf-8 -*-
from django.db import models
from .queryset import AffiliateCountQuerySet, AffiliateBannerQuerySet,\
    PaymentRequestQuerySet


class AffiliateCountManager(models.Manager):
    def get_query_set(self):
        return AffiliateCountQuerySet(self.model)

    def __getattr__(self, attr, *args):
        # see https://code.djangoproject.com/ticket/15062 for details
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)


class AffiliateBannerManager(models.Manager):
    def get_query_set(self):
        return AffiliateBannerQuerySet(self.model)

    def __getattr__(self, attr, *args):
        # see https://code.djangoproject.com/ticket/15062 for details
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)


class PaymentRequestManager(models.Manager):
    def get_query_set(self):
        return PaymentRequestQuerySet(self.model)

    def __getattr__(self, attr, *args):
        # see https://code.djangoproject.com/ticket/15062 for details
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)
