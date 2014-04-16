# -*- coding: utf-8 -*-
from django.db import models


class News(models.Model):
    title = models.CharField(max_length=50, blank=True)
    text = models.TextField(blank=True)

    def __unicode__(self):
        return self.title
