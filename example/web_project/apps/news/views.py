# -*- coding: utf-8 -*-
from django.views.generic import ListView
from .models import News


class NewsListView(ListView):
    model = News
    template_name = "news/list.html"
