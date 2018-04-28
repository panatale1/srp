from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile, Review, Announcement


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_filter = ('make_public', 'user')
    search_fields = ['^user__first_name', '^user__last_name']
    raw_id_fields = ['user']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    pass


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
