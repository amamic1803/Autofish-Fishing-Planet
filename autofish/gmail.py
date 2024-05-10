import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
from random import randint

from PIL import ImageGrab


class Gmail:
	def __init__(self, e_mail, key, server="smtp.gmail.com", port=587):
		self.my_e_mail = e_mail
		self.my_login_key = key
		self.my_server = server
		self.my_server_port = port

	def verify_credentials(self):
		with smtplib.SMTP(host=self.my_server, port=self.my_server_port) as smtp:
			try:
				smtp.ehlo()
				smtp.starttls()
				smtp.ehlo()
				smtp.login(user=self.my_e_mail, password=self.my_login_key)
				smtp.quit()
				return True
			except (smtplib.SMTPException,
			        smtplib.SMTPServerDisconnected,
			        smtplib.SMTPResponseException,
			        smtplib.SMTPSenderRefused,
			        smtplib.SMTPRecipientsRefused,
			        smtplib.SMTPDataError,
			        smtplib.SMTPConnectError,
			        smtplib.SMTPHeloError,
			        smtplib.SMTPNotSupportedError,
			        smtplib.SMTPAuthenticationError):
				return False

	def send_gmail(self, to: str, subject: str = "", body: str = "", file_paths: list = None, byte_streams: list = None, screenshot: bool = False):
		# generating email
		e_mail = MIMEMultipart()
		e_mail["From"] = self.my_e_mail
		e_mail["To"] = to
		e_mail["Subject"] = subject
		e_mail.attach(MIMEText(body))

		file_names = []
		if file_paths is not None:
			for i in file_paths:
				if os.path.exists(i):
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
		if byte_streams is not None:
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
		with smtplib.SMTP(host=self.my_server, port=self.my_server_port) as smtp:
			try:
				smtp.ehlo()
				smtp.starttls()
				smtp.ehlo()
				smtp.login(user=self.my_e_mail, password=self.my_login_key)
				smtp.send_message(msg=e_mail, from_addr=self.my_e_mail, to_addrs=to)
				smtp.quit()
				return True
			except (smtplib.SMTPException,
			        smtplib.SMTPServerDisconnected,
			        smtplib.SMTPResponseException,
			        smtplib.SMTPSenderRefused,
			        smtplib.SMTPRecipientsRefused,
			        smtplib.SMTPDataError,
			        smtplib.SMTPConnectError,
			        smtplib.SMTPHeloError,
			        smtplib.SMTPNotSupportedError,
			        smtplib.SMTPAuthenticationError):
				return False
