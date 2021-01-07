from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


debug_urls = []
if settings.DEBUG:
    debug_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cdn/', include('cdn.urls'))
] + debug_urls
