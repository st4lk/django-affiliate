from __future__ import print_function, division, absolute_import, unicode_literals
import logging
from decimal import Decimal as D
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from django.conf import settings
from . import settings as affiliate_settings
from .utils import add_affiliate_code

l = logging.getLogger(__name__)


class AffiliateManager(models.Manager):
    def create_affiliate(self, user, **extra_fields):
        affiliate = self.model(user=user, **extra_fields)
        affiliate.save()
        return affiliate


class AbstractAffiliate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("User"))
    reward_amount = models.DecimalField(_("reward amount"), max_digits=5,
        decimal_places=2, default=affiliate_settings.REWARD_AMOUNT)
    reward_percentage = models.BooleanField(_('in percent'),
        default=affiliate_settings.REWARD_PERCENTAGE)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    objects = AffiliateManager()

    class Meta:
        abstract = True
        verbose_name = _("Affiliate")
        verbose_name_plural = _("Affiliates")

    def __str__(self):
        return six.text_type(self.aid)

    @property
    def aid(self):
        return self.pk

    def exist(self):
        return True

    def build_absolute_affiliate_uri(self, request, location=None):
        location = location or affiliate_settings.DEFAULT_LINK
        uri = request.build_absolute_uri(location)
        return add_affiliate_code(uri, self.pk)

    def calc_affiliate_reward(self, total_price):
        if self.reward_percentage:
            return total_price * (self.reward_amount / D('100'))
        else:
            return self.reward_amount


class NoAffiliate(object):
    is_active = False

    def exist(self):
        return False


class Affiliate(AbstractAffiliate):

    class Meta:
        swappable = 'AFFILIATE_AFFILIATE_MODEL'
