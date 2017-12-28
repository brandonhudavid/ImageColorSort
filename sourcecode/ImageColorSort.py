from tkinter import *
from tkinter import filedialog
import PIL
from PIL import Image
import colorsys
import operator
import os, sys


# used by PyInstaller to find files
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# used by color_comp to return numeric %
def percentage(decimal):
	return round(decimal*100, 5)

def getRGBfromI(RGBint):
    blue =  RGBint & 255
    green = (RGBint >> 8) & 255
    red =   (RGBint >> 16) & 255
    return red, green, blue

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
		# if RGB data stored as integer
		if isinstance(pixel, int):
			pixel = getRGBfromI(pixel)
		# most time occupied when converting to HSV
		hsv = colorsys.rgb_to_hsv(pixel[0], pixel[1], pixel[2])
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

### GUI SETUP ###
class GUI:

	def __init__(self, master, color):
		# title, icon, window size, default font
		master.title("ImageColorSort")
		master.iconbitmap(resource_path("bd_icon.ico"))
		master.geometry("475x700")
		master.option_add("*Font", "Helvetica 14")

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

		# bg image created in canvas underneath output frame
		self.bg_img = PhotoImage(file=resource_path("bd_bg.gif"))
		self.bg_canvas = Canvas(master)
		self.bg_canvas.pack(side=LEFT, fill=BOTH, expand=YES)
		self.bg_canvas.create_image(0, 0, image=self.bg_img, anchor='nw')
		self.outputFrame = Frame(self.bg_canvas)
		self.outputFrame.pack()

		# helper frame in canvas, stores and destroys text in color sort
		self.helperFrame = Frame(self.bg_canvas)
		# vertical scrollbar for mode 3
		self.vsb = Scrollbar(self.bg_canvas, orient="vertical", command=self.bg_canvas.yview)
		# self.bg_canvas.configure(yscrollcommand=self.vsb.set)
		# self.vsb.pack(side=RIGHT, fill=Y)
		# self.bg_canvas.create_window((237,0), window=self.helperFrame, anchor=N,\
		# 	tags="self.helperFrame")
		#self.helperFrame.bind("<Configure>", self.onFrameConfigure)

		# header
		self.header = Label(self.topFrame, text="ImageColorSort", \
			font="Helvetica 24 bold").pack(pady=(10,0))
		self.developer = Label(self.topFrame, text="developed by " \
			+ "Brandon David\n" + \
			"(https://github.com/brandonhudavid/ImageColorSort)", \
			font="Helvetica 13").pack()
		self.supported = Label(self.topFrame, text="Supported file types: "\
			+".jpg, .jpeg, .png", font="Helvetica 14 underline").pack(pady=10)

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

		# Button for each color
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
		self.modefunc = "color_comp"
		mainloop()

	# opens image or directory, depending on mode
	def fileselect(self):
		if self.modefunc == "color_sort":
			self.filename = filedialog.askdirectory()
			if self.filename != "":
				self.dirpath = self.filename
				self.file["text"] = "/"+os.path.split(self.filename)[1]
				if len(self.file["text"]) > 30:
					self.file["text"] = self.file["text"][:20]+"..."\
						+self.file["text"][-14:]
		else:
			# supports .jpg, .png, and .jpeg image formats
			self.filename = filedialog.askopenfilename(\
				filetypes=[("Image File",'.jpg .png .jpeg')])
			if self.filename != "":
				self.img = Image.open(self.filename, 'r')
				self.file["text"] = os.path.split(self.filename)[1]
				if len(self.file["text"]) > 30:
					self.file["text"] = self.file["text"][:15]+"..."\
						+self.file["text"][-14:]
		self.initswitch()

	# enable "Initialize" button if file is selected
	def initswitch(self):
		if self.file["text"] != "no file selected":
			self.initialize.config(state=NORMAL)
		else:
			self.initialize.config(state=DISABLED)

	# used by color buttons to change self.color
	def colorselect(self, color):
		self.color = color

	# switching modes; reconfigure buttons, functions, file selection
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

	# run when "Initialize" is clicked
	def mode(self, func):
		# canvas, helperFrame, & scrollbar management
		self.bg_canvas.delete("all")
		self.vsb.destroy()
		self.bg_canvas.yview_moveto(0.0)
		self.bg_canvas.create_image(0, 0, image=self.bg_img, anchor='nw')
		self.helperFrame = Frame(self.bg_canvas)
		self.outputFrame = Frame(self.bg_canvas)
		self.outputFrame.pack(side=BOTTOM)
		self.vsb = Scrollbar(self.bg_canvas, orient="vertical")
		self.bg_canvas.create_window((237,0), window=self.helperFrame, anchor=N,\
			tags="self.helperFrame")

		# different functions for different modes
		if func == "color_comp":
			self.color_comp(self.img)
		if func == "color_choose":
			self.color_choose(self.img, self.color)
		if func == "color_sort":
			self.output["text"] = ""
			self.color_sort(self.dirpath, self.color)

	# used by scrollbar to scroll through helperFrame
	def onFrameConfigure(self, event):
		'''Reset the scroll region to encompass the inner frame'''
		self.bg_canvas.configure(scrollregion=self.bg_canvas.bbox("all"))

	# mode 1 (color_value returns string if Error)
	def color_comp(self, img):
		color_value = color_in_img(img)
		if isinstance(color_value, str):
			self.output["text"] = color_value
		else:
			comp_output = color_value[0] + " is the most used color,\n" + \
			"composing " + str(percentage(color_value[1])) + "% of the image"
			self.output["text"] = comp_output

	# mode 2
	def color_choose(self, img, color):
		color_value = color_in_img(img, color)
		choose_output = "color selected: " + color + "\n" \
		+ "percent composition: " + str(percentage(color_value)) + "%"
		self.output["text"] = choose_output

	# mode 3
	def color_sort(self, path, color):
		direc = os.listdir(path)
		files = {}
		# only opens .jpg, .png, .jpeg
		for infile in direc:
			if infile[-4:] == ".jpg" or infile[-4:] == ".png" or\
				infile[-5:] == ".jpeg" or infile[-4:] == ".JPG" or\
				infile[-4:] == ".PNG" or infile[-5:] == ".JPEG":
				img = Image.open(path+"/"+infile)
				decimal = color_in_img(img, color)
				files[infile] = decimal
		files_sorted = sorted(files.items(), key=operator.itemgetter(1), \
		 				reverse=True)
		# return Error if no supported files
		if len(files_sorted) == 0:
			self.output["text"] = "Error: no supported image file in "\
				+"selected directory\n(must be .jpg, .jpeg, or .png)"
		else:
			# if more than 15 files, add scrollbar
			if len(files_sorted) > 15:
				self.vsb.configure(command=self.bg_canvas.yview)
				self.bg_canvas.configure(yscrollcommand=self.vsb.set)
				self.vsb.pack(side=RIGHT, fill=Y)
				self.helperFrame.bind("<Configure>", self.onFrameConfigure)
			# create two columns for file name and color composition
			Label(self.helperFrame, text="file name",\
				font="Helvetica 14 underline").grid(row=0)
			Label(self.helperFrame, text="composition of "+color,\
				font="Helvetica 14 underline").grid(row=0, column=1)
			i = 1
			for value in files_sorted:
				if len(str(value[0])) > 30:
					Label(self.helperFrame, text=str(value[0])[:15]\
					+"..."+str(value[0])[-10:]).grid(row=i, sticky=E)
				else:
					Label(self.helperFrame, text=value[0]).grid(row=i)
				Label(self.helperFrame, text=str(percentage(value[1]))[:8]\
				+"%").grid(row=i, column=1)
				i+=1

root = Tk()
color = StringVar()
ICS_gui = GUI(root, color)
