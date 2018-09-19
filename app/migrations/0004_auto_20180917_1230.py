# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-17 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180917_1024'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': 'account', 'verbose_name_plural': 'accounts'},
        ),
        migrations.AddField(
            model_name='account',
            name='mobile_number',
            field=models.CharField(default=1, max_length=50, verbose_name='Mobile Number'),
            preserve_default=False,
        ),
    ]
