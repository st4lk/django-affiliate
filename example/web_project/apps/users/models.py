# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from apps.partner.models import Affiliate


class User(AbstractUser):

    def __unicode__(self):
        return self.username

# Create affiliate for each new user
post_save.connect(Affiliate.create_affiliate, sender=User)
