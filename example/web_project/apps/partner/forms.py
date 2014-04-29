# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from apps.partner.models import Affiliate


class CreateAffiliateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateAffiliateForm, self).__init__(*args, **kwargs)

    def clean(self):
        try:
            self.user.affiliate
            raise forms.ValidationError(_("Affiliate already created"))
        except Affiliate.DoesNotExist:
            pass
        return self.cleaned_data

    def save(self):
        aff = Affiliate.create_affiliate(user=self.user)
        return aff


class AffiliateWithdrawRequestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.affiliate = kwargs.pop('affiliate', None)
        super(AffiliateWithdrawRequestForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.affiliate is None:
            raise forms.ValidationError(_("Affiliate not found"))
        if self.affiliate.pay_requests.pending().exists():
            raise forms.ValidationError(_("Request is already sent"))
        return self.cleaned_data

    def save(self):
        return self.affiliate.create_payment_request()
