# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class BaseAffiliateAdmin(admin.ModelAdmin):
    list_display = "aid", "balance", "total_payed", "total_payments_count"


class BaseAffiliateCountAdmin(admin.ModelAdmin):
    list_display = "affiliate", "date", "total_views", "unique_visitors"


class BaseAffiliateBannerAdmin(admin.ModelAdmin):
    list_display = "image", "get_width", "get_height", "enabled"
    list_editable = "enabled",

    def get_width(self, obj):
        return obj.image.width
    get_width.short_description = _("Width")

    def get_height(self, obj):
        return obj.image.height
    get_height.short_description = _("Height")
