# -*- coding: utf-8 -*-
from django.db.models.query import QuerySet
from django.db.models import F


class AffiliateCountQuerySet(QuerySet):

    def incr_count_views(self, aid, date, ip):
        return self.filter(affiliate=aid, date=date, ip=ip).update(
            count_views=F('count_views')+1)
