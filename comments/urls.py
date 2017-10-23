from django.conf.urls import url
from . import views
from posts.views import PostApiVoteToggleRedirect, PostVoteToggleRedirect

app_name = 'comments'

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/(?P<pk>[0-9]+)/delete$', views.comment_delete, name='delete'),
    url(r'^(?P<slug>[\w-]+)/(?P<pk>[0-9]+)/like/$', PostVoteToggleRedirect.as_view(), name='upvote-toggle'),
    url(r'^api/(?P<slug>[\w-]+)/(?P<pk>[0-9]+)/like/$', PostApiVoteToggleRedirect.as_view(), name='upvote-toggle-api'),

]
