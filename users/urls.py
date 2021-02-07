from django.urls import path, include
from . import views


app_name = 'auth'
urlpatterns = [
    path('api/', include('users.api.views')),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('settings', views.SettingsView.as_view(), name='settings'),
]
