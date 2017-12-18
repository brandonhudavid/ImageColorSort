from PIL import Image
import colorsys
import time

start_time = time.clock()

def color_comp():
	print("File name?")
	img = input("")

	try:
		im = Image.open(img, 'r')
		width, height = im.size
		#converted = list(map(lambda x: colorsys.rgb_to_hsv(*x), list(im.getdata())))
		#return converted[100]

		#x = [colorsys.rgb_to_hsv(*pixel) for pixel in list(im.getdata())]
		#return x[100]
		#pixel_values = list(im.getdata())

		color_dict = {}
		for pixel in list(im.getdata()):
			converted = colorsys.rgb_to_hsv(*pixel)
			if converted in color_dict:
				color_dict[converted] += 1
			else:
				color_dict[converted] = 1





			color_data.append(colorsys.rgb_to_hsv(*pixel))
		return color_data[100]

	except FileNotFoundError:
		return "Error: file <" + filename + "> not found"

print(color_comp())

print("Runtime: ", time.clock() - start_time, "seconds")

# Runtime for converted: 4.1s
# Runtime for list comprehension: 3.77s
# Runtime for append: 3.95s
