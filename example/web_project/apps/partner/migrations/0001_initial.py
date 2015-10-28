# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('products', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(settings.AFFILIATE_AFFILIATE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AffiliateTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('reward_amount', models.DecimalField(max_digits=5, decimal_places=2)),
                ('reward_percentage', models.BooleanField(default=False)),
                ('reward', models.DecimalField(max_digits=5, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('affiliate', models.ForeignKey(to=settings.AFFILIATE_AFFILIATE_MODEL)),
                ('bought_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(to='products.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
