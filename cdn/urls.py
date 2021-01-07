from django.urls import path
from . import views

app_name = 'cdn'
urlpatterns = [
    path('direct/<str:pk>', views.ServeByIdView.as_view(), name='by_id'),
    path('path/<path:path>', views.ServeByPathView.as_view(), name='by_path'),
]
