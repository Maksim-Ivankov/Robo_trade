import customtkinter
from tkinter import messagebox
import models.real_test_trade as real

def strat1_param(frame,step_4_real_test_trade,frame_2_set4_2_set_1,frame_2_set4_2_set_2,frame_2_set4_2_set_3,frame_2_set4_2_set_4,frame_2_set4_3_set_1,frame_2_set4_3_set_2,frame_2_set4_3_set_3,frame_2_set4_3_set_4,frame_2_set4_4_set_1,frame_2_set4_4_set_2,frame_2_set4_4_set_3,frame_2_set4_4_set_4):
    if frame_2_set4_2_set_1.get()=='': 
        messagebox.showinfo('Внимание','Введите комиссию мейкер')
    elif frame_2_set4_2_set_2.get()=='': 
        messagebox.showinfo('Внимание','Введите комиссию тейкер')
    elif frame_2_set4_2_set_3.get()=='': 
        messagebox.showinfo('Внимание','Введите тейк профит')
    elif frame_2_set4_2_set_4.get()=='': 
        messagebox.showinfo('Внимание','Введите cтоп лосс')
    elif frame_2_set4_3_set_1.get()=='': 
        messagebox.showinfo('Внимание','Введите депозит')
    elif frame_2_set4_3_set_2.get()=='': 
        messagebox.showinfo('Внимание','Введите плечо')
    elif frame_2_set4_3_set_3.get()=='': 
        messagebox.showinfo('Внимание','Введите верх канала')
    elif frame_2_set4_3_set_4.get()=='': 
        messagebox.showinfo('Внимание','Введите низ канала')
    elif frame_2_set4_4_set_1.get()=='': 
        messagebox.showinfo('Внимание','Введите угол тренда лонг')
    elif frame_2_set4_4_set_2.get()=='': 
        messagebox.showinfo('Внимание','Введите угол тренда шорт')
    elif frame_2_set4_4_set_3.get()=='': 
        messagebox.showinfo('Внимание','Введите объём торгов мин')
    elif frame_2_set4_4_set_4.get()=='': 
        messagebox.showinfo('Внимание','Введите объём торгов макс')
    else:
        real.COMMISSION_MAKER = float(float(frame_2_set4_2_set_1.get())/100)
        real.COMMISSION_TAKER = float(float(frame_2_set4_2_set_2.get())/100)
        real.TP = float(float(frame_2_set4_2_set_3.get())/100)
        real.SL = float(float(frame_2_set4_2_set_4.get())/100)
        real.DEPOSIT = int(frame_2_set4_3_set_1.get())
        real.LEVERAGE = int(frame_2_set4_3_set_2.get())
        real.CANAL_MAX = float(float(frame_2_set4_3_set_3.get())/100)
        real.CANAL_MIN = float(float(frame_2_set4_3_set_4.get())/100)
        real.CORNER_LONG = int(frame_2_set4_4_set_1.get())
        real.CORNER_SHORT = int(frame_2_set4_4_set_2.get())
        real.CANDLE_COIN_MIN = int(frame_2_set4_4_set_3.get())
        real.CANDLE_COIN_MAX = int(frame_2_set4_4_set_4.get())
        data_settings_1 = [real.COMMISSION_MAKER,real.COMMISSION_TAKER,real.TP,real.SL,real.DEPOSIT,real.LEVERAGE,real.CANAL_MAX,real.CANAL_MIN,real.CORNER_LONG,real.CORNER_SHORT,real.CANDLE_COIN_MIN,real.CANDLE_COIN_MAX]
        
        step_4_real_test_trade(frame,data_settings_1)



