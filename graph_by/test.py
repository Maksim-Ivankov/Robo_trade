import tkinter as tk



root = tk.Tk()

canvas = tk.Canvas(root, width=400, height=400, background="green")
xsb = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
ysb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
canvas.configure(scrollregion=(0,0,1000,1000))

xsb.grid(row=1, column=0, sticky="ew")
ysb.grid(row=0, column=1, sticky="ns")
canvas.grid(row=0, column=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)





# Это то, что позволяет использовать мышь
canvas.bind("<ButtonPress-1>", lambda event: move_start(event))
canvas.bind("<B1-Motion>", lambda event:move_move(event))
canvas.bind("<MouseWheel>",lambda event:zoomer(event))

def move_start(event):
    canvas.scan_mark(event.x, event.y)
    
def move_move(event):
    canvas.scan_dragto(event.x, event.y, gain=1)

def zoomer(event):
    true_x = canvas.canvasx(event.x)
    true_y = canvas.canvasy(event.y)    
    if (event.delta > 0):
        canvas.scale("all", true_x, true_y, 1.1, 1.1)
    elif (event.delta < 0):
        canvas.scale("all", true_x, true_y, 0.9, 0.9)
    canvas.configure(scrollregion = canvas.bbox("all"))



























root.mainloop()








