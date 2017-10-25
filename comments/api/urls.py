from django.conf.urls import include, url
from . import views

app_name = 'api-comments'

urlpatterns = [
    url(r'^$', views.CommentListAPIView.as_view(), name='index'),
    url(r'^create/$', views.CommentCreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', views.CommentDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', views.CommentUpdateAPIView.as_view(), name='update'),

]