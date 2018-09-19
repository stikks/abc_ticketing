# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout

from app.services import authentication
from app import models, forms

# Create your views here.


def index(request):
    """
    landing page
    simple login page
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            if authentication.authenticate_user(request, **form.cleaned_data):
                return redirect('dashboard')

            messages.error(request, 'Invalid username/password combination.')

        messages.error(request, form.errors)

    return render(request, 'index.html')


def register(request):
    """
    register account view
    :param request:
    :return:
    """
    if request.method == 'POST':

        form = forms.RegistrationForm(request.POST)

        if form.is_valid():
            if authentication.register_user(request, **form.cleaned_data):
                return redirect('dashboard')

        messages.error(request, form.errors)

    return render(request, 'register.html')


@login_required
def dashboard(request):
    """
    user dashboard view
    access status of vouchers
    :param request:
    :return:
    """
    account = models.Account.objects.get(user_ptr=request.user)
    voucher_requests = account.voucher_requests
    discount_vouchers = account.discount_vouchers
    return render(request, 'dashboard.html', locals())


@login_required
def logout_view(request):
    """
    logout user
    :param request:
    :return:
    """
    logout(request)

    return redirect('index')