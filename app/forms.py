from django import forms
from . import models
from django.db.models import Q


class LoginForm(forms.Form):
    """
    login form
    """
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(max_length=512, required=True, widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    """
    register new account form
    """
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(max_length=512, required=True, widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=512)
    middle_name = forms.CharField(required=True, max_length=512)
    last_name = forms.CharField(required=True, max_length=512)
    mobile_number = forms.CharField(required=True, max_length=50)
    state_of_correspondence = forms.CharField(required=True, max_length=255)

    def clean(self):
        """
        validate email address and username
        """
        cleaned_data = super(RegistrationForm, self).clean()

        if self.is_valid():
            username_exists = models.Account.objects.filter(Q(username=cleaned_data['username'])).exists()
            if username_exists:
                self._errors['username'] = self.error_class(['A user with this username already exists'])

            email_exists = models.Account.objects.filter(Q(email=cleaned_data['email'])).exists()
            if email_exists:
                self._errors['email'] = self.error_class(['A user with this email already exists'])

        return cleaned_data

