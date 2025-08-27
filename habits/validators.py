from datetime import timedelta

from django.core.exceptions import ValidationError


class RewardOrRelatedHabitValidator:
    """
    Валидатор для проверки, что заполнено только одно из полей:
    reward (вознаграждение) или related_habit (связанная привычка)
    """

    def __call__(self, attrs):
        reward = attrs.get("reward")
        related_habit = attrs.get("related_habit")
        if reward and related_habit:
            raise ValidationError(
                "В модели не должно быть заполнено одновременно и поле вознаграждения, "
                "и поле связанной привычки. Можно заполнить только одно из двух полей."
            )


class FillTimeValidator:
    """
    Валидатор для проверки, что время выполнения должно быть не больше 120 секунд
    """

    def __call__(self, attrs):
        time_to_complete = attrs.get("time_to_complete")
        if time_to_complete and time_to_complete > timedelta(seconds=120):
            raise ValidationError(
                "В модели время выполнения привычки должно быть не больше 120 секунд."
            )


class PleasantHabitInRelatedHabitValidator:
    """
    Валидатор для проверки, попадание в связанные привычки только привычек с признаком приятной привычки.
    """

    def __call__(self, attrs):
        sign_of_a_pleasant_habit = attrs.get(
            "sign_of_a_pleasant_habit"
        )  # приятная привычка
        related_habit = attrs.get("related_habit")  # связная привычка
        if related_habit:  # если существует связная привычка
            if (
                not related_habit.sign_of_a_pleasant_habit
            ):  # если в связной привычке нет приятной тогда выбрасываем исключение
                raise ValidationError(
                    "В связанные привычки могут попадать только привычки с признаком приятной привычки"
                )


class PleasantHabitValidator:
    """
    Валидатор для проверки, что у приятной привычки не может быть вознаграждения или связанной привычки
    """

    def __call__(self, attrs):
        sign_of_a_pleasant_habit = attrs.get("sign_of_a_pleasant_habit")
        reward = attrs.get("reward")
        related_habit = attrs.get("related_habit")
        if sign_of_a_pleasant_habit and (reward or related_habit):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )


class NumberOfHabitsCompletedValidator:
    """
    Валидатор для проверки, что нельзя выполнять привычку реже, чем 1 раз в 7 дней
    """

    def __call__(self, attrs):
        periodicity = attrs.get("periodicity")  # период
        if periodicity and periodicity > timedelta(days=7):
            # Если интервал выполнения привычки будет больше недели, например 8 дней, тогда
            # выполнение привычки может произойти на 8 дней, что вызовет исключение
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней")
