from PIL import Image
from numpy import average, round
#im = Image.open('gradient.jpg', 'r')
#width, height = im.size
#pixel_values = list(im.getdata())

#black_data = []
#for pixel in pixel_values:
#    black_data.append(average(pixel))

#black_value = average(black_data)/256.0*100
#print(black_data)

#print("This photo is " + str(int(round(black_value))) + "% black.")

print("File name?")
filename = input("")


def calc_black(img):

    im = Image.open(str(img), 'r')
    width, height = im.size
    pixel_values = list(im.getdata())
    #print(width, height)

    black_data = []
    for pixel in pixel_values:
        black_data.append(average(pixel))


    black_value = average(black_data)/256.0*100
    print("This photo is " + str(int(round(black_value))) + "% black.")

try:
    calc_black(filename)
except FileNotFoundError:
    print("Error: file <" + filename + "> not found")
