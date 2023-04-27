from PIL import ImageGrab
import cv2
import time
import mouse
import numpy as np
import sys
import os
import json


def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except AttributeError:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

def load_data():
	""" Loads data used by bot process """

	global bot_data

	bot_data = dict()

	with open(resource_path("../run_data/values.json"), "r") as file:
		bot_data["values"] = json.loads(file.read())

	bot_data["images"] = {}

	bot_data["images"]["digits"] = []
	for i in range(10):
		for j in ("", "_dark"):
			bot_data["images"]["digits"].append(cv2.imread(resource_path(f"../run_data\\images\\cv_templates\\digits\\{i}{j}.png"), cv2.IMREAD_GRAYSCALE))

	bot_data["images"]["pop_ups"] = [
		cv2.imread(resource_path(r"../run_data/images/cv_templates/pop_ups/claim_green.png"), cv2.IMREAD_GRAYSCALE),
		cv2.imread(resource_path(r"../run_data/images/cv_templates/pop_ups/close_gray.png"), cv2.IMREAD_GRAYSCALE),
		cv2.imread(resource_path(r"../run_data/images/cv_templates/pop_ups/close_gray_2.png"), cv2.IMREAD_GRAYSCALE),
		cv2.imread(resource_path(r"../run_data/images/cv_templates/pop_ups/close_orange.png"), cv2.IMREAD_GRAYSCALE),
		cv2.imread(resource_path("../run_data/images/cv_templates/pop_ups/close_orange_2.png"), cv2.IMREAD_GRAYSCALE),
		cv2.imread(resource_path(r"../run_data/images/cv_templates/pop_ups/extend_orange.png"), cv2.IMREAD_GRAYSCALE),
		cv2.imread(resource_path(r"../run_data/images/cv_templates/pop_ups/ok_orange.png"), cv2.IMREAD_GRAYSCALE)
	]

	bot_data["images"]["caught_fish"] = {
		"discard": cv2.imread(resource_path(r"../run_data/images/cv_templates/caught_fish/discard_gray.png"), cv2.IMREAD_GRAYSCALE),
		"keep": cv2.imread(resource_path(r"../run_data/images/cv_templates/caught_fish/keep_orange.png"), cv2.IMREAD_GRAYSCALE),
		"release": cv2.imread(resource_path(r"../run_data/images/cv_templates/caught_fish/release_gray.png"), cv2.IMREAD_GRAYSCALE)
	}

	bot_data["images"]["time_warp"] = {
		"next_morning_gray": cv2.imread(resource_path(r"../run_data/images/cv_templates/time_warp/next_morning_gray.png"), cv2.IMREAD_GRAYSCALE)
	}

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
				for image in bot_data["images"]["pop_ups"]:
					inf = cv2.minMaxLoc(cv2.matchTemplate(cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2GRAY), image, cv2.TM_SQDIFF))
					if inf[0] <= 1000000:
						mouse.move(inf[2][0], inf[2][1], absolute=True, duration=0)
						mouse.click(button="left")
						changes = True
						ret_changes = True
						time.sleep(2)
						break
				changes = False
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


if __name__ == "__main__":
	load_data()
	time.sleep(7.5)

	for arg in ("float-state", "fullkeepnet", "pop_ups", "caught_fish", "lineLen", "after_reel_in", "hooked_fish"):
		print(f"{arg}: {checks(arg)}")
