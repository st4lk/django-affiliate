# -*- coding: utf-8 -*-
from decimal import Decimal as D
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractAffiliate(models.Model):
    aid = models.CharField(_("Affiliate code"), max_length=150,
        unique=True)
    count_views = models.IntegerField(_("Page views count"), default=0)
    count_payments = models.IntegerField(_("Payments count"), default=0)
    balance = models.DecimalField(_("Affiliate balance"), max_digits=6,
        decimal_places=2, default=D("0.0"))

    class Meta:
        abstract = True
        verbose_name = _("Affiliate")
        verbose_name_plural = _("Affiliates")

    def __unicode__(self):
        return self.aid

    def generate_aid(self):
        pass
