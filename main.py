import os
import smtplib
import sys
import time
import tkinter
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
from multiprocessing import Process, freeze_support
from random import randint
from tkinter.messagebox import showerror, showinfo

import cv2
import keyboard
import mouse
import numpy as np
import psutil
from PIL import Image as ImagePIL
from PIL import ImageGrab, ImageTk


def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except AttributeError:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

def hex_to_rgb(hex_value):
	hex_value = hex_value.lstrip("#")
	return tuple(int(hex_value[i:i + 2], 16) for i in (0, 2, 4))

def rotate_image(image, angle):
	image_center = tuple(np.array(image.shape[1::-1]) / 2)
	rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
	result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
	return result

def motions(tip):
	match tip:
		case "Twitching":
			mouse.press(button="left")
			time.sleep(0.05)
			mouse.press(button="right")
			time.sleep(0.25)
			mouse.release(button="right")
			time.sleep(0.65)
		case "Stop&Go":
			mouse.press(button="left")
			time.sleep(1.425)
			mouse.release(button="left")
			time.sleep(0.45)
		case "Lift&Drop":
			mouse.press(button="left")
			time.sleep(1.75)
			mouse.release(button="left")
			time.sleep(0.25)
			mouse.press(button="right")
			time.sleep(0.25)
			mouse.release(button="right")
			time.sleep(0.25)
		case "Straight":
			mouse.press(button="left")
			time.sleep(1)
		case "Straight & Slow":
			mouse.press(button="left")
			time.sleep(1)
		case "Popping":
			pass
		case "Walking":
			pass
		case "Float":
			pass
		case "Bottom":
			pass

def checks(tip):
	global full_val_low, full_val_high
	#global bluetension_val_low, bluetension_val_high
	#global bluefish_val_low, bluefish_val_high
	global image_close_orange
	global image_close_gray
	global image_extend_orange
	global image_ok_orange
	global image_claim_green
	global image_release_gray, image_discard_gray, image_keep_orange
	global images_digits

	match tip:
		case "float-state":
			pass
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

def warp(auto_time_warp, night, status_mails, e_mail_client):
	# TODO: warp function
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

def action(retrieve, cast_len, num_of_rods, night_toggle, auto_time_warp_toggle, status_mails_toggle, email):
	load_data()
	while psutil.Process(os.getpid()).parent() is not None:
		line_length = checks("lineLen")

		# TODO: release fish with fine
		# TODO: solve float and bottom

		if line_length == 0:
			mouse.release(button="left")
			mouse.release(button="right")
			time.sleep(3)

			checks("aftReIn")

			# TODO: check for rod damage, change rod

			if checks("full"):  # TODO: warp by time of day, not only full keepnet
				warp(auto_time_warp_toggle, night_toggle, status_mails_toggle, email)
			else:
				# cast
				mouse.press(button="left")
				time.sleep(0.8575 + ((1.1 * cast_len) / 100))
				mouse.release(button="left")
				time.sleep(8 + ((4 * cast_len) / 100))
		elif line_length <= 5:
			# reel in slower if 5 meters or less
			mouse.press(button="left")
			time.sleep(1)
		else:
			# TODO: reel-in if fish is hooked
			match retrieve:
				case "Float":
					match checks("float-state"):
						case "wait":
							time.sleep(0.75)
						case "bite":
							motions("Twitching")
						case "empty":
							motions("Twitching")
				case "Bottom":
					pass
				case _:
					motions(retrieve)

def start():
	global started
	global process_action
	global root, background_image, background_label

	global retrieve, cast_len, num_of_rods
	global night_toggle, auto_time_warp_toggle, status_mails_toggle
	global email

	if not started:
		started = True
		background_image.clean_background(x=0, y=root.winfo_height() - 20, ind=3)
		background_image.draw_circle((10, root.winfo_height() - 10), 3, color="#2DFA09", filled=True)
		background_image.generate_tkinter_img()
		background_label.configure(image=background_image.image_tkinter)
		process_action = Process(target=action, args=(retrieve, cast_len, num_of_rods, night_toggle, auto_time_warp_toggle, status_mails_toggle, email))
		process_action.start()
	else:
		try:
			process_action.kill()
			process_action.join()
			process_action.close()
		except (NameError, ValueError):
			pass

		background_image.clean_background(x=0, y=root.winfo_height() - 20, ind=3)
		background_image.draw_circle((10, root.winfo_height() - 10), 3, color="#FF0000", filled=True)
		background_image.generate_tkinter_img()
		background_label.configure(image=background_image.image_tkinter)

		mouse.release(button="left")
		mouse.release(button="right")

		started = False

