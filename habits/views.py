from rest_framework.views import APIView

from habits.models import Habit
from habits.pagination import HabitPagination
from habits.serializers import HabitSerializer


class MyView(APIView):
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
