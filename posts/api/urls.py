from django.conf.urls import include, url
from . import views

app_name = 'posts'

urlpatterns = [
    url(r'^$', views.PostListAPIView.as_view(), name='index'),
    url(r'^create/$', views.PostCreateAPIView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', views.PostDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.PostDestroyAPIView.as_view(), name='delete'),
    url(r'^(?P<slug>[\w-]+)/update/$', views.PostUpdateAPIView.as_view(), name='update'),
]