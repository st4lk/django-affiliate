# -*- coding: utf-8 -*-
import logging
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail
from affiliate.abstract_models import AbstractAffiliate, AbstractAffiliateCount,\
    AbstractAffiliateBanner, AbstractPaymentRequest
from affiliate.signals import affiliate_post_reward, affiliate_post_withdraw

l = logging.getLogger(__name__)


class Affiliate(AbstractAffiliate):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    @classmethod
    def create_affiliate(cls, user):
        aff = cls(user=user)
        aff.aid = aff.generate_aid()
        l.info("Creating affiliate #{0} for user {1}"
            .format(aff.aid, user))
        aff.save()


class AffiliateCount(AbstractAffiliateCount):
    pass


class AffiliateBanner(AbstractAffiliateBanner):
    pass


class PaymentRequest(AbstractPaymentRequest):
    pass


@receiver(affiliate_post_reward)
def affiliate_rewared(sender, affiliate, reward, **kwargs):
    subject = "Dear {0}. You've recieved an affiliate reward!"\
        .format(affiliate.user)
    message = ("Reward amount: {amt:.2f} {currency}.\n"
        "You current balance is: {balance:.2f} {currency}. Thank you!"
        .format(amt=reward, balance=affiliate.balance,
            currency=settings.DEFAULT_CURRENCY))
    send_mail(subject, message, settings.SITE_EMAIL, [affiliate.user.email])


@receiver(affiliate_post_withdraw)
def affiliate_withdraw_completed(sender, payment_request, **kwargs):
    aff = payment_request.affiliate
    subject = "Dear {0}. Your withdraw transaction was processed"\
        .format(aff.user)
    message = ("Transaction amount: {amt:.2f} {currency}.\n"
        "You current balance is: {balance:.2f} {currency}. Thank you!"
        .format(amt=payment_request.amount, balance=aff.balance,
            currency=settings.DEFAULT_CURRENCY))
    send_mail(subject, message, settings.SITE_EMAIL, [aff.user.email])
