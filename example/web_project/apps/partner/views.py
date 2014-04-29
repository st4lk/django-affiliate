# -*- coding: utf-8 -*-
from affiliate.views import AffiliateBaseView
from .models import AffiliateBanner


class AffiliateView(AffiliateBaseView):
    template_name = "partner/affiliate.html"

    def get_affiliate_banner_model(self):
        return AffiliateBanner
