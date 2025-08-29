from celery import shared_task
from habits.services import send_tg_message
from users.models import User


@shared_task
def get_info(action, time, email):
    # получаем пользователя по email
    user = User.objects.get(email=email)
    # формируем сообщение
    message = f"Время для действия {action}: {time}"
    if user.tg_chat_id:
        send_tg_message(user.tg_chat_id, message)
