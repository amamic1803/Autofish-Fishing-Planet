from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
from random import randint
from smtplib import SMTP, SMTP_SSL
from PIL import ImageGrab
import os


def send_gmail(my_address: str, my_password: str, my_server: str, to_address: str, if_ssl: bool = True, if_tls: bool = False, subject: str = "", body: str = "", file_paths: list = [], byte_streams: list = [], screenshot: bool = False):
	# generating email
	e_mail = MIMEMultipart()
	e_mail["From"] = my_address
	e_mail["To"] = to_address
	e_mail["Subject"] = subject
	e_mail.attach(MIMEText(body))

	file_existance = True

	file_names = []

	for i in file_paths:
		if not os.path.exists(i):
			file_existance = False
		else:
			basen = os.path.basename(i)
			while basen in file_names:
				basen = f'{basen.split(".")[0]}{randint(10 ** 10, 10 ** 15)}.{basen.split(".")[1]}'
			file_names.append(basen)
			file = open(i, "rb")
			attac = MIMEBase("application", "octet-stream")
			attac.set_payload(file.read())
			encoders.encode_base64(attac)
			attac.add_header("Content-Disposition", f'attachement; filename="{basen}"')
			e_mail.attach(attac)
			del file, attac, basen

	for i in byte_streams:
		basen = i[1]
		while basen in file_names:
			basen = f'{basen.split(".")[0]}{randint(10 ** 10, 10 ** 15)}.{basen.split(".")[1]}'
		file_names.append(basen)
		attac = MIMEBase("application", "octet-stream")
		attac.set_payload(i[0])
		encoders.encode_base64(attac)
		attac.add_header("Content-Disposition", f'attachement; filename="{basen}"')
		e_mail.attach(attac)
		del attac, basen

	if screenshot:
		basen = "screenshot.png"
		while basen in file_names:
			basen = f"screenshot{randint(10 ** 10, 10 ** 15)}.png"
		scrnsht = BytesIO()
		ImageGrab.grab().save(scrnsht, format="png")
		scrn = MIMEBase("application", "octet-stream")
		scrn.set_payload(scrnsht.getvalue())
		encoders.encode_base64(scrn)
		scrn.add_header("Content-Disposition", f'attachment; filename="{basen}"')
		e_mail.attach(scrn)
		del scrn, scrnsht, basen

	del file_names

	# sending email
	if if_ssl:
		with SMTP_SSL(my_server) as smtp:
			try:
				smtp.ehlo()
				smtp.login(my_address, my_password)
				smtp.send_message(e_mail, my_address, to_address)
				mail_sent = True
			except:
				mail_sent = False
	elif if_tls:
		with SMTP(my_server) as smtp:
			try:
				smtp.ehlo()
				smtp.starttls()
				smtp.login(my_address, my_password)
				smtp.send_message(e_mail, my_address, to_address)
				mail_sent = True
			except:
				mail_sent = False
	else:
		with SMTP(my_server) as smtp:
			try:
				smtp.ehlo()
				smtp.login(my_address, my_password)
				smtp.send_message(e_mail, my_address, to_address)
				mail_sent = True
			except:
				mail_sent = False

	if mail_sent:
		ret_message = "E-Mail sent successfully!"
	else:
		ret_message = "E-Mail failed to send!"

	if not file_existance:
		ret_message += "\nAt least one file not found!"

	return mail_sent, ret_message


if __name__ == "__main__":
	# print(send_email(my_address="", my_password="", my_server="", to_address="", if_ssl=True, if_tls=False, subject="test-subject", body="test-body", file_paths=[], byte_streams=[[open(r"test.png", "rb").read(), "test-byte.png"]], screenshot=True))
	pass
