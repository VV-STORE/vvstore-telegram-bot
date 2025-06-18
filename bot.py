import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
GOOGLE_KEY = os.getenv("GOOGLE_KEY").replace('\\n', '\n')
GOOGLE_KEY = os.getenv("GOOGLE_KEY")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Получаю данные...")

    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('google_key.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_url(SHEET_URL).sheet1
        data = sheet.get_all_values()

        text = "\n".join([" | ".join(row) for row in data])
        bot.send_message(message.chat.id, text)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

bot.polling()
