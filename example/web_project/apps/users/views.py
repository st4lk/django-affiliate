# -*- coding: utf-8 -*-
from django.views.generic import CreateView, FormView
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from relish.views.messages import SuccessMessageMixin
from relish.decorators import instance_cache

from apps.partner.models import Affiliate, AffiliateBanner
from .forms import UserForm, CreateAffiliateForm, UpdateAffiliateForm
from .models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = "account/signup.html"

    def get_success_url(self):
        # TODO: reverse
        return self.request.POST.get('next', reverse('home'))

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


class UserAffiliateView(SuccessMessageMixin, FormView):
    template_name = "account/affiliate.html"

    @instance_cache
    def get_user(self):
        return User.objects.get(pk=self.kwargs['pk'])

    @instance_cache
    def get_affiliate(self):
        user = self.get_user()
        try:
            return Affiliate.objects.get(user=user)
        except Affiliate.DoesNotExist:
            return None

    def get_form_class(self):
        affiliate = self.get_affiliate()
        if affiliate:
            form_class = UpdateAffiliateForm
        else:
            form_class = CreateAffiliateForm
        return form_class

    def get_form_kwargs(self):
        kwargs = super(UserAffiliateView, self).get_form_kwargs()
        kwargs['user'] = self.get_user()
        return kwargs

    def get_success_url(self):
        return self.request.get_full_path()

    def get_success_message(self):
        if self.get_affiliate():
            return _("TOOD")
        else:
            return _("Affiliate successfully created")

    def form_valid(self, form):
        form.save()
        return super(UserAffiliateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UserAffiliateView, self).get_context_data(**kwargs)
        context['affiliate'] = self.get_affiliate()
        context['banners'] = AffiliateBanner.objects.enabled()
        return context
