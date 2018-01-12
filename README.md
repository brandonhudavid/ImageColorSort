#### by Brandon David
###### code last updated December 28, 2017
# ImageColorSort
A multi-functional image processing Python script that analyzes pixel hues within images. There are 3 modes available:</br>
![alt text](https://github.com/brandonhudavid/ImageColorSort/tree/master/sourcecode/img-readme.png "Logo Title Text 1")
1. **Find the most used color in an image:**</br>
Select an image from your computer. The program will return the most used color and that color's percent composition of the image.
2. **Find the % composition of a color in an image:**</br>
Select an image from your computer and select a color. The program will return the color selected and that color's percent composition of the image.
3. **Sort all images in a directory by color:**</br>
Select a directory from your computer and select a color to sort by. The program will list all files within the directory and their respective percent color composition, from highest composition to lowest.
___
## Getting Started
### Prerequisites
Program compatible with MAC OS X devices. Analyzes images of jpg, jpeg, and png format. Can access files outside of the local directory. The sourcecode folder is not required to run the program.
### Installing
To use ImageColorSort, download **ImageColorSort.zip.001** and **ImageColorSort.zip.002**. Extracting the two zip files simultaneously will create the **ImageColorSort** app. To run the program, control + left click on the app and click Open.
## Using ImageColorSort
1. Select from the three modes.
2. Select an image file or folder from your computer.
3. If necessary, select a color to analyze.
4. Initialize and wait for data output.
## Built With
* [PyInstaller](http://www.pyinstaller.org/) - Compiles program into MAC OS X application bundle
* [Pillow](https://pillow.readthedocs.io/en/5.0.0/) - PIL fork, dictionaries pixel data from images
* [Tkinter](https://docs.python.org/2/library/tkinter.html) - GUI toolkit, establishes user interface and returns human-readable data
