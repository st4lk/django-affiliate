# -*- coding: utf-8 -*-
from django.contrib import admin


class BaseAffiliateAdmin(admin.ModelAdmin):
    list_display = "aid", "balance", "count_views", "count_payments"
