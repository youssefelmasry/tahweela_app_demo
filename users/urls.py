from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserRegisterView
from users.serializers import CustomObtainTokenSerializer

from django.urls import path

urlpatterns = [
    path('register/', UserRegisterView.as_view()),
    path('token/obtain/', TokenObtainPairView.as_view(serializer_class=CustomObtainTokenSerializer)),
    path('token/refresh/', TokenRefreshView.as_view()),
]
