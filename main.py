from imports import *
from models.model import *

# открываем по центру
win = customtkinter.CTk()
win.title("Robo_trade")
w = 1000
h = 800
ws = win.winfo_screenwidth()
hs = win.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
win.geometry('%dx%d+%d+%d' % (w, h, x, y))    
# выстраиваем сетку гридов
win.grid_rowconfigure(0, weight=1)
win.grid_columnconfigure(1, weight=1)

from component.UI.images.images import * # импорт всех картинок, которые используем здесь

#бработка нажатия по кнопкам
def home_button_event():
    select_frame_by_name("home")
def frame_2_button_event():
    select_frame_by_name("frame_2")
def frame_3_button_event():
    select_frame_by_name("frame_3")
def frame_4_button_event():
    select_frame_by_name("frame_4")
def frame_5_button_event():
    select_frame_by_name("frame_5")
def frame_6_button_event():
    select_frame_by_name("frame_6")
def frame_7_button_event():
    select_frame_by_name("frame_7")
def frame_8_button_event():
    select_frame_by_name("frame_8")
    
# создаем навигацию фреймов - фреймы и кнопки
navigation_frame = customtkinter.CTkFrame(win, corner_radius=0)
navigation_frame_label = customtkinter.CTkLabel(navigation_frame, text="Робо трейд", image=logo_image,compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
home_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Главная",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=home_image, anchor="w", command=home_button_event)
frame_2_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Историческая торговля",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=chat_image, anchor="w", command=frame_2_button_event)
frame_3_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Реальная тестовая торговля",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=add_user_image, anchor="w", command=frame_3_button_event)
frame_4_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Фьючерсы Binance",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=add_user_image, anchor="w", command=frame_4_button_event)
frame_5_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Торговый робот",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=add_user_image, anchor="w", command=frame_5_button_event)
frame_6_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Настройки робота",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=add_user_image, anchor="w", command=frame_6_button_event)
frame_7_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Профиль",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=add_user_image, anchor="w", command=frame_7_button_event)
frame_8_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Настройки программы",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=add_user_image, anchor="w", command=frame_8_button_event)
home_frame = customtkinter.CTkFrame(win, corner_radius=0, fg_color="transparent")
second_frame = customtkinter.CTkFrame(win, corner_radius=0, fg_color="transparent")
third_frame = customtkinter.CTkFrame(win, corner_radius=0, fg_color="transparent")
frame_4 = customtkinter.CTkFrame(win, corner_radius=0, fg_color="transparent")
frame_5 = customtkinter.CTkFrame(win, corner_radius=0, fg_color="transparent")
frame_6 = customtkinter.CTkFrame(win, corner_radius=0, fg_color="transparent")
frame_7 = customtkinter.CTkFrame(win, corner_radius=0, fg_color="transparent")
frame_8 = customtkinter.CTkFrame(win, corner_radius=0, fg_color="transparent")
frame_loading = customtkinter.CTkFrame(win, corner_radius=0, fg_color="transparent")


#рисуем навигацию и фреймы
navigation_frame.grid(row=0, column=0, sticky="nsew")
navigation_frame.grid_rowconfigure(9, weight=1)
navigation_frame_label.grid(row=0, column=0, padx=0, pady=20)
home_button.grid(row=1, column=0, sticky="ew")
frame_2_button.grid(row=2, column=0, sticky="ew")
frame_3_button.grid(row=3, column=0, sticky="ew")
frame_4_button.grid(row=4, column=0, sticky="ew")
frame_5_button.grid(row=5, column=0, sticky="ew")
frame_6_button.grid(row=6, column=0, sticky="ew")
frame_7_button.grid(row=7, column=0, sticky="ew")
frame_8_button.grid(row=8, column=0, sticky="ew")

def select_frame_by_name(name): #выбирает и открывает фрейм
    home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
    frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
    frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
    frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
    frame_5_button.configure(fg_color=("gray75", "gray25") if name == "frame_5" else "transparent")
    frame_6_button.configure(fg_color=("gray75", "gray25") if name == "frame_6" else "transparent")
    frame_7_button.configure(fg_color=("gray75", "gray25") if name == "frame_7" else "transparent")
    frame_8_button.configure(fg_color=("gray75", "gray25") if name == "frame_8" else "transparent")
    # показать выбранный фрейм
    if name == "home":
        home_frame.grid(row=0, column=1, sticky="nsew")
    else:
        home_frame.grid_forget()
    if name == "frame_2":
        second_frame.grid(row=0, column=1, sticky="nsew")
    else:
        second_frame.grid_forget()
    if name == "frame_3":
        third_frame.grid(row=0, column=1, sticky="nsew")
    else:
        third_frame.grid_forget()
    if name == "frame_4":
        frame_4.grid(row=0, column=1, sticky="nsew")
    else:
        frame_4.grid_forget()
    if name == "frame_5":
        frame_5.grid(row=0, column=1, sticky="nsew")
    else:
        frame_5.grid_forget()
    if name == "frame_6":
        frame_6.grid(row=0, column=1, sticky="nsew")
    else:
        frame_6.grid_forget()
    if name == "frame_7":
        frame_7.grid(row=0, column=1, sticky="nsew")
    else:
        frame_7.grid_forget()
    if name == "frame_8":
        frame_8.grid(row=0, column=1, sticky="nsew")
    else:
        frame_8.grid_forget()
        
        

        # создаем страницы фреймов

select_frame_by_name("home")
        

# frame_8.grid_rowconfigure(0, weight=1)
frame_8.grid_columnconfigure(0, weight=2)

# НАСТРОЙКИ ПРОГРАММЫ
def change_appearance_mode_event(new_appearance_mode):
    customtkinter.set_appearance_mode(new_appearance_mode)
def settings_prog():
    
    label_title1 = customtkinter.CTkLabel(frame_8, text="Настройки программы", fg_color="transparent",anchor='center',font=('Arial',20,'bold'))
    frame_8_set = customtkinter.CTkFrame(frame_8, corner_radius=0, fg_color="transparent")
    label_title2 = customtkinter.CTkLabel(frame_8_set, text="Оформление программы", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    appearance_mode_menu = customtkinter.CTkOptionMenu(frame_8_set, values=["Dark", "Light", "System"],command=change_appearance_mode_event)
    label_title1.pack(pady=20)
    frame_8_set.pack()
    label_title2.grid(row=0, column=0, sticky="ew",padx=20)
    appearance_mode_menu.grid(row=0, column=1, sticky="ew")

# ПРОФИЛЬ
def profile():
    label_title1 = customtkinter.CTkLabel(frame_7, text="Профиль", fg_color="transparent",anchor='center',font=('Arial',20,'bold'))
    frame_7_set1 = customtkinter.CTkFrame(frame_7, corner_radius=10, fg_color="#2B2B2B")
    label_title2 = customtkinter.CTkLabel(frame_7_set1, text="Логин", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    label_title3 = customtkinter.CTkLabel(frame_7_set1, text=NAME, fg_color="transparent", text_color='#1F6AA5',anchor='center',font=('Arial',14,'normal'))
    label_title4 = customtkinter.CTkLabel(frame_7_set1, text="Ключ шифрования", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    label_title5 = customtkinter.CTkLabel(frame_7_set1, text=API_KEY, fg_color="transparent", text_color='#1F6AA5',anchor='center',font=('Arial',14,'normal'))
    label_title6 = customtkinter.CTkLabel(frame_7_set1, text="Email", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    label_title7 = customtkinter.CTkLabel(frame_7_set1, text='MaksimIvankov26@yandex.ru', fg_color="transparent", text_color='#1F6AA5',anchor='center',font=('Arial',14,'normal'))
    frame_7_set2 = customtkinter.CTkScrollableFrame(frame_7, corner_radius=10, fg_color="#2B2B2B", orientation='horizontal', width=600, height=140)
    label_title8 = customtkinter.CTkLabel(frame_7_set2, text="API_KEY_BINANCE", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    label_title9 = customtkinter.CTkLabel(frame_7_set2, text=key, fg_color="transparent", text_color='#1F6AA5',anchor='center',font=('Arial',14,'normal'))
    label_title10 = customtkinter.CTkLabel(frame_7_set2, text="API_SECRET_KEY_BINANCE", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    label_title11 = customtkinter.CTkLabel(frame_7_set2, text=secret, fg_color="transparent", text_color='#1F6AA5',anchor='center',font=('Arial',14,'normal'))
    label_title12 = customtkinter.CTkLabel(frame_7_set2, text="API_KEY_TELEGRAM", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    label_title13 = customtkinter.CTkLabel(frame_7_set2, text=TG_API, fg_color="transparent", text_color='#1F6AA5',anchor='center',font=('Arial',14,'normal'))
    label_title14 = customtkinter.CTkLabel(frame_7_set2, text="ID_TELEGRAM", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    label_title15 = customtkinter.CTkLabel(frame_7_set2, text=TG_ID, fg_color="transparent", text_color='#1F6AA5',anchor='center',font=('Arial',14,'normal'))

    label_title1.pack(pady=20)
    frame_7_set1.pack(pady=10)
    label_title2.grid(row=0, column=0, sticky="w",padx=20)
    label_title3.grid(row=0, column=1, sticky="w",padx=20)
    label_title4.grid(row=1, column=0, sticky="w",padx=20)
    label_title5.grid(row=1, column=1, sticky="w",padx=20)
    label_title6.grid(row=2, column=0, sticky="w",padx=20)
    label_title7.grid(row=2, column=1, sticky="w",padx=20)
    frame_7_set2.pack(pady=10,padx=20)
    label_title8.grid(row=0, column=0, sticky="w",padx=20)
    label_title9.grid(row=0, column=1, sticky="w",padx=20)
    label_title10.grid(row=1, column=0, sticky="w",padx=20)
    label_title11.grid(row=1, column=1, sticky="w",padx=20)
    label_title12.grid(row=2, column=0, sticky="w",padx=20)
    label_title13.grid(row=2, column=1, sticky="w",padx=20)
    label_title14.grid(row=3, column=0, sticky="w",padx=20)
    label_title15.grid(row=3, column=1, sticky="w",padx=20)

# ИСТОРИЧЕСКАЯ ТОРГОВЛЯ

set1_timveframe = {"5m":5, "15m":15, "30m":30, "1h":60}
set1_time = {"12 часов":720, "24 часа":1440, "2 дня":2880, "3 дня":4320}
TF = '5m'
VOLUME = 144
DEPOSIT = 100
Leverage = 20
wait_time = int(set1_timveframe.get(TF))
coin_mas_10 = []
def get_setting_timeframe(data):
    global TF
    global VOLUME
    timeframe = set1_timveframe.get(TF)
    time = set1_time.get("12 часов")
    VOLUME = int(time/timeframe)
    TF = data
def get_setting_time(data):
    global VOLUME
    timeframe = set1_timveframe.get(TF)
    time = set1_time.get(data)
    VOLUME = int(time/timeframe)
def is_loading():
    frame_loading.grid(row=0, column=1, sticky="nsew")
    customtkinter.CTkLabel(frame_loading, text="Загрузка данных", fg_color="transparent",anchor='center',justify='center',font=('Arial',20,'bold')).pack(pady=20)

def get_dataframe_with_binance(frame_2_set2_2_1):
    is_loading()
    print('лоло')
    # thread = threading.Thread(target=print(generate_dataframe(TF,VOLUME,wait_time)))
    # thread.start()
    # print('УСПЕХ!!!!!')
    # file = open('../ROBO_TRADE/DF/coin.txt', mode="r")
    # coin_mas_10 = file.read().split('|')
    # i=-1
    # for coin in coin_mas_10:
    #     i=i+1
    #     customtkinter.CTkButton(frame_2_set2_2_1, text=coin).grid(row=i, column=0, sticky="ew",pady=5)
def historical_trade():
    label_title1 = customtkinter.CTkLabel(second_frame, text="Торговля по историческим данным", fg_color="transparent",anchor='center',font=('Arial',20,'bold'))
    frame_2_set1 = customtkinter.CTkFrame(second_frame, corner_radius=10, fg_color="transparent")
    button1 = customtkinter.CTkButton(frame_2_set1, text="Информация")
    button2 = customtkinter.CTkButton(frame_2_set1, text="Инструкция")
    button3 = customtkinter.CTkButton(frame_2_set1, text="История торгов")
    frame_2_set2 = customtkinter.CTkFrame(second_frame, corner_radius=10, fg_color="#2B2B2B")
    frame_2_set2_1 = customtkinter.CTkFrame(frame_2_set2, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set2_2 = customtkinter.CTkFrame(frame_2_set2, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set2_3 = customtkinter.CTkFrame(frame_2_set2, corner_radius=0, fg_color="#2B2B2B")
    #----
    label_title1_1 = customtkinter.CTkLabel(frame_2_set2_1, text="Сбор данных", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    label_title1_1_1 = customtkinter.CTkLabel(frame_2_set2_1, text="Таймфрейм", fg_color="transparent",anchor='center',font=('Arial',12,'normal'))
    appearance_mode_menu1 = customtkinter.CTkOptionMenu(frame_2_set2_1, values=["5m", "15m", "30m", "1h"],command=get_setting_timeframe)
    label_title1_1_2 = customtkinter.CTkLabel(frame_2_set2_1, text="Длительность", fg_color="transparent",anchor='center',font=('Arial',12,'normal'))
    appearance_mode_menu2 = customtkinter.CTkOptionMenu(frame_2_set2_1, values=["12 часов", "24 часа", "2 дня", "3 дня"],command=get_setting_time)
    button4 = customtkinter.CTkButton(frame_2_set2_1, text="Получить данные", command=lambda:get_dataframe_with_binance(frame_2_set2_2_1))
    #----
    label_title1_2 = customtkinter.CTkLabel(frame_2_set2_2, text="Монеты роста/падения", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    frame_2_set2_2_1 = customtkinter.CTkScrollableFrame(frame_2_set2_2, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=20, height=50)
    
    
    # ----
    label_title1_3_1 = customtkinter.CTkLabel(frame_2_set2_3, text="Датасет с биржи Binance", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    label_title1_3_2 = customtkinter.CTkLabel(frame_2_set2_3, text="                                         ", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    frame_2_set2_3_1 = customtkinter.CTkScrollableFrame(frame_2_set2_3, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=200, height=50)
    
    label_title1.pack(pady=20)
    frame_2_set1.pack(pady=10)
    button1.grid(row=0, column=0, sticky="ew",padx=10)
    button2.grid(row=0, column=1, sticky="ew",padx=10)
    button3.grid(row=0, column=2, sticky="ew",padx=10)
    frame_2_set2.pack(pady=10)
    frame_2_set2_1.grid(row=0, column=1, sticky="ew",padx=10)
    frame_2_set2_2.grid(row=0, column=2, sticky="ew",padx=10)
    frame_2_set2_3.grid(row=0, column=3, sticky="ew",padx=10,columnspan = 2)
    label_title1_1.grid(row=0, column=0, sticky="ew")
    label_title1_1_1.grid(row=1, column=0, sticky="ew")
    appearance_mode_menu1.grid(row=2, column=0, sticky="ew",pady=[0,10])
    label_title1_1_2.grid(row=3, column=0, sticky="ew")
    appearance_mode_menu2.grid(row=4, column=0, sticky="ew",pady=[0,10])
    button4.grid(row=5, column=0, sticky="ew",pady=10,padx=20)
    label_title1_2.grid(row=0, column=0, sticky="ew",pady=10)
    frame_2_set2_2_1.grid(row=1, column=0, sticky="ew",pady=[0,20])
    label_title1_3_1.grid(row=0, column=0, sticky="ew",pady=10)
    label_title1_3_2.grid(row=0, column=1, sticky="ew",pady=10)
    frame_2_set2_3_1.grid(row=1, column=0, columnspan=2, sticky="ew",pady=[0,20])
    


historical_trade()
settings_prog()
profile()

win.mainloop()