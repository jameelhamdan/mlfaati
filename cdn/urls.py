from django.urls import path
from . import views

app_name = 'cdn'
urlpatterns = [
    path('direct/<str:pk>', views.ServeByIdView.as_view(), name='by_id'),
    path('direct/<str:space_name>/<str:pk>', views.ServeByIdView.as_view(), name='by_space_and_id'),
    path('path/<str:space_name>/<path:path>', views.ServeByPathView.as_view(), name='by_path'),
]
