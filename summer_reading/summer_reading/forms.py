from __future__ import unicode_literals

from phonenumber_field.formfields import PhoneNumberField

from django import forms
from django.core.exceptions import ValidationError

from .models import Review, User


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author', 'title', 'review', 'make_public']


class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    school = forms.CharField(max_length=64)
    age = forms.IntegerField()
    next_grade = forms.IntegerField()
    phone = PhoneNumberField()
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'max_length': '50'}),
        required=True, min_length=8,
        error_messages={'required': 'Please enter your password',
                        'min_length': 'Choose a password that is between 8 and 50 characters'}
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'max_length': '50'}),
        required=True, min_length=8,
        error_messages={'required': 'Please confirm your password'},
        label='Confirm your password'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'school', 'age', 'next_grade', 'phone', 'email', 'password']
    def clean(self):
        data = super(SignUpForm, self).clean()
        password, password_2 = data.get('password'), data.get('password_confirm')
        if password and password_2 and password != password_2:
            code = 'password-confirmation-mismatch'
            errs = {
                ('password', 'Must match password confirmation'),
                ('password_confirm', 'Must match password'),
            }
            for field, msg in errs:
                self.add_error(field, ValidationError(msg, code))
        return data
