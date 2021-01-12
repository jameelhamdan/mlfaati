from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views


app_name = 'console'
urlpatterns = [
    path('api/', include('console.api.views')),
    path('browse/<int:pk>', login_required(views.BrowseView.as_view()), name='browse_space'),
    path('', login_required(views.HomeView.as_view()), name='home'),
]
