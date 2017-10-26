from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^posts/', include('posts.urls', namespace='posts')),
    url(r'^api/posts/', include('posts.api.urls', namespace='api-posts')),
    url(r'^api/comments/', include('comments.api.urls', namespace='api-comments')),
    url(r'^api/accounts/', include('accounts.api.urls', namespace='api-accounts')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns.append(url(r'^', views.index, name='index'))
