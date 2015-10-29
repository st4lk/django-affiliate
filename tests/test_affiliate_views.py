from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from model_mommy import mommy

from affiliate.utils import get_affiliate_model

Affiliate = get_affiliate_model()


class TestAffiliateView(TestCase):
    def setUp(self):
        super(TestAffiliateView, self).setUp()
        self.user = mommy.make(settings.AUTH_USER_MODEL, username='john')
        self.user.set_password('123456')
        self.user.save()

    def test_partner_get(self):
        self.client.login(username=self.user.username, password='123456')
        resp = self.client.get(reverse('partner:affiliate'))
        self.assertEqual(resp.status_code, 200)

    def test_partner_create(self):
        self.client.login(username=self.user.username, password='123456')
        resp = self.client.post(reverse('partner:affiliate'))
        self.assertRedirects(resp, reverse('partner:affiliate'))
        affiliate = Affiliate.objects.get()
        self.assertEqual(affiliate.user, self.user)
