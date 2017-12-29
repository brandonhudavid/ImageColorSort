#### by Brandon David
###### last updated December 28, 2017
# ImageColorSort
##### A multi-functional image processing Python script that analyzes pixel hues within images. Compiled into MAC OS X application bundle with PyInstaller.
___

The script uses Pillow, a PIL fork, to dictionary pixel data from images and Tkinter, a GUI toolkit, to establish a user interface that returns human-readable data. The user can access files outside of the local directory.

To use ImageColorSort, download **ImageColorSort.zip.001** and **ImageColorSort.zip.002**. Extracting the two zip files simultaneously will create the **ImageColorSort** app. To run the program, control + left click on the app and click Open. The sourcecode folder is not required to run the program.

There are 3 modes available:
1. **Find the most used color in an image:**</br>
Select a jpg image from your computer. The program will return the most used color and that color's percent composition of the image.
2. **Find the % composition of a color in an image:**</br>
Select a jpg image from your computer and select a color. The program will return the color selected and that color's percent composition of the image.
3. **Sort all images in a directory by color:**</br>
Select a directory from your computer and select a color to sort by. The program will list all jpg files within the directory from highest color composition to lowest.
