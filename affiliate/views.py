# -*- coding: utf-8 -*-
from decimal import Decimal as D
from django.views.generic import FormView
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from relish.views.messages import SuccessMessageMixin
from relish.decorators import instance_cache
from .tools import get_affiliate_model
from .forms import AffiliateCreateForm, AffiliateWithdrawRequestForm

MIN_REQUEST_AMOUNT = getattr(settings, 'AFFILIATE_MIN_BALANCE_FOR_REQUEST', D('1.0'))


class AffiliateBaseView(SuccessMessageMixin, FormView):
    """
    Probably you need to redefine some methods here to respect
    your custom Affiliate model.
    This view asserts, that Affiliate has OneToOne relationship to User.
    """
    template_name = "partner/affiliate.html"

    @property
    @instance_cache
    def user(self):
        return self.request.user

    def get_affiliate_model(self):
        return get_affiliate_model()

    def get_affiliate_banner_model(self):
        raise NotImplementedError()

    @property
    @instance_cache
    def affiliate(self):
        aff_model = self.get_affiliate_model()
        try:
            return aff_model.objects.get(user=self.user)
        except aff_model.DoesNotExist:
            return None

    def get_form_class(self):
        if self.affiliate:
            form_class = AffiliateWithdrawRequestForm
        else:
            form_class = AffiliateCreateForm
        return form_class

    def get_form_kwargs(self):
        kwargs = super(AffiliateBaseView, self).get_form_kwargs()
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
            return _("Affiliate account successfully created")

    def form_valid(self, form):
        form.save()
        return super(AffiliateBaseView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AffiliateBaseView, self).get_context_data(**kwargs)
        affiliate = self.affiliate
        context['affiliate'] = affiliate
        if affiliate:
            context['min_request_amount'] = MIN_REQUEST_AMOUNT
            context['currency_label'] = affiliate.get_currency()
            context['requested'] = affiliate.pay_requests.pending()
            context['avaliable_for_request'] = affiliate.balance >= MIN_REQUEST_AMOUNT
            context['pay_requests'] = affiliate.pay_requests.all()
            aff_banner_model = self.get_affiliate_banner_model()
            context['banners'] = aff_banner_model.objects.enabled()
            context['visitor_stats'] = affiliate.stats.for_last_days(30)
        return context
