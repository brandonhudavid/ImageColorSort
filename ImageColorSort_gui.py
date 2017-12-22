from tkinter import *
from tkinter import filedialog
from PIL import Image
import colorsys
import operator
import os, sys

# used by color_comp to return numeric %
def percentage(decimal):
	return round(decimal*100, 5)

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
		# window size
		master.title("ImageColorSort")
		master.geometry("475x700")

		# pack frames
		self.topFrame = Frame(master)
		self.topFrame.pack()
		self.fileFrame = Frame(master, pady=5)
		self.fileFrame.pack()
		self.midFrame = Frame(master)
		self.midFrame.pack(pady=(5,0))
		self.midFrame2 = Frame(master)
		self.midFrame2.pack(pady=(0,10))
		self.bottomFrame = Frame(master)
		self.bottomFrame.pack()

		# bg image
		self.bg_img = PhotoImage(file="bd_bg.gif")
		self.bg_canvas = Canvas(master)
		self.bg_canvas.pack(side=TOP, fill=BOTH, expand=YES)
		self.bg_canvas.create_image(0, 0, image=self.bg_img, anchor='nw')

		self.outputFrame = Frame(self.bg_canvas)
		self.outputFrame.pack()
		# creates and destroys text in mode 3
		self.helperFrame = Frame(self.outputFrame)
		self.helperFrame.pack(side=TOP)

		# change default font
		master.option_add("*Font", "Helvetica 14")
		# title
		self.header = Label(self.topFrame, text="ImageColorSort", \
			font="Helvetica 24 bold").pack(pady=(10,0))
		self.developer = Label(self.topFrame, text="developed by " \
			+ "Brandon David\n" + \
			"(https://github.com/brandonhudavid/ImageColorSort)", \
			font="Helvetica 13").pack(pady=(0,10))
		# Buttons for modes
		self.button_comp = Radiobutton(self.topFrame, text="Find the most " \
			+ "used color in an image", value=1, variable="mode", \
			command=lambda: self.modeswitch(0))
		self.button_comp.pack()
		self.button_choose = Radiobutton(self.topFrame, text="Find the " \
			+ "% composition of a color in an image", value=2, \
			variable="mode", command=lambda: self.modeswitch(1))
		self.button_choose.pack()
		self.button_sort = Radiobutton(self.topFrame, text="Sort all " \
			+ "images in a directory by color", value=3, \
			variable="mode", command=lambda: self.modeswitch(2))
		self.button_sort.pack()
		# Buttons to select file
		self.select = Button(self.fileFrame, text="Select file...", \
			command=self.fileselect).pack()
		self.file = Label(self.fileFrame, text="no file selected")
		self.file.pack()

		# creating button for each color
		self.red = Radiobutton(self.midFrame, text="red", \
			state=NORMAL, value=1, variable="colors", command=lambda: \
			self.colorselect("red"))
		self.orange = Radiobutton(self.midFrame, text="orange", \
			state=NORMAL, value=2, variable="colors", command=lambda: \
			self.colorselect("orange"))
		self.yellow = Radiobutton(self.midFrame, text="yellow", \
			state=NORMAL, value=3, variable="colors", command=lambda: \
			self.colorselect("yellow"))
		self.green = Radiobutton(self.midFrame, text="green", \
			state=NORMAL, value=4, variable="colors", command=lambda: \
			self.colorselect("green"))
		self.cyan = Radiobutton(self.midFrame2, text="cyan", \
			state=NORMAL, value=5, variable="colors", command=lambda: \
			self.colorselect("cyan"))
		self.blue = Radiobutton(self.midFrame2, text="blue", \
			state=NORMAL, value=6, variable="colors", command=lambda: \
			self.colorselect("blue"))
		self.purple = Radiobutton(self.midFrame2, text="purple", \
			state=NORMAL, value=7, variable="colors", command=lambda: \
			self.colorselect("purple"))
		self.pink = Radiobutton(self.midFrame2, text="pink", \
			state=NORMAL, value=8, variable="colors", command=lambda: \
			self.colorselect("pink"))
		for button in (self.red, self.orange, self.yellow, self.green, \
			self.cyan, self.blue, self.purple, self.pink):
			button.pack(side=LEFT)

		# Initialize button
		self.initialize = Button(self.bottomFrame, text="Initialize", \
			state=DISABLED, command=lambda: self.mode(self.modefunc))
		self.initialize.pack()
		# Output text
		self.output = Label(self.outputFrame)
		self.output.pack(side=BOTTOM)

		# initial selection of buttons
		self.red.invoke()
		self.button_comp.invoke()
		self.modefunc = "color_choose"
		mainloop()

	def fileselect(self):
		if self.modefunc == "color_sort":
			self.filename = filedialog.askdirectory()
			if self.filename != "":
				self.dirpath = self.filename
				self.file["text"] = "/"+os.path.split(self.filename)[1]
		else:
			self.filename = filedialog.askopenfilename(\
				filetypes=[("Image File",'.jpg')])
			if self.filename != "":
				self.img = Image.open(self.filename, 'r')
				self.file["text"] = os.path.split(self.filename)[1]

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
		self.helperFrame.destroy()
		self.helperFrame = Frame(self.outputFrame)
		self.helperFrame.pack()
		if func == "color_comp":
			self.color_comp(self.img)
		if func == "color_choose":
			self.color_choose(self.img, self.color)
		if func == "color_sort":
			self.output["text"] = ""
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
			choose_output = "color selected: " + color + "\n" \
			+ "percent composition: " + str(percentage(color_value)) + "%"
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
		if len(files_sorted) == 0:
			Label(self.helperFrame, text="Error: no jpg file in selected "\
				+"directory").pack()
		else:
			Label(self.helperFrame, text="file name",\
				font="Helvetica 14 underline").grid(row=0)
			Label(self.helperFrame, text="composition of "+color,\
				font="Helvetica 14 underline").grid(row=0, column=1)
			i = 1
			for value in files_sorted:
				if len(str(value[0])) > 19:
					Label(self.helperFrame, text=str(value[0])[:15]+str("...")+\
					str(value[0])[-4:]).grid(row=i, sticky=E)
				else:
					Label(self.helperFrame, text=value[0]).grid(row=i)
				Label(self.helperFrame, text=str(percentage(value[1]))[:8]+"%").\
					grid(row=i, column=1)
				i+=1

root = Tk()
color = StringVar()
ICS_gui = GUI(root, color)
