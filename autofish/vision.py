import time

import cv2
import mouse
import numpy as np
from PIL import ImageGrab

from .load_data import load_values, load_templates


class Vision:
	def __init__(self, screen_res: tuple[int, int]):
		self.screen_res = screen_res
		self.values = load_values()
		self.cv_templates = load_templates(self.screen_res)

	@staticmethod
	def color_distance(color1: tuple[int, int, int], color2: tuple[int, int, int]) -> float:
		""" Returns the distance between two colors in the RGB color space."""
		return np.linalg.norm(np.array(color1) - np.array(color2))

	def line_length(self) -> int:
		""" Returns the length of the line in the game or -1 if the line length is not detected."""

		# grab the part of the screen where the line length is displayed
		top_left = self.values["line_length_pos"][f"{self.screen_res[0]}x{self.screen_res[1]}"]["top_left"]
		bottom_right = self.values["line_length_pos"][f"{self.screen_res[0]}x{self.screen_res[1]}"]["bottom_right"]
		bbox = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])
		cv_img = cv2.cvtColor(np.array(ImageGrab.grab(bbox=bbox)), cv2.COLOR_RGB2GRAY)

		# dictionary of x positions and the detected digits and their match values at that position
		# x_pos_digit_map = {x_position: [(digit, match_value), ...], ...}
		x_pos_digit_map = dict()
		digits_variations = len(self.cv_templates["digits"]) // 10
		for i in range(len(self.cv_templates["digits"])):
			result = cv2.matchTemplate(cv_img, self.cv_templates["digits"][i], cv2.TM_SQDIFF)
			positions = np.where(result <= 11_500_000)
			positions_x = positions[1]
			positions_y = positions[0]

			# dictionary of x positions and the minimum match value at that position for current digit
			x_pos_matches = dict()
			for x, y in zip(positions_x, positions_y):
				if x in x_pos_matches.keys():
					x_pos_matches[x] = min(x_pos_matches[x], result[y, x])
				else:
					x_pos_matches[x] = result[y, x]

			# add the minimum value for each x position to the x_pos_digit_map
			for x in x_pos_matches.keys():
				if x in x_pos_digit_map.keys():
					x_pos_digit_map[x].append((i // digits_variations, x_pos_matches[x]))
				else:
					x_pos_digit_map[x] = [(i // digits_variations, x_pos_matches[x])]

		# normalize the x positions (merge the x positions that are close to each other)
		coordinates = list(x_pos_digit_map.keys())
		norm_x_pos_digit_map = dict()
		while len(coordinates) != 0:
			coord = coordinates.pop()
			coord_values = x_pos_digit_map[coord]
			for i in range(-10, 11):
				if coord + i in coordinates:
					coord_values.extend(x_pos_digit_map[coord + i])
					coordinates.remove(coord + i)
			norm_x_pos_digit_map[coord] = coord_values

		x_pos_ordered = list(norm_x_pos_digit_map.keys())
		x_pos_ordered.sort()
		line_length = ""
		for i in x_pos_ordered:
			digit = min(norm_x_pos_digit_map[i], key=lambda x: x[1])[0]
			line_length += str(digit)

		# return the line length as an integer or -1 if the line length is not detected
		if line_length == "":
			return -1
		else:
			return int(line_length)

	def fish_caught(self) -> bool:
		""" Check if the fish is caught (and process the pop-ups), return True if the fish was caught, False otherwise."""
		img = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2GRAY)

		disc = cv2.minMaxLoc(cv2.matchTemplate(img, self.cv_templates["fish"]["discard"], cv2.TM_SQDIFF))
		if disc[0] <= 1000000:
			mouse.move(disc[2][0], disc[2][1], absolute=True, duration=0)
			mouse.click(button="left")
			time.sleep(2)
			return True

		keep = cv2.minMaxLoc(cv2.matchTemplate(img, self.cv_templates["fish"]["keep"], cv2.TM_SQDIFF))
		if keep[0] <= 1000000:
			mouse.move(keep[2][0], keep[2][1], absolute=True, duration=0)
			mouse.click(button="left")
			time.sleep(2)
			return True

		rel = cv2.minMaxLoc(cv2.matchTemplate(img, self.cv_templates["fish"]["release"], cv2.TM_SQDIFF))
		if rel[0] <= 1000000:
			mouse.move(rel[2][0], rel[2][1], absolute=True, duration=0)
			mouse.click(button="left")
			time.sleep(2)
			return True

		return False

	def fish_hooked(self) -> bool:
		# grab the part of the screen where the fish hooked bar is displayed
		top_left = self.values["fish_hooked_pos"][f"{self.screen_res[0]}x{self.screen_res[1]}"]["top_left"]
		bottom_right = self.values["fish_hooked_pos"][f"{self.screen_res[0]}x{self.screen_res[1]}"]["bottom_right"]
		bbox = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])
		screen_load = ImageGrab.grab(bbox=bbox).load()

		pixel = screen_load[0, 0]
		return self.color_distance(pixel, self.values["fish_hooked_blue"]) <= 10

	def full_keepnet(self) -> bool:
		""" Check if the keepnet is full, return True if the keepnet is full, False otherwise. """

		# grab the part of the screen where the keepnet is displayed
		top_left = self.values["full_keepnet_pos"][f"{self.screen_res[0]}x{self.screen_res[1]}"]["top_left"]
		bottom_right = self.values["full_keepnet_pos"][f"{self.screen_res[0]}x{self.screen_res[1]}"]["bottom_right"]
		bbox = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])
		screen_load = ImageGrab.grab(bbox=bbox).load()

		# check if any pixel in the keepnet is orange
		for i in range(0, np.shape(screen_load)[0]):
			if self.color_distance(screen_load[0, i], self.values["full_keepnet_orange"]) <= 10:
				return True
		return False

	def close_popups(self) -> bool:
		""" Close the pop-ups that might appear on the screen. Return True if any pop-up was closed, False otherwise. """

		ret_changes = False

		changes = True
		while changes:
			changes = False

			# deal with normal pop-ups (achievements, extend license, etc.)
			for image in self.cv_templates["popups"]:
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

			# deal with buy popup (must be closed by clicking on the "X" button)
			screenshot = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2GRAY)
			inf = cv2.minMaxLoc(cv2.matchTemplate(screenshot, self.cv_templates["offers"]["buy"], cv2.TM_SQDIFF))
			if inf[0] <= 1_000_000:
				inf2 = cv2.minMaxLoc(cv2.matchTemplate(screenshot, self.cv_templates["offers"]["x"], cv2.TM_SQDIFF))
				shape = np.shape(self.cv_templates["offers"]["x"])
				mouse.move(inf2[2][0] + shape[1] // 2, inf2[2][1] + shape[0] // 2, absolute=True, duration=0)
				mouse.click(button="left")
				changes = True
				ret_changes = True
				time.sleep(2)

		return ret_changes
