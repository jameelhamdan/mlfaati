from django.urls import include, path


app_name = 'api'
urlpatterns = [
    path('browser/', include('api.browser.views')),
    path('space/', include('api.space.views')),
    path('folder/', include('api.folder.views')),
    path('file/', include('api.file.views')),
]
