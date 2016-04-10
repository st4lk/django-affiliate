import logging

from . import app_settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import SimpleLazyObject
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.http import HttpResponseRedirect

from .models import NoAffiliate
from . import utils

l = logging.getLogger(__name__)


AffiliateModel = utils.get_affiliate_model()

def _get_affiliate_instance(aid_code):
    try:
        return AffiliateModel.objects.filter(pk=aid_code).first()
    except (ValueError, TypeError) as e:
        l.warning(u"Bad aid_code type: %s. Error message: %s.", aid_code, e)
        return None


def get_affiliate(request, new_aid, prev_aid, prev_aid_dt):
    if not hasattr(request, '_cached_affiliate'):
        affiliate = _get_affiliate_instance(new_aid)
        if affiliate is None or not affiliate.is_active:
            prev_affiliate = None
            if prev_aid:
                prev_affiliate = _get_affiliate_instance(prev_aid)
            if prev_affiliate is None or not prev_affiliate.is_active:
                affiliate = affiliate or prev_affiliate or NoAffiliate()
            else:
                affiliate = prev_affiliate
                if app_settings.SAVE_IN_SESSION:
                    request.session['_aid'] = prev_aid
                    if prev_aid_dt:
                        request.session['_aid_dt'] = prev_aid_dt
        request._cached_affiliate = affiliate
    return request._cached_affiliate


class AffiliateMiddleware(object):

    def process_request(self, request):
        new_aid, prev_aid, prev_aid_dt = None, None, None
        if app_settings.SAVE_IN_SESSION:
            session = getattr(request, 'session', None)
            if not session:
                raise ImproperlyConfigured(
                    "session attribute should be set for request. Please add "
                    "'django.contrib.sessions.middleware.SessionMiddleware' "
                    "to your MIDDLEWARE_CLASSES")
            elif app_settings.SAVE_IN_SESSION:
                prev_aid = session.get('_aid', None)
                prev_aid_dt = session.get('_aid_dt', None)
        now = timezone.now()
        new_aid = request.GET.get(app_settings.PARAM_NAME, None)
        if new_aid:
            if app_settings.SAVE_IN_SESSION:
                session['_aid'] = new_aid
                session['_aid_dt'] = now.isoformat()
            if app_settings.REMOVE_PARAM_AND_REDIRECT and request.method == 'GET':
                url = utils.remove_affiliate_code(request.get_full_path())
                return HttpResponseRedirect(url)
        if prev_aid and app_settings.SAVE_IN_SESSION:
            if prev_aid_dt is None:
                l.error('_aid_dt not found in session')
                if not new_aid:
                    session['_aid_dt'] = now.isoformat()
            else:
                prev_aid_dt_obj = parse_datetime(prev_aid_dt)
                if (now - prev_aid_dt_obj).total_seconds() > app_settings.SESSION_AGE:
                    # aid expired
                    prev_aid = None
                    prev_aid_dt = None
                    if not new_aid:
                        session.pop('_aid')
                        session.pop('_aid_dt')
        request.affiliate = SimpleLazyObject(lambda: get_affiliate(request, new_aid, prev_aid, prev_aid_dt))
