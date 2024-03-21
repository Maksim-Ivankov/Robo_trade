from tkinter import *
import os   
import sys
sys.path.insert(1,os.path.join(sys.path[0],'../../../'))

image_path=sys.path[0] + "\image\png\kist.png"

root = Tk()

button = Button(root, text="Click me!")
img = PhotoImage(file=image_path) 
button.config(image=img)
button.pack() # Displaying the button

root.mainloop()