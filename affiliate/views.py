# -*- coding: utf-8 -*-
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from .forms import AffiliateCreateForm
from .tools import get_affiliate_model


class AffiliateBaseView(SuccessMessageMixin, generic.CreateView):
    """
    Probably you need to redefine some methods here to respect
    your custom Affiliate model.
    """
    template_name = "partner/affiliate.html"

    def get_affiliate_banner_model(self):
        raise NotImplementedError()

    @property
    def affiliate(self):
        if not hasattr(self, '_affiliate'):
            self._affiliate = get_affiliate_model().objects.filter(user=self.request.user).first()
        return self._affiliate

    def get_form_class(self):
        return AffiliateCreateForm

    def get_form_kwargs(self):
        kwargs = super(AffiliateBaseView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return self.request.get_full_path()

    def get_success_message(self, cleaned_data):
        return _("Affiliate account successfully created")

    def get_context_data(self, **kwargs):
        context = super(AffiliateBaseView, self).get_context_data(**kwargs)
        context['affiliate'] = self.affiliate
        if self.affiliate:
            context['affiliate_link'] = self.affiliate.build_absolute_affiliate_uri(self.request)
        return context
