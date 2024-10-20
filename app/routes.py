from flask import request, jsonify
from mailersend import emails
import os

from .user_handler import *
from .send_email import send_email
from .telegram import send_telegram_message
from app import app


# Crear Usuarios
@app.route('/users', methods=['POST'])
def createUser():
    data = request.get_json()
    message, status = create_user(data)
    return jsonify(message), status

# Obtener todos usuario
@app.route('/users', methods=['GET'])
def get_users():
    users = get_all_users()
    return jsonify(users), 200

#Obtener todos usuarios
@app.route('/users/<int:userId>', methods=['GET'])
def get_user(userId):
    user= get_user_id(userId)

    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

# Actualizar usuario
@app.route('/users/<int:userId>', methods=['PUT'])
def updateUser(userId):
    data = request.get_json()
    message, status = update_user(userId, data)
    return jsonify(message), status

# Eliminar usuario
@app.route('/users/<int:userId>', methods=['DELETE'])
def deleteUser(userId):
    message, status = delete_user(userId)
    return jsonify(message), status

# Enviar mensaje por correo electronico
@app.route('/sendemail', methods=['POST'])
def SendEmail():
    data = request.get_json()

    # Validacion para que los datos de la peticion esten completos 
    if 'recipients' not in data  or 'subject' not in data or 'content' not in data:
        return jsonify({"Faltan datos para enviar el correo: recipients, subject, o content"}), 400
    
    recipients = data['recipients']
    subject = data['subject']
    content = data['content']
    
    # Llamar a la función send_email para enviar el correo
    try:
        response = send_email(recipients, subject, content)
        return jsonify({"message": "Mensaje enviado","":response}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


# Enviar mensaje por Telegram
@app.route('/sendTelegram', methods=['POST'])
async def send_telegram():
    data = request.get_json()
    chat_id = data.get('chat_id')
    message = data.get('message')

    if not chat_id or not message:
        return jsonify({"error": "Se requiere chat_id y message"}), 400
    
    try:
        await send_telegram_message(chat_id, message)
        return jsonify({"message": "Mensaje enviado correctamente"}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500
