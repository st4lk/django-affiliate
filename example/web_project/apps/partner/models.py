# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from affiliate.models import AbstractAffiliate, AbstractAffiliateCount


class Affiliate(AbstractAffiliate):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='affiliates')


class AffiliateCount(AbstractAffiliateCount):
    pass
