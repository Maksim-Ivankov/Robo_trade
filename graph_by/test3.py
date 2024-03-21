from tkinter import *

current = None

width_line = 6
color_line = 'blue'
active_color_line='red'



def main():
    global canvas
    root = Tk()
    canvas = Canvas(root, width=600, height=600, bg='white')
    canvas.pack()
    main_crate_line(canvas)
    root.mainloop()
    
    
# точка входа в рисунок линией
def main_crate_line(canvas):
    canvas.tag_click = False # чтобы при нажатии на линию не начинать рисовать новую
    canvas.bind("<Motion>", motion) # благодаря этому линия тянется от точки нажатия, без - просто тепается
    canvas.bind("<ButtonPress-1>", Mousedown)
    
def Mousedown(event):
    global current
    global flag
    event.widget.focus_set()  # таким образом, клавиша escape будет работать
    if current is None:
        # if event.widget.tag_click:
        #     event.widget.tag_click = False
        #     return
        # новая строка начинается с того места, где пользователь нажал
        x0 = event.x
        y0 = event.y
        print('1 нажатие')
        flag = 1
        current = event.widget.create_line(x0, y0, event.x, event.y,width=width_line,fill=color_line)
        return
    if flag == 1:
        print('2 нажатие')
        coords = event.widget.coords(current)
        x0 = coords[2]
        y0 = coords[3]
        current = event.widget.create_line(x0, y0, event.x, event.y,width=width_line,fill=color_line)
        flag = 0
        current = None
        
def motion(event):
    if current:
        coords = event.widget.coords(current)
        coords[2] = event.x
        coords[3] = event.y
        event.widget.coords(current, *coords)
        
main()



