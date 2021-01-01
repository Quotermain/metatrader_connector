import smtplib, ssl
from email.message import EmailMessage

PORT = 465
LOGIN = 'pavelhat233@gmail.com'
PASSWORD = 'quotermain233'

def send_message(message):
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
		server.login(LOGIN, PASSWORD)
		sender = LOGIN
		reciever = 'bpconsult45@gmail.com'
		message = f"Subject: {message}\n "
		server.sendmail(sender, reciever, message)

if __name__ == '__main__':
	send_message('test')
