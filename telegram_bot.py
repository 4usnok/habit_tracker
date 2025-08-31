import os

import telebot
from dotenv import load_dotenv
from telebot import types
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from habits.models import Habit

from users.models import User
load_dotenv()

token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start','help'])
def handle_start(message):

    # Создание клавиатуры
    keyboard = types.ReplyKeyboardMarkup(row_width=10)
    button1 = types.KeyboardButton('Информация о привычках')
    keyboard.add(button1)

    bot.reply_to(
        message,
        'Здравствуйте, я ваш трекер привычек. Выберите пожалуйста действие',
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):

    user = User.objects.get(tg_chat_id=message.chat.id)
    habits = Habit.objects.filter(user=user)

    if message.text == 'Информация о привычках':
        # Действия при нажатии на кнопку
        if not habits.exists():
            bot.reply_to(
                message,
                "🤷‍♀️ Нет привычек к выполнению"
            )
            return
        response = f"📃 Информация о привычках пользователя {user.email}: \n\n"
        for habit in habits:
            response += f"🎯 {habit.action}\n"
            response += f"🕐 время: {habit.time} \n"
            response += f"🗺 место: {habit.place} \n"
            response += f"🎁 вознаграждение: {habit.reward} \n\n"
        bot.reply_to(
            message, response
        )

bot.infinity_polling()
