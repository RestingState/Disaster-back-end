import smtplib
from email.message import EmailMessage
from app.rest import Config
import requests


def send_email(reciever, subject, text):
    """
    receiver: str (email format)
    subject: str
    text: str

    Sends an email from 'stellarly.events@gmail.com' email to a given receiver
    """
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'Stellarly Events <stellarly.events@gmail.com>'
    msg['To'] = reciever
    msg.set_content(text)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login('stellarly.events@gmail.com', Config.ADMIN_PASSWORD)
    server.send_message(msg)
    server.quit()


def check_email_existance(email):
    """
    email: str

    Uses isitrealemail api to check whether given email exists and returns str status

    If exists, status is 'valid'
    """
    api_key = '88eccb50-0c86-48e9-92b3-d6339958e18c'
    response = requests.get(
        "https://isitarealemail.com/api/email/validate",
        params={'email': email},
        headers={'Authorization': "Bearer " + api_key})

    status = response.json()['status']
    return status
