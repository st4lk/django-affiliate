# -*- coding: utf-8 -*-
import urllib
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy
from freezegun import freeze_time
from affiliate.settings import PARAM_NAME, SESSION_AGE


class TestAffiliateMiddleware(TestCase):
    def test_no_affiliate_in_url(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['request'].affiliate.exist())

    def test_bad_affiliate_code(self):
        resp = self.client.get(self.get_aid_url('/', 123))
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['request'].affiliate.exist())

    def test_affiliate_assigned(self):
        affiliate = mommy.make('affiliate.Affiliate')
        resp = self.client.get(self.get_aid_url('/', affiliate.aid))
        self.assertEqual(resp.status_code, 200)
        affiliate_resp = resp.context['request'].affiliate
        self.assertTrue(affiliate_resp.exist())
        self.assertEqual(affiliate.aid, affiliate_resp.aid)

    def test_previous_affiliate_is_used(self):
        affiliate = mommy.make('affiliate.Affiliate')
        resp = self.client.get(self.get_aid_url('/', affiliate.aid))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(self.get_aid_url('/', affiliate.aid + 100))  # invalid aid code
        self.assertEqual(resp.status_code, 200)
        affiliate_resp = resp.context['request'].affiliate
        self.assertTrue(affiliate_resp.exist())
        self.assertEqual(affiliate.aid, affiliate_resp.aid)

    def test_affiliate_saved_in_session(self):
        affiliate = mommy.make('affiliate.Affiliate')
        self.client.get(self.get_aid_url('/', affiliate.aid))

        # next response without aid still contains affiliate
        with freeze_time(timezone.now() + timedelta(seconds=SESSION_AGE - 1)):
            resp = self.client.get('/')

        self.assertEqual(resp.status_code, 200)
        affiliate_resp = resp.context['request'].affiliate
        self.assertTrue(affiliate_resp.exist())
        self.assertEqual(affiliate.aid, affiliate_resp.aid)

    def test_affiliate_session_expired(self):
        affiliate = mommy.make('affiliate.Affiliate')
        self.client.get(self.get_aid_url('/', affiliate.aid))

        # affiliate is expired
        with freeze_time(timezone.now() + timedelta(seconds=SESSION_AGE + 1)):
            resp = self.client.get('/')

        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['request'].affiliate.exist())

    def test_previous_affiliate_session_expired(self):
        affiliate = mommy.make('affiliate.Affiliate')
        resp = self.client.get(self.get_aid_url('/', affiliate.aid))
        self.assertEqual(resp.status_code, 200)

        # affiliate is expired
        with freeze_time(timezone.now() + timedelta(seconds=SESSION_AGE + 1)):
            resp = self.client.get(self.get_aid_url('/', affiliate.aid + 100))  # invalid aid code

        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context['request'].affiliate.exist())

    def get_aid_url(self, url, aid_code):
        return '?'.join([url, urllib.urlencode({PARAM_NAME: aid_code})])
