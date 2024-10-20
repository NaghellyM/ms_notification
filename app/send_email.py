import os
import json
from flask import request
from mailersend import emails

# Funciones para cargar y guardar email
def load_email():
    with open('send_email.json', 'r') as file:
        return json.load(file)
    
def save_email(emails): 
    with open('send_email.json', 'w') as file:
        json.dump(emails, file, indent=4)

# Funcion para enviar correo electronico
def send_email(recipients, subject, content):
    email = load_email()
    data = request.get_json()

    recipients = data['recipients']
    newMessage = {
        "subject": data['subject'],
        "content": data['content'],
        'recipients': recipients
    }

    email.append(newMessage)
    save_email(email)
    
    mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))
    mail_body = {}
    mail_from = {
        "name": "GSTCP",
        "email": "ms_notificacion@trial-yzkq340d9q2ld796.mlsender.net",
    }
    
    reply_to = {
        "name": "Respuesta",
        "email": "karennmo2115@gmail.com",
    }

    # Establecer los detalles del correo
    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(subject, mail_body)
    mailer.set_html_content(f"<h1>{subject}</h1><br><p>{content}</p>", mail_body)
    mailer.set_reply_to(reply_to, mail_body)

    # Enviar correo
    response = mailer.send(mail_body)

    return response
