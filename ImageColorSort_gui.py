from tkinter import *
from tkinter import filedialog
from PIL import Image
import colorsys
import operator
import os, sys

# used by color_comp to return numeric %
def percentage(decimal):
	return int(round(decimal*100))

### HELPER FUNCTION FOR ALL MODES ###
def color_in_img(img, color=None):
	# initialize image data
	width, height = img.size
	max_dim = 1000
	# resize if image is larger than max dimensions
	if max(width, height) > max_dim:
		# resize ratio
		rr = min(max_dim/width, max_dim/height)
		img = img.resize((int(rr*width), int(rr*height)))
	color_dict = {}
	pixel_data = list(img.getdata())
	num_pixels = len(pixel_data)
	for pixel in pixel_data:
		# most time occupied when converting to HSV
		hsv = colorsys.rgb_to_hsv(*pixel)
		# add weight values to HSV keys in dictionary
		try:
			color_dict[hsv] += 1
		except KeyError:
			color_dict[hsv] = 1

	# counters, corresponding to color names
	counter = [0, 0, 0, 0, 0, 0, 0, 0]

	for pixel in color_dict:
		# if saturation is 0 OR value is 0, skip pixel
		if pixel[1] == 0 or pixel[2] == 0:
			continue
		hue = pixel[0]
		weight = color_dict[pixel]
		if hue >= 346/360 or (hue >= 0 and hue <= 20/360):
			counter[0] += 1*weight
		if hue >= 11/360 and hue <= 50/360:
			counter[1] += 1*weight
		if hue >= 41/360 and hue <= 80/360:
			counter[2] += 1*weight
		if hue >= 61/360 and hue <= 169/360:
			counter[3] += 1*weight
		if hue >= 141/360 and hue <= 220/360:
			counter[4] += 1*weight
		if hue >= 201/360 and hue <= 280/360:
			counter[5] += 1*weight
		if hue >= 241/360 and hue <= 330/360:
			counter[6] += 1*weight
		if hue >= 321/360 and hue <= 355/360:
			counter[7] += 1*weight

	# if no color specified
	if color == None:
		# value of highest counter
		max_count = max(counter)
		# if image has no color
		if max_count == 0:
			return "Error: image has no color"
			# raise ValueError\
			# ("<" + img + "> has no color")
		# index of counter
		max_index = counter.index(max_count)
		# color corresponding to highest counter
		color_most = colorname[max_index]
		return color_most, max_count/num_pixels

	# if a color is specified
	color_index = colorname.index(color)
	color_count = counter[color_index]
	return color_count/num_pixels

# list of all color names
colorname = ["red", "orange", "yellow", "green", "cyan", "blue", \
				"purple", "pink"]


