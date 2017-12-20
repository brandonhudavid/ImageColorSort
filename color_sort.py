from PIL import Image
from numba import jit
import colorsys
import time
import glob
import operator

#check runtime
start_time = time.clock()

def percentage(decimal):
	return int(round(decimal*100))

# returns a color and the % composition of that color in image
def color_in_img(img, color=None):
	# file name exists
	try:
		# initialize image data
		fnf_error = False
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
		print("pixel list created at ", time.clock() - start_time, "sec")
		for pixel in pixel_data:
			# most time occupied when converting to HSV
			hsv = colorsys.rgb_to_hsv(*pixel)
			# add weight values to HSV keys in dictionary
			try:
				color_dict[hsv] += 1
			except KeyError:
				color_dict[hsv] = 1
		print("pixels dictionaried at ", time.clock() - start_time, "sec")

	# file name does not exist
	except FileNotFoundError:
		fnf_error = True
		pass
	if fnf_error:
		raise TypeError

	# counters, corresponding to color names
	counter = [0, 0, 0, 0, 0, 0, 0, 0]
	#colorname = ["red", "orange", "yellow", "green", "cyan", "blue", \
	#				"purple", "pink"]

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

	if color == None:
		# value of highest counter
		max_count = max(counter)
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

colorname = ["red", "orange", "yellow", "green", "cyan", "blue", \
				"purple", "pink"]

def color_sort():
	print("Color?")
	for name in colorname:
		print(name)
	color = input("")
	if color not in colorname:
		raise TypeError\
		("<" + color + "> not a valid color input")

	files = {}
	# input file name
	for infile in glob.glob("*.jpg"):
		img = Image.open(infile, 'r')
		decimal = color_in_img(img, color)
		files[infile] = decimal
	files_sorted = sorted(files.items(), key=operator.itemgetter(1), \
	 				reverse=True)
	print("<file name> | <composition of " + color + ">")
	print("--------------------------------------")
	for value in files_sorted:
		print(value)


color_sort()

# print runtime
print("Runtime: ", time.clock() - start_time, "seconds")
