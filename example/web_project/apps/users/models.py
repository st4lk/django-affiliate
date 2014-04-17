# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models
from affiliate.models import AbstractAffiliate, AbstractAffiliateCount


class User(AbstractUser):

    def __unicode__(self):
        return self.username


class Affiliate(AbstractAffiliate):
    user = models.ForeignKey(User, related_name='affiliates')


class AffiliateCount(AbstractAffiliateCount):
    pass
