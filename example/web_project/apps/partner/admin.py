# -*- coding: utf-8 -*-
from django.contrib import admin
from affiliate.admin import BaseAffiliateAdmin, BaseAffiliateStatsAdmin,\
    BaseAffiliateBannerAdmin, BaseWithdrawRequestAdmin
from .models import Affiliate, AffiliateStats, AffiliateBanner,\
    WithdrawRequest


class AffiliateAdmin(BaseAffiliateAdmin):
    pass


class AffiliateStatsAdmin(BaseAffiliateStatsAdmin):
    pass


class AffiliateBannerAdmin(BaseAffiliateBannerAdmin):
    pass


class WithdrawRequestAdmin(BaseWithdrawRequestAdmin):
    pass


admin.site.register(Affiliate, AffiliateAdmin)
admin.site.register(AffiliateStats, AffiliateStatsAdmin)
admin.site.register(AffiliateBanner, AffiliateBannerAdmin)
admin.site.register(WithdrawRequest, WithdrawRequestAdmin)
