from PIL import Image
from numpy import average, round
import numpy as np
from numba import njit
import colorsys

# returns percentage of black in photo
def calc_black():
    print("File name?")
    filename = input("")

    def black_in_img(img):
        try:
            im = Image.open(img, 'r')
            width, height = im.size
            pixel_values = list(im.getdata())

            black_data = []
            for pixel in pixel_values:
                black_data.append(average(pixel))

            black_value = average(black_data)/256.0*100
            return "This photo is " + str(int(round(black_value))) + "% black."

        except FileNotFoundError:
            return "Error: file <" + filename + "> not found"

    return black_in_img(filename)

# returns most used color in image
def color_comp():
    print("File name?")
    filename = input("")

    def color_in_img(img):

        # Convert HSV to degrees/percentages/percentages
        def hue(pixel):
            return np.round(pixel[0]*360, 1)

        def saturation(pixel):
            return np.round(pixel[1]*100, 1)

        def value(pixel):
            return np.round(pixel[2]/255*100, 1)

        # Bounds for colors, ranges decided with:
        # http://www.workwithcolor.com/red-color-hue-range-01.htm
        def redval(pixel):
            if hue(pixel) >= 346 or (hue(pixel) >= 0 and hue(pixel) <= 20):
                return True

        def orangeval(pixel):
            if hue(pixel) >= 11 and hue(pixel) <= 50:
                return True

        def yellowval(pixel):
            if hue(pixel) >= 41 and hue(pixel) <= 80:
                return True

        def greenval(pixel):
            if hue(pixel) >= 61 and hue(pixel) <= 169:
                return True

        def cyanval(pixel):
            if hue(pixel) >= 141 and hue(pixel) <= 220:
                return True

        def blueval(pixel):
            if hue(pixel) >= 201 and hue(pixel) <= 280:
                return True

        def purpleval(pixel):
            if hue(pixel) >= 241 and hue(pixel) <= 330:
                return True

        def pinkval(pixel):
            if hue(pixel) >= 321 and hue(pixel) <= 355:
                return True

        valuefunc = np.array([redval, orangeval, yellowval, greenval, cyanval, \
                                blueval, purpleval, pinkval])

        valuecount = np.array([0, 0, 0, 0, 0, 0, 0, 0])

        colorname = np.array(["red", "orange", "yellow", "green", "cyan", \
                                "blue", "purple", "pink"])

        #try:
        im = Image.open(img, 'r')
        width, height = im.size
        pixel_values = np.array(im.getdata())
        color_data = np.array([0, 0, 0])
        i = 0
        for pixel in pixel_values:
            color_data = np.vstack((color_data, \
                np.asarray(colorsys.rgb_to_hsv(*pixel))))
        @njit
        def ex(img):
            for pixel in color_data:
                if np.round(pixel[0]*360, 1) >= 346 or (np.round(pixel[0]*360, 1) >= 0 and np.round(pixel[0]*360, 1) <= 20):
                    i += 1
                #if saturation(pixel) == 0:
                #    continue
                #if saturation(pixel) == 100 and value(pixel) == 0:
                #    continue
                #for color in valuefunc:
                #    if color(pixel):
                #        valuecount[index] += 1
                #    index += 1
            return i
            #max_index = np.argmax(valuecount)
            #return max_index
        return ex(img)
            #return colorname[max_index] + " is the most used color, composing " \
            #    + str(int(round(valuecount[max_index]/len(pixel_values)*100))) \
            #    + "% of the image"

        #except FileNotFoundError:
        #    return "Error: file <" + filename + "> not found"

    return color_in_img(filename)

# select ImageColorSort mode
def mode_select():
    mode_dict = {"black calc": calc_black,
                 "color comp": color_comp}

    print("Select a mode:")
    for key in mode_dict:
        print("- " + key)
    mode = input("")

    try:
        return mode_dict[mode]()
    except KeyError:
        return "Error: <" + mode + "> not a valid mode"

print(mode_select())
