from telegram import Bot
from telegram.error import TelegramError
import os
import json

# Funciones para cargar y guardar mensajes de Telegram
def load_telegram():
    try:
        with open('telegram.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  

def save_telegram(telegram): 
    with open('telegram.json', 'w') as file:
        json.dump(telegram, file, indent=4)

# Función para enviar mensajes por Telegram
async def send_telegram_message(chat_id, message):
    telegram_messages = load_telegram()

    new_message = {
        "chat_id": chat_id,
        "message": message
    }
    telegram_messages.append(new_message)
    
    save_telegram(telegram_messages)

    telegram_bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))

    try:
        await telegram_bot.send_message(chat_id=chat_id, text=message)
    except TelegramError as e:
        raise Exception(f"Error al enviar el mensaje: {str(e)}")
