import os
import sys
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
from multiprocessing import Process, freeze_support
from random import randint
from smtplib import SMTP, SMTP_SSL

import cv2
import keyboard
import mouse
import numpy as np
import psutil
from PIL import ImageGrab


def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except AttributeError:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

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

def action(retrieve, auto_time_warp):
	load_data()
	while psutil.Process(os.getpid()).parent() is not None:
		line_length = checks("lineLen")

		if line_length == 0:
			mouse.release(button="left")
			mouse.release(button="right")
			time.sleep(3)
			checks("aftReIn")
			if checks("full"):
				warp(auto_time_warp)
			else:
				motions("cast")
				caught = False
		elif line_length <= 5:
			mouse.press(button="left")
			time.sleep(1)
		else:
			if retrieve != "float":
				motions(retrieve)
			else:
				match checks("float-state"):
					case "wait":
						time.sleep(0.75)
					case "bite":
						motions("twitching")
					case "empty":
						motions("twitching")

def warp(auto_time_warp):
	global image_next_morning_gray
	keyboard.press_and_release("t")
	time.sleep(3)
	if auto_time_warp:
		while True:
			time.sleep(1)
			inf = cv2.minMaxLoc(cv2.matchTemplate(cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2GRAY), image_next_morning_gray, cv2.TM_SQDIFF))
			if inf[0] <= 1000000:
				mouse.move(inf[2][0], inf[2][1], absolute=True, duration=0)
				mouse.click(button="left")
				time.sleep(5)
				break
	else:
		# send_gmail(my_address=values.email_address, my_password=values.email_password, my_server=values.email_server, to_address=values.email_recipient, subject="Fishing-Planet-Autofisher: Manual time-warp", body="Keepnet is full!\nAwaiting manual time-warp!", screenshot=True)
		psutil.Process(os.getpid()).kill()

def motions(tip):
	match tip:
		case "twitching":
			mouse.press(button="left")
			time.sleep(0.05)
			mouse.press(button="right")
			time.sleep(0.25)
			mouse.release(button="right")
			time.sleep(0.65)
		case "stop-n-go":
			mouse.press(button="left")
			time.sleep(2)
			mouse.release(button="left")
			time.sleep(0.5)
		case "cast":
			mouse.press(button="left")
			time.sleep(1.935)
			mouse.release(button="left")
			time.sleep(12)

