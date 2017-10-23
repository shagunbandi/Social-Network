from django.conf.urls import include, url
from django.contrib.auth import logout
from . import views

app_name = 'accounts'

urlpatterns = [
    # User
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^search/$', views.search_username, name='search'),

    # Friend Requests
    url(r'^sendrequest/(?P<username>[\w-]+)/$', views.send_request, name='send-request'),
    url(r'^cancelrequest/(?P<username>[\w-]+)/$', views.cancel_sent_request, name='cancel-request'),
    url(r'^declinerequest/(?P<username>[\w-]+)/$', views.decline_request, name='decline-request'),
    url(r'^acceptrequest/(?P<username>[\w-]+)/$', views.accept_request, name='accept-request'),
    url(r'^unfriend/(?P<username>[\w-]+)/$', views.unfriend, name='unfriend'),

    # Profile
    url(r'^profile/(?P<username>[\w-]+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<username>[\w-]+)/friend_list/$', views.friend_list, name='friend_list'),
    url(r'^profile/(?P<username>[\w-]+)/friend_requests/$', views.friend_requests, name='friend_requests'),
    url(r'^profile/(?P<username>[\w-]+)/user_posts/$', views.user_posts, name='user_posts'),
    url(r'^profile/(?P<username>[\w-]+)/user_comments/$', views.user_comments, name='user_comments'),
    url(r'^profile/(?P<username>[\w-]+)/liked_posts/$', views.liked_posts, name='liked_posts'),
]