from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_filter = ('make_public', 'user')
    search_fields = ['^user__first_name', '^user__last_name']
    raw_id_fields = ['user']

admin.site.register(User, UserAdmin)