def strat1(frame,step_2_real_test_trade,step_4_real_test_trade):
    label_title112 = customtkinter.CTkLabel(frame, text="Настройте стратегии и запустите реальную тестовую торговлю", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    frame_2_strat_1= customtkinter.CTkFrame(frame, corner_radius=0, fg_color="#2B2B2B")
    label__2_set4_2_set_1_title = customtkinter.CTkLabel(frame_2_strat_1, text="Канал, тренд, локаль, объём", fg_color="transparent",anchor='center',font=('Arial',15,'bold'))
    frame_2_set4_2 = customtkinter.CTkFrame(frame_2_strat_1, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_3 = customtkinter.CTkFrame(frame_2_strat_1, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_4 = customtkinter.CTkFrame(frame_2_strat_1, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_2_set_1 = customtkinter.CTkEntry(frame_2_set4_2, placeholder_text="0.2",justify="center")
    frame_2_set4_2_set_2 = customtkinter.CTkEntry(frame_2_set4_2, placeholder_text="0.1",justify="center")
    frame_2_set4_2_set_3 = customtkinter.CTkEntry(frame_2_set4_2, placeholder_text="1.2",justify="center")
    frame_2_set4_2_set_4 = customtkinter.CTkEntry(frame_2_set4_2, placeholder_text="0.4",justify="center")
    label__2_set4_2_set_1 = customtkinter.CTkLabel(frame_2_set4_2, text="Комиссия мейкер, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_2_set_2 = customtkinter.CTkLabel(frame_2_set4_2, text="Комиссия тейкер, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_2_set_3 = customtkinter.CTkLabel(frame_2_set4_2, text="Тейк профит, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_2_set_4 = customtkinter.CTkLabel(frame_2_set4_2, text="Стоп лосс, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    frame_2_set4_3_set_1 = customtkinter.CTkEntry(frame_2_set4_3, placeholder_text="100",justify="center")
    frame_2_set4_3_set_2 = customtkinter.CTkEntry(frame_2_set4_3, placeholder_text="20",justify="center")
    frame_2_set4_3_set_3 = customtkinter.CTkEntry(frame_2_set4_3, placeholder_text="85",justify="center")
    frame_2_set4_3_set_4 = customtkinter.CTkEntry(frame_2_set4_3, placeholder_text="15",justify="center")
    label__2_set4_3_set_1 = customtkinter.CTkLabel(frame_2_set4_3, text="Деозит, $", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_3_set_2 = customtkinter.CTkLabel(frame_2_set4_3, text="Плечо", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_3_set_3 = customtkinter.CTkLabel(frame_2_set4_3, text="Верх канала, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_3_set_4 = customtkinter.CTkLabel(frame_2_set4_3, text="Низ канала, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    frame_2_set4_4_set_1 = customtkinter.CTkEntry(frame_2_set4_4, placeholder_text="10",justify="center")
    frame_2_set4_4_set_2 = customtkinter.CTkEntry(frame_2_set4_4, placeholder_text="10",justify="center")
    frame_2_set4_4_set_3 = customtkinter.CTkEntry(frame_2_set4_4, placeholder_text="200000",justify="center")
    frame_2_set4_4_set_4 = customtkinter.CTkEntry(frame_2_set4_4, placeholder_text="500000",justify="center")
    label__2_set4_4_set_1 = customtkinter.CTkLabel(frame_2_set4_4, text="Угол тренда лонг", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_4_set_2 = customtkinter.CTkLabel(frame_2_set4_4, text="Угол тренда шорт", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_4_set_3 = customtkinter.CTkLabel(frame_2_set4_4, text="Объём торгов мин", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_4_set_4 = customtkinter.CTkLabel(frame_2_set4_4, text="Объм торгов макс", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    frame_2_set412 = customtkinter.CTkFrame(frame, corner_radius=10, fg_color="transparent")
    button3212 = customtkinter.CTkButton(frame_2_set412, text="Назад",command=lambda:step_2_real_test_trade(frame))
    button3213 = customtkinter.CTkButton(frame_2_set412, text="Запустить торговлю",command=lambda:strat1_param(frame,step_4_real_test_trade,frame_2_set4_2_set_1,frame_2_set4_2_set_2,frame_2_set4_2_set_3,frame_2_set4_2_set_4,frame_2_set4_3_set_1,frame_2_set4_3_set_2,frame_2_set4_3_set_3,frame_2_set4_3_set_4,frame_2_set4_4_set_1,frame_2_set4_4_set_2,frame_2_set4_4_set_3,frame_2_set4_4_set_4))
    frame_2_set4_2_set_1.insert(0, round(real.COMMISSION_MAKER*100,3))
    frame_2_set4_2_set_2.insert(0, round(real.COMMISSION_TAKER*100,3))
    frame_2_set4_2_set_3.insert(0, round(real.TP*100,3))
    frame_2_set4_2_set_4.insert(0, round(real.SL*100,3))
    frame_2_set4_3_set_1.insert(0, real.DEPOSIT)
    frame_2_set4_3_set_2.insert(0, real.LEVERAGE)
    frame_2_set4_3_set_3.insert(0, round(real.CANAL_MAX*100,3))
    frame_2_set4_3_set_4.insert(0, round(real.CANAL_MIN*100,3))
    frame_2_set4_4_set_1.insert(0, real.CORNER_LONG)
    frame_2_set4_4_set_2.insert(0, real.CORNER_SHORT)
    frame_2_set4_4_set_3.insert(0, real.CANDLE_COIN_MIN)
    frame_2_set4_4_set_4.insert(0, real.CANDLE_COIN_MAX)
    
    
    label_title112.pack(pady=0, anchor='n')
    frame_2_strat_1.pack(pady=20, anchor='n')
    label__2_set4_2_set_1_title.grid(row=0, column=0, sticky="ew",padx=10,columnspan = 3,pady=10)
    frame_2_set4_2.grid(row=1, column=0, sticky="ew",padx=10)
    frame_2_set4_3.grid(row=1, column=1, sticky="ew",padx=10)
    frame_2_set4_4.grid(row=1, column=2, sticky="ew",padx=10)
    label__2_set4_2_set_1.pack(pady=1)
    frame_2_set4_2_set_1.pack(pady=1)
    label__2_set4_2_set_2.pack(pady=1)
    frame_2_set4_2_set_2.pack(pady=1)
    label__2_set4_2_set_3.pack(pady=1)
    frame_2_set4_2_set_3.pack(pady=1)
    label__2_set4_2_set_4.pack(pady=1)
    frame_2_set4_2_set_4.pack(pady=1)
    label__2_set4_3_set_1.pack(pady=1)
    frame_2_set4_3_set_1.pack(pady=1)
    label__2_set4_3_set_2.pack(pady=1)
    frame_2_set4_3_set_2.pack(pady=1)
    label__2_set4_3_set_3.pack(pady=1)
    frame_2_set4_3_set_3.pack(pady=1)
    label__2_set4_3_set_4.pack(pady=1)
    frame_2_set4_3_set_4.pack(pady=1)
    label__2_set4_4_set_1.pack(pady=1)
    frame_2_set4_4_set_1.pack(pady=1)
    label__2_set4_4_set_2.pack(pady=1)
    frame_2_set4_4_set_2.pack(pady=1)
    label__2_set4_4_set_3.pack(pady=1)
    frame_2_set4_4_set_3.pack(pady=1)
    label__2_set4_4_set_4.pack(pady=1)
    frame_2_set4_4_set_4.pack(pady=20)
    frame_2_set412.pack(pady=20, anchor='n')
    button3212.grid(row=0, column=0, sticky="ew",padx=10)
    button3213.grid(row=0, column=1, sticky="ew",padx=10)
    # button6 = customtkinter.CTkButton(frame_2_strat_1, text="Запустить торговлю")
    # button6 = customtkinter.CTkButton(frame_2_strat_1, text="Запустить торговлю",command=lambda:start_historical_trade_strat_1(frame_2_set2_graph,frame_3_set4_1_2,frame_3_set4_1_1_1,frame_2_set4_2_set_1,frame_2_set4_2_set_2,frame_2_set4_2_set_3,frame_2_set4_2_set_4,frame_2_set4_3_set_1,frame_2_set4_3_set_2,frame_2_set4_3_set_3,frame_2_set4_3_set_4,frame_2_set4_4_set_1,frame_2_set4_4_set_2,frame_2_set4_4_set_3,frame_2_set4_4_set_4))
    # button6.grid(row=1, column=1, sticky="ew",padx=10,pady=15)
    