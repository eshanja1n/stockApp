import email
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account

class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30)

    class Meta:
        model = Account
        fields = ('username', 'email', 'fullname', 'password1', 'password2')


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('username', 'password')
    
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Invalid Login")

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('username', 'email', 'fullname', 'bio')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % account.email)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already in use.' % account.username)
    
    def clean_bio(self):
        if self.is_valid():
            bio = self.cleaned_data['bio']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(bio=bio)
            except Account.DoesNotExist:
                return bio
    
    def clean_fullname(self):
        if self.is_valid():
            fullname = self.cleaned_data['fullname']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(fullname=fullname)
            except Account.DoesNotExist:
                return fullname
            # raise forms.ValidationError('Username "%s" is already in use.' % account.username)

    # def clean_fullname(self):
    #     if self.is_valid():
    #         fullname = self.cleaned_data['fullname']
    #         account = Account.objects.exclude(pk=self.instance.pk).get(fullname=fullname)
            # try:
            #     account = Account.objects.exclude(pk=self.instance.pk).get(username=fullname)
            # except Account.DoesNotExist:
            #     return fullname
            # raise forms.ValidationError('Fullname "%s" is already in use.' % account.fullname)