from PIL import Image
from numpy import average, round
from numba import njit
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
		pixel_values = list(im.getdata())

		color_data = []
		for pixel in pixel_values:
			color_data.append(colorsys.rgb_to_hsv(*pixel))

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

		counter = [0, 0]
		colorname = ["purple", "blank"]

		@njit
		def color_count(hue):
			if hue >= 241/360 and hue <= 330/360:
				return 0
			else:
				return 1
		# without @njit: 0.3275s
		# with @njit: 0.45s

        #valuedict = {"purple": purpleval}

        #valuecount = {"purple": 0}
		for pixel in color_data:
			if pixel[1] == 0 or (pixel[1] == 1 and pixel[2] == 0):
				continue
			color = color_count(pixel[0])
			counter[color] += 1

		max_count = max(counter)
		max_index = counter.index(max_count)
		color_most = colorname[max_index]

		return color_most + " is the most used color, composing " \
			+ str(int(round(max_count/len(pixel_values)*100))) \
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
