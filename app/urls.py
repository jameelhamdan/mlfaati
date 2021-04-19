from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse
from django.views import generic


class IndexView(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('auth:login')


debug_urls = []
if settings.DEBUG:
    debug_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cdn/', include('cdn.urls')),
    path('api/v1/', include('api.urls')),
    path('console/', include('console.urls')),
    path('auth/', include('users.urls')),
    path('docs', include('docs.urls')),
    path('', IndexView.as_view(), name='index'),
] + debug_urls
