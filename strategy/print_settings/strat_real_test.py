import customtkinter
from tkinter import messagebox
import models.real_test_trade as real

import strategy.strategys.strat_1 as str_1
import strategy.strategys.strat_2 as str_2

# валидация инпутов настроек стратегии 1
def strat1_param():
    if frame_2_set4_3_set_3.get()=='': 
        messagebox.showinfo('Внимание','Введите верх канала')
    elif frame_2_set4_3_set_4.get()=='': 
        messagebox.showinfo('Внимание','Введите низ канала')
    elif frame_2_set4_4_set_1.get()=='': 
        messagebox.showinfo('Внимание','Введите угол тренда лонг')
    elif frame_2_set4_4_set_2.get()=='': 
        messagebox.showinfo('Внимание','Введите угол тренда шорт')
    else:
        str_1.CANAL_MAX = float(float(frame_2_set4_3_set_3.get())/100)
        str_1.CANAL_MIN = float(float(frame_2_set4_3_set_4.get())/100)
        str_1.CORNER_LONG = int(frame_2_set4_4_set_1.get())
        str_1.CORNER_SHORT = int(frame_2_set4_4_set_2.get())
        return [real.COMMISSION_MAKER,real.COMMISSION_TAKER,real.TP,real.SL,real.DEPOSIT,real.LEVERAGE,str_1.CANAL_MAX,str_1.CANAL_MIN,str_1.CORNER_LONG,str_1.CORNER_SHORT,real.CANDLE_COIN_MIN,real.CANDLE_COIN_MAX]
        
# валидация инпутов настроек стратегии 2 
def strat2_param():
    if frame_2_set4_4_set_133.get()=='': 
        messagebox.showinfo('Внимание','Введите коэфициент основной скользящей средней')
    elif frame_2_set4_4_set_12.get()=='': 
        messagebox.showinfo('Внимание','Введите коэфициент медленной скользящей средней')
    else:
        str_2.MIDDLE_1 = int(frame_2_set4_4_set_133.get())
        str_2.MIDDLE_2 = int(frame_2_set4_4_set_12.get())
        return [real.COMMISSION_MAKER,real.COMMISSION_TAKER,real.TP,real.SL,real.DEPOSIT,real.LEVERAGE,str_2.MIDDLE_1,str_2.MIDDLE_2,real.CANDLE_COIN_MIN,real.CANDLE_COIN_MAX]

# отрисовка настреок стратегии 1
def strat1(frame):
    global frame_2_set4_3_set_3
    global frame_2_set4_3_set_4
    global frame_2_set4_4_set_1
    global frame_2_set4_4_set_2
    label_title112 = customtkinter.CTkLabel(frame, text="Настройки стартегии 'Канал, тренд, локаль, объём'", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    frame_2_strat_1= customtkinter.CTkFrame(frame, corner_radius=10, fg_color="#2B2B2B")
    label__2_set4_2_set_1_title = customtkinter.CTkLabel(frame_2_strat_1, text="Канал, тренд, локаль, объём", fg_color="transparent",anchor='center',font=('Arial',15,'bold'))
    frame_2_set4_3 = customtkinter.CTkFrame(frame_2_strat_1, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_4 = customtkinter.CTkFrame(frame_2_strat_1, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_3_set_3 = customtkinter.CTkEntry(frame_2_set4_3, placeholder_text="85",justify="center")
    frame_2_set4_3_set_4 = customtkinter.CTkEntry(frame_2_set4_3, placeholder_text="15",justify="center")
    label__2_set4_3_set_3 = customtkinter.CTkLabel(frame_2_set4_3, text="Верх канала, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_3_set_4 = customtkinter.CTkLabel(frame_2_set4_3, text="Низ канала, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    frame_2_set4_4_set_1 = customtkinter.CTkEntry(frame_2_set4_4, placeholder_text="10",justify="center")
    frame_2_set4_4_set_2 = customtkinter.CTkEntry(frame_2_set4_4, placeholder_text="10",justify="center")
    label__2_set4_4_set_1 = customtkinter.CTkLabel(frame_2_set4_4, text="Угол тренда лонг", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_4_set_2 = customtkinter.CTkLabel(frame_2_set4_4, text="Угол тренда шорт", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    frame_2_set4_3_set_3.insert(0, round(str_1.CANAL_MAX*100,3))
    frame_2_set4_3_set_4.insert(0, round(str_1.CANAL_MIN*100,3))
    frame_2_set4_4_set_1.insert(0, str_1.CORNER_LONG)
    frame_2_set4_4_set_2.insert(0, str_1.CORNER_SHORT)

    label_title112.pack(pady=0, anchor='n')
    frame_2_strat_1.pack(pady=20, anchor='n')
    label__2_set4_2_set_1_title.grid(row=0, column=0, sticky="ew",padx=10,columnspan = 3,pady=10)
    frame_2_set4_3.grid(row=1, column=1, sticky="ew",padx=10)
    frame_2_set4_4.grid(row=1, column=2, sticky="ew",padx=10,pady=[16,0])
    label__2_set4_3_set_3.pack(pady=1)
    frame_2_set4_3_set_3.pack(pady=1)
    label__2_set4_3_set_4.pack(pady=1)
    frame_2_set4_3_set_4.pack(pady=1)
    label__2_set4_4_set_1.pack(pady=1)
    frame_2_set4_4_set_1.pack(pady=1)
    label__2_set4_4_set_2.pack(pady=1)
    frame_2_set4_4_set_2.pack(pady=[1,20])

# отрисовка настреок стратегии 2
def strat2(frame):
    global frame_2_set4_4_set_133, frame_2_set4_4_set_12
    label_title112 = customtkinter.CTkLabel(frame, text="Настройки стартегии 'Скользящие средние'", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    frame_2_strat_1= customtkinter.CTkFrame(frame, corner_radius=10, fg_color="#2B2B2B")
    label__2_set4_3_set_4 = customtkinter.CTkLabel(frame_2_strat_1, text="Коэфициент основной скользящей средней", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    frame_2_set4_4_set_133 = customtkinter.CTkEntry(frame_2_strat_1, placeholder_text="6",justify="center")
    label__2_set4_3_set_42 = customtkinter.CTkLabel(frame_2_strat_1, text="Коэфициент медленной скользящей средней", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    frame_2_set4_4_set_12 = customtkinter.CTkEntry(frame_2_strat_1, placeholder_text="12",justify="center")
    
    frame_2_set4_4_set_133.insert(0, str_2.MIDDLE_1)
    frame_2_set4_4_set_12.insert(0, str_2.MIDDLE_2)
    
    label_title112.pack(pady=0, anchor='n')
    frame_2_strat_1.pack(pady=20, anchor='n')
    label__2_set4_3_set_4.pack(pady=[20,0], anchor='n')
    frame_2_set4_4_set_133.pack(pady=0, anchor='n')
    label__2_set4_3_set_42.pack(pady=0,padx=20, anchor='n')
    frame_2_set4_4_set_12.pack(pady=[0,20], anchor='n')