from PIL import Image
from numpy import average, round
import colorsys
import time

start_time = time.clock()

# returns percentage of black in photo
def calc_black():
    print("File name?")
    filename = input("")

    return black_in_img(filename)

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


# select ImageColorSort mode

print(calc_black())

print(time.clock() - start_time, "seconds")
