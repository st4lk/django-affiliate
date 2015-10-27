# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models

@admin.register(models.AffiliateTransaction)
class AffiliateTransactionAdmin(admin.ModelAdmin):
    list_display = ('affiliate', 'product', 'price', 'bought_by',
        'reward_amount', 'reward_percentage', 'reward')
