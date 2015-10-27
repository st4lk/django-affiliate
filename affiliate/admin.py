# -*- coding: utf-8 -*-
from django.contrib import admin
from .tools import get_model
from . import settings as affiliate_settings

Affiliate = get_model(affiliate_settings.AFFILIATE_MODEL)


@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'is_active', 'reward_amount',
        'reward_percentage', 'created_at')