def checks(tip):
	global full_val_low, full_val_high
	global image_close_orange
	global image_close_gray
	global image_extend_orange
	global image_ok_orange
	global image_claim_green
	global image_release_gray, image_discard_gray, image_keep_orange
	global images_digits

	match tip:
		case "float-state":
			screen_load = ImageGrab.grab().load()
			for i in range(162, 200):
				if (full_val_low[0] <= screen_load[88, i][0] <= full_val_high[0]) and (full_val_low[1] <= screen_load[88, i][1] <= full_val_high[1]) and (full_val_low[2] <= screen_load[88, i][2] <= full_val_high[2]):
					return True
			return False
		case "full":
			screen_load = ImageGrab.grab().load()
			for i in range(162, 200):
				if (full_val_low[0] <= screen_load[88, i][0] <= full_val_high[0]) and (full_val_low[1] <= screen_load[88, i][1] <= full_val_high[1]) and (full_val_low[2] <= screen_load[88, i][2] <= full_val_high[2]):
					return True
			return False
		case "close-orange":
			inf = cv2.minMaxLoc(cv2.matchTemplate(cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2GRAY), image_close_orange, cv2.TM_SQDIFF))
			if inf[0] <= 1000000:
				mouse.move(inf[2][0], inf[2][1], absolute=True, duration=0)
				mouse.click(button="left")
				return True
			return False
		case "close-gray":
			inf = cv2.minMaxLoc(cv2.matchTemplate(cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2GRAY), image_close_gray, cv2.TM_SQDIFF))
			if inf[0] <= 1000000:
				mouse.move(inf[2][0], inf[2][1], absolute=True, duration=0)
				mouse.click(button="left")
				return True
			return False
		case "extend":
			inf = cv2.minMaxLoc(cv2.matchTemplate(cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2GRAY), image_extend_orange, cv2.TM_SQDIFF))
			if inf[0] <= 1000000:
				mouse.move(inf[2][0], inf[2][1], absolute=True, duration=0)
				mouse.click(button="left")
				return True
			return False
		case "ok":
			inf = cv2.minMaxLoc(cv2.matchTemplate(cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2GRAY), image_ok_orange, cv2.TM_SQDIFF))
			if inf[0] <= 1000000:
				mouse.move(inf[2][0], inf[2][1], absolute=True, duration=0)
				mouse.click(button="left")
				return True
			return False
		case "claim":
			inf = cv2.minMaxLoc(cv2.matchTemplate(cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2GRAY), image_claim_green, cv2.TM_SQDIFF))
			if inf[0] <= 1000000:
				mouse.move(inf[2][0], inf[2][1], absolute=True, duration=0)
				mouse.click(button="left")
				return True
			return False
		case "caughtfish":
			img = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2GRAY)
			rel = cv2.minMaxLoc(cv2.matchTemplate(img, image_release_gray, cv2.TM_SQDIFF))
			disc = cv2.minMaxLoc(cv2.matchTemplate(img, image_discard_gray, cv2.TM_SQDIFF))
			keep = cv2.minMaxLoc(cv2.matchTemplate(img, image_keep_orange, cv2.TM_SQDIFF))
			if disc[0] <= 1000000:
				mouse.move(disc[2][0], disc[2][1], absolute=True, duration=0)
				mouse.click(button="left")
				time.sleep(2)
				return True
			elif keep[0] <= 1000000:
				mouse.move(keep[2][0], keep[2][1], absolute=True, duration=0)
				mouse.click(button="left")
				time.sleep(2)
				return True
			elif rel[0] <= 1000000:
				mouse.move(rel[2][0], rel[2][1], absolute=True, duration=0)
				mouse.click(button="left")
				time.sleep(2)
				return True
			return False
		case "aftReIn":
			while True:
				if checks("caughtfish"):
					pass
				elif checks("close-orange"):
					pass
				elif checks("close-gray"):
					pass
				elif checks("extend"):
					pass
				elif checks("ok"):
					pass
				elif checks("claim"):
					pass
				else:
					break
				time.sleep(2)
		case "lineLen":
			cv_img = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(1423, 916, 1666, 1020))), cv2.COLOR_RGB2GRAY)
			poz_u_znam = {}
			digits_variations = len(images_digits) // 10
			for i in range(len(images_digits)):
				result = cv2.matchTemplate(cv_img, images_digits[i], cv2.TM_SQDIFF)
				pozicije = np.where(result <= 11500000)
				pozicije_x = pozicije[1]
				pozicije_y = pozicije[0]
				tem = {}
				for j in zip(pozicije_y, pozicije_x):
					if j[1] in tem.keys():
						tem[j[1]].append(result[j])
					else:
						tem[j[1]] = [result[j]]
				for j in tem.keys():
					if j in poz_u_znam.keys():
						poz_u_znam[j].append((i // digits_variations, min(tem[j])))
					else:
						poz_u_znam[j] = [(i // digits_variations, min(tem[j]))]
			koordinate = list(poz_u_znam.keys())
			norm_poz_u_znam = {}
			while len(koordinate) != 0:
				koord = koordinate[0]
				vrijednosti_koord = poz_u_znam[koord]
				koordinate.remove(koord)
				for i in range(1, 11):
					if koord - i in koordinate:
						vrijednosti_koord.extend(poz_u_znam[koord - i])
						koordinate.remove(koord - i)
					if koord + i in koordinate:
						vrijednosti_koord.extend(poz_u_znam[koord + i])
						koordinate.remove(koord + i)
				norm_poz_u_znam[koord] = vrijednosti_koord
			redoslijed = list(norm_poz_u_znam.keys())
			redoslijed.sort()
			broj = ""
			for i in redoslijed:
				mogucnosti = norm_poz_u_znam[i]
				vrijednost = mogucnosti[0][1]
				znamenka = mogucnosti[0][0]
				for j in mogucnosti:
					if j[1] < vrijednost:
						vrijednost = j[1]
						znamenka = j[0]
				broj += str(znamenka)
			if broj == "":
				broj = "0"
			return int(broj)

def start():
	global process_action
	global retrieve
	global auto_time_warp

	try:
		alive = process_action.is_alive()
	except (NameError, ValueError):
		alive = False

	if not alive:
		process_action = Process(target=action, args=(retrieve, auto_time_warp))
		process_action.start()

	else:
		process_action.kill()
		process_action.join()
		process_action.close()

		mouse.release(button="left")
		mouse.release(button="right")

def ext():
	global process_action

	keyboard.unhook_all_hotkeys()

	try:
		process_action.kill()
		process_action.join()
		process_action.close()
	except NameError:
		pass
	except ValueError:
		pass

	if mouse.is_pressed(button="left"):
		mouse.release(button="left")
	if mouse.is_pressed(button="right"):
		mouse.release(button="right")

	psutil.Process(os.getpid()).kill()

def load_data():
	global bluetension_val_low, bluetension_val_high
	bluetension_val_low = (25, 50, 170)
	bluetension_val_high = (55, 80, 200)

	global bluefish_val_low, bluefish_val_high
	bluefish_val_low = (40, 40, 120)
	bluefish_val_high = (70, 70, 170)

	global full_val_low, full_val_high
	full_val_low = (250, 185, 0)
	full_val_high = (260, 195, 5)

	global images_digits
	images_digits = []
	for i in range(10):
		for j in ("", "_dark"):
			images_digits.append(cv2.imread(resource_path(f"run_data\\{i}{j}.png"), cv2.IMREAD_GRAYSCALE))

	global image_claim_green
	image_claim_green = cv2.imread(resource_path(r"run_data/claim_green.png"), cv2.IMREAD_GRAYSCALE)

	global image_close_gray
	image_close_gray = cv2.imread(resource_path(r"run_data/close_gray.png"), cv2.IMREAD_GRAYSCALE)

	global image_close_orange
	image_close_orange = cv2.imread(resource_path(r"run_data/close_orange.png"), cv2.IMREAD_GRAYSCALE)

	global image_discard_gray
	image_discard_gray = cv2.imread(resource_path(r"run_data/discard_gray.png"), cv2.IMREAD_GRAYSCALE)

	global image_extend_orange
	image_extend_orange = cv2.imread(resource_path(r"run_data/extend_orange.png"), cv2.IMREAD_GRAYSCALE)

	global image_keep_orange
	image_keep_orange = cv2.imread(resource_path(r"run_data/keep_orange.png"), cv2.IMREAD_GRAYSCALE)

	global image_next_morning_gray
	image_next_morning_gray = cv2.imread(resource_path(r"run_data/next_morning_gray.png"), cv2.IMREAD_GRAYSCALE)

	global image_ok_orange
	image_ok_orange = cv2.imread(resource_path(r"run_data/ok_orange.png"), cv2.IMREAD_GRAYSCALE)

	global image_release_gray
	image_release_gray = cv2.imread(resource_path(r"run_data/release_gray.png"), cv2.IMREAD_GRAYSCALE)

	"""
	email_address = ""
	email_password = ""
	email_server = ""
	email_ssl = True
	email_tls = False
	email_recipient = ""
	
	orangekeep_val_low = (190, 120, 50)
	orangekeep_val_high = (245, 165, 95)
	bluetension_val_low = (25, 50, 170)
	bluetension_val_high = (55, 80, 200)
	bluefish_val_low = (40, 40, 120)
	bluefish_val_high = (70, 70, 170)
	whitebar_val_low = (180, 0, 0)
	whitebar_val_high = (235, 150, 150)
	full_val_low = (250, 185, 0)
	full_val_high = (260, 195, 5)  # (255, 190, 0)
	
	# bobber_val_low = (142, 8, 8)
	# bobber_val_high = (215, 165, 165)
	"""

def main():
	global retrieve, auto_time_warp

	retrieve_types = {1: "twitching",
	                  2: "stop-n-go",
	                  3: "float"}

	while True:
		os.system("cls")
		print("1. TWITCHING\n2. STOP & GO\n3. FLOAT\n\n")
		try:
			retrieve = retrieve_types[int(input("TYPE NUMBER: ").strip("."))]
			break
		except ValueError:
			print("INVALID NUMBER")
			time.sleep(2.5)
		except KeyError:
			print("INVALID NUMBER")
			time.sleep(2.5)

	while True:
		os.system("cls")
		auto_time_warp = input("AUTO TIME-WARP?(Y/N): ").upper()

		if "Y" in auto_time_warp or "YES" in auto_time_warp:
			auto_time_warp = True
			break
		elif "N" in auto_time_warp or "NO" in auto_time_warp:
			auto_time_warp = False
			break
		else:
			print("INVALID INPUT!")
			time.sleep(2.5)

	keyboard.add_hotkey("š", start, suppress=True, trigger_on_release=True)
	keyboard.add_hotkey("đ", ext, suppress=True, trigger_on_release=True)

	# instructions
	os.system("cls")

	retrieve_prt = retrieve
	if auto_time_warp:
		auto_time_warp_prt = "yes"
	else:
		auto_time_warp_prt = "no"

	print(f"\nTYPE: {retrieve_prt}\nAUTO TIME-WARP: {auto_time_warp_prt}\n\nPress š to start/stop\nPress đ to exit")

	keyboard.wait()


if __name__ == "__main__":
	freeze_support()

	main()
