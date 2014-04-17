# -*- coding: utf-8 -*-
from django.db import models
from .queryset import AffiliateCountQuerySet


class AffiliateCountManager(models.Manager):
    def get_query_set(self):
        return AffiliateCountQuerySet(self.model)

    def __getattr__(self, attr, *args):
        # see https://code.djangoproject.com/ticket/15062 for details
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)
