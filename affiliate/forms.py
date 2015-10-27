# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from .utils import get_affiliate_model
Affiliate = get_affiliate_model()


class AffiliateCreateForm(forms.ModelForm):
    """
    Redefine it to respect your custom Affiliate model.
    This form asserts, that Affiliate has OneToOne relationship to User.
    """
    class Meta:
        model = Affiliate
        fields = ()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AffiliateCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        try:
            self.user.affiliate
            raise forms.ValidationError(_("Affiliate already created"))
        except Affiliate.DoesNotExist:
            pass
        return self.cleaned_data

    def save(self, commit=True):
        aff = Affiliate(user=self.user, **self.cleaned_data)
        if commit:
            aff.save()
        return aff
