# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    list_display = "title", "price",


admin.site.register(models.Product, ProductAdmin)
