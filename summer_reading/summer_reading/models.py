from __future__ import unicode_literals

from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    SCHOOL_CHOICES = (
        ('Alexander Hamilton Junior/Senior High School', 'Alexander Hamilton Junior/Senior High School'),
        ('Edgemont Junior/Senior High School', 'Edgemont Junior/Senior High School'),
        ('Maria Regina High School', 'Maria Regina High School'),
        ('R.J. Bailey School', 'R.J. Bailey School'),
        ('Scarsdale Middle School', 'Scarsdale Middle School'),
        ('Scarsdale High School', 'Scarsdale High School'),
        ('Solomon Schechter School', 'Solomon Schechter School'),
        ('Woodlands Middle/High School', 'Woodlands Middle/High School'),
        ('Other', 'Other')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    school = models.CharField(max_length=64, choices=SCHOOL_CHOICES, default='Alexander Hamliton Junior/Senior High School', blank=True)
    other_school = models.CharField(max_length=64, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    next_grade = models.CharField(max_length=7, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Profile for {0} {1}'.format(self.user.first_name, self.user.last_name)


class Review(models.Model):
    author = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    review = models.TextField()
    make_public = models.NullBooleanField()
    user = models.ForeignKey(User, related_name='reviews')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{0} from {1} {2}'.format(self.title, self.user.first_name, self.user.last_name)


class Announcement(models.Model):
    title = models.CharField(max_length=64, null=True, blank=True)
    announcement = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, related_name='announcements',
        limit_choices_to={'is_staff': True, 'is_superuser': True})

    def __unicode__(self):
        return '{0} by {1} {2}'.format(self.title, self.author.first_name, self.author.last_name)

    @property
    def name(self):
        return '{0} {1}'.format(self.author.first_name, self.author.last_name)


class Rules(models.Model):
    content = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Rules'

    def __unicode__(self):
        return 'Rules created on {0}/{1}/{2}'.format(
            self.created.month, self.created.day, self.created.year)
