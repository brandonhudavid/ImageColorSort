from tkinter import *
from tkinter import filedialog

def fileselect():
	fileopen = filedialog.askopenfile()
	name["text"] = str(fileopen)
	fileattr = name["text"]
	filename = ""
	for elem in fileattr:
		filename += elem
		if filename[-1:] == "/":
			filename = ""
		if filename[-3:] == "jpg":
			break
	name["text"] = filename

root = Tk()
topFrame = Frame(root, width=500, height=200).pack()
bottomFrame = Frame(root, width=500, height=200).pack()

header = Label(topFrame, text="ImageColorSort").pack(side=TOP)
button_comp = Button(topFrame, text="color comp").pack(side=TOP)
select = Button(bottomFrame, text="Select file...", \
            command=fileselect).pack(side=BOTTOM)
name = Label(bottomFrame, text="").pack(side=BOTTOM)

mainloop()

# class GUI:
# 	def __init__(self, master, name):
# 		self.topFrame = Frame(master, width=1000, height=500)
# 		self.topFrame.pack()
# 		self.bottomFrame = Frame(master, width=1000, height=500)
# 		self.bottomFrame.pack(side=BOTTOM)
#
# 		self.header = Label(self.topFrame, text="ImageColorSort")
# 		self.header.pack()
#
# 		self.button_comp = Button(self.topFrame, text="color comp")
# 		self.button_comp.pack(side=BOTTOM)
#
# 		self.output = Button(self.topFrame, text="Select file...", \
# 			command=self.fileselect)
# 		self.output.pack(side=BOTTOM)
#
# 		self.file = Label(self.topFrame)
# 		self.file.pack(side=BOTTOM)
#
# 		mainloop()
#
# 	def fileselect(self):
# 		self.fileopen = filedialog.askopenfile()
# 		self.file["text"] = self.fileopen
# 		self.filename = self.file["text"]
# 		self.name = ""
# 		for elem in self.filename:
# 			self.name += elem
# 			if self.name[-1:] == "/":
# 				self.name = ""
# 			if self.name[-3:] == "jpg":
# 				break
# 		self.file["text"] = self.name
