# -*- coding: utf-8 -*-
from django.db.models.query import QuerySet
from django.db.models import F


class AffiliateCountQuerySet(QuerySet):

    def incr_count_views(self, aid, date, ip_new=False):
        kw = dict(total_views=F('total_views')+1)
        if ip_new:
            kw['unique_visitors'] = F('unique_visitors')+1
        return self.filter(affiliate=aid, date=date).update(**kw)


class AffiliateBannerQuerySet(QuerySet):

    def enabled(self):
        return self.filter(enabled=True)
