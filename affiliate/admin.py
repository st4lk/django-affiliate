# -*- coding: utf-8 -*-
from django.contrib import admin


class BaseAffiliateAdmin(admin.ModelAdmin):
    list_display = "aid", "balance", "count_payments"


class BaseAffiliateCountAdmin(admin.ModelAdmin):
    list_display = "affiliate", "count_views", "date", "ip"
