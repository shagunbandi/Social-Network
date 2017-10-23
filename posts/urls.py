from django.conf.urls import include, url
from . import views

app_name = 'posts'

urlpatterns = [
    # Posts
    url(r'^$', views.posts_list, name='index'),
    url(r'^create/$', views.posts_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', views.posts_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/update$', views.posts_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete$', views.posts_delete, name='delete'),
    url(r'^(?P<slug>[\w-]+)/like/$', views.PostVoteToggleRedirect.as_view(), name='upvote-toggle'),
    url(r'^api/(?P<slug>[\w-]+)/like/$', views.PostApiVoteToggleRedirect.as_view(), name='upvote-toggle-api'),

    # Comment
    url(r'^', include('comments.urls', namespace='comments')),

]
