from django import forms
from django.db import models
from django.db.models import fields
from .models import manager_account


class manager_account_form(forms.ModelForm):
    man_email = forms.CharField(widget=forms.EmailInput())
    man_pass = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = manager_account
        fields = [
            'man_userid',
            'man_fullname',
            'man_email',
            'man_phone',
            'man_pass'
        ]


class manager_login_raw_form(forms.Form):
    man_userid = forms.CharField()
    man_pass = forms.CharField(widget=forms.PasswordInput())