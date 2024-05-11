import json
import os
import sys

import cv2


# List of possible retrieve types
RETRIEVE_TYPES = [
	"Twitching",
	"Stop&Go",
	"Lift&Drop",
	"Straight",
	"Straight & Slow",
	"Popping",
	"Walking",
	"Float",
	"Bottom"
]


def get_filenames(path: str) -> list[str]:
	""" Returns list of filenames in given path """

	filenames = [os.path.join(path, f) for f in os.listdir(path)]
	filenames = [f for f in filenames if os.path.isfile(f)]
	filenames.sort()

	return filenames

def resource_path(relative_path: str) -> str:
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except AttributeError:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

def load_values() -> dict:
	""" Loads values used by bot process """

	with open(os.path.join(resource_path("resources"), "values.json"), "r") as file:
		values = json.loads(file.read())

	return values

def load_templates(screen_res: tuple[int, int]) -> dict:
	""" Loads cv templates used by bot process """

	base_path = resource_path(f"resources/cv_templates/{screen_res[0]}x{screen_res[1]}")
	templates = dict()

	templates["digits"] = load_digits(base_path)
	templates["fish"] = load_fish(base_path)
	templates["offers"] = load_offers(base_path)
	templates["popups"] = load_popups(base_path)
	templates["warp"] = load_warp(base_path)

	return templates

def load_digits(base_path) -> list:
	""" Loads digits used by bot process """

	digits_path = os.path.join(base_path, "digits")
	digits_files = get_filenames(digits_path)

	digits = []
	for digit_file in digits_files:
		digits.append(cv2.imread(digit_file, cv2.IMREAD_GRAYSCALE))

	return digits

def load_popups(base_path) -> list:
	""" Loads popups used by bot process """

	popups_path = os.path.join(base_path, "popups")
	popups_files = get_filenames(popups_path)

	popups = []
	for popup_file in popups_files:
		popups.append(cv2.imread(popup_file, cv2.IMREAD_GRAYSCALE))

	return popups

def load_offers(base_path) -> dict:
	""" Loads offers used by bot process.
	Returns tuple of (buy, x) templates.
	Buy template is used to check if there is a purchase offer.
	X template is used to find the location of sign X to close the offer window. """

	offers_path = os.path.join(base_path, "offers")
	offers_files = get_filenames(offers_path)
	assert len(offers_files) == 2, "There should be exactly 2 templates for purchase offers, buy and x templates."

	offers = dict()
	for offer_file in offers_files:
		match os.path.splitext(os.path.basename(offer_file))[0]:
			case "buy":
				offers["buy"] = cv2.imread(offer_file, cv2.IMREAD_GRAYSCALE)
			case "x":
				offers["x"] = cv2.imread(offer_file, cv2.IMREAD_GRAYSCALE)
			case _:
				raise ValueError("Invalid file name for offer template.")

	return offers

def load_fish(base_path) -> dict:
	""" Loads templates for keeping/releasing/discarding the fish """

	fish_path = os.path.join(base_path, "fish")
	fish_files = get_filenames(fish_path)

	fish = dict()
	for fish_file in fish_files:
		fish[os.path.splitext(os.path.basename(fish_file))[0]] = cv2.imread(fish_file, cv2.IMREAD_GRAYSCALE)

	return fish

def load_warp(base_path) -> dict:
	""" Loads templates for time warp """

	warp_path = os.path.join(base_path, "warp")
	warp_files = get_filenames(warp_path)

	warp = dict()
	for warp_file in warp_files:
		warp[os.path.splitext(os.path.basename(warp_file))[0]] = cv2.imread(warp_file, cv2.IMREAD_GRAYSCALE)

	return warp
