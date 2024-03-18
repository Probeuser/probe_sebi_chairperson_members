import sys
import smtplib
import traceback
from config import sebi_config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from log import log

def send_email(subject, message):
        # Email configuration
        sender_email = 'probepoc2023@gmail.com'
        receiver_email = 'probepoc2023@gmail.com'
        password = 'rovqljwppgraopla'  

        # Email content
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"Manual intervention required for {subject}"
        msg.attach(MIMEText(str(message), 'plain'))

        # Connect to the SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)

