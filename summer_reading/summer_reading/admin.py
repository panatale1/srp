from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .forms import ReviewAdminForm
from .models import UserProfile, Review, Announcement, Rules


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_filter = ('make_public', 'user')
    search_fields = ['^user__first_name', '^user__last_name']
    raw_id_fields = ['user']
    form = ReviewAdminForm


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    pass


@admin.register(Rules)
class RulesAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'modified')


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class ReviewInline(admin.StackedInline):
    model = Review
    can_delete = False
    extra = 1
    form = ReviewAdminForm


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, ReviewInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
