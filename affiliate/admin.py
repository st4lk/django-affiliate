# -*- coding: utf-8 -*-
from django.contrib import admin


class BaseAffiliateAdmin(admin.ModelAdmin):
    list_display = "aid", "balance", "total_payed", "total_payments_count"


class BaseAffiliateCountAdmin(admin.ModelAdmin):
    list_display = "affiliate", "date", "total_views", "unique_visitors"
