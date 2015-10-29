# -*- coding: utf-8 -*-
from django.views import generic
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.views import redirect_to_login
from affiliate.utils import get_affiliate_model
from .models import Product
from apps.partner.models import AffiliateTransaction

Affiliate = get_affiliate_model()


class ProductListView(generic.ListView):
    template_name = "products/list.html"
    model = Product
    context_object_name = 'products'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path())
        self.buy_product(request)
        return super(ProductListView, self).get(request, *args, **kwargs)

    def buy_product(self, request):
        # just to show how affiliate works.
        pk = None
        for key in request.POST:
            if key.startswith('product'):
                pk = int(key.split("_")[-1])
                break
        if pk:
            product = Product.objects.get(pk=pk)
            messages.add_message(request, messages.INFO,
                _("Product %(product)s was bought" % {"product": product.title}))
            if request.affiliate.exists() and request.affiliate.is_active:
                affiliate = request.affiliate
                AffiliateTransaction.objects.create(
                    affiliate=affiliate,
                    product=product,
                    price=product.price,
                    bought_by=self.request.user,
                    reward_amount=affiliate.reward_amount,
                    reward_percentage=affiliate.reward_percentage,
                    reward=affiliate.calc_affiliate_reward(product.price))
