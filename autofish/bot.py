import os
import time
import numpy as np

import cv2
import keyboard
import mouse
import psutil
from PIL import ImageGrab
from .load_data import load_data


# Fishing bot functions

def motions(tip):
	""" Collection of moves for fishing """
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
			mouse.press(button="left")
			mouse.press(button="right")
			time.sleep(0.5)
			mouse.release(button="left")
			mouse.release(button="right")
			time.sleep(1.4)
		case "Walking":
			mouse.press(button="left")
			mouse.press(button="right")
			time.sleep(0.25)
			mouse.release(button="left")
			mouse.release(button="right")
			time.sleep(0.85)
		case "Float":
			pass
		case "Bottom":
			pass

def checks(tip):
	""" Collection of screen vision checks while fishing """

	global bot_data

	match tip:
		case "float-state":
			pass
		case "fullkeepnet":
			screen_load = ImageGrab.grab().load()
			for i in range(162, 200):
				if ((bot_data["values"]["fullkeepnet_orange"]["low"][0] <= screen_load[88, i][0] <= bot_data["values"]["fullkeepnet_orange"]["high"][0]) and
					(bot_data["values"]["fullkeepnet_orange"]["low"][1] <= screen_load[88, i][1] <= bot_data["values"]["fullkeepnet_orange"]["high"][1]) and
					(bot_data["values"]["fullkeepnet_orange"]["low"][2] <= screen_load[88, i][2] <= bot_data["values"]["fullkeepnet_orange"]["high"][2])):
					return True
			return False
		case "hookedfish":
			screen_load = ImageGrab.grab(bbox=(1631, 794, 1632, 795)).load()
			if ((bot_data["values"]["hookedfish_blue"]["low"][0] <= screen_load[0, 0][0] <= bot_data["values"]["hookedfish_blue"]["high"][0]) and
				(bot_data["values"]["hookedfish_blue"]["low"][1] <= screen_load[0, 0][1] <= bot_data["values"]["hookedfish_blue"]["high"][1]) and
				(bot_data["values"]["hookedfish_blue"]["low"][2] <= screen_load[0, 0][2] <= bot_data["values"]["hookedfish_blue"]["high"][2])):
				return True
			else:
				return False
		case "caught_fish":
			img = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2GRAY)

			disc = cv2.minMaxLoc(cv2.matchTemplate(img, bot_data["images"]["caught_fish"]["discard"], cv2.TM_SQDIFF))
			if disc[0] <= 1000000:
				mouse.move(disc[2][0], disc[2][1], absolute=True, duration=0)
				mouse.click(button="left")
				time.sleep(2)
				return True

			keep = cv2.minMaxLoc(cv2.matchTemplate(img, bot_data["images"]["caught_fish"]["keep"], cv2.TM_SQDIFF))
			if keep[0] <= 1000000:
				mouse.move(keep[2][0], keep[2][1], absolute=True, duration=0)
				mouse.click(button="left")
				time.sleep(2)
				return True

			rel = cv2.minMaxLoc(cv2.matchTemplate(img, bot_data["images"]["caught_fish"]["release"], cv2.TM_SQDIFF))
			if rel[0] <= 1000000:
				mouse.move(rel[2][0], rel[2][1], absolute=True, duration=0)
				mouse.click(button="left")
				time.sleep(2)
				return True

			return False
		case "pop_ups":
			ret_changes = False
			changes = True
			while changes:
				changes = False
				for image in bot_data["images"]["pop_ups"]["list"]:
					inf = cv2.minMaxLoc(cv2.matchTemplate(cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2GRAY), image, cv2.TM_SQDIFF))
					if inf[0] <= 1000000:
						mouse.move(inf[2][0], inf[2][1], absolute=True, duration=0)
						mouse.click(button="left")
						changes = True
						ret_changes = True
						time.sleep(2)
						break
				if changes:
					continue
				# buy
				inf = cv2.minMaxLoc(cv2.matchTemplate(cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2GRAY), bot_data["images"]["pop_ups"]["buy"][0], cv2.TM_SQDIFF))
				if inf[0] <= 1_000_000:
					inf2 = cv2.minMaxLoc(cv2.matchTemplate(cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2GRAY), bot_data["images"]["pop_ups"]["buy"][1], cv2.TM_SQDIFF))
					shape = np.shape(bot_data["images"]["pop_ups"]["buy"][1])
					mouse.move(inf2[2][0] + shape[1] // 2, inf2[2][1] + shape[0] // 2, absolute=True, duration=0)
					mouse.click(button="left")
					changes = True
					ret_changes = True
					time.sleep(2)
			return ret_changes
		case "after_reel_in":
			while True:
				if checks("caught_fish"):
					time.sleep(2)
				elif checks("pop_ups"):
					time.sleep(2)
				else:
					break
		case "lineLen":
			cv_img = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(1423, 916, 1666, 1020))), cv2.COLOR_RGB2GRAY)
			poz_u_znam = {}
			digits_variations = len(bot_data["images"]["digits"]) // 10
			for i in range(len(bot_data["images"]["digits"])):
				result = cv2.matchTemplate(cv_img, bot_data["images"]["digits"][i], cv2.TM_SQDIFF)
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
				return broj
			else:
				return int(broj)

def warp(auto_time_warp, night):
	""" Warps fishing time """

	# TODO: warp function
	global bot_data
	keyboard.press_and_release("t")
	time.sleep(3)
	if auto_time_warp:
		while True:
			time.sleep(3)
			inf = cv2.minMaxLoc(cv2.matchTemplate(cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2GRAY), bot_data["images"]["time_warp"]["next_morning_gray"], cv2.TM_SQDIFF))
			if inf[0] <= 1000000:
				mouse.move(inf[2][0], inf[2][1], absolute=True, duration=0)
				mouse.click(button="left")
				time.sleep(5)
				break
	else:
		psutil.Process(os.getpid()).kill()

def action(retrieve, cast_len, num_of_rods, night_toggle, auto_time_warp_toggle, status_mails_toggle, email):
	""" Main bot logic (process) """

	load_data()
	fish_hooked = checks("hookedfish")
	while psutil.Process(os.getpid()).parent() is not None:
		line_length = checks("lineLen")

		# TODO: release fish with fine

		if line_length == "":  # can't detect line length on screen, wait
			time.sleep(2)
			checks("after_reel_in")
		elif line_length == 0:  # line length is zero, check for caught fish, received achievements, ..., cast again
			mouse.release(button="left")
			mouse.release(button="right")
			time.sleep(3)

			checks("after_reel_in")
			fish_hooked = False

			# TODO: check for rod damage, change rod

			if checks("fullkeepnet"):  # TODO: warp by time of day, not only full keepnet
				warp(auto_time_warp_toggle, night_toggle)
				if status_mails_toggle:
					email.send_gmail(to=email.my_e_mail, subject="Autofish - full keepnet", message="The Autofish bot has filled a keepnet/stringer!", screenshot=True)
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
			if not fish_hooked:  # if fish was not hooked in current cast, check if it is hooked now
				fish_hooked = checks("hookedfish")

			if fish_hooked:  # if fish was hooked in the current cast, reel in using twitching (it is most effective for reeling in fish)
				motions("Twitching")
			else:
				# TODO: implement float and bottom fishing
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
