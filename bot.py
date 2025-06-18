import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# Получение переменных окружения
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
SHEET_URL = os.getenv("SHEET_URL")
GOOGLE_KEY = json.loads(os.getenv("GOOGLE_KEY"))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Получаю данные...")

    try:
        # Авторизация через сервисный ключ
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_KEY, scope)
        client = gspread.authorize(creds)

        # Получение данных из таблицы
        sheet = client.open_by_url(SHEET_URL).sheet1
        data = sheet.get_all_values()

        # Отправка данных пользователю
        text = "\n".join([" | ".join(row) for row in data])
        bot.send_message(message.chat.id, text)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

bot.polling()
