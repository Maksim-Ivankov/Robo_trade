import customtkinter
from PIL import Image
import os
from config import API_KEY,NAME
from main import *

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('blue')

# Центровка окна
app = customtkinter.CTk()
app.title("Robo_trade")
w = 350
h = 470
ws = app.winfo_screenwidth()
hs = app.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
app.geometry('%dx%d+%d+%d' % (w, h, x, y))

# обработка кнопки
def sign_in():
    name = input_name.get()
    api_key = input_api_key.get()
    if name == 'MIN':
        if api_key == 'Q9YG6hceTGDVqKqEDIgxKRGH9Gcb6LXVU3DNHjEjGrrdHcEzM6':
            print('входим')
            app.destroy()
            prog = App()
            prog.mainloop()
        else:
            input_name.configure(border_color="red",border_width=2)
            input_api_key.configure(border_color="red",border_width=2)
    else:
            input_name.configure(border_color="red",border_width=2)
            input_api_key.configure(border_color="red",border_width=2)

# создаем компоненты
image_path = os.path.join(os.path.dirname(__file__),'image/favicon.jpg')
image = customtkinter.CTkImage(light_image=Image.open(image_path),size=(216*1.53,110*1.53))
image_label = customtkinter.CTkLabel(app, image=image,text='')
image_label.place(x=10,y=10)
label_title = customtkinter.CTkLabel(app, text="Авторизация", fg_color="transparent",anchor='center',font=('Arial',20,'bold'))
label_input_name = customtkinter.CTkLabel(app, text="Введите логин", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
input_name = customtkinter.CTkEntry(app, placeholder_text="Pupkin",width=200,justify='center')
input_name.insert(0, NAME )
label_input_api_key = customtkinter.CTkLabel(app, text="Введите Api-key", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
input_api_key = customtkinter.CTkEntry(app, placeholder_text="Введите ключ",width=300,justify='center')
input_api_key.insert(0, API_KEY )
button_sign_in = customtkinter.CTkButton(app, text="Войти",command=sign_in)


# рисуем компоненты
label_title.pack(pady=[190,10])
label_input_name.pack(pady=10)
input_name.pack()
label_input_api_key.pack(pady=10)
input_api_key.pack()
button_sign_in.pack(pady=[20,0])

app.mainloop()