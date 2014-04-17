# -*- coding: utf-8 -*-
from decimal import Decimal as D
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .managers import AffiliateCountManager


class AbstractAffiliate(models.Model):
    aid = models.CharField(_("Affiliate code"), max_length=150,
        unique=True, primary_key=True)
    total_payments_count = models.IntegerField(_("Total payments count"),
        default=0)
    total_payed = models.DecimalField(_("Total payed to affiliate"),
        max_digits=6, decimal_places=2, default=D("0.0"))
    balance = models.DecimalField(_("Affiliate balance"), max_digits=6,
        decimal_places=2, default=D("0.0"))

    class Meta:
        abstract = True
        verbose_name = _("Affiliate")
        verbose_name_plural = _("Affiliates")

    def __unicode__(self):
        return self.aid

    def generate_aid(self):
        try:
            last_aid = self.objects.order_by("-aid")[0].aid
        except IndexError:
            last_aid = "100"
        return str(int(last_aid) + 1)


class AbstractAffiliateCount(models.Model):
    # don't create additional index on fk, as we've already declared
    # compound index, that is started with affiliate
    affiliate = models.ForeignKey(settings.AFFILIATE_MODEL, db_index=False)
    count_views = models.IntegerField(_("Page views count"), default=0)
    count_payments = models.IntegerField(_("Payments count"), default=0)
    ip = models.IPAddressField()
    date = models.DateField(_("Date"), auto_now_add=True)

    objects = AffiliateCountManager()

    class Meta:
        abstract = True
        # TODO would be great to have following fields as compound primary key
        # look https://code.djangoproject.com/wiki/MultipleColumnPrimaryKeys
        # and https://code.djangoproject.com/ticket/373
        index_together = [
            ["affiliate", "date", "ip"],
        ]
        verbose_name = _("Affiliate count")
        verbose_name_plural = _("Affiliate counts")
        ordering = "-id",
