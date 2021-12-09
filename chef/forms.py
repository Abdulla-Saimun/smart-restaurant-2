from django import forms
from .models import chef_account


class chef_account_form(forms.ModelForm):
    chef_email = forms.CharField(widget=forms.EmailInput())
    chef_pass = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = chef_account
        fields = [
            'chef_userid',
            'chef_fullname',
            'chef_email',
            'chef_phone',
            'chef_pass'
        ]