from PIL import Image
import numpy as np
import time

def rgb_to_hsv(rgb):
    # Translated from source of colorsys.rgb_to_hsv
    # r,g,b should be a numpy arrays with values between 0 and 255
    # rgb_to_hsv returns an array of floats between 0.0 and 1.0.
    rgb = rgb.astype('float')
    hsv = np.zeros_like(rgb)
    # in case an RGBA array was passed, just copy the A channel
    hsv[..., 3:] = rgb[..., 3:]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    maxc = np.max(rgb[..., :3], axis=-1)
    minc = np.min(rgb[..., :3], axis=-1)
    hsv[..., 2] = maxc
    mask = maxc != minc
    hsv[mask, 1] = (maxc - minc)[mask] / maxc[mask]
    rc = np.zeros_like(r)
    gc = np.zeros_like(g)
    bc = np.zeros_like(b)
    rc[mask] = (maxc - r)[mask] / (maxc - minc)[mask]
    gc[mask] = (maxc - g)[mask] / (maxc - minc)[mask]
    bc[mask] = (maxc - b)[mask] / (maxc - minc)[mask]
    hsv[..., 0] = np.select(
        [r == maxc, g == maxc], [bc - gc, 2.0 + rc - bc], default=4.0 + gc - rc)
    hsv[..., 0] = (hsv[..., 0] / 6.0) % 1.0
    return hsv

start_time = time.clock()
def color_comp():
	# input file name
    print("File name?")
    img = input("")

	# file name exists
    try:
		# initialize image data
        im = Image.open(img, 'r')
        color_list = []
        color_dict = {}
        pixel_data = rgb_to_hsv(np.array(im))
        print("pixel list created at ", time.clock() - start_time, "sec")
        for array in pixel_data:
            color_list.extend(array)
        for hsv in color_list:
            try:
            	color_dict[tuple(hsv)] += 1
            except KeyError:
            	color_dict[tuple(hsv)] = 1
        print("pixels dictionaried at ", time.clock() - start_time, "sec")

    except FileNotFoundError:
        return "Error: file <" + filename + "> not found"

print(color_comp())
