from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import views as auth_views
from django.views import generic
from common.views import PageMixin
from . import models, forms
import api.models


class LoginView(PageMixin, auth_views.LoginView):
    template_name = 'users/login.html'
    form_class = forms.LoginForm
    page_title = _('Sign in')
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)

        return super(LoginView, self).form_valid(form)


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('auth:login')


class SettingsView(PageMixin, generic.UpdateView):
    template_name = 'settings/index.html'
    form_class = forms.SettingsForm
    success_url = reverse_lazy('auth:settings')
    page_title = _('Settings')
    breadcrumbs = [
        (_('Settings'), '#'),
    ]

    def get_object(self, queryset=None):
        return models.User.objects.get(pk=self.request.user.pk)
