from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views


app_name = 'console'
urlpatterns = [
    path('api/', include('console.api.views')),
    path('space/create', login_required(views.CreateSpaceView.as_view()), name='space_create'),
    path('space/<int:pk>/update', login_required(views.UpdateSpaceView.as_view()), name='space_update'),
    path('space/<int:pk>/browse', login_required(views.BrowseView.as_view()), name='space_browse'),
    path('', login_required(views.HomeView.as_view()), name='home'),
]
