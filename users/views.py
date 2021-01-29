from rest_framework.generics import CreateAPIView
from rest_framework import permissions

from users.serializers import UserRegisterSerializer

class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]