def load_data():
	global full_val_low, full_val_high
	full_val_low = (250, 185, 0)
	full_val_high = (260, 195, 5)

	#global bluetension_val_low, bluetension_val_high
	#bluetension_val_low = (25, 50, 170)
	#bluetension_val_high = (55, 80, 200)

	#global bluefish_val_low, bluefish_val_high
	#bluefish_val_low = (40, 40, 120)
	#bluefish_val_high = (70, 70, 170)

	"""
	# bobber_val_low = (142, 8, 8)
	# bobber_val_high = (215, 165, 165)
	"""

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

def background_click(event):
	global started
	global night_toggle_1, night_toggle_2
	global auto_time_warp_toggle_1, auto_time_warp_toggle_2
	global status_mails_toggle_1, status_mails_toggle_2
	if not started:
		if event.x <= 50:
			if 115 <= event.y <= 150:
				retrieve_select()
			elif 155 <= event.y <= 190:
				cast_len_select()
			elif 195 <= event.y <= 230:
				rods_select()
		if event.x >= 505:
			if 115 <= event.y <= 150:
				toggle_btn(night_toggle_1, night_toggle_2, toggle_night())
			elif 155 <= event.y <= 190:
				toggle_btn(auto_time_warp_toggle_1, auto_time_warp_toggle_2, toggle_auto_time_warp())
			elif 195 <= event.y <= 230:
				toggle_btn(status_mails_toggle_1, status_mails_toggle_2, toggle_status_mails())

