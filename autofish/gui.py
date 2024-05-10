import tkinter as tk
from multiprocessing import Process
from tkinter.messagebox import showerror, showinfo

import cv2
import keyboard
import mouse
import numpy as np
from PIL import Image as ImagePIL
from PIL import ImageTk

from .gmail import Gmail
from .load_data import resource_path, RETRIEVE_TYPES


class App:
	def __init__(self):
		self.email = None
		self.bot_process = None
		self.started = False
		self.retrieve = RETRIEVE_TYPES[0]
		self.cast_len = 100
		self.num_of_rods = 1
		self.night_toggle = False
		self.auto_time_warp_toggle = False
		self.status_mails_toggle = False

		self.width = 600
		self.height = 280

		self.root = tk.Tk()
		self.root.geometry(
			f"{self.width}x{self.height}"
			f"+{(self.root.winfo_screenwidth() // 2) - (self.width // 2)}"
			f"+{(self.root.winfo_screenheight() // 2) - (self.height // 2)}"
		)
		self.root.resizable(False, False)
		self.root.title("Autofish-Fishing-Planet")

		# generate background image
		self.background_image = BackgroundImage(self.width, self.height)
		self.background_image.generate_gradient(starting_color="#008DBF", ending_color="#087E31", do_vertical=True)
		self.background_image.paste_image(cv2.imread(resource_path("resources/gui_elements/fish_logo.png"), cv2.IMREAD_UNCHANGED), x_loc=15, y_loc=15)
		self.background_image.paste_image(cv2.imread(resource_path("resources/gui_elements/pencil.png"), cv2.IMREAD_UNCHANGED), x_loc=15, y_loc=126)
		self.background_image.paste_image(cv2.imread(resource_path("resources/gui_elements/pencil.png"), cv2.IMREAD_UNCHANGED), x_loc=15, y_loc=166)
		self.background_image.paste_image(cv2.imread(resource_path("resources/gui_elements/pencil.png"), cv2.IMREAD_UNCHANGED), x_loc=15, y_loc=206)
		self.background_image.add_text("Autofish-Fishing-Planet", cv2.FONT_HERSHEY_SCRIPT_COMPLEX, text_thickness=1, x_loc=90, y_loc=0, x_width=self.width - 90, y_height=100, color="#ffffff")
		self.background_image.add_text("START/STOP: Alt+X", cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=0, y_loc=self.height - 25, x_width=self.width, y_height=15, color="#ffffff")
		self.background_image.add_text("Retrieve:", cv2.FONT_HERSHEY_SCRIPT_COMPLEX, text_thickness=1, x_loc=15, y_loc=120, x_width=175, y_height=25, color="#ffffff")
		self.background_image.add_text("Night:", cv2.FONT_HERSHEY_SCRIPT_COMPLEX, text_thickness=1, x_loc=347, y_loc=120, x_width=250, y_height=25, color="#ffffff")
		self.background_image.add_text("Cast length:", cv2.FONT_HERSHEY_SCRIPT_COMPLEX, text_thickness=1, x_loc=34, y_loc=160, x_width=175, y_height=25, color="#ffffff")
		self.background_image.add_text("Auto time warp:", cv2.FONT_HERSHEY_SCRIPT_COMPLEX, text_thickness=1, x_loc=285, y_loc=160, x_width=250, y_height=25, color="#ffffff")
		self.background_image.add_text("Rods:", cv2.FONT_HERSHEY_SCRIPT_COMPLEX, text_thickness=1, x_loc=23, y_loc=200, x_width=125, y_height=25, color="#ffffff")
		self.background_image.add_text("Status e-mails:", cv2.FONT_HERSHEY_SCRIPT_COMPLEX, text_thickness=1, x_loc=265, y_loc=200, x_width=300, y_height=25, color="#ffffff")

		self.background_image.save_background(x=150, y=120, width=175, height=30)
		self.background_image.add_text(self.retrieve, cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=150, y_loc=127, x_width=175, y_height=16, color="#000000")
		self.background_image.save_background(x=200, y=160, width=75, height=30)
		self.background_image.add_text(f"{self.cast_len} %", cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=200, y_loc=167, x_width=75, y_height=16, color="#000000")
		self.background_image.save_background(x=220, y=200, width=35, height=30)
		self.background_image.add_text(str(self.num_of_rods), cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=220, y_loc=207, x_width=35, y_height=16, color="#000000")

		self.background_image.save_background(x=0, y=self.height - 20, width=20, height=20)
		self.background_image.draw_circle((10, self.height - 10), 3, color="#FF0000", filled=True)

		self.background_image.generate_tkinter_img()
		self.background_label = tk.Label(self.root, borderwidth=0, highlightthickness=0, image=self.background_image.image_tkinter)
		self.background_label.place(x=0, y=0, width=self.width, height=self.height)
		self.background_label.bind("<ButtonRelease-1>", self.background_click)

		self.night_toggle_1 = tk.Label(self.root, cursor="hand2", borderwidth=0, highlightthickness=3, highlightcolor="#000000",
		                               highlightbackground="#000000", background="#FF0000", activebackground="#FF0000")
		self.night_toggle_2 = tk.Label(self.root, cursor="hand2", highlightthickness=0, borderwidth=0, highlightcolor="#000000",
		                               highlightbackground="#000000", background="#FF0000", activebackground="#FF0000")
		self.night_toggle_1.bind("<ButtonRelease-1>", lambda event: self.toggle_btn(self.night_toggle_1, self.night_toggle_2, self.toggle_night()))
		self.night_toggle_2.bind("<ButtonRelease-1>", lambda event: self.toggle_btn(self.night_toggle_1, self.night_toggle_2, self.toggle_night()))
		self.night_toggle_1.place(x=525, width=25, y=123, height=25)
		self.night_toggle_2.place(x=550, width=25, y=128, height=15)

		self.auto_time_warp_toggle_1 = tk.Label(self.root, cursor="hand2", borderwidth=0, highlightthickness=3, highlightcolor="#000000",
		                                        highlightbackground="#000000", background="#FF0000", activebackground="#FF0000")
		self.auto_time_warp_toggle_2 = tk.Label(self.root, cursor="hand2", highlightthickness=0, borderwidth=0, highlightcolor="#000000",
		                                        highlightbackground="#000000", background="#FF0000", activebackground="#FF0000")
		self.auto_time_warp_toggle_1.bind("<ButtonRelease-1>", lambda event: self.toggle_btn(self.auto_time_warp_toggle_1, self.auto_time_warp_toggle_2, self.toggle_auto_time_warp()))
		self.auto_time_warp_toggle_2.bind("<ButtonRelease-1>", lambda event: self.toggle_btn(self.auto_time_warp_toggle_1, self.auto_time_warp_toggle_2, self.toggle_auto_time_warp()))
		self.auto_time_warp_toggle_1.place(x=525, width=25, y=163, height=25)
		self.auto_time_warp_toggle_2.place(x=550, width=25, y=168, height=15)

		self.status_mails_toggle_1 = tk.Label(self.root, cursor="hand2", borderwidth=0, highlightthickness=3, highlightcolor="#000000",
		                                      highlightbackground="#000000", background="#FF0000", activebackground="#FF0000")
		self.status_mails_toggle_2 = tk.Label(self.root, cursor="hand2", highlightthickness=0, borderwidth=0, highlightcolor="#000000",
		                                      highlightbackground="#000000", background="#FF0000", activebackground="#FF0000")
		self.status_mails_toggle_1.bind("<ButtonRelease-1>", lambda event: self.toggle_btn(self.status_mails_toggle_1, self.status_mails_toggle_2, self.toggle_status_mails()))
		self.status_mails_toggle_2.bind("<ButtonRelease-1>", lambda event: self.toggle_btn(self.status_mails_toggle_1, self.status_mails_toggle_2, self.toggle_status_mails()))
		self.status_mails_toggle_1.place(x=525, width=25, y=203, height=25)
		self.status_mails_toggle_2.place(x=550, width=25, y=208, height=15)

		self.hotkey = "Alt+X"
		self.toggle_hotkey(True)

		# adding an icon putting at end to prevent flash while starting
		# (adding icon draws window immediately, before all other elements are drawn)
		self.root.iconbitmap(resource_path("resources/fish_icon.ico"))

		self.root.mainloop()

		# cleanup
		self.toggle_hotkey(False)
		try:
			self.bot_process.kill()
			self.bot_process.join()
			self.bot_process.close()
			mouse.release(button="left")
			mouse.release(button="right")
		except (AttributeError, NameError, ValueError):
			pass

	def background_click(self, event):
		if not self.started:
			if event.x <= 50:
				if 115 <= event.y <= 150:
					self.retrieve_select()
				elif 155 <= event.y <= 190:
					self.cast_len_select()
				elif 195 <= event.y <= 230:
					self.rods_select()
			if event.x >= 505:
				if 115 <= event.y <= 150:
					self.toggle_btn(self.night_toggle_1, self.night_toggle_2, self.toggle_night())
				elif 155 <= event.y <= 190:
					self.toggle_btn(self.auto_time_warp_toggle_1, self.auto_time_warp_toggle_2, self.toggle_auto_time_warp())
				elif 195 <= event.y <= 230:
					self.toggle_btn(self.status_mails_toggle_1, self.status_mails_toggle_2, self.toggle_status_mails())

	def toggle_btn(self, widget1, widget2, variable):
		if not self.started:
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

	def toggle_night(self):
		if not self.started:
			self.night_toggle = not self.night_toggle
		return not self.night_toggle

	def toggle_auto_time_warp(self):
		if not self.started:
			self.auto_time_warp_toggle = not self.auto_time_warp_toggle
		return not self.auto_time_warp_toggle

	def toggle_status_mails(self):
		if not self.started:
			if not self.status_mails_toggle:
				self.toggle_hotkey(False)

				width = 450
				height = 115

				background_image = BackgroundImage(width=width, height=height)
				wood_texture = cv2.imread(resource_path("resources/gui_elements/wood_texture.png"), cv2.IMREAD_UNCHANGED)

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

				background_image.add_text("Gmail", cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=0, y_loc=12,
				                          x_width=width, y_height=25, color="#ffffff")
				background_image.add_text("E-mail:", cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=0, y_loc=50,
				                          x_width=100, y_height=20, color="#ffffff")
				background_image.add_text("Key:", cv2.FONT_HERSHEY_DUPLEX, text_thickness=1, x_loc=18, y_loc=82,
				                          x_width=100, y_height=20, color="#ffffff")
				background_image.paste_image(cv2.imread(resource_path("resources/gui_elements/check_mark.png"), cv2.IMREAD_UNCHANGED),
				                             x_loc=width - 38, y_loc=8, bgr=True)
				background_image.paste_image(cv2.imread(resource_path("resources/gui_elements/question_mark.png"), cv2.IMREAD_UNCHANGED),
				                             x_loc=5, y_loc=5, bgr=True)
				background_image.generate_tkinter_img()

				select_window = tk.Toplevel(self.root)
				select_window.title("Gmail sign in!")
				select_window.geometry(
					f"{width}x{height}"
					f"+{(self.root.winfo_screenwidth() // 2) - (width // 2)}"
					f"+{(self.root.winfo_screenheight() // 2) - (height // 2)}")
				select_window.resizable(False, False)
				select_window.grab_set()
				select_window.focus()

				background_image.tick_click = False

				def gmail_window_back_click(event):
					if event.x >= (width - 50) and event.y <= 50:
						background_image.tick_click = True
						select_window.destroy()
					elif event.x <= 35 and event.y <= 35:
						showinfo(title="Instructions!",
						         message=
						         """1. Go to "My Account" in Gmail\n2. Enter "App passwords" in the search bar\n3. Create new app password\n4. Write down the key\n5. Sign in with your e-mail and key into Autofish""",
						         parent=select_window)

				background_lbl = tk.Label(select_window, highlightthickness=0, borderwidth=0, image=background_image.image_tkinter)
				background_lbl.bind("<ButtonRelease-1>", gmail_window_back_click)
				background_lbl.place(x=0, y=0, width=width, height=height)

				email_var = tk.StringVar(master=select_window, value="")
				email_entry = tk.Entry(select_window, borderwidth=0,
				                       highlightthickness=2, highlightcolor="#ffffff",
				                       highlightbackground="#ffffff",
				                       background="#4B5555", insertbackground="#ffffff",
				                       font=("Calibri", 12), foreground="#ffffff",
				                       justify=tk.CENTER,
				                       textvariable=email_var)
				email_entry.place(x=95, width=350, y=50, height=25)

				key_var = tk.StringVar(master=select_window, value="")
				key_entry = tk.Entry(select_window, borderwidth=0,
				                     highlightthickness=2, highlightcolor="#ffffff", highlightbackground="#ffffff",
				                     background="#4B5555", insertbackground="#ffffff",
				                     show="*", font=("Calibri", 12), foreground="#ffffff",
				                     justify=tk.CENTER, textvariable=key_var)
				key_entry.place(x=95, width=350, y=82, height=25)

				select_window.iconbitmap(resource_path("resources/fish_icon.ico"))
				select_window.wait_window()

				if background_image.tick_click:
					self.email = Gmail(email_var.get().strip(" "), key_var.get())
					if self.email.verify_credentials():
						self.status_mails_toggle = not self.status_mails_toggle
						self.toggle_hotkey(True)
						return not self.status_mails_toggle
					else:
						showerror(title="Error!", message="Couldn't sign in to Gmail!", parent=self.root)
						self.toggle_hotkey(True)
						return None
				else:
					return None
			else:
				self.status_mails_toggle = not self.status_mails_toggle
				return not self.status_mails_toggle

	def toggle_hotkey(self, turn_on=True):
		if turn_on:
			keyboard.add_hotkey(self.hotkey, self.toggle_bot, suppress=True, trigger_on_release=True)
		else:
			keyboard.remove_all_hotkeys()

	def retrieve_select(self):
		if not self.started:
			self.toggle_hotkey(False)

			option_height = 30
			width = 250
			height = option_height * len(RETRIEVE_TYPES)

			background_image = BackgroundImage(width=width, height=height)
			wood_texture = cv2.imread(resource_path("resources/gui_elements/wood_texture.png"), cv2.IMREAD_UNCHANGED)
			pasted_height = 0
			while pasted_height < height:
				if height - (pasted_height + wood_texture.shape[0]) < 0:
					wood_texture = wood_texture[:height - pasted_height, :]
				background_image.paste_image(wood_texture, x_loc=0, y_loc=pasted_height, bgr=True)
				pasted_height += wood_texture.shape[0]
			del wood_texture
			for i in range(len(RETRIEVE_TYPES)):
				background_image.add_text(RETRIEVE_TYPES[i], cv2.FONT_HERSHEY_DUPLEX, text_thickness=1,
				                          x_loc=0, y_loc=(i * option_height) + (option_height // 3) // 2,
				                          x_width=width, y_height=(2 * option_height) // 3, color="#ffffff")
			background_image.generate_tkinter_img()

			select_window = tk.Toplevel(self.root)
			select_window.title("Select retrieve!")
			select_window.geometry(
				f"{width}x{height}"
				f"+{(self.root.winfo_screenwidth() // 2) - (width // 2)}"
				f"+{(self.root.winfo_screenheight() // 2) - (height // 2)}"
			)
			select_window.resizable(False, False)
			select_window.grab_set()
			select_window.focus()

			def retrieve_select_click(event):
				self.retrieve = RETRIEVE_TYPES[event.y // option_height]
				select_window.destroy()
				self.background_image.clean_background(x=150, y=120, ind=0)
				self.background_image.add_text(self.retrieve, cv2.FONT_HERSHEY_DUPLEX, text_thickness=1,
				                               x_loc=150, y_loc=127, x_width=175, y_height=16, color="#000000")
				self.background_image.generate_tkinter_img()
				self.background_label.configure(image=self.background_image.image_tkinter)

			background_lbl = tk.Label(select_window, highlightthickness=0, borderwidth=0, image=background_image.image_tkinter)
			background_lbl.place(x=0, y=0, width=width, height=height)
			background_lbl.bind("<ButtonRelease-1>", retrieve_select_click)

			select_window.iconbitmap(resource_path("resources/fish_icon.ico"))
			select_window.wait_window()
			self.toggle_hotkey(True)

	def cast_len_select(self):
		if not self.started:
			self.toggle_hotkey(False)

			width = 450
			height = 80

			background_gradient_image = BackgroundImage(width=350, height=40)
			background_gradient_image.generate_gradient(starting_color="#38A0B2", ending_color="#B9B63D")

			background_image = BackgroundImage(width=width, height=height)
			wood_texture = cv2.imread(resource_path("resources/gui_elements/wood_texture.png"), cv2.IMREAD_UNCHANGED)

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

			background_image.add_text(" 0 % ", cv2.FONT_HERSHEY_DUPLEX, text_thickness=1,
			                          x_loc=0, y_loc=20, x_width=50, y_height=40, color="#ffffff")
			background_image.add_text("100 %", cv2.FONT_HERSHEY_DUPLEX, text_thickness=1,
			                          x_loc=400, y_loc=20, x_width=50, y_height=40, color="#ffffff")

			line_loc = 50 + int(round(350 * (self.cast_len / 100), 0))

			background_image.draw_line((line_loc, 19), (line_loc, 60), "#E2062C", 2)

			background_image.generate_tkinter_img()

			select_window = tk.Toplevel(self.root)
			select_window.title("Select cast length!")
			select_window.geometry(
				f"{width}x{height}"
				f"+{(self.root.winfo_screenwidth() // 2) - (width // 2)}"
				f"+{(self.root.winfo_screenheight() // 2) - (height // 2)}")
			select_window.resizable(False, False)
			select_window.grab_set()
			select_window.focus()

			def cast_len_select_click(event, x_start, box_size):
				if event.x < x_start:
					self.cast_len = 15
				elif event.x >= x_start + box_size:
					self.cast_len = 100
				else:
					self.cast_len = int(round(((event.x - x_start) / box_size) * 100, 0))
					if self.cast_len < 15:
						self.cast_len = 15
				select_window.destroy()
				self.background_image.clean_background(x=200, y=160, ind=1)
				self.background_image.add_text(f"{self.cast_len} %", cv2.FONT_HERSHEY_DUPLEX, text_thickness=1,
				                               x_loc=200, y_loc=167, x_width=75, y_height=16, color="#000000")
				self.background_image.generate_tkinter_img()
				self.background_label.configure(image=self.background_image.image_tkinter)

			background_lbl = tk.Label(select_window, highlightthickness=0, borderwidth=0, image=background_image.image_tkinter)
			background_lbl.place(x=0, y=0, width=width, height=height)
			background_lbl.bind("<ButtonRelease-1>", lambda event: cast_len_select_click(event, 50, 350))

			select_window.iconbitmap(resource_path("resources/fish_icon.ico"))
			select_window.wait_window()
			self.toggle_hotkey(True)

	def rods_select(self):
		if not self.started:
			self.toggle_hotkey(False)

			width = 250
			height = 30
			rods = 7

			background_image = BackgroundImage(width=width, height=height)
			wood_texture = cv2.imread(resource_path("resources/gui_elements/wood_texture.png"), cv2.IMREAD_UNCHANGED)
			pasted_height = 0
			while pasted_height < height:
				if height - (pasted_height + wood_texture.shape[0]) < 0:
					wood_texture = wood_texture[:height - pasted_height, :]
				background_image.paste_image(wood_texture, x_loc=0, y_loc=pasted_height, bgr=True)
				pasted_height += wood_texture.shape[0]
			del wood_texture
			for i in range(1, rods + 1):
				background_image.add_text(str(i), cv2.FONT_HERSHEY_DUPLEX, text_thickness=1,
				                          x_loc=(((width - (height * rods)) // 2) + ((i - 1) * height)),
				                          y_loc=((height // 3) // 2), x_width=height, y_height=(2 * height) // 3,
				                          color="#ffffff")
			background_image.generate_tkinter_img()

			select_window = tk.Toplevel(self.root)
			select_window.title("Select rods!")
			select_window.geometry(
				f"{width}x{height}"
				f"+{(self.root.winfo_screenwidth() // 2) - (width // 2)}"
				f"+{(self.root.winfo_screenheight() // 2) - (height // 2)}")
			select_window.resizable(False, False)
			select_window.grab_set()
			select_window.focus()

			def rods_select_click(event, x_start, box_size):
				if event.x < x_start:
					self.num_of_rods = 1
				elif event.x >= ((rods * box_size) + x_start):
					self.num_of_rods = rods
				else:
					self.num_of_rods = ((event.x - x_start) // box_size) + 1
				select_window.destroy()
				self.background_image.clean_background(x=220, y=200, ind=2)
				self.background_image.add_text(str(self.num_of_rods), cv2.FONT_HERSHEY_DUPLEX, text_thickness=1,
				                               x_loc=220, y_loc=207, x_width=35, y_height=16, color="#000000")
				self.background_image.generate_tkinter_img()
				self.background_label.configure(image=self.background_image.image_tkinter)

			background_lbl = tk.Label(select_window, highlightthickness=0, borderwidth=0, image=background_image.image_tkinter)
			background_lbl.place(x=0, y=0, width=width, height=height)
			background_lbl.bind("<ButtonRelease-1>", lambda event: rods_select_click(event, ((width - (height * rods)) // 2), height))

			select_window.iconbitmap(resource_path("resources/fish_icon.ico"))
			select_window.wait_window()
			self.toggle_hotkey(True)

	def toggle_bot(self):
		""" Starts/stops bot process, edits GUI accordingly"""

		if not self.started:
			self.started = True
			self.background_image.clean_background(x=0, y=self.root.winfo_height() - 20, ind=3)
			self.background_image.draw_circle((10, self.root.winfo_height() - 10), 3, color="#2DFA09", filled=True)
			self.background_image.generate_tkinter_img()
			self.background_label.configure(image=self.background_image.image_tkinter)
			self.bot_process = Process(target=action, args=(self.retrieve, self.cast_len, self.num_of_rods, self.night_toggle, self.auto_time_warp_toggle, self.status_mails_toggle, self.email))
			self.bot_process.start()
		else:
			try:
				self.bot_process.kill()
				self.bot_process.join()
				self.bot_process.close()
				mouse.release(button="left")
				mouse.release(button="right")
			except (AttributeError, NameError, ValueError):
				pass

			self.background_image.clean_background(x=0, y=self.root.winfo_height() - 20, ind=3)
			self.background_image.draw_circle((10, self.root.winfo_height() - 10), 3, color="#FF0000", filled=True)
			self.background_image.generate_tkinter_img()
			self.background_label.configure(image=self.background_image.image_tkinter)

			self.started = False


class BackgroundImage:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.image = np.zeros((self.height, self.width, 3), dtype="uint8")
		self.image_tkinter = None
		self.saved_backgrounds = []

	def generate_gradient(self, starting_color, ending_color, do_vertical=False):
		starting_color = self.hex_to_rgb(starting_color)
		ending_color = self.hex_to_rgb(ending_color)

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
		self.image = cv2.putText(self.image, text, text_origin, text_font, text_scale, self.hex_to_rgb(color), thickness=text_thickness, lineType=cv2.LINE_AA)

	def draw_circle(self, center, radius, color, thickness=1, filled=True):
		if filled:
			thickness = - 1
		self.image = cv2.circle(self.image, center, radius, self.hex_to_rgb(color), thickness=thickness, lineType=cv2.LINE_AA)

	def draw_line(self, point_1, point_2, color, thickness=1):
		self.image = cv2.line(self.image, point_1, point_2, self.hex_to_rgb(color), thickness=thickness, lineType=cv2.LINE_AA)

	def save_background(self, x, y, width, height):
		self.saved_backgrounds.append(np.copy(self.image[y:y + height, x:x + width]))

	def clean_background(self, x, y, ind):
		self.image[y:y + self.saved_backgrounds[ind].shape[0], x:x + self.saved_backgrounds[ind].shape[1]] = self.saved_backgrounds[ind]

	def generate_tkinter_img(self):
		self.image_tkinter = ImageTk.PhotoImage(ImagePIL.fromarray(self.image))

	@staticmethod
	def hex_to_rgb(hex_value):
		""" Convert color from HEX to RGB value """
		hex_value = hex_value.lstrip("#")
		return tuple(int(hex_value[i:i + 2], 16) for i in (0, 2, 4))
