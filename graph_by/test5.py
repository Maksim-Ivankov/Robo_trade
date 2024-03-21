from tkinter import *   
import os   
import sys
sys.path.insert(1,os.path.join(sys.path[0],'../../../'))

ws = Tk()
ws.title('PythonGuides')
ws.geometry('40x500')




image_path=sys.path[0] + "\image\png\kist.png"


canvas = Canvas(
    ws,
    width = 40, 
    height = 500
    )      
canvas.pack()      
img = PhotoImage(file=image_path)      
canvas.create_image(10,10, anchor=NW, image=img)      
ws.mainloop()  
















