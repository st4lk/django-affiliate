# -*- coding: utf-8 -*-
from django.views.generic import CreateView, FormView
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from relish.views.messages import SuccessMessageMixin
from relish.decorators import instance_cache

from apps.partner.models import Affiliate, AffiliateBanner
from .forms import UserForm, CreateAffiliateForm, AffiliatePaymentRequestForm
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


class UserAffiliateView(SuccessMessageMixin, FormView):
    template_name = "account/affiliate.html"

    @property
    @instance_cache
    def user(self):
        return self.request.user

    @property
    @instance_cache
    def affiliate(self):
        try:
            return Affiliate.objects.get(user=self.user)
        except Affiliate.DoesNotExist:
            return None

    def get_form_class(self):
        if self.affiliate:
            form_class = AffiliatePaymentRequestForm
        else:
            form_class = CreateAffiliateForm
        return form_class

    def get_form_kwargs(self):
        kwargs = super(UserAffiliateView, self).get_form_kwargs()
        affiliate = self.affiliate
        if affiliate:
            kwargs['affiliate'] = affiliate
        else:
            kwargs['user'] = self.user
        return kwargs

    def get_success_url(self):
        return self.request.get_full_path()

    def get_success_message(self):
        if self.affiliate:
            return _("Request for payment was sent")
        else:
            return _("Affiliate successfully created")

    def form_valid(self, form):
        form.save()
        return super(UserAffiliateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UserAffiliateView, self).get_context_data(**kwargs)
        context['affiliate'] = self.affiliate
        context['min_request_amount'] = MIN_REQUEST_AMOUNT
        context['currency_label'] = Affiliate.get_currency()
        if self.affiliate:
            context['requested'] = self.affiliate.pay_requests.pending()
            context['avaliable_for_request'] = self.affiliate.balance >= MIN_REQUEST_AMOUNT
            context['pay_requests'] = self.affiliate.pay_requests.all()
            context['banners'] = AffiliateBanner.objects.enabled()
            context['visitor_stats'] = self.affiliate.stats.for_last_days(30)
        return context
