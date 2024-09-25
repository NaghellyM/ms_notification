import json
import os

from aiogram import Bot
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from mailersend import emails


# Funciones para cargar y guardar usuarios
def load_users():
    with open('telegram.json', 'r') as file:
        return json.load(file)

    # 'w' modo escritura


def save_users(users):
    with open('telegram.json', 'w') as file:
        json.dump(users, file, indent=4)


app = Flask(__name__)


@app.route('/users', methods=['GET'])
def getUsers():
    users = load_users()
    return jsonify(users)


@app.route('/users/<int:userId>', methods=['GET'])
def getUser(userId):
    users = load_users()
    user = None
    i = 0
    found = False
    # Búsqueda utilizando while y bandera
    while i < len(users) and not found:
        if users[i]['id'] == userId:
            user = users[i]
            found = True
    i += 1
    if found:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/users', methods=['POST'])
def createUser():
    users = load_users()
    data = request.get_json()

    if len(users) > 0:
        i = 1
        last_user = users[0]

        while i < len(users):
            if users[i]['id'] > last_user['id']:
                last_user = users[i]
            i += 1

        new_id = last_user['id'] + 1
    else:
        new_id = 1

    new_user = {
        "id": new_id,
        "name": data['name'],
        "password": data['password'],
        "email": data['email'],
        "nickname": data['nickname']
    }
    users.append(new_user)
    save_users(users)
    return jsonify({"message": "User created successfully"}), 204


@app.route('/users/<int:userId>', methods=['PUT'])
def updateUser(userId):
    users = load_users()
    user = None
    i = 0
    found = False
    # Búsqueda utilizando while y bandera
    while i < len(users) and not found:
        if users[i]['id'] == userId:
            user = users[i]
            found = True
        i += 1
    if found:
        data = request.get_json()
        user['name'] = data['name']
        user['password'] = data['password']
        user['email'] = data['email']
        user['nickname'] = data['nickname']
        save_users(users)
        return jsonify({"message": "User updated successfully"})
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/users/<int:userId>', methods=['DELETE'])
def deleteUser(userId):
    users = load_users()
    user = None
    i = 0
    found = False
    # Búsqueda utilizando while y bandera
    while i < len(users) and not found:
        if users[i]['id'] == userId:
            user = users[i]
            found = True
        i += 1
    if found:
        users.remove(user)
        save_users(users)
        return jsonify({"message": "User deleted successfully"}, 202)
    else:
        return jsonify({"error": "User not found"}), 404


# Email
@app.route('/sendemail', methods=['POST'])
def enviarCorreo():
    user = load_users()
    data = request.get_json()

    # recipients = data.get('recipients', [])
    recipients = data['recipients']
    newMessage = {
        "subject": data['subject'],
        "content": data['content'],
        'recipients': recipients
    }

    user.append(newMessage)
    save_users(user)

    load_dotenv()
    mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))
    mail_body = {}

    mail_from = {
        "name": "",
        "email": "contacto@trial-zr6ke4nodv9lon12.mlsender.net",
    }

    newMessage.get('recipients', [recipients])

    # Destinatarios
    reply_to = {
        "name": "Name",
        "email": "reply@domain.com",
    }

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(data['subject'], mail_body)
    mailer.set_html_content(f"<h1>{data['subject']}</h1><br><p>{data['content']}</p>", mail_body)
    mailer.set_reply_to(reply_to, mail_body)

    response = mailer.send(mail_body)
    print("respuesta de MailerSend:", response)
    return jsonify({"message": "Email sent successfully", "response": response}, 202)


# Telegram
async def send_telegram_message(chat_id, message):
    Karen_Bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    await Karen_Bot.send_message(chat_id=chat_id, text=message)


@app.route('/sendTelegram', methods=['POST'])
async def sendTelegram():
    data = request.get_json()
    chat_id = data['chat_id']
    message = data['message']

    user = load_users()
    newMessage = {
        "chat_id": chat_id,
        "message": message,
    }
    user.append(newMessage)
    save_users(user)

    await send_telegram_message(chat_id, message)
    return jsonify({"message": "Message sent successfully"}), 202


if __name__ == '__main__':
    app.run(debug=True)
