# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from .tools import get_affiliate_model
AffiliateModel = get_affiliate_model()


class AffiliateCreateForm(forms.Form):
    """
    Redefine it to respect your custom Affiliate model.
    This form asserts, that Affiliate has OneToOne relationship to User.
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AffiliateCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        try:
            self.user.affiliate
            raise forms.ValidationError(_("Affiliate already created"))
        except AffiliateModel.DoesNotExist:
            pass
        return self.cleaned_data

    def save(self):
        aff = AffiliateModel.create_affiliate(user=self.user)
        return aff


class AffiliateWithdrawRequestForm(forms.Form):
    """
    Redefine it to respect your custom WithdrawRequest model.
    """
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
