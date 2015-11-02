from __future__ import print_function, division, absolute_import, unicode_literals
import logging
from decimal import Decimal as D
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from django.conf import settings
from . import app_settings
from .utils import add_affiliate_code

l = logging.getLogger(__name__)


class AffiliateManager(models.Manager):
    def create_affiliate(self, user, **extra_fields):
        affiliate = self.model(user=user, **extra_fields)
        affiliate.save()
        return affiliate


class AbstractAffiliate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("user"))
    reward_amount = models.DecimalField(_("reward amount"), max_digits=16,
        decimal_places=5, default=app_settings.REWARD_AMOUNT)
    reward_percentage = models.BooleanField(_('in percent'),
        default=app_settings.REWARD_PERCENTAGE)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    objects = AffiliateManager()

    class Meta:
        abstract = True
        verbose_name = _("affiliate")
        verbose_name_plural = _("affiliates")

    def __str__(self):
        return six.text_type(self.aid)

    @property
    def aid(self):
        return self.pk

    def exists(self):
        return True

    def build_absolute_affiliate_uri(self, request, location=None):
        uri = request.build_absolute_uri(self.build_affiliate_url(location))
        return add_affiliate_code(uri, self.pk)

    def build_affiliate_url(self, location=None):
        location = location or app_settings.DEFAULT_LINK
        return add_affiliate_code(location, self.pk)

    def calc_affiliate_reward(self, total_price):
        if self.reward_percentage:
            return total_price * (self.reward_amount / D('100'))
        else:
            return self.reward_amount

    @property
    def quantized_reward_amount(self):
        return self.reward_amount.quantize(D('0.01'))


class NoAffiliate(object):
    is_active = False

    def exists(self):
        return False
