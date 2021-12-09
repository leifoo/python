# https://realpython.com/python-send-email/

import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = ""  # Enter your address
receiver_email = "".replace(' ', '').replace(',', ';').split(';') # Enter receiver address
# password = input("Type your password and press enter: ")
password = ''
message = """\
Subject: Test: Send email with Python

http://www.google.com/
This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)