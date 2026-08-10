from dotenv import load_dotenv
import os

# for sending smtp email (SMTP - Simple Mail transfer protocol)
# multipart is used for suppose we want to send the mail with subject and body, and attachments, in one mail then we should use the multipart (MIMEMultipart creates that email container.)

# MIMEText is used for the sending mail body

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME")

def send_email(to_email, subject, body):
    try:
        message = MIMEMultipart()
        message["From"] = f"{SMTP_FROM_NAME} <{SMTP_USER}>"
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER,to_email,message.as_string())
        server.quit()

        print("Email sent successfully.")

    except Exception as e:
        import traceback
        traceback.print_exc()
