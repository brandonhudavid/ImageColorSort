#### by Brandon David
# ImageColorSort
###### A Python script that is intended to sort all image files in a folder by a color value. Utilizes Pillow, a PIL fork.
12/16/17 </br>
* returns & composition of black in an image
* added color_comp, returns most used color in image and % composition
* runs slowly due to iteration through every single pixel </br>
12/17/17 </br>
* optimized runtime by removing functions
* dictionary with unique HSV keys and weight values for duplicate keys
* imported njit from numba for faster calculations but no improvement
