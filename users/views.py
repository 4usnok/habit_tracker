from typing import Optional

from packaging.utils import _
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPE_BYTES
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import RegistrationSerializer, MyTokenObtainPairSerializer


class CreateUser(generics.CreateAPIView):
    """Создание/регистрация пользователя"""

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.save()

class UsersListAPIView(generics.ListAPIView):
    """Просмотр списка пользователей"""

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

class RetrieveUserAPIView(generics.RetrieveAPIView):
    """Просмотр конкретного пользователя"""

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    """Получение JWT-токена"""

    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def my_protected_view(request):
    # Ваш код представления
    return Response({'message': 'Авторизовано!'})
