from decimal import Decimal as D
from django.test import TestCase
from model_mommy import mommy

from affiliate.utils import get_affiliate_model

Affiliate = get_affiliate_model()


class TestAffiliateModel(TestCase):
    def test_build_partner_absolute_link(self):
        resp = self.client.get('/')
        request = resp.context['request']
        affiliate = mommy.make(Affiliate)
        url = affiliate.build_absolute_affiliate_uri(request, '/')
        self.assertEqual('http://testserver/?aid={0}'.format(affiliate.aid), url)

    def test_build_partner_relative_link(self):
        affiliate = mommy.make(Affiliate)
        url = affiliate.build_affiliate_url('/')
        self.assertEqual('/?aid={0}'.format(affiliate.aid), url)

    def test_calc_affiliate_reward_percent(self):
        affiliate = mommy.make(Affiliate, reward_amount=D('0.5'), reward_percentage=True)
        self.assertEqual(affiliate.calc_affiliate_reward(10000), D('50'))

    def test_calc_affiliate_reward_fixed(self):
        affiliate = mommy.make(Affiliate, reward_amount=D('0.5'), reward_percentage=False)
        self.assertEqual(affiliate.calc_affiliate_reward(D('0.5')), D('0.5'))
