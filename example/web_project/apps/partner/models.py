# -*- coding: utf-8 -*-
import logging
from django.db import models
from django.conf import settings
from affiliate.models import AbstractAffiliate, AbstractAffiliateCount,\
    AbstractAffiliateBanner, AbstractPaymentRequest

l = logging.getLogger(__name__)


class Affiliate(AbstractAffiliate):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    @classmethod
    def create_affiliate(cls, user):
        aff = cls(user=user)
        aff.aid = aff.generate_aid()
        l.info("Creating affiliate #{0} for user {1}"
            .format(aff.aid, user))
        aff.save()


class AffiliateCount(AbstractAffiliateCount):
    pass


class AffiliateBanner(AbstractAffiliateBanner):
    pass


class PaymentRequest(AbstractPaymentRequest):
    pass
