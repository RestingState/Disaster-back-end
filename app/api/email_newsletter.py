import smtplib
from email.message import EmailMessage
from app.rest import Config
import requests


def send_event_email(name, reciever, subject, city, text):
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
    text = text.replace('\n', '<br>')
    msg.set_content(f'''
<!DOCTYPE html>
<html>
    <body style="background-color: #f5f5f5; margin: 0 auto; padding: 20px 20px;">
        <div style="border-radius: 8px; background-color: #1b1b1b; margin-bottom: 8px; text-align: center; height: 90px;">
            <p style="font-size: 25px; font-family: 'Fira Sans', Helvetica, Arial, sans-serif; color: #ffffff; font-weight: 800; margin: 0; padding: 0; vertical-align: middle; line-height: 90px;">Stellarly</p>
        </div>
        <div style="border-radius: 10px; background-color: #ffffff; padding: 40px 30px; text-align: left; margin-bottom: 8px;">
            <p style="font-family: 'Fira Sans', Helvetica, Arial, sans-serif; font-size: 36px; color: #151515; font-weight: 800; letter-spacing: -0.6px; line-height: 46px; margin: 0; margin-bottom: 15px; padding: 0px 10px;">Dear {name},</p>
            <p style="font-family: 'Fira Sans', Helvetica, Arial, sans-serif !important; font-size: 20px; color: #333333; margin: 0; padding: 0px 10px; line-height: 30px; letter-spacing: -0.2px;">
                We are happy to announce that you are subscribed to satellites that will soon fly over {city}. Here is a list of these events:
            </p>
            <br />
            <br />
            <p style="font-family: 'Fira Sans', Helvetica, Arial, sans-serif !important; font-size: 20px; color: #333333; margin: 0; padding: 0px 10px; line-height: 30px; letter-spacing: -0.2px;">{text}</p>
            <br />
            <br />
            <p style="text-decoration: none; font-family: 'Fira Sans', Helvetica, Arial, sans-serif !important; font-size: 20px; color: #333333; margin: 0; padding: 0px 10px; line-height: 30px; letter-spacing: -0.2px;">
                Visit our website to get more information<br />
                www.stellarly.com
            </p>
        </div>
        <div style="border-radius: 8px; background-color: #1b1b1b; padding: 40px 30px; margin-bottom: 10px; height: 150px;">
            <p style="font-family: 'Fira Sans', Helvetica, Arial, sans-serif; color: #ffffff; font-size: 18px; font-weight: 500; line-height: 24px; letter-spacing: -0.2px; margin: 0; padding: 0px 10px;">Contact Us</p>
        </div>
    </body>
</html>
    ''', subtype='html')

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login('stellarly.events@gmail.com', Config.ADMIN_PASSWORD)
    server.send_message(msg)
    server.quit()


def send_feedback_email(name, email, text):
    msg = EmailMessage()
    msg['Subject'] = f'Message from {name} <{email}>'
    msg['From'] = f'{email} <stellarly.events@gmail.com>'
    msg['To'] = 'stellarly.events@gmail.com'
    msg.set_content(f'Received message:\n{text}')

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
