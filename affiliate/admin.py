# -*- coding: utf-8 -*-
from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.util import unquote
from django.http import HttpResponseRedirect
from .abstract_models import NotEnoughMoneyError


class BaseAffiliateAdmin(admin.ModelAdmin):
    list_display = ("aid", "balance", "total_payed", "total_payments_count",
        "created_at")


class BaseAffiliateStatsAdmin(admin.ModelAdmin):
    list_display = ("affiliate", "date", "total_views", "unique_visitors",
        "payments_count", "payments_amount", "rewards_amount")


class BaseAffiliateBannerAdmin(admin.ModelAdmin):
    list_display = "image", "get_width", "get_height", "enabled"
    list_editable = "enabled",

    def get_width(self, obj):
        return obj.image.width
    get_width.short_description = _("Width")

    def get_height(self, obj):
        return obj.image.height
    get_height.short_description = _("Height")


class BaseWithdrawRequestAdmin(admin.ModelAdmin):
    list_display = "affiliate", "amount", "status", "created_at"
    change_form_template = 'admin/request_change_form.html'
    readonly_fields = "payed_at", "status", "amount",

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        resp = super(BaseWithdrawRequestAdmin, self).change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)
        if request.method == 'POST' and '_affiliate_payed' in request.POST\
                and isinstance(resp, HttpResponseRedirect):
            # assert, that HttpResponseRedirect means successfull operation
            payment_request = self.get_object(request, unquote(object_id))
            try:
                payment_request.payment_made()
                msg = _('Payment successfully marked as payed')
                msg_level = messages.INFO
            except NotEnoughMoneyError:
                msg = _('Payment failed: not enough money in affiliate account')
                msg_level = messages.ERROR
            self.message_user(request, msg, level=msg_level)
        return resp
