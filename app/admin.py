# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from app import models

admin.site.register(models.Account)
admin.site.register(models.DiscountVoucher)
admin.site.register(models.VoucherRequest)