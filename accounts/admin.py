from django.contrib import admin
from .models import UserProfile


class UserProfileModel(admin.ModelAdmin):
    # list_display = ['user', 'get_friend_list', 'get_friend_request']
    list_display = ['user']

    class Meta:
        model = UserProfile


admin.site.register(UserProfile, UserProfileModel)
