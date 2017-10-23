from django.contrib import admin
from .models import Comment


class CommentAdminModel(admin.ModelAdmin):
    list_display = ['user', 'content', 'date']
    list_display_links = ['content']
    list_filter = ['user', 'date']
    search_fields = ['content', 'user']

    class Meta:
        model = Comment


admin.site.register(Comment, CommentAdminModel)
