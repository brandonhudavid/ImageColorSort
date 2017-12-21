#### by Brandon David
###### last updated December 21, 2017
# ImageColorSort
##### A Python script that is intended to sort all image files in a folder by a color value. Utilizes Pillow, a PIL fork.
___

**ImageColorSort.py** utilizes and prints to the terminal, but cannot access directories other than the one it is currently in.

**ImageColorSort_gui.py** utilizes tkinter to create a GUI and allows the user to access any directory on the computer.

There are 3 modes available:
1. Find the most used color in an image:
Select an image from your computer. The program will return the most used color and that color's percent composition of the image.
2. Find the % composition of a color in an image:
Select an image from your computer and select a color. The program will return the color selected and that color's percent composition of the image.
3. Sort all images in a directory by color:
Select a directory from your computer and select a color to sort by. The program will list all jpg files within the directory from highest color composition to lowest.
