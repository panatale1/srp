# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-28 00:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summer_reading', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
