import os
import sys
import time

import cv2
import keyboard
import mouse
import numpy as np
import psutil
from PIL import ImageGrab

from .vision import Vision


class Bot(Vision):
	def __init__(self, screen_res: tuple[int, int], retrieve, cast_len, num_of_rods, night_toggle, auto_time_warp_toggle, status_mails_toggle, email):
		super().__init__(screen_res)
		self.retrieve = retrieve
		self.cast_len = cast_len
		self.num_of_rods = num_of_rods
		self.night_toggle = night_toggle
		self.auto_time_warp_toggle = auto_time_warp_toggle
		self.status_mails_toggle = status_mails_toggle
		self.email = email

		self.run()

	def run(self):
		fish_hooked = self.fish_hooked()
		while psutil.Process(os.getpid()).parent() is not None:
			line_length = self.line_length()

			# TODO: release fish with fines

			if line_length == -1:  # can't detect line length on screen, wait
				time.sleep(2)
				while True:
					if self.fish_caught():
						time.sleep(2)
					elif self.close_popups():
						time.sleep(2)
					else:
						break
			elif line_length == 0:  # line length is zero
				# release mouse buttons
				mouse.release(button="left")
				mouse.release(button="right")
				time.sleep(3)

				# process fish caught (if any) and close pop-ups
				while True:
					if self.fish_caught():
						time.sleep(2)
					elif self.close_popups():
						time.sleep(2)
					else:
						break

				# reset fish_hooked (if fish was hooked in the previous cast)
				fish_hooked = False

				# TODO: check for rod damage, change rod
				# TODO: warp by time of day, not only full keepnet

				# check if keepnet is full and warp time if it is
				if self.full_keepnet():
					if self.status_mails_toggle:
						if not self.email.send(
								to=self.email.my_e_mail,
								subject="Autofish - full keepnet",
								message="The Autofish bot has filled a keepnet/stringer!",
								screenshot=True):
							print("Error sending email!", file=sys.stderr)

					self.time_warp()
				else:
					# cast the rod if keepnet is not full
					mouse.press(button="left")
					time.sleep(0.8575 + ((1.1 * self.cast_len) / 100))
					mouse.release(button="left")
					time.sleep(8 + ((4 * self.cast_len) / 100))
			elif line_length <= 5:
				# reel in straight if the line length is less than or equal to 5
				mouse.press(button="left")
				time.sleep(1)
			else:
				# line length is greater than 5

				# if fish was not hooked in current cast, check if it is hooked now
				if not fish_hooked:
					fish_hooked = self.fish_hooked()

				# if fish was hooked in the current cast, reel it in
				# (using Twitching as that is very effective retrieve for reeling in fish)
				if fish_hooked:
					self.motions("Twitching")
				else:
					# otherwise, use the retrieve method specified by the user
					# TODO: implement float and bottom fishing
					match self.retrieve:
						case "Float":
							pass
						case "Bottom":
							pass
						case _:
							self.motions(self.retrieve)

	def time_warp(self):
		""" Warps fishing time """

		# press "t" to open the time warp menu
		keyboard.press_and_release("t")
		time.sleep(3)

		# if the auto time warp toggle is on proceed with the time warp, otherwise kill the bot process
		if self.auto_time_warp_toggle:
			# check if the next morning button is visible, otherwise wait
			while True:
				time.sleep(5)
				inf = cv2.minMaxLoc(
					cv2.matchTemplate(
						cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2GRAY),
						self.cv_templates["warp"]["next_morning"],
						cv2.TM_SQDIFF
					)
				)
				if inf[0] <= 1000000:
					mouse.move(inf[2][0], inf[2][1], absolute=True, duration=0)
					mouse.click(button="left")
					time.sleep(5)
					break
		else:
			psutil.Process(os.getpid()).kill()

	@staticmethod
	def motions(retrieve_type):
		""" Collection of moves for fishing """

		match retrieve_type:
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
