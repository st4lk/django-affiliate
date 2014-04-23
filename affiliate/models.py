# -*- coding: utf-8 -*-
from decimal import Decimal as D
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .managers import AffiliateCountManager

START_AID = getattr(settings, 'AFFILIATE_START_AID', "100")


class AbstractAffiliate(models.Model):
    aid = models.CharField(_("Affiliate code"), max_length=150,
        unique=True, primary_key=True)
    total_payments_count = models.IntegerField(_("Total payments count"),
        default=0)
    total_payed = models.DecimalField(_("Total payed to affiliate"),
        max_digits=6, decimal_places=2, default=D("0.0"))
    balance = models.DecimalField(_("Affiliate balance"), max_digits=6,
        decimal_places=2, default=D("0.0"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        abstract = True
        verbose_name = _("Affiliate")
        verbose_name_plural = _("Affiliates")

    def __unicode__(self):
        return self.aid

    def generate_aid(self):
        try:
            last_aid = self._default_manager.order_by("-aid")[0].aid
        except IndexError:
            last_aid = START_AID
        return str(int(last_aid) + 1)

    @classmethod
    def create_affiliate(cls, *args, **kwargs):
        # Override this method to define your custom creation logic
        raise NotImplementedError()


class AbstractAffiliateCount(models.Model):
    # don't create additional index on fk, as we've already declared
    # compound index, that is started with affiliate
    affiliate = models.ForeignKey(settings.AFFILIATE_MODEL, db_index=False)
    unique_visitors = models.IntegerField(_("Unique visitors count"),
        default=0)
    total_views = models.IntegerField(_("Total page views count"),
        default=0)
    count_payments = models.IntegerField(_("Payments count"), default=0)
    date = models.DateField(_("Date"), auto_now_add=True)

    objects = AffiliateCountManager()

    class Meta:
        abstract = True
        # TODO would be great to have following fields as compound primary key
        # look https://code.djangoproject.com/wiki/MultipleColumnPrimaryKeys
        # and https://code.djangoproject.com/ticket/373
        unique_together = [
            ["affiliate", "date"],
        ]
        verbose_name = _("Affiliate count")
        verbose_name_plural = _("Affiliate counts")
        ordering = "-id",
