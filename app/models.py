# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

from . import services

class Abstract(models.Model):
    """
    extended in new models
    contains common fields
    """
    class Meta:
        abstract = True

    date_created = models.DateTimeField(auto_now_add=True)


# Create your models here.
class Account(User, Abstract):
    """
    Extension of django user model
    additions: state, middle_name
    """

    class Meta:
        verbose_name = 'account'
        verbose_name_plural = 'accounts'

    middle_name = models.TextField('Middle Name')
    state_of_correspondence = models.CharField('State', max_length=255)
    profile_image = models.ImageField('Profile Image')
    mobile_number = models.CharField('Mobile Number', max_length=50)

    def __repr__(self):
        return '<Account: {} {}>'.format(self.first_name, self.last_name)


class DiscountVoucher(Abstract):
    """
    discount voucher model
    """
    user = models.ForeignKey(Account, related_name='discount_vouchers')
    code = models.CharField(max_length=255)

    def __str__(self):
        return '<{}: {} >'.format(self.user, self.code)


class VoucherRequest(Abstract):
    """
    discount voucher request
    """
    __original_state = None

    user = models.ForeignKey(Account, related_name='voucher_requests')
    status = models.CharField(max_length=20, choices=[('approved', 'approved'), ('rejected', 'rejected')], null=True)
    rejection_reason = models.TextField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(VoucherRequest, self).__init__(*args, **kwargs)
        self.__original_state = self.status

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.status != self.__original_state:    # check if state has changed
            print('sending email')

        if self.status == 'approved':
            DiscountVoucher.objects.create(user=self.user, code=services.generate_code(15))

        super(VoucherRequest, self).save(force_insert, force_update, *args, **kwargs)

    def __repr__(self):
        return '<VoucherRequest: {}>'.format(self.date_created)

    def __str__(self):
        return '<{}>'.format(self.date_created)


@receiver(models.signals.post_save, sender=Account)
def create_auto_voucher_request(sender, instance, created, **kwargs):
    """
    generates a voucher request for newly registered user
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    if created:
        VoucherRequest.objects.create(user=instance)