def retrieve_select():
	global retrieve_types, root, started, hotkey
	if not started:
		keyboard.unhook_all_hotkeys()

		option_height = 30

		width = 250
		height = option_height * len(retrieve_types)

		background_image = BackgroundImage(width=width, height=height)
		wood_texture = cv2.imread(resource_path("run_data\\wood_texture.png"), cv2.IMREAD_UNCHANGED)
		pasted_height = 0
		while pasted_height < height:
			if height - (pasted_height + wood_texture.shape[0]) < 0:
				wood_texture = wood_texture[:height - pasted_height, :]
			background_image.paste_image(wood_texture, x_loc=0, y_loc=pasted_height, bgr=True)
			pasted_height += wood_texture.shape[0]
		del wood_texture

		for i in range(len(retrieve_types)):
			background_image.add_text(retrieve_types[i], cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=0, y_loc=(i * option_height) + (option_height // 3) // 2, x_width=width, y_height=(2 * option_height) // 3, color="#ffffff")

		background_image.generate_tkinter_img()

		select_window = tkinter.Toplevel(root)
		select_window.title("Select retrieve!")
		select_window.geometry(f"{width}x{height}+{(root.winfo_screenwidth() // 2) - (width // 2)}+{(root.winfo_screenheight() // 2) - (height // 2)}")
		select_window.resizable(False, False)
		select_window.grab_set()
		select_window.focus()

		background_lbl = tkinter.Label(select_window, highlightthickness=0, borderwidth=0, image=background_image.image_tkinter)
		background_lbl.place(x=0, y=0, width=width, height=height)
		background_lbl.bind("<ButtonRelease-1>", lambda event: retrieve_select_click(event, option_height, retrieve_types, select_window))

		select_window.iconbitmap(resource_path("data\\fish_icon.ico"))
		select_window.wait_window()
		keyboard.add_hotkey(hotkey, start, suppress=True, trigger_on_release=True)

def retrieve_select_click(event, option_height, retrieve_types, toplevel_win):
	global retrieve
	global background_image, background_label
	retrieve = retrieve_types[event.y // option_height]
	toplevel_win.destroy()
	background_image.clean_background(x=150, y=120, ind=0)
	background_image.add_text(retrieve, cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=150, y_loc=127, x_width=175, y_height=16, color="#000000")
	background_image.generate_tkinter_img()
	background_label.configure(image=background_image.image_tkinter)

def cast_len_select():
	global root, started, hotkey, cast_len
	if not started:
		keyboard.unhook_all_hotkeys()

		width = 450
		height = 80

		background_gradient_image = BackgroundImage(width=350, height=40)
		background_gradient_image.generate_gradient(starting_color="#38A0B2", ending_color="#B9B63D")

		background_image = BackgroundImage(width=width, height=height)
		wood_texture = cv2.imread(resource_path("run_data\\wood_texture.png"), cv2.IMREAD_UNCHANGED)

		pasted_height = 0
		while pasted_height < height:
			if height - (pasted_height + wood_texture.shape[0]) < 0:
				wood_texture = wood_texture[:height - pasted_height, :]
			background_image.paste_image(wood_texture, x_loc=0, y_loc=pasted_height, bgr=True)
			pasted_height += wood_texture.shape[0]
		pasted_width = 0
		while pasted_width < width:
			if width - (pasted_width + wood_texture.shape[1]) < 0:
				wood_texture = wood_texture[:, :width - pasted_width]
			background_image.paste_image(wood_texture, x_loc=pasted_width, y_loc=0, bgr=True)
			pasted_width += wood_texture.shape[1]
		del wood_texture

		background_image.paste_image(background_gradient_image.image, x_loc=50, y_loc=20)
		del background_gradient_image

		background_image.add_text(" 0 % ", cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=0, y_loc=20, x_width=50, y_height=40, color="#ffffff")
		background_image.add_text("100 %", cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=400, y_loc=20, x_width=50, y_height=40, color="#ffffff")

		line_loc = 50 + int(round(350 * (cast_len / 100), 0))

		background_image.draw_line((line_loc, 19), (line_loc, 60), "#E2062C", 2)

		background_image.generate_tkinter_img()

		select_window = tkinter.Toplevel(root)
		select_window.title("Select cast length!")
		select_window.geometry(f"{width}x{height}+{(root.winfo_screenwidth() // 2) - (width // 2)}+{(root.winfo_screenheight() // 2) - (height // 2)}")
		select_window.resizable(False, False)
		select_window.grab_set()
		select_window.focus()

		background_lbl = tkinter.Label(select_window, highlightthickness=0, borderwidth=0, image=background_image.image_tkinter)
		background_lbl.place(x=0, y=0, width=width, height=height)
		background_lbl.bind("<ButtonRelease-1>", lambda event: cast_len_select_click(event, 50, 350, select_window))

		select_window.iconbitmap(resource_path("data\\fish_icon.ico"))
		select_window.wait_window()
		keyboard.add_hotkey(hotkey, start, suppress=True, trigger_on_release=True)

def cast_len_select_click(event, x_start, box_size, toplevel_win):
	global cast_len
	global background_image, background_label
	if event.x < x_start:
		cast_len = 15
	elif event.x >= x_start + box_size:
		cast_len = 100
	else:
		cast_len = int(round(((event.x - x_start) / box_size) * 100, 0))
		if cast_len < 15:
			cast_len = 15
	toplevel_win.destroy()
	background_image.clean_background(x=200, y=160, ind=1)
	background_image.add_text(f"{cast_len} %", cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=200, y_loc=167, x_width=75, y_height=16, color="#000000")
	background_image.generate_tkinter_img()
	background_label.configure(image=background_image.image_tkinter)

def rods_select():
	global root, started, hotkey
	if not started:
		keyboard.unhook_all_hotkeys()

		width = 250
		height = 30
		rods = 7

		background_image = BackgroundImage(width=width, height=height)
		wood_texture = cv2.imread(resource_path("run_data\\wood_texture.png"), cv2.IMREAD_UNCHANGED)
		pasted_height = 0
		while pasted_height < height:
			if height - (pasted_height + wood_texture.shape[0]) < 0:
				wood_texture = wood_texture[:height - pasted_height, :]
			background_image.paste_image(wood_texture, x_loc=0, y_loc=pasted_height, bgr=True)
			pasted_height += wood_texture.shape[0]
		del wood_texture

		for i in range(1, rods + 1):
			background_image.add_text(str(i), cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=(((width - (height * rods)) // 2) + ((i - 1) * height)), y_loc=((height // 3) // 2), x_width=height, y_height=(2 * height) // 3, color="#ffffff")

		background_image.generate_tkinter_img()

		select_window = tkinter.Toplevel(root)
		select_window.title("Select rods!")
		select_window.geometry(f"{width}x{height}+{(root.winfo_screenwidth() // 2) - (width // 2)}+{(root.winfo_screenheight() // 2) - (height // 2)}")
		select_window.resizable(False, False)
		select_window.grab_set()
		select_window.focus()

		background_lbl = tkinter.Label(select_window, highlightthickness=0, borderwidth=0, image=background_image.image_tkinter)
		background_lbl.place(x=0, y=0, width=width, height=height)
		background_lbl.bind("<ButtonRelease-1>", lambda event: rods_select_click(event, rods, ((width - (height * rods)) // 2), height, select_window))

		select_window.iconbitmap(resource_path("data\\fish_icon.ico"))
		select_window.wait_window()
		keyboard.add_hotkey(hotkey, start, suppress=True, trigger_on_release=True)

def rods_select_click(event, rods, x_start, box_size, toplevel_win):
	global num_of_rods
	global background_image, background_label
	if event.x < x_start:
		num_of_rods = 1
	elif event.x >= ((rods * box_size) + x_start):
		num_of_rods = rods
	else:
		num_of_rods = ((event.x - x_start) // box_size) + 1
	toplevel_win.destroy()
	background_image.clean_background(x=220, y=200, ind=2)
	background_image.add_text(str(num_of_rods), cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=220, y_loc=207, x_width=35, y_height=16, color="#000000")
	background_image.generate_tkinter_img()
	background_label.configure(image=background_image.image_tkinter)

def toggle_btn(widget1, widget2, variable):
	global started
	if not started:
		if variable is None:
			pass
		elif not variable:
			widget1.config(background="#2DFA09", activebackground="#2DFA09", highlightthickness=0)
			widget2.config(background="#2DFA09", activebackground="#2DFA09", highlightthickness=3)
			widget1.place_configure(y=widget1.winfo_y() + 5, height=widget1.winfo_height() - 10)
			widget2.place_configure(y=widget2.winfo_y() - 5, height=widget2.winfo_height() + 10)
		else:
			widget1.config(background="#FF0000", activebackground="#FF0000", highlightthickness=3)
			widget2.config(background="#FF0000", activebackground="#FF0000", highlightthickness=0)
			widget1.place_configure(y=widget1.winfo_y() - 5, height=widget1.winfo_height() + 10)
			widget2.place_configure(y=widget2.winfo_y() + 5, height=widget2.winfo_height() - 10)

def toggle_night():
	global night_toggle
	global started
	if not started:
		night_toggle = not night_toggle
	return not night_toggle

def toggle_auto_time_warp():
	global auto_time_warp_toggle
	global started
	if not started:
		auto_time_warp_toggle = not auto_time_warp_toggle
	return not auto_time_warp_toggle

def toggle_status_mails():
	global root
	global status_mails_toggle
	global started
	global tick_click
	if not started:
		if not status_mails_toggle:
			keyboard.unhook_all_hotkeys()

			tick_click = False
			width = 450
			height = 115

			background_image = BackgroundImage(width=width, height=height)
			wood_texture = cv2.imread(resource_path("run_data\\wood_texture.png"), cv2.IMREAD_UNCHANGED)

			pasted_height = 0
			while pasted_height < height:
				if height - (pasted_height + wood_texture.shape[0]) < 0:
					wood_texture = wood_texture[:height - pasted_height, :]
				background_image.paste_image(wood_texture, x_loc=0, y_loc=pasted_height, bgr=True)
				pasted_height += wood_texture.shape[0]
			pasted_width = 0
			while pasted_width < width:
				if width - (pasted_width + wood_texture.shape[1]) < 0:
					wood_texture = wood_texture[:, :width - pasted_width]
				background_image.paste_image(wood_texture, x_loc=pasted_width, y_loc=0, bgr=True)
				pasted_width += wood_texture.shape[1]
			del wood_texture

			background_image.add_text("Gmail", cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=0, y_loc=12, x_width=width, y_height=25, color="#ffffff")
			background_image.add_text("E-mail:", cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=0, y_loc=50, x_width=100, y_height=20, color="#ffffff")
			background_image.add_text("Key:", cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=18, y_loc=82, x_width=100, y_height=20, color="#ffffff")

			background_image.paste_image(cv2.imread(resource_path("run_data\\check-mark.png"), cv2.IMREAD_UNCHANGED), x_loc=width - 38, y_loc=8, bgr=True)
			background_image.paste_image(cv2.imread(resource_path("run_data\\question-mark.png"), cv2.IMREAD_UNCHANGED), x_loc=5, y_loc=5, bgr=True)

			background_image.generate_tkinter_img()

			select_window = tkinter.Toplevel(root)
			select_window.title("Gmail sign in!")
			select_window.geometry(f"{width}x{height}+{(root.winfo_screenwidth() // 2) - (width // 2)}+{(root.winfo_screenheight() // 2) - (height // 2)}")
			select_window.resizable(False, False)
			select_window.grab_set()
			select_window.focus()

			background_lbl = tkinter.Label(select_window, highlightthickness=0, borderwidth=0, image=background_image.image_tkinter)
			background_lbl.bind("<ButtonRelease-1>", lambda event: gmail_window_back_click(event, width, select_window))
			background_lbl.place(x=0, y=0, width=width, height=height)

			email_var = tkinter.StringVar(master=select_window, value="")
			email_entry = tkinter.Entry(select_window, borderwidth=0,
			                            highlightthickness=2, highlightcolor="#ffffff", highlightbackground="#ffffff",
			                            background="#4B5555", insertbackground="#ffffff",
			                            font=("Calibri", 12), foreground="#ffffff",
			                            justify=tkinter.CENTER,
			                            textvariable=email_var)
			email_entry.place(x=95, width=350, y=50, height=25)

			key_var = tkinter.StringVar(master=select_window, value="")
			key_entry = tkinter.Entry(select_window, borderwidth=0,
			                          highlightthickness=2, highlightcolor="#ffffff", highlightbackground="#ffffff",
			                          background="#4B5555", insertbackground="#ffffff",
			                          show="*", font=("Calibri", 12), foreground="#ffffff",
			                          justify=tkinter.CENTER,
			                          textvariable=key_var)
			key_entry.place(x=95, width=350, y=82, height=25)

			select_window.iconbitmap(resource_path("data\\fish_icon.ico"))
			select_window.wait_window()

			if_tick_click = tick_click
			del tick_click

			if if_tick_click:
				if verify_mail_credentials(email_var.get().strip(" "), key_var.get()):
					status_mails_toggle = not status_mails_toggle
					keyboard.add_hotkey(hotkey, start, suppress=True, trigger_on_release=True)
					return not status_mails_toggle
				else:
					showerror(title="Error!", message="Couldn't sign in to Gmail!", parent=root)
					keyboard.add_hotkey(hotkey, start, suppress=True, trigger_on_release=True)
					return None
			else:
				return None
		else:
			status_mails_toggle = not status_mails_toggle
			return not status_mails_toggle

def gmail_window_back_click(event, width, window):
	global tick_click
	if event.x >= (width - 50) and event.y <= 50:
		tick_click = True
		window.destroy()
	elif event.x <= 35 and event.y <= 35:
		showinfo(title="Instructions!", message="""1. go to My Account in Gmail\n2. click on Security\n3. scroll down to the Signing into Google\n4. click on App Password (2-step auth should be enabled)\n5. under Select App choose other\n6. enter familiar name (e.g. Autofish-Fishing-Planet)\n7. click Generate\n8. write down key from yellow bar\n9. use that key to sign in in future""", parent=window)

def verify_mail_credentials(e_mail, key):
	global email
	email = Gmail(e_mail=e_mail, key=key)
	if email.verify_credentials():
		return True
	else:
		email = None
		return False

class BackgroundImage:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.image = np.zeros((self.height, self.width, 3), dtype="uint8")
		self.image_tkinter = None
		self.saved_backgrounds = []

	def generate_gradient(self, starting_color, ending_color, do_vertical=False):
		starting_color = hex_to_rgb(starting_color)
		ending_color = hex_to_rgb(ending_color)

		gradient_range = self.height if do_vertical else self.width

		for curr_index in range(gradient_range):
			row_color = np.zeros(3, dtype="uint8")
			for i in range(3):
				row_color[i] = (int(round((starting_color[i] * (((gradient_range - 1) - curr_index) / (gradient_range - 1))) + (ending_color[i] * (curr_index / (gradient_range - 1))), 0)))

			if do_vertical:
				self.image[curr_index, :] = row_color
			else:
				self.image[:, curr_index] = row_color

	def paste_image(self, img_to_paste, x_loc, y_loc, bgr=False):
		if bgr:
			img_to_paste = cv2.cvtColor(img_to_paste, cv2.COLOR_BGRA2RGBA)
		x1, y1 = x_loc, y_loc
		x2, y2 = x1 + img_to_paste.shape[1], y1 + img_to_paste.shape[0]

		try:
			alpha_s = img_to_paste[:, :, 3] / 255.0
			alpha_l = 1.0 - alpha_s

			for c in range(0, 3):
				self.image[y1:y2, x1:x2, c] = (alpha_s * img_to_paste[:, :, c] + alpha_l * self.image[y1:y2, x1:x2, c])
		except IndexError:
			self.image[y1:y2, x1:x2, :] = img_to_paste

	def add_text(self, text, text_font, text_thickness, x_loc, y_loc, x_width, y_height, color):
		text_scale = cv2.getFontScaleFromHeight(text_font, int(round(y_height * 0.75, 0)), thickness=text_thickness)
		text_size = cv2.getTextSize(text, text_font, text_scale, text_thickness)
		while text_size[0][0] > x_width * 0.85:
			text_scale -= 0.01
			text_size = cv2.getTextSize(text, text_font, text_scale, text_thickness)
		text_origin = (int(round((x_width - text_size[0][0]) / 2, 0)) + x_loc, int(round((y_height + text_size[0][1]) / 2, 0)) + y_loc)
		self.image = cv2.putText(self.image, text, text_origin, text_font, text_scale, hex_to_rgb(color), thickness=text_thickness, lineType=cv2.LINE_AA)

	def draw_circle(self, center, radius, color, thickness=1, filled=True):
		if filled:
			thickness = - 1
		self.image = cv2.circle(self.image, center, radius, hex_to_rgb(color), thickness=thickness, lineType=cv2.LINE_AA)

	def draw_line(self, point_1, point_2, color, thickness=1):
		self.image = cv2.line(self.image, point_1, point_2, hex_to_rgb(color), thickness=thickness, lineType=cv2.LINE_AA)

	def save_background(self, x, y, width, height):
		self.saved_backgrounds.append(np.copy(self.image[y:y + height, x:x + width]))

	def clean_background(self, x, y, ind):
		self.image[y:y + self.saved_backgrounds[ind].shape[0], x:x + self.saved_backgrounds[ind].shape[1]] = self.saved_backgrounds[ind]

	def generate_tkinter_img(self):
		self.image_tkinter = ImageTk.PhotoImage(ImagePIL.fromarray(self.image))

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

def main():
	global started
	global root
	global background_image, background_label
	global retrieve, cast_len, num_of_rods
	global night_toggle, auto_time_warp_toggle, status_mails_toggle
	global night_toggle_1, night_toggle_2
	global auto_time_warp_toggle_1, auto_time_warp_toggle_2
	global status_mails_toggle_1, status_mails_toggle_2
	global retrieve_types
	global hotkey
	global email

	email = None
	started = False
	retrieve_types = ["Twitching",
	                  "Stop&Go",
	                  "Lift&Drop",
	                  "Straight",
	                  "Straight & Slow",
	                  "Popping",
	                  "Walking",
	                  "Float",
	                  "Bottom"]
	retrieve = retrieve_types[0]
	cast_len = 100
	num_of_rods = 1
	night_toggle = False
	auto_time_warp_toggle = False
	status_mails_toggle = False

	width = 600
	height = 280

	root = tkinter.Tk()
	root.geometry(f"{width}x{height}+{(root.winfo_screenwidth() // 2) - (width // 2)}+{(root.winfo_screenheight() // 2) - (height // 2)}")
	root.resizable(False, False)
	root.title("Autofish-Fishing-Planet")

	background_image = BackgroundImage(width, height)
	background_image.generate_gradient(starting_color="#008DBF", ending_color="#087E31", do_vertical=True)
	background_image.paste_image(cv2.imread(resource_path("run_data/fish_logo.png"), cv2.IMREAD_UNCHANGED), x_loc=15, y_loc=15)
	background_image.paste_image(cv2.imread(resource_path("run_data/pencil.png"), cv2.IMREAD_UNCHANGED), x_loc=15, y_loc=126)
	background_image.paste_image(cv2.imread(resource_path("run_data/pencil.png"), cv2.IMREAD_UNCHANGED), x_loc=15, y_loc=166)
	background_image.paste_image(cv2.imread(resource_path("run_data/pencil.png"), cv2.IMREAD_UNCHANGED), x_loc=15, y_loc=206)
	background_image.add_text("Autofish-Fishing-Planet", cv2.FONT_HERSHEY_SCRIPT_COMPLEX, text_thickness=1, x_loc=90, y_loc=0, x_width=width - 90, y_height=100, color="#ffffff")
	background_image.add_text("START/STOP: Alt+X", cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=0, y_loc=height - 25, x_width=width, y_height=15, color="#ffffff")
	background_image.add_text("Retrieve:", cv2.FONT_HERSHEY_SCRIPT_COMPLEX, text_thickness=1, x_loc=15, y_loc=120, x_width=175, y_height=25, color="#ffffff")
	background_image.add_text("Night:", cv2.FONT_HERSHEY_SCRIPT_COMPLEX, text_thickness=1, x_loc=347, y_loc=120, x_width=250, y_height=25, color="#ffffff")
	background_image.add_text("Cast length:", cv2.FONT_HERSHEY_SCRIPT_COMPLEX, text_thickness=1, x_loc=34, y_loc=160, x_width=175, y_height=25, color="#ffffff")
	background_image.add_text("Auto time warp:", cv2.FONT_HERSHEY_SCRIPT_COMPLEX, text_thickness=1, x_loc=285, y_loc=160, x_width=250, y_height=25, color="#ffffff")
	background_image.add_text("Rods:", cv2.FONT_HERSHEY_SCRIPT_COMPLEX, text_thickness=1, x_loc=23, y_loc=200, x_width=125, y_height=25, color="#ffffff")
	background_image.add_text("Status e-mails:", cv2.FONT_HERSHEY_SCRIPT_COMPLEX, text_thickness=1, x_loc=265, y_loc=200, x_width=300, y_height=25, color="#ffffff")

	background_image.save_background(x=150, y=120, width=175, height=30)
	background_image.add_text(retrieve, cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=150, y_loc=127, x_width=175, y_height=16, color="#000000")
	background_image.save_background(x=200, y=160, width=75, height=30)
	background_image.add_text(f"{cast_len} %", cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=200, y_loc=167, x_width=75, y_height=16, color="#000000")
	background_image.save_background(x=220, y=200, width=35, height=30)
	background_image.add_text(str(num_of_rods), cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=220, y_loc=207, x_width=35, y_height=16, color="#000000")

	background_image.save_background(x=0, y=height - 20, width=20, height=20)
	background_image.draw_circle((10, height - 10), 3, color="#FF0000", filled=True)

	background_image.generate_tkinter_img()
	background_label = tkinter.Label(root, borderwidth=0, highlightthickness=0, image=background_image.image_tkinter)
	background_label.place(x=0, y=0, width=width, height=height)

	night_toggle_1 = tkinter.Label(root, borderwidth=0,
	                               highlightthickness=3, highlightcolor="#000000", highlightbackground="#000000",
	                               background="#FF0000", activebackground="#FF0000")
	night_toggle_2 = tkinter.Label(root, highlightthickness=0, borderwidth=0,
	                               highlightcolor="#000000", highlightbackground="#000000",
	                               background="#FF0000", activebackground="#FF0000")
	night_toggle_1.bind("<ButtonRelease-1>", lambda event: toggle_btn(night_toggle_1, night_toggle_2, toggle_night()))
	night_toggle_2.bind("<ButtonRelease-1>", lambda event: toggle_btn(night_toggle_1, night_toggle_2, toggle_night()))
	night_toggle_1.place(x=525, width=25, y=123, height=25)
	night_toggle_2.place(x=550, width=25, y=128, height=15)

	auto_time_warp_toggle_1 = tkinter.Label(root, borderwidth=0,
	                                        highlightthickness=3, highlightcolor="#000000", highlightbackground="#000000",
	                                        background="#FF0000", activebackground="#FF0000")
	auto_time_warp_toggle_2 = tkinter.Label(root, highlightthickness=0, borderwidth=0,
	                                        highlightcolor="#000000", highlightbackground="#000000",
	                                        background="#FF0000", activebackground="#FF0000")
	auto_time_warp_toggle_1.bind("<ButtonRelease-1>", lambda event: toggle_btn(auto_time_warp_toggle_1, auto_time_warp_toggle_2, toggle_auto_time_warp()))
	auto_time_warp_toggle_2.bind("<ButtonRelease-1>", lambda event: toggle_btn(auto_time_warp_toggle_1, auto_time_warp_toggle_2, toggle_auto_time_warp()))
	auto_time_warp_toggle_1.place(x=525, width=25, y=163, height=25)
	auto_time_warp_toggle_2.place(x=550, width=25, y=168, height=15)

	status_mails_toggle_1 = tkinter.Label(root, borderwidth=0,
	                                      highlightthickness=3, highlightcolor="#000000", highlightbackground="#000000",
	                                      background="#FF0000", activebackground="#FF0000")
	status_mails_toggle_2 = tkinter.Label(root, highlightthickness=0, borderwidth=0,
	                                      highlightcolor="#000000", highlightbackground="#000000",
	                                      background="#FF0000", activebackground="#FF0000")
	status_mails_toggle_1.bind("<ButtonRelease-1>", lambda event: toggle_btn(status_mails_toggle_1, status_mails_toggle_2, toggle_status_mails()))
	status_mails_toggle_2.bind("<ButtonRelease-1>", lambda event: toggle_btn(status_mails_toggle_1, status_mails_toggle_2, toggle_status_mails()))
	status_mails_toggle_1.place(x=525, width=25, y=203, height=25)
	status_mails_toggle_2.place(x=550, width=25, y=208, height=15)

	hotkey = "Alt+X"
	keyboard.add_hotkey(hotkey, start, suppress=True, trigger_on_release=True)

	background_label.bind("<ButtonRelease-1>", background_click)

	root.iconbitmap(resource_path("data\\fish_icon.ico"))  # putting at end to prevent flash while starting (adding icon draws window immediately, before all other elements are drawn)
	root.mainloop()

	# shut down everything
	keyboard.unhook_all_hotkeys()
	try:
		process_action.kill()
		process_action.join()
		process_action.close()
		mouse.release(button="left")
		mouse.release(button="right")
	except (NameError, ValueError):
		pass


if __name__ == "__main__":
	freeze_support()

	main()
