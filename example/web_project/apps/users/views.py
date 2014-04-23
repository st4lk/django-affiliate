# -*- coding: utf-8 -*-
from django.views.generic import CreateView, FormView
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from relish.views.messages import SuccessMessageMixin
from .forms import UserForm, CreateAffiliateForm, UpdateAffiliateForm
from .models import User
from apps.partner.models import Affiliate


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
    model = User
    template_name = "account/affiliate.html"

    def get_user(self):
        user = getattr(self, '_user', None)
        if user is None:
            user = User.objects.get(pk=self.kwargs['pk'])
            self._user = user
        return user

    def get_affiliate(self):
        if hasattr(self, "_affiliate"):
            aff = self._affiliate
        else:
            user = self.get_user()
            try:
                aff = Affiliate.objects.get(user=user)
            except Affiliate.DoesNotExist:
                aff = None
            self._affiliate = aff
        return aff

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
        return context
