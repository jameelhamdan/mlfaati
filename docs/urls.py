from django.urls import path
from .views import RootView, ServeView


app_name = 'docs'
urlpatterns = [
    path('', RootView.as_view(), name='root'),
    path('/<path:path>', ServeView.as_view(), name='files'),
]
