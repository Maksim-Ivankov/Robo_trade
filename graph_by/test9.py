import tkinter as tk

def drag_start(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y
    # print(event.widget.find_withtag("current"))

def drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)
    # print(event.widget.find_withtag("current"))

root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()
rect = canvas.create_rectangle(10, 10, 50, 50, fill="blue")
canvas.tag_bind(rect, "<Button-1>", drag_start)
canvas.tag_bind(rect, "<B1-Motion>", drag_motion)
root.mainloop()
