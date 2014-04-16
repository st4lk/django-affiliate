from datetime import datetime

from django.conf import settings
from django.http import HttpResponseRedirect
from .tools import get_affiliate_param_name, remove_affiliate_code


AFFILIATE_NAME = get_affiliate_param_name()
AFFILIATE_SESSION = getattr(settings, 'AFFILIATE_SESSION', True)
AFFILIATE_SESSION_AGE = getattr(settings, 'AFFILIATE_SESSION_AGE', 24*60*60)


class AffiliateMiddleware(object):

    def process_request(self, request):
        aid = None
        aid_from_url = False
        session = request.session
        now = datetime.now()
        if request.method in 'GET':
            aid = request.GET.get(AFFILIATE_NAME, None)
            if aid:
                aid_from_url = True
                request.aid = aid
                if AFFILIATE_SESSION:
                    session['aid'] = aid
                    session['aid_dt'] = now
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
        if aid_from_url and AFFILIATE_SESSION:
            url = remove_affiliate_code(request.get_full_path())
            return HttpResponseRedirect(url)
        request.aid = aid
