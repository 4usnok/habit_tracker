import os

import telebot
from dotenv import load_dotenv
from telebot import types
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from habits.models import Habit
from users.models import User
from habits.tasks import get_info

load_dotenv()

token=os.getenv("BOT_TOKEN")
bot=telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Информация о привычках")
    markup.add(item1)
    bot.send_message(message.chat.id,'Здравствуйте! Выберите необходимую для вас функцию', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Информация о привычках")
def habits_info(message):
    user = User.objects.get(tg_chat_id=message.chat.id)
    habit = Habit.objects.filter(user=user).first()

    # Используем данные из БД
    task = get_info.delay(
        action=habit.action if habit else "Проверить привычки",
        time=habit.time if habit else "2025-03-15",
        email=user.email
    )

    # Сообщение, которое будет выводиться в боте
    bot.send_message(
        message.chat.id,
        f"✅ Задача запущена для {user.email}!\n\n"
        f"📋 Описание привычки:\n"
        f"• Действие: {habit.action if habit else 'Проверить привычки'}\n"
        f"• Время: {habit.time.strftime('%Y-%m-%d') if habit else '2025-03-15'}\n"
        f"• Email: {user.email}\n\n"
        f"🆔 ID задачи: {task.id}"
    )

bot.infinity_polling()
