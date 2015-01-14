Affiliate system for django
===========================

Affiliate system to reward partners with their visitors payments.
Contains abstract models with basic functionality, so it is easy to
subclass them and add your custom logic and relations.

Example
-------

Visitor goes to site with affiliate code:

::

    http://site.com/?aid=12345

This code is saved in his cookies (also another way is supported: keep
aid=12345 at every url). Now each request object has property
``request.aid``, so you can access to affiliate, that attract current
visitor, and therefore reward him at needed event. Affiliate can make a
withdraw request, if his balance have some money.

You can find example project in this repository.

Requirements
------------

-  python (2.7)
-  django (1.5, 1.6)

Quick start
-----------

1. Install this package to your python distribution

2. Add ‘affiliate’ to INSTALLED\_APP:

   ::

       INSTALLED_APPS = [
           # ...
           'affiliate',
       ]

3. Add ‘affiliate.context\_processors.common’ to
   TEMPLATE\_CONTEXT\_PROCESSORS:

   ::

       TEMPLATE_CONTEXT_PROCESSORS = (
           # ...
           'affiliate.context_processors.common',
       )

4. Add ‘affiliate.middleware.AffiliateMiddleware’ to
   MIDDLEWARE\_CLASSES:

   ::

       MIDDLEWARE_CLASSES = (
           # ...
           'affiliate.middleware.AffiliateMiddleware',
       )

5. Subclass affiliate abstract\_models:

   ::

       from django.db import models
       from django.conf import settings
       from affiliate.abstract_models import AbstractAffiliate,\
           AbstractAffiliateStats, AbstractAffiliateBanner, AbstractWithdrawRequest


       class Affiliate(AbstractAffiliate):
           user = models.OneToOneField(settings.AUTH_USER_MODEL)

           @classmethod
           def create_affiliate(cls, user):
               aff = cls(user=user)
               aff.aid = aff.generate_aid()
               l.info("Creating affiliate #{0} for user {1}"
                   .format(aff.aid, user))
               aff.save()


       class AffiliateStats(AbstractAffiliateStats):
           pass


       class AffiliateBanner(AbstractAffiliateBanner):
           pass


       class WithdrawRequest(AbstractWithdrawRequest):
           pass

6. Define your affiliate models in settings.py:

   ::

       AFFILIATE_MODEL = "partner.Affiliate"
       AFFILIATE_COUNT_MODEL = "partner.AffiliateStats"

7. Create affiliate cabinet:

   ::

       from affiliate.views import AffiliateBaseView
       from .models import AffiliateBanner


       class AffiliateView(AffiliateBaseView):
           template_name = "partner/affiliate.html"

           def get_affiliate_banner_model(self):
               return AffiliateBanner


8.  Define url for affiliate cabinet:

    ::

        from django.conf.urls import patterns, url
        from django.contrib.auth.decorators import login_required
        import views

        urlpatterns = patterns('',
            # ...
            url(r'^$',
                login_required(views.AffiliateView.as_view()), name='affiliate'),
            # ...
        )

9.  Create tables

    ::

        python manage.py syncdb

10. Finally, reward affiliate

    ::

        from apps.partner.models import Affiliate
        from django.views.generic import FormView

        class SomeView(FormView):
            # ...

            def form_valid(self.form):
                product = self.get_product()
                affiliate = Affiliate.objects.get(aid=self.request.aid)
                affiliate.reward_affiliate(product.price)
                return super(SomeView, self).form_valid(form)

Optional
^^^^^^^^

To always keep the aid GET parameter (maybe you don’t trust the cookies
or you want to reward affiliate only if his visitor make payment at
current link access, and not tomorrow)

11.1. Load ‘affiliate\_urls’ tags:

::

    {% load affiliate_urls %}

11.2. Use ‘url\_aff’ instead of ‘url’ template tag:

::

    <a href="{% url_aff 'home' %}">Home</a>

Configuration
-------------

Define in settings.py

Required
^^^^^^^^

-  ``AFFILIATE_MODEL`` - model, that subclass AbstractAffiliate.
   “appname.ModelName”. Example: “partner.Affiliate”
-  ``AFFILIATE_COUNT_MODEL`` - model, that subclass AbstractAffiliate.
   “appname.ModelName”. Example: “partner.AffiliateStats”

Optional
^^^^^^^^

-  ``AFFILIATE_SESSION`` - save affiliate id in session or not. Default
   ``True``
-  ``AFFILIATE_SESSION_AGE`` - how long keep affiliate id in session, in
   seconds. Default ``5 * 24 * 60 * 60`` seconds (5 days)
-  ``AFFILIATE_SKIP_PATH_STARTS`` - paths to ignore during tracking
   affiliate statistics. Default ``[]``. Example:
   ``['/admin/', '/users/affiliate/']``
-  ``AFFILIATE_START_AID`` - start number of affiliate id. Default
   ``1000``
-  ``AFFILIATE_MIN_BALANCE_FOR_REQUEST`` - minimal amount for withdraw.
   Default ``Decimal(1.0)``
-  ``AFFILIATE_REWARD_AMOUNT`` - reward amount per payment. Default
   ``Decimal("5.0")``
-  ``AFFILIATE_REWARD_PERCENTAGE`` - reward is set in percent. Default
   ``True``
