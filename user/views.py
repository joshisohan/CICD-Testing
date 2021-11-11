"""This module contians views related to user login and creation"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import authentication, permissions
from user import serializers


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    """Creat a new user"""
    serializer_class = serializers.UserSerializer


class AuthTokenView(ObtainAuthToken):
    """An authentication token create view"""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UpdateUserView(generics.RetrieveUpdateAPIView):
    """Update existing user profile"""
    serializer_class = serializers.UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Return the authenticated user object"""
        return self.request.user
