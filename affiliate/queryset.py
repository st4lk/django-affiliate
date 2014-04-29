# -*- coding: utf-8 -*-
from datetime import timedelta
from django.db.models.query import QuerySet
from django.db.models import F
from django.utils.timezone import now


class AffiliateStatsQuerySet(QuerySet):

    def incr_count_views(self, aid, date, ip_new=False):
        kw = dict(total_views=F('total_views')+1)
        if ip_new:
            kw['unique_visitors'] = F('unique_visitors')+1
        return self.filter(affiliate=aid, date=date).update(**kw)

    def for_last_days(self, days):
        # TODO: for MySQL add FORCE INDEX (affiliate_id)
        days_ago = now() - timedelta(days=days)
        return self.filter(date__gte=days_ago).order_by("-date")


class WithdrawRequestQuerySet(QuerySet):
    def pending(self):
        return self.filter(status=self.model.PAY_STATUS.pending)


class AffiliateBannerQuerySet(QuerySet):

    def enabled(self):
        return self.filter(enabled=True)
