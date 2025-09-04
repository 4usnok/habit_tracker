from rest_framework import generics, permissions
from rest_framework.views import APIView

from habits.models import Habit
from habits.pagination import HabitPagination
from habits.permissions import IsOwner
from habits.serializers import HabitValidSerializer, HabitSerializer


class MyView(APIView):
    """Пагинация"""

    pagination_class = HabitPagination

    def get(self, request):
        queryset = Habit.objects.all()
        # Создаем экземпляр пагинатора
        paginator = self.pagination_class()
        # Пагинируем queryset
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        # Сериализируем
        serializer = HabitSerializer(paginated_queryset, many=True)
        # Возвращаем пагинированный ответ
        return paginator.get_paginated_response(serializer.data)


class ListPrivateAPIViewPermissions(generics.ListAPIView):
    """Просмотр списка привычек владельца"""

    queryset = Habit.objects.all()
    serializer_class = HabitValidSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)


class ListPublicAPIViewPermissions(generics.ListAPIView):
    """Просмотр публичного списка владельца"""

    queryset = Habit.objects.all()
    serializer_class = HabitValidSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class CreateAPIViewPermissions(generics.ListCreateAPIView):
    """Создание привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitValidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RetrieveAPIViewPermissions(generics.RetrieveAPIView):
    """Пользователь имеет право просматривать только свои привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitValidSerializer
    permission_classes = [
        IsOwner,
        permissions.IsAuthenticated,
    ]  # Применение пользовательского разрешения


class UpdateAPIViewPermissions(generics.UpdateAPIView):
    """Пользователь имеет право редактировать только свои привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitValidSerializer
    permission_classes = [
        IsOwner,
        permissions.IsAuthenticated,
    ]  # Применение пользовательского разрешения


class DestroyAPIViewPermissions(generics.DestroyAPIView):
    """Пользователь имеет право удалять только свои привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitValidSerializer
    permission_classes = [
        IsOwner,
        permissions.IsAuthenticated,
    ]  # Применение пользовательского разрешения
