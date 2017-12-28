#### by Brandon David
###### last updated December 28, 2017
# ImageColorSort
##### A multi-functional image processing Python script that processes pixel hues within jpg images. Utilizes Pillow, a PIL fork, and Tkinter, a GUI toolkit. Compiled into .exe file with PyInstaller.
___

The script uses Pillow to dictionary pixel data from images and Tkinter to establish a user interface that returns human-readable data. The user can access any directory on the computer.

To use program, download the folder **ImageColorSort** and run the file **ImageColorSort.exe**.

There are 3 modes available:
1. **Find the most used color in an image:**</br>
Select a jpg image from your computer. The program will return the most used color and that color's percent composition of the image.
2. **Find the % composition of a color in an image:**</br>
Select a jpg image from your computer and select a color. The program will return the color selected and that color's percent composition of the image.
3. **Sort all images in a directory by color:**</br>
Select a directory from your computer and select a color to sort by. The program will list all jpg files within the directory from highest color composition to lowest.