class GUI:

	def __init__(self, master, color):
		master.geometry("500x700")
		self.topFrame = Frame(master)
		self.topFrame.pack()
		self.fileFrame = Frame(master, pady=5)
		self.fileFrame.pack()
		self.midFrame = Frame(master, pady=5)
		self.midFrame.pack()
		self.bottomFrame = Frame(master)
		self.bottomFrame.pack()
		self.header = Label(self.topFrame, text="ImageColorSort", \
			font="Helvetica 18 bold", pady=10).pack()
		self.button_comp = Radiobutton(self.topFrame, text="Find the most " \
			+ "used color in an image", value=1, variable="mode", \
			command=lambda: self.modeswitch(0), font="Helvetica 14")
		self.button_comp.pack()
		self.button_choose = Radiobutton(self.topFrame, text="Find the " \
			+ "% composition of a color in an image", value=2, \
			variable="mode", command=lambda: self.modeswitch(1), \
			font="Helvetica 14")
		self.button_choose.pack()
		self.button_sort = Radiobutton(self.topFrame, text="Sort all" \
			+ "images in a directory by color", value=3, \
			variable="mode", command=lambda: self.modeswitch(2), \
			font="Helvetica 14")
		self.button_sort.pack()
		self.select = Button(self.fileFrame, text="Select file...", \
			command=self.fileselect, font="Helvetica 14").pack()
		self.file = Label(self.fileFrame, text="no file selected", \
			font="Helvetica 14")
		self.file.pack()

		# creating button for each color
		self.red = Radiobutton(self.midFrame, text="red", \
			state=NORMAL, value=1, variable="colors", command=lambda: \
			self.colorselect("red"), font="Helvetica 14")
		self.orange = Radiobutton(self.midFrame, text="orange", \
			state=NORMAL, value=2, variable="colors", command=lambda: \
			self.colorselect("orange"), font="Helvetica 14")
		self.yellow = Radiobutton(self.midFrame, text="yellow", \
			state=NORMAL, value=3, variable="colors", command=lambda: \
			self.colorselect("yellow"), font="Helvetica 14")
		self.green = Radiobutton(self.midFrame, text="green", \
			state=NORMAL, value=4, variable="colors", command=lambda: \
			self.colorselect("green"), font="Helvetica 14")
		self.cyan = Radiobutton(self.midFrame, text="cyan", \
			state=NORMAL, value=5, variable="colors", command=lambda: \
			self.colorselect("cyan"), font="Helvetica 14")
		self.blue = Radiobutton(self.midFrame, text="blue", \
			state=NORMAL, value=6, variable="colors", command=lambda: \
			self.colorselect("blue"), font="Helvetica 14")
		self.purple = Radiobutton(self.midFrame, text="purple", \
			state=NORMAL, value=7, variable="colors", command=lambda: \
			self.colorselect("purple"), font="Helvetica 14")
		self.pink = Radiobutton(self.midFrame, text="pink", \
			state=NORMAL, value=8, variable="colors", command=lambda: \
			self.colorselect("pink"), font="Helvetica 14")

		for button in (self.red, self.orange, self.yellow, self.green, \
			self.cyan, self.blue, self.purple, self.pink):
			button.pack(side=LEFT)

		self.initialize = Button(self.bottomFrame, text="Initialize", \
			state=DISABLED, command=lambda: self.mode(self.modefunc), \
			font="Helvetica 14")
		self.initialize.pack()
		self.output = Label(self.bottomFrame, font="Helvetica 14")
		self.output.pack()

		# initial selection of buttons
		self.red.invoke()
		self.button_comp.invoke()
		self.modefunc = "color_choose"
		mainloop()

	def fileselect(self):
		if self.modefunc == "color_sort":
			self.filename = filedialog.askdirectory()
			self.dirpath = self.filename
			self.file["text"] = self.filename
		else:
			self.filename = filedialog.askopenfilename(\
				filetypes=[("Image File",'.jpg')])
			if self.filename != "":
				self.img = Image.open(self.filename, 'r')
				self.file["text"] = self.filename

		self.initswitch()

	def initswitch(self):
		if self.file["text"] != "no file selected":
			self.initialize.config(state=NORMAL)
		else:
			self.initialize.config(state=DISABLED)

	def colorselect(self, color):
		self.color = color

	def modeswitch(self, switch):
		if switch:
			for button in (self.red, self.orange, self.yellow, self.green, \
				self.cyan, self.blue, self.purple, self.pink):
				button.config(state=NORMAL)
			if switch == 1:
				self.modefunc = "color_choose"
			if switch == 2:
				self.modefunc = "color_sort"
		else:
			for button in (self.red, self.orange, self.yellow, self.green, \
				self.cyan, self.blue, self.purple, self.pink):
				button.config(state=DISABLED)
			self.modefunc = "color_comp"
		self.file["text"] = "no file selected"
		self.initswitch()

	def mode(self, func):
		if func == "color_comp":
			self.color_comp(self.img)
		if func == "color_choose":
			self.color_choose(self.img, self.color)
		if func == "color_sort":
			self.color_sort(self.dirpath, self.color)

	def color_comp(self, img):
		color_value = color_in_img(img)
		if isinstance(color_value, str):
			self.output["text"] = color_value
		else:
			comp_output = color_value[0] + " is the most used color, " + \
			"composing " + str(percentage(color_value[1])) + "% of the image"
			self.output["text"] = comp_output

	def color_choose(self, img, color):
		color_value = color_in_img(img, color)
		if isinstance(color_value, str):
			self.output["text"] = color_value
		else:
			choose_output = "color selected: " + color + " || " \
			+ "% composition: " + str(percentage(color_value)) + "%"
			self.output["text"] = choose_output

	def color_sort(self, path, color):
		direc = os.listdir(path)
		files = {}
		for infile in direc:
			if infile[-4:] == ".jpg" or infile[-4:] == ".JPG":
				img = Image.open(path+"/"+infile)
				decimal = color_in_img(img, color)
				files[infile] = decimal
		files_sorted = sorted(files.items(), key=operator.itemgetter(1), \
		 				reverse=True)
		self.output["text"] = "<file name> | <composition of " + str(color) \
			+ ">\n------------------------------------\n"
		for value in files_sorted:
			self.output["text"] += str(value) + "\n"


root = Tk()
color = StringVar()
ICS_gui = GUI(root, color)
