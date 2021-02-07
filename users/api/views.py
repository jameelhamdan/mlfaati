from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions, authentication
from django.urls import path, reverse_lazy
from django.views import generic
import api.models


class DeleteTokenView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]
    lookup_url_kwarg = 'key'
    lookup_field = 'key'

    def get_queryset(self):
        return api.models.Token.objects.filter(user=self.request.user)


class AddTokenView(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        token = self.request.user.new_token()
        messages.success(self.request, _('Added Token.'))
        return reverse_lazy('auth:settings')


urlpatterns = [
    path('token/add', login_required(AddTokenView.as_view()), name='api_token_add'),
    path('token/<str:key>/delete', DeleteTokenView.as_view(), name='api_token_delete'),
]
