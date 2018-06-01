from __future__ import unicode_literals

from ckeditor.widgets import CKEditorWidget
import django_superform
from intl_tel_input.widgets import IntlTelInputWidget
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import  PhoneNumberPrefixWidget

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Review, UserProfile


class ReviewForm(forms.ModelForm):
    review = forms.CharField(widget=CKEditorWidget())
    make_public = forms.BooleanField(
        widget=forms.CheckboxInput(), initial=True, required=False)

    class Meta:
        model = Review
        fields = ['title', 'author', 'review', 'make_public']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs.update(
            {'instance': Review(user=user, title='', author='', make_public=True, review='')}
        )
        super(ReviewForm, self).__init__(*args, **kwargs)


class UserProfileForm(forms.ModelForm):
    GRADE_CHOICES = (
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('College', 'College'),
    )
    age = forms.IntegerField()
    phone = forms.CharField(widget=IntlTelInputWidget(allow_dropdown=False))
    next_grade = forms.ChoiceField(choices=GRADE_CHOICES, initial='6')
    other_school = forms.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ['school', 'age', 'phone', 'next_grade', 'other_school']
     

class UserProfileField(django_superform.ModelFormField):

    def get_instance(self, form, name):
        try:
            return form.instance.profile
        except UserProfile.DoesNotExist:
            return None

    def get_prefix(self, form, name):
        return name

    def save(self, form, name, composite_form, commit):
        profile = super(UserProfileField, self).save(
            form, name, composite_form, False)
        if profile:
            profile.user = form.instance
            if commit:
                profile.save()
        return profile


class SignUpForm(django_superform.SuperModelForm):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
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
    profile = UserProfileField(UserProfileForm)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean(self):
        data = super(SignUpForm, self).clean()
        password, password_2 = data.get('password'), data.get('password_confirm')
        self.forms['profile'].empty_permitted = True
        if password and password_2 and password != password_2:
            code = 'password-confirmation-mismatch'
            errs = {
                ('password', 'Must match password confirmation'),
                ('password_confirm', 'Must match password'),
            }
            for field, msg in errs:
                self.add_error(field, ValidationError(msg, code))
        return data
