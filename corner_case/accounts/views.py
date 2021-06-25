from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer


class CreateUserView(CreateAPIView):
    """
    Register
    Only logged in users can create other accounts
    """
    model = get_user_model()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer
