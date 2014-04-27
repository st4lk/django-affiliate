# -*- coding: utf-8 -*-
from django.contrib import admin
from affiliate.admin import BaseAffiliateAdmin, BaseAffiliateStatsAdmin,\
    BaseAffiliateBannerAdmin, BasePaymentRequestAdmin
from .models import Affiliate, AffiliateStats, AffiliateBanner,\
    PaymentRequest


class AffiliateAdmin(BaseAffiliateAdmin):
    pass


class AffiliateStatsAdmin(BaseAffiliateStatsAdmin):
    pass


class AffiliateBannerAdmin(BaseAffiliateBannerAdmin):
    pass


class PaymentRequestAdmin(BasePaymentRequestAdmin):
    pass


admin.site.register(Affiliate, AffiliateAdmin)
admin.site.register(AffiliateStats, AffiliateStatsAdmin)
admin.site.register(AffiliateBanner, AffiliateBannerAdmin)
admin.site.register(PaymentRequest, PaymentRequestAdmin)
