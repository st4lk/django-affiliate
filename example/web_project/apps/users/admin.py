# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from affiliate.admin import BaseAffiliateAdmin
from .models import User, Affiliate


class UserAdmin(admin.ModelAdmin):
    create_form_class = UserCreationForm
    update_form_class = UserChangeForm


class AffiliateAdmin(BaseAffiliateAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Affiliate, AffiliateAdmin)
