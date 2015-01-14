from datetime import datetime
import logging

from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.cache import get_cache
from .tools import get_affiliate_param_name, remove_affiliate_code,\
    get_seconds_day_left, get_affiliate_model, get_affiliatestats_model
from relish.helpers.request import get_client_ip

l = logging.getLogger(__name__)


AFFILIATE_NAME = get_affiliate_param_name()
AFFILIATE_SESSION = getattr(settings, 'AFFILIATE_SESSION', True)
AFFILIATE_SESSION_AGE = getattr(settings, 'AFFILIATE_SESSION_AGE', 5 * 24 * 60 * 60)
AFFILIATE_SKIP_PATH = getattr(settings, 'AFFILIATE_SKIP_PATH_STARTS', [])

C_PFX = 'a_'

AffiliateModel = get_affiliate_model()
AffiliateModelStats = get_affiliatestats_model()


class AffiliateMiddleware(object):
    datetime_format = '%Y-%m-%d %H:%M:%S'

    def process_request(self, request):
        aid = None
        session = request.session
        now = datetime.now()
        if request.method == 'GET':
            aid = request.GET.get(AFFILIATE_NAME, None)
            if aid:
                request.aid = aid
                if AFFILIATE_SESSION:
                    session['aid'] = aid
                    session['aid_dt'] = now.strftime(self.datetime_format)
                    url = remove_affiliate_code(request.get_full_path())
                    return HttpResponseRedirect(url)
        if not aid and AFFILIATE_SESSION:
            aid = session.get('aid', None)
            if aid:
                aid_dt = session.get('aid_dt', None)
                if aid_dt is None:
                    l.error('aid_dt not found in session')
                else:
                    aid_dt = datetime.strptime(aid_dt, self.datetime_format)
                    if (now - aid_dt).seconds > AFFILIATE_SESSION_AGE:
                        # aid expired
                        aid = None
                        session.pop('aid')
                        session.pop('aid_dt')
        request.aid = aid

    def process_response(self, request, response):
        aid = getattr(request, "aid", None)
        if not aid:
            l.error("aid not set")
        elif response.status_code == 200 and self.is_track_path(request.path):
            now = datetime.now()
            ip = get_client_ip(request)
            cache = get_cache('default')
            c_key = "".join((C_PFX, aid))
            ip_new, aid_ip_pool = self.is_new_ip(c_key, cache, ip)
            if ip_new:
                aid_ip_pool.add(ip)
                timeout = get_seconds_day_left(now)
                cache.set(c_key, aid_ip_pool, timeout)
            nb = AffiliateModelStats.objects.incr_count_views(aid, now,
                ip_new=ip_new)
            if not nb:
                try:
                    aff = AffiliateModel.objects.get(aid=aid)
                    AffiliateModelStats.objects.create(affiliate=aff,
                        total_views=1, unique_visitors=1)
                except AffiliateModel.DoesNotExist:
                    l.warning("Access with unknown affiliate code: {0}"
                        .format(aid))
        return response

    def is_track_path(self, path):
        return len(filter(path.startswith, AFFILIATE_SKIP_PATH)) == 0

    def is_new_ip(self, c_key, cache, ip):
        aid_ip_pool = cache.get(c_key)
        ip_new = True
        if aid_ip_pool:
            if isinstance(aid_ip_pool, set):
                ip_new = ip not in aid_ip_pool
        if not aid_ip_pool:
            aid_ip_pool = set()
        return ip_new, aid_ip_pool

# TODO: attach lazy method to request: affiliate, that return Affiliate instance
