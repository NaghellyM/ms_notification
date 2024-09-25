from mailersend import emails
from dotenv import load_dotenv
import os

load_dotenv()

mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

# define an empty dict to populate with mail values
mail_body = {}

mail_from = {
    "name": "Servidor de prueba",
    "email": "contact@trial-351ndgw2nndgzqx8.mlsender.net",
}

recipients = [
    {
        "name": "Karen Moreno",
        "email": "karennmo2115@gmail.com",
    }
]

#Para responder los correos
reply_to = {
    "name": "Servidor prueba",
    "email": "karennmo2115@gmail.com",
}

mailer.set_mail_from(mail_from, mail_body)
mailer.set_mail_to(recipients, mail_body)
mailer.set_subject("Servidor de prueba", mail_body)
mailer.set_html_content("<h1>Correo de prueba</h1>", mail_body)
mailer.set_plaintext_content("Correcto", mail_body)
mailer.set_reply_to(reply_to, mail_body)

# using print() will also return status code and data
print(mailer.send(mail_body))