from datetime import datetime
import logging

from django.conf import settings
from django.http import HttpResponseRedirect
from django.db.models.loading import get_model
from .tools import get_affiliate_param_name, remove_affiliate_code
from relish.helpers.request import get_client_ip

l = logging.getLogger(__name__)


AFFILIATE_NAME = get_affiliate_param_name()
AFFILIATE_SESSION = getattr(settings, 'AFFILIATE_SESSION', True)
AFFILIATE_SESSION_AGE = getattr(settings, 'AFFILIATE_SESSION_AGE', 24*60*60)
AFFILIATE_SKIP_PATH = getattr(settings, 'AFFILIATE_SKIP_PATH_STARTS', [])
AFFILIATE_MODEL = settings.AFFILIATE_MODEL
AFFILIATE_COUNT_MODEL = settings.AFFILIATE_COUNT_MODEL

AffiliateModel = get_model(*AFFILIATE_MODEL.split("."))
AffiliateModelCount = get_model(*AFFILIATE_COUNT_MODEL.split("."))


class AffiliateMiddleware(object):

    def process_request(self, request):
        aid = None
        session = request.session
        now = datetime.now()
        if request.method in 'GET':
            aid = request.GET.get(AFFILIATE_NAME, None)
            if aid:
                request.aid = aid
                if AFFILIATE_SESSION:
                    session['aid'] = aid
                    session['aid_dt'] = now
                    url = remove_affiliate_code(request.get_full_path())
                    return HttpResponseRedirect(url)
        if not aid and AFFILIATE_SESSION:
            aid = session.get('aid', None)
            if aid:
                aid_dt = session.get('aid_dt', None)
                # if (now - aid_dt).seconds > :
                if (now - aid_dt).seconds > AFFILIATE_SESSION_AGE:
                    # aid expired
                    aid = None
                    session.pop('aid')
                    session.pop('aid_dt')
        request.aid = aid

    def process_response(self, request, response):
        aid = request.aid
        if aid and response.status_code == 200\
                and self.is_track_path(request.path):
            now = datetime.now()
            ip = get_client_ip(request)
            nb = AffiliateModelCount.objects.incr_count_views(aid, now, ip)
            if not nb:
                try:
                    aff = AffiliateModel.objects.get(aid=aid)
                    AffiliateModelCount.objects.create(affiliate=aff,
                        ip=ip, count_views=1)
                except AffiliateModel.DoesNotExist:
                    l.warning("Access with unknown affiliate code: {0}"
                        .format(aid))
        return response

    def is_track_path(self, path):
        return len(filter(path.startswith, AFFILIATE_SKIP_PATH)) == 0
