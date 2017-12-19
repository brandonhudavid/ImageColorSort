from PIL import Image
from numpy import average, array, concatenate
from numba import jit
import colorsys
import time

start_time = time.clock()

# returns most used color in image
def color_comp():
	print("File name?")
	img = input("")

	try:
		im = Image.open(img, 'r')
		width, height = im.size
		color_dict = {}
		pixel_data = list(im.getdata())
		for pixel in pixel_data:
			converted = colorsys.rgb_to_hsv(*pixel)
			if converted in color_dict:
				color_dict[converted] += 1
			else:
				color_dict[converted] = 1
		#color_data = [colorsys.rgb_to_hsv(*px) for px in list(im.getdata())]

	except FileNotFoundError:
		return "Error: file <" + filename + "> not found"

	def color_in_img(img):
        # Convert HSV to degrees/percentages/percentages
        #def hue(pixel):
        #    return round(pixel[0]*360, 1)

        #def saturation(pixel):
        #    return round(pixel[1]*100, 1)

        #def value(pixel):
        #    return round(pixel[2]/255*100, 1)

		counter = [0, 0, 0, 0, 0, 0, 0, 0]
		colorname = ["red", "orange", "yellow", "green", "cyan", "blue", \
						"purple", "pink"]

		@jit
		def color_count(hue):
			indices = array([8])
			if hue >= 346/360 or (hue >= 0 and hue <= 20/360):
				indices = concatenate((indices, array([0])))
			if hue >= 11/360 and hue <= 50/360:
				indices = concatenate((indices, array([1])))
			if hue >= 41/360 and hue <= 80/360:
				indices = concatenate((indices, array([2])))
			if hue >= 61/360 and hue <= 169/360:
				indices = concatenate((indices, array([3])))
			if hue >= 141/360 and hue <= 220/360:
				indices = concatenate((indices, array([4])))
			if hue >= 201/360 and hue <= 280/360:
				indices = concatenate((indices, array([5])))
			if hue >= 241/360 and hue <= 330/360:
				indices = concatenate((indices, array([6])))
			if hue >= 321/360 and hue <= 355/360:
				indices = concatenate((indices, array([7])))
			return indices

		# without @njit: 0.3275s
		# with @njit: 0.45s

        #valuedict = {"purple": purpleval}

        #valuecount = {"purple": 0}
		for pixel in color_dict:
			if pixel[1] == 0 or (pixel[1] == 1 and pixel[2] == 0):
				continue
			#add weight argument for adjacent duplicate pixels
			index_array = color_count(pixel[0])
			for elem in index_array[1:]:
				counter[int(elem)] += 1*color_dict[pixel]

			#counter[color] += 1

		max_count = max(counter)
		max_index = counter.index(max_count)
		color_most = colorname[max_index]

		return color_most + " is the most used color, composing " \
			+ str(int(round(max_count/len(pixel_data)*100))) \
			+ "% of the image"

	return color_in_img(img)

# select ImageColorSort mode
def mode_select():
    mode_dict = {"color comp": color_comp}

    print("Select a mode.")
    for key in mode_dict:
        print(key)
    mode = input("")

    try:
        return mode_dict[mode]()
    except KeyError:
        return "Error: <" + mode + "> not a valid mode"

print(mode_select())

print("Runtime: ", time.clock() - start_time, "seconds")
