# -*- coding: utf-8 -*-
from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.conf import settings

from .forms import UserForm
from .models import User


MIN_REQUEST_AMOUNT = getattr(settings, 'AFFILIATE_MIN_BALANCE_FOR_REQUEST', 0)


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = "account/signup.html"

    def get_success_url(self):
        # TODO: reverse
        return self.request.POST.get('next', reverse('products:list'))

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'])
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())
