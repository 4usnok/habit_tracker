from rest_framework import serializers

from habits.models import Habit
from habits.validators import (FillTimeValidator,
                               NumberOfHabitsCompletedValidator,
                               PleasantHabitInRelatedHabitValidator,
                               PleasantHabitValidator,
                               RewardOrRelatedHabitValidator)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RewardOrRelatedHabitValidator(),
            FillTimeValidator(),
            PleasantHabitInRelatedHabitValidator(),
            PleasantHabitValidator(),
            NumberOfHabitsCompletedValidator(),
        ]
