from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import views as auth_views
from common.views import PageMixin
from . import forms


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

