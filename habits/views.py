from rest_framework.views import APIView

from habits.models import Habit
from habits.pagination import HabitPagination
from habits.serializers import HabitSerializer


class MyView(APIView):
    pagination_class = HabitPagination

    def get(self, request):
        queryset = Habit.objects.all()
        paginator = self.pagination_class()  # Создаем экземпляр пагинатора
        paginated_queryset = paginator.paginate_queryset(
            queryset, request
        )  # Пагинируем queryset
        serializer = HabitSerializer(paginated_queryset, many=True)  # Сериализируем
        return paginator.get_paginated_response(
            serializer.data
        )  # Возвращаем пагинированный ответ
