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

		image = PhotoImage(file="bd_bg.gif")
		# get the width and height of the image
		w = image.width()
		h = image.height()
		# position coordinates of root 'upper left corner'
		x = 200
		y = 50
		# size the root to fit the image
		master.geometry("%dx%d+%d+%d" % (w, h, x, y))
		# tk.Frame has no image argument
		# so use a label as a panel/frame
		panel = Label(master, image=image)
		panel.pack(side='top', fill='both', expand='yes')
		# put a button widget on the panel
		button = Button(panel, text='button widget')
		button.pack(side='top', pady=5)
		# save the panel's image from 'garbage collection'
		panel.image = image
		# start the event loop

		# filename = PhotoImage("bd_bg.gif")
		# self.bg = Canvas(master, bg="blue")
		# self.bg.pack(side='top', fill='both', expand='yes')
		# self.bg.create_image(0, 0, image=filename, anchor='nw')
		mainloop()

root = Tk()
ICS_gui = GUI(root)
