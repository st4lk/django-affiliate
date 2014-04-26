# -*- coding: utf-8 -*-
from django.views.generic import ListView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from .models import Product
from apps.partner.models import Affiliate


class ProductListView(ListView):
    template_name = "products/list.html"
    model = Product
    context_object_name = 'products'

    def post(self, request, *args, **kwargs):
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
            if request.aid:
                affiliate = Affiliate.objects.get(aid=request.aid)
                affiliate.reward_affiliate(product.price)
