# -*- coding: utf-8 -*-
import logging
from django.db import models
from django.conf import settings
from affiliate.models import AbstractAffiliate, AbstractAffiliateCount

l = logging.getLogger(__name__)


class Affiliate(AbstractAffiliate):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='affiliates')

    @classmethod
    def create_affiliate(cls, sender, instance, created, **kwargs):
        if created:
            aff = cls(user=instance)
            aff.aid = aff.generate_aid()
            l.info("Creating affiliate #{0} for user {1}"
                .format(aff.aid, instance))
            aff.save()


class AffiliateCount(AbstractAffiliateCount):
    pass
