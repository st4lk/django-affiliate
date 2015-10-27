# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models

class AffiliateTransactionAdmin(admin.ModelAdmin):
    list_display = ('affiliate', 'product', 'price', 'bought_by',
        'reward_amount', 'reward_percentage', 'reward')


admin.site.register(models.AffiliateTransaction, AffiliateTransactionAdmin)
