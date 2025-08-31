from celery import shared_task

from habits.models import Habit
from habits.services import send_tg_message
from users.models import User


@shared_task
def get_info(email):
    # получаем пользователя по email
    user = User.objects.get(email=email)
    habit = Habit.objects.filter(user=user).first()
    if not habit:
        return {
            'status': 'error',
            'message': 'У пользователя нет привычек',
            'email': email
        }
    # формируем сообщение
    message = f"Время для действия {habit.action}: {habit.time}"

    if user.tg_chat_id:
        send_tg_message(user.tg_chat_id, message)

    return {
        'action': habit.action,
        'time': str(habit.time),
        'email': user.email,
        'message_sent': bool(user.tg_chat_id)
    }
