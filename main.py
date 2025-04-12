import os
import logging
import telebot
import openai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)

# Приветственное сообщение
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Здравствуйте! Опишите вашу проблему, и я помогу подобрать подходящего специалиста.")

# Обработка пользовательских сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты ассистент, помогающий подобрать психотерапевта по описанию проблемы."},
                {"role": "user", "content": message.text},
            ],
            temperature=0.7,
        )
        reply = response.choices[0].message["content"]
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

bot.polling()