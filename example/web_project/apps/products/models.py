# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from relish.helpers import upload_to


class Product(models.Model):
    """Very simple product"""

    title = models.CharField(_("Title"), max_length=50)
    description = models.TextField(_("Description"))
    image = models.ImageField(_("Image"),
        upload_to=upload_to("images/products/"), blank=True, null=True)
    price = models.DecimalField(_("Product price"), max_digits=5,
        decimal_places=2)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __unicode__(self):
        return self.title

    def get_image_url(self):
        if self.image:
            return self.image.url
        else:
            return settings.DEFAULT_IMAGE
