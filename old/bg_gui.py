from tkinter import *
from tkinter import filedialog
from PIL import Image
import colorsys
import operator
import os, sys


class GUI:

	def __init__(self, master):
		# window size
		master.title("ImageColorSort")

		# image = PhotoImage(file="bd_bg.gif")
		# panel = Label(master, image=image)
		# panel.pack(side=TOP, fill=BOTH, expand=YES)
		# panel.image = image
		# start the event loop

		filename = PhotoImage(file="bd_bg.gif")
		self.bg = Canvas(master)
		self.bg.pack(side='top', fill='both', expand='yes')
		self.bg.create_image(0, 0, image=filename, anchor='nw')
		mainloop()

root = Tk()
ICS_gui = GUI(root)
