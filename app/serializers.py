from rest_framework import serializers

from . import models


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = '__all__'


class DiscountVoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DiscountVoucher
        fields = ("code",)


class VoucherRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VoucherRequest
        exclude = ('user',)
