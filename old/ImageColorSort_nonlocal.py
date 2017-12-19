from PIL import Image
from numpy import average, array, concatenate
from numba import njit
import colorsys
import time

#check runtime
start_time = time.clock()

# returns most used color in image
def color_comp():
	# input file name
	print("File name?")
	img = input("")

	# file name exists
	try:
		# initialize image data
		im = Image.open(img, 'r')
		color_dict = {}
		pixel_data = list(im.getdata())
		num_pixels = len(pixel_data)
		for pixel in pixel_data:
			hsv = colorsys.rgb_to_hsv(*pixel)
			# add weight values to HSV keys in dictionary
			if hsv in color_dict:
				color_dict[hsv] += 1
			else:
				color_dict[hsv] = 1

	# file name does not exist
	except FileNotFoundError:
		return "Error: file <" + filename + "> not found"

	def color_in_img(img):

		# counters, corresponding to color names
		counter = [0, 0, 0, 0, 0, 0, 0, 0]
		colorname = ["red", "orange", "yellow", "green", "cyan", "blue", \
						"purple", "pink"]

		#@njit
		def color_count(hue, weight):
			# place holder array, cannot use empty list []
			nonlocal counter
			# concatenate a number corresponding to color
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

		for pixel in color_dict:
			# if saturation is 0 OR value is 0, skip pixel
			if pixel[1] == 0 or pixel[2] == 0:
				continue
			color_count(pixel[0], color_dict[pixel])
			# multiply increment by weight value corresponding to HSV key

		# value of highest counter
		max_count = max(counter)
		# index of counter
		max_index = counter.index(max_count)
		# color corresponding to highest counter
		color_most = colorname[max_index]

		return color_most + " is the most used color, composing " \
			+ str(int(round(max_count/num_pixels*100))) + "% of the image"

	return color_in_img(img)

# select ImageColorSort mode
def mode_select():
    mode_dict = {"color comp": color_comp}

	# prints list of modes
    print("Select a mode.")
    for key in mode_dict:
        print(key)
    mode = input("")

    try:
        return mode_dict[mode]()
	# if mode inputted does not exist
    except KeyError:
        return "Error: <" + mode + "> not a valid mode"

print(mode_select())

# print runtime
print("Runtime: ", time.clock() - start_time, "seconds")

# Runtime of phototest.jpg (1333 x 2000px):
#	5.1s
