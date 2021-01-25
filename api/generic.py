from rest_framework import permissions
from . import authentication


class BaseAPIView:
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
