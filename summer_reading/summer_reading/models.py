from __future__ import unicode_literals

from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    school = models.CharField(max_length=64, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    next_grade = models.CharField(max_length=7, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)

    def __unicode__(self):
        return 'Profile for {0} {1}'.format(self.user.first_name, self.user.last_name)


class Review(models.Model):
    author = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    review = models.TextField()
    make_public = models.NullBooleanField()
    user = models.ForeignKey(User, related_name='reviews')
    created = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{0} from {1} {2}'.format(self.title, self.user.first_name, self.user.last_name)
