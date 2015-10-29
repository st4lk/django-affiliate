# -*- coding: utf-8 -*-
from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserCreateView(CreateView):
    model = get_user_model()
    form_class = UserCreationForm
    template_name = "account/signup.html"

    def get_success_url(self):
        return self.request.POST.get('next', reverse('products:list'))

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'])
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())
