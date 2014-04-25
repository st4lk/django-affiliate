# -*- coding: utf-8 -*-
from django.contrib import admin
from affiliate.admin import BaseAffiliateAdmin, BaseAffiliateCountAdmin,\
    BaseAffiliateBannerAdmin, BasePaymentRequestAdmin
from .models import Affiliate, AffiliateCount, AffiliateBanner,\
    PaymentRequest


class AffiliateAdmin(BaseAffiliateAdmin):
    pass


class AffiliateCountAdmin(BaseAffiliateCountAdmin):
    pass


class AffiliateBannerAdmin(BaseAffiliateBannerAdmin):
    pass


class PaymentRequestAdmin(BasePaymentRequestAdmin):
    pass


admin.site.register(Affiliate, AffiliateAdmin)
admin.site.register(AffiliateCount, AffiliateCountAdmin)
admin.site.register(AffiliateBanner, AffiliateBannerAdmin)
admin.site.register(PaymentRequest, PaymentRequestAdmin)
