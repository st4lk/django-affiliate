# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from apps.partner.models import Affiliate


class User(AbstractUser):

    def __unicode__(self):
        return self.username

    def make_affiliate(self):
        Affiliate.create_affiliate(self)
