from django.contrib import admin
from .models import Post


class PostAdminModel(admin.ModelAdmin):
    list_display = ['title', 'slug', 'updates', 'timestamp']
    list_display_links = ['title']
    list_filter = ['user','timestamp']
    search_fields = ['title', 'content']

    class Meta:
        model = Post


admin.site.register(Post, PostAdminModel)
