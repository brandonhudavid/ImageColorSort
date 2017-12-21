from tkinter import *
from tkinter import filedialog
from PIL import Image
import colorsys
import operator


# class GUI:
# 	def __init__(self, master, name):
# 		self.topFrame = Frame(master, width=1000, height=500)
# 		self.topFrame.pack()
# 		#self.bottomFrame = Frame(master, width=1000, height=500)
# 		#self.bottomFrame.pack(side=BOTTOM)
#
# 		self.header = Label(self.topFrame, text="ImageColorSort")
# 		self.header.pack()
#
# 		self.button_comp = Button(self.topFrame, text="color comp")
# 		self.button_comp.pack(side=BOTTOM)
#
# 		self.output = Button(self.topFrame, text="Select file...", \
# 			command=self.fileselect)
# 		self.output.pack(side=BOTTOM)
#
# 		self.file = Label(self.topFrame)
# 		self.file.pack(side=BOTTOM)
#
# 		mainloop()
#
# 	def fileselect(self):
# 		self.fileopen = filedialog.askopenfile()
# 		self.file["text"] = self.fileopen
# 		self.filename = self.file["text"]
# 		self.name = ""
# 		for elem in self.filename:
# 			self.name += elem
# 			if self.name[-1:] == "/":
# 				self.name = ""
# 			if self.name[-3:] == "jpg":
# 				break
# 		self.file["text"] = self.name


	# def changelabel(self):
	# 	self.output["text"] = "File name?"
	# 	self.file = Entry(self.bottomFrame, textvariable=name)
	# 	self.file.pack(side=BOTTOM)
	# 	self.enter = Button(self.bottomFrame, text="Enter", \
	# 				command=self.filename)
	# 	self.enter.pack(side=RIGHT)
    #
	# def filename(self):
	# 	self.filename = name.get()
	# 	testLabel = Label(self.bottomFrame, text=self.filename)
	# 	testLabel.pack()


#header = Label(root, text="ImageColorSort created by Brandon David")
#header.grid(row=0)
#header.pack()

#topFrame = Frame(root)
#topFrame.pack()
#bottomFrame = Frame(root)
#bottomFrame.pack(side=BOTTOM)

#button_comp = Button(text="color comp")
#button_comp.grid(row=1)

#file_input = Entry(root)
#file_input.grid(row=2)

#root.mainloop()




# from PIL import Image
# import colorsys
# import operator
#
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
			raise ValueError\
			("<" + img + "> has no color")
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
#
### FUNCTIONS FOR ALL MODES ###
def color_comp(img):
	# # input file name
	# print("File name?")
	# filename = input("")
    #
	# try:
	# 	fnf_error = False
	# 	img = Image.open(filename, 'r')
	# except FileNotFoundError:
	# 	fnf_error = True
	# if fnf_error:
	# 	raise TypeError\
	# 	("<" + filename + "> not found in directory")

	color_value = color_in_img(img)
	print(color_value[0] + " is the most used color, composing " \
		+ str(percentage(color_value[1])) + "% of the image")
#
# def color_choose():
# 	# input file name
# 	print("File name?")
# 	filename = input("")
#
# 	try:
# 		fnf_error = False
# 		img = Image.open(filename, 'r')
# 	except FileNotFoundError:
# 		fnf_error = True
# 	if fnf_error:
# 		raise TypeError\
# 		("<" + filename + "> not found in directory")
#
# 	#input color choice
# 	print("Color?")
# 	for name in colorname:
# 		print(name)
# 	color = input("")
# 	if color not in colorname:
# 		raise TypeError\
# 		("<" + color + "> not a valid color input")
#
# 	color_value = color_in_img(img, color)
# 	print("color selected: " + color + " | % composition: " \
# 			+ str(percentage(color_value)) + "%")
#
# def color_sort():
# 	print("Color?")
# 	for name in colorname:
# 		print(name)
# 	color = input("")
# 	if color not in colorname:
# 		raise TypeError\
# 		("<" + color + "> not a valid color input")
#
# 	files = {}
# 	# input file name
# 	for infile in glob.glob("*.jpg"):
# 		img = Image.open(infile, 'r')
# 		decimal = color_in_img(img, color)
# 		files[infile] = decimal
# 	files_sorted = sorted(files.items(), key=operator.itemgetter(1), \
# 	 				reverse=True)
# 	print("<file name> | <composition of " + color + ">")
# 	print("--------------------------------------")
# 	for value in files_sorted:
# 		print(value)
#
# ### Select ImageColorSort mode ###
# def mode_select():
# 	mode_dict = {"color comp": color_comp,
# 				 "color choose": color_choose,
# 				 "color sort": color_sort}
#
# 	# prints list of modes
# 	print("Select a mode.")
# 	for key in mode_dict:
# 		print(key)
# 	mode = input("")
#
# 	try:
# 		return mode_dict[mode]()
# 	# if mode inputted does not exist
# 	except KeyError:
# 		pass
# 	raise TypeError\
# 		("<" + mode + "> not a valid mode")
#
# mode_select()

class GUI:
	# use a for loop to create buttons corresponding to colors
	def __init__(self, master):
		master.geometry("500x250")
		self.name = StringVar()
		self.topFrame = Frame(master).pack()
		self.bottomFrame = Frame(master).pack()
		self.header = Label(self.topFrame, text="ImageColorSort").pack()
		self.button_comp = Radiobutton(self.topFrame, text="Find the most " \
			+ "used color in an image").pack()
		self.select = Button(self.bottomFrame, text="Select file...", \
			command=self.fileselect).pack()
		self.file = Label(self.bottomFrame, text="no file selected")
		self.file.pack()

		self.initialize = Button(self.bottomFrame, text="Initialize", \
			state=DISABLED, command=lambda: color_comp(self.img))
		self.initialize.pack()
		mainloop()

	def fileselect(self):
		self.fileopen = filedialog.askopenfilename(\
			filetypes=[("Image File",'.jpg')])
		self.img = Image.open(self.fileopen)
		self.file["text"] = self.fileopen
		self.initswitch()

	def initswitch(self):
		if self.file["text"] != "no file selected":
			self.initialize.config(state=NORMAL)
		else:
			self.initialize.config(state=DISABLED)

root = Tk()
GUI(root)
