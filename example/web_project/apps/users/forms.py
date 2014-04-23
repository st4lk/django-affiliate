# -*- coding: utf-8 -*-
from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from apps.partner.models import Affiliate
from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,
        label="Password")
    password1 = forms.CharField(widget=forms.PasswordInput,
        label="Confirm password")

    def clean_username(self):
        username_form = self.cleaned_data['username']
        if User.objects.filter(username=username_form).exists():
            raise forms.ValidationError("Username is already taken")
        return username_form

    def clean(self):
        pwd = self.cleaned_data.get('password', "")
        pwd1 = self.cleaned_data.get('password1', "")
        if pwd != pwd1:
            if self._errors.get('password1', None) is None:
                self._errors['password1'] = ErrorList()
            self._errors['password1'].append("Passwords are not equal")
            # self.add_error('password1', "Passwords are not equal")
        return self.cleaned_data

    def save(self):
        kwargs = self.cleaned_data.copy()
        del kwargs['password1']
        return User.objects.create_user(**kwargs)

    class Meta:
        model = User
        fields = "username", "password", "password1"


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


class UpdateAffiliateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UpdateAffiliateForm, self).__init__(*args, **kwargs)

    def save(self):
        # TODO
        return None
