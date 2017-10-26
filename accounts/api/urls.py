from django.conf.urls import include, url
from . import views

app_name = 'api-accounts'

urlpatterns = [
    url(r'^register/$', views.UserCreateAPIView.as_view(), name='register'),
    url(r'^login/$', views.UserLoginAPIView.as_view(), name='login'),
]