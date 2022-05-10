import datetime
import os
import smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject):
    smtp_server = os.environ.get('SMTP_SERVER')
    port = os.environ.get('PORT')
    sender_email = os.environ.get('EMAIL_SENDER')
    receiver_email = os.environ.get('EMAIL_TO')
    cc_email = os.environ.get('EMAIL_CC')
    password = os.environ.get('EMAIL_PASSWORD')
    body = os.environ.get('BODY')

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message['CC'] = cc_email

    message.attach(MIMEText(body, 'plain'))
    filename = 'output.xlsx'

    with open(filename, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        'Content-Disposition', f'attachment; filename= {filename}'
    )
    print(message.as_string())
    message.attach(part)
    text = message.as_string()

    answer = input('do you want to send this email?[Y/n]')
    if answer.strip() in ['no', 'No', 'n', 'N']:
        return
    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, int(port))
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)

        server.sendmail(sender_email, receiver_email, text)
    except Exception as e:
        print(e)
    finally:
        server.quit()


if __name__ == '__main__':
    send_email("Flash's Daily Task Log for Sun 8/May/22")
