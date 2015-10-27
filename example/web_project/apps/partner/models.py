# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings


class AffiliateTransaction(models.Model):
    affiliate = models.ForeignKey('affiliate.Affiliate')
    product = models.ForeignKey('products.Product')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    bought_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    reward_amount = models.DecimalField(max_digits=5, decimal_places=2)
    reward_percentage = models.BooleanField()
    reward = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
