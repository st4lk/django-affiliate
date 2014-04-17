# -*- coding: utf-8 -*-
from django.contrib import admin
from affiliate.admin import BaseAffiliateAdmin, BaseAffiliateCountAdmin
from .models import Affiliate, AffiliateCount


class AffiliateAdmin(BaseAffiliateAdmin):
    pass


class AffiliateCountAdmin(BaseAffiliateCountAdmin):
    pass


admin.site.register(Affiliate, AffiliateAdmin)
admin.site.register(AffiliateCount, AffiliateCountAdmin)
