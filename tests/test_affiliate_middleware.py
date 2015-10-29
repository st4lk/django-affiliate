# -*- coding: utf-8 -*-
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from model_mommy import mommy
from freezegun import freeze_time

from affiliate import app_settings
from .utils import get_aid_url, modify_settings


class TestAffiliateMiddleware(TestCase):
    def test_no_affiliate_in_url(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['request'].affiliate.exists())

    def test_bad_affiliate_code(self):
        resp = self.client.get(get_aid_url('/', 123))
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['request'].affiliate.exists())

    def test_affiliate_assigned(self):
        affiliate = mommy.make('affiliate.Affiliate')
        resp = self.client.get(get_aid_url('/', affiliate.aid))
        self.assertEqual(resp.status_code, 200)
        affiliate_resp = resp.context['request'].affiliate
        self.assertTrue(affiliate_resp.exists())
        self.assertEqual(affiliate.aid, affiliate_resp.aid)

    def test_previous_affiliate_is_used(self):
        affiliate = mommy.make('affiliate.Affiliate')
        resp = self.client.get(get_aid_url('/', affiliate.aid))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(get_aid_url('/', affiliate.aid + 100))  # invalid aid code
        self.assertEqual(resp.status_code, 200)
        affiliate_resp = resp.context['request'].affiliate
        self.assertTrue(affiliate_resp.exists())
        self.assertEqual(affiliate.aid, affiliate_resp.aid)

    def test_affiliate_saved_in_session(self):
        affiliate = mommy.make('affiliate.Affiliate')
        self.client.get(get_aid_url('/', affiliate.aid))

        # next response without aid still contains affiliate
        with freeze_time(timezone.now() + timedelta(seconds=app_settings.SESSION_AGE - 1)):
            resp = self.client.get('/')

        self.assertEqual(resp.status_code, 200)
        affiliate_resp = resp.context['request'].affiliate
        self.assertTrue(affiliate_resp.exists())
        self.assertEqual(affiliate.aid, affiliate_resp.aid)

    def test_affiliate_session_expired(self):
        affiliate = mommy.make('affiliate.Affiliate')
        self.client.get(get_aid_url('/', affiliate.aid))

        # affiliate is expired
        with freeze_time(timezone.now() + timedelta(seconds=app_settings.SESSION_AGE + 1)):
            resp = self.client.get('/')

        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['request'].affiliate.exists())

    def test_previous_affiliate_session_expired(self):
        affiliate = mommy.make('affiliate.Affiliate')
        resp = self.client.get(get_aid_url('/', affiliate.aid))
        self.assertEqual(resp.status_code, 200)

        # affiliate is expired
        with freeze_time(timezone.now() + timedelta(seconds=app_settings.SESSION_AGE + 1)):
            resp = self.client.get(get_aid_url('/', affiliate.aid + 100))  # invalid aid code

        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['request'].affiliate.exists())

    def test_affiliate_code_in_post_request(self):
        affiliate = mommy.make('affiliate.Affiliate')
        resp = self.client.post(get_aid_url(reverse('users:signup'), affiliate.aid),
            dict(username='newuser', password1='123456', password2='123456'))
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get('/')
        self.assertTrue(resp.context['request'].affiliate.exists())
        self.assertEqual(resp.context['request'].affiliate.pk, affiliate.pk)


@modify_settings(MIDDLEWARE_CLASSES={
    'remove': [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ],
}, INSTALLED_APPS={
    'remove': [
        'django.contrib.sessions'
    ]
})
class TestAffiliateMiddlewareNoSession(TestCase):
    def test_no_session_affiliate_in_url(self):
        app_settings.SAVE_IN_SESSION = False

        affiliate = mommy.make('affiliate.Affiliate')
        resp = self.client.get(get_aid_url('/', affiliate.aid))
        self.assertEqual(resp.status_code, 200)
        affiliate_resp = resp.context['request'].affiliate
        self.assertTrue(affiliate_resp.exists())
        self.assertEqual(affiliate.aid, affiliate_resp.aid)

        # next request can't remember previous affiliate
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['request'].affiliate.exists())

    def test_no_session_exception_raised(self):
        app_settings.SAVE_IN_SESSION = True

        affiliate = mommy.make('affiliate.Affiliate')
        with self.assertRaises(ImproperlyConfigured):
            self.client.get(get_aid_url('/', affiliate.aid))
