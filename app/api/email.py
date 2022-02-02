import smtplib
from email.message import EmailMessage
from app.rest import Config


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
