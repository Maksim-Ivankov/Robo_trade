import customtkinter
import time
import requests
import pandas as pd
from tkinter import *
import tkinter as tk
from datetime import datetime
import os   
import sys
sys.path.insert(1,os.path.join(sys.path[0],'../../../'))
import asyncio
import websockets
import json
import threading
from CTkTable import *
from binance.um_futures import UMFutures


key = 'QIT80MTFskjHSr82dtsteA6bG01CUeODQCg65KoYaQ5LmPcSpYDzyv1Oa7fugW3m'
secret = 'uMLo0WdaCv5FHBauV8QI4LZoDgmmVFf5Jd8TboKYRxHnHx6pmNrhg5bmdBgO54xI'


value_get_data = 180


client = UMFutures(key=key, secret=secret)

# первичные настройки окна
def settings_window():
    global win
    win = customtkinter.CTk()
    win.title("Robo_trade")
    w = 1020
    h = 800
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))    
    # выстраиваем сетку гридов
    win.grid_rowconfigure(0, weight=1)
    win.grid_columnconfigure(1, weight=1)
settings_window()


def pump_graph(frame):    
    global value_pump_today
    global value_pump_now
    global value_pump_30_day
    global frame_table_pump_now
    global frame_table_pump_today
    global frame_table_pump_30_day
    
    frame_pump_our = customtkinter.CTkFrame(frame, corner_radius=0, fg_color="transparent")
    
    # сейчас
    frame_pump_now = customtkinter.CTkFrame(frame_pump_our, corner_radius=0)
    label_title1_1_now = customtkinter.CTkLabel(frame_pump_now, text="Вероятность пампов", fg_color="transparent",anchor='center',font=('Arial',16,'normal'), width = 600)
    frame_table_pump_now = customtkinter.CTkFrame(frame_pump_now, corner_radius=0)
    value_pump_now = [['Монета','Вероятность пампа %','% за сегодня']]
    table_pump_now = CTkTable(master=frame_table_pump_now, row=1, column=3, values=value_pump_now)
    table_pump_now.pack(expand=True, padx=20, pady=20)
    frame_pump_now.pack(pady=0)
    label_title1_1_now.pack()
    frame_table_pump_now.pack()
    
    # за 24 часа
    frame_pump_today = customtkinter.CTkFrame(frame_pump_our, corner_radius=0)
    label_title1_1_today = customtkinter.CTkLabel(frame_pump_today, text="Пампы за 24 часа", fg_color="transparent",anchor='center',font=('Arial',16,'normal'), width = 600)
    frame_table_pump_today = customtkinter.CTkFrame(frame_pump_today, corner_radius=0)
    value_pump_today = [['Монета','% роста','Время начала','Длительность']]
    table_pump_today = CTkTable(master=frame_table_pump_today, row=1, column=4, values=value_pump_today)
    table_pump_today.pack(expand=True, padx=20, pady=20)
    frame_pump_today.pack(pady=20)
    label_title1_1_today.pack()
    frame_table_pump_today.pack()
    
    # за 30 дней
    frame_pump_30_day = customtkinter.CTkScrollableFrame(frame_pump_our, corner_radius=0, width=700, height=300)
    label_title1_1_30_day = customtkinter.CTkLabel(frame_pump_30_day, text="Пампы за 30 дней", fg_color="transparent",anchor='center',font=('Arial',16,'normal'), width = 600)
    frame_table_pump_30_day = customtkinter.CTkFrame(frame_pump_30_day, corner_radius=0)
    value_pump_30_day = [['№','Дата','Монета','% роста','Время начала','Длительность']]
    table_pump_30_day = CTkTable(master=frame_table_pump_30_day, row=1, column=6, values=value_pump_30_day)
    table_pump_30_day.pack(expand=True, fill="both", padx=20, pady=20)
    frame_pump_30_day.pack(pady=0)
    label_title1_1_30_day.pack()
    frame_table_pump_30_day.pack()
    
    
    frame_pump_our.pack(pady=[100,0])
    print('Орисовали графику')
    thread226 = threading.Thread(target=lambda:search_pump())
    thread226.start()

# здесь ищем и отрисовываем все пампы, что находим
def search_pump():
    top_coin = get_top_coin()
    count_coin = 0
    print(len(top_coin))
    number_row_table_today = 1
    number_row_table_30_day = 1
    try:
        for key in top_coin:
            count_coin = count_coin+1
            flag_pump = 0
            print(f'Обработано {count_coin}/{len(top_coin)}')
            df = get_futures_klines(key)
            for index, row in df.iterrows ():
                if index == (value_get_data-1): break
                if index != 0:
                    # если вторая свеча больше первой больше чем в 2 раза
                    if float(row['VOLUME'])/float(df['VOLUME'][index-1]) > 2:
                        # если третья свеча больше чем вторая больше чем в 2.5 раза
                        if float(df['VOLUME'][index+1])/float(row['VOLUME']) > 2.5:
                            flag_pump=1
                            
                            # print(f'ПАМП 30 дней - монета {key}|{index}')
                            value_pump_30_day.append([number_row_table_30_day,datetime.fromtimestamp(int(df['open_time'][index+1]/1000)).strftime('%d.%m.%Y'),key,top_coin[key],datetime.fromtimestamp(int((df['open_time'][index+1]/1000)-10800)).strftime('%H:%M'),'???'])
                            clean_card_menu(frame_table_pump_30_day)
                            number_row_table_30_day = number_row_table_30_day + 1
                            table_pump_30_day = CTkTable(master=frame_table_pump_30_day, row=number_row_table_30_day, column=6, values=value_pump_30_day)
                            table_pump_30_day.pack(expand=True, padx=20, pady=20) 
                            # если нашли памп в последних 6 свечах
                            if index > (value_get_data-6):
                                number_row_table_today = number_row_table_today + 1
                                # print(f'ПАМП 24 часа - монета {key}|{index}')
                                value_pump_today.append([key,top_coin[key],datetime.fromtimestamp(int((df['open_time'][index+1]/1000)-10800)).strftime('%H:%M'),'???'])
                                clean_card_menu(frame_table_pump_today)
                                table_pump_today = CTkTable(master=frame_table_pump_today, row=number_row_table_today, column=4, values=value_pump_today)
                                table_pump_today.pack(expand=True, padx=20, pady=20) 
            if flag_pump == 0:
                # print(f'Монета {key} - нет пампа')
                pass           
            time.sleep(1)
    except Exception as e:
        print(f'Ошибка работы цикла пампов - {e}') 

# Получите последние n свечей по n минут для торговой пары, обрабатываем и записывае данные в датафрейм
def get_futures_klines(symbol,TF='4h',VOLUME=value_get_data):
    try:
        time.sleep(2)
        x = requests.get('https://fapi.binance.com/fapi/v1/klines?symbol='+symbol.lower()+'&limit='+str(VOLUME)+'&interval='+TF)
        df=pd.DataFrame(x.json())
        df.columns=['open_time','open','high','low','close','VOLUME','close_time','d1','d2','d3','d4','d5']
        df=df.drop(['d1','d2','d3','d4','d5'],axis=1)
        df['open']=df['open'].astype(float)
        df['high']=df['high'].astype(float)
        df['low']=df['low'].astype(float)
        df['close']=df['close'].astype(float)
        df['VOLUME']=df['VOLUME'].astype(float)
        return(df) # возвращаем датафрейм с подготовленными данными
    except Exception as e:
        print(e)

# Получаем активные монеты на бирже
def get_top_coin():
    print('Получаем монеты')
    try:
        how_mach_coin = 49
        data = client.ticker_24hr_price_change()
        change={}
        coin_max={}
        coin_min={}
        coin_mas1 = {}
        coin_mas2 = {}
        for i in data:
            change[i['symbol']] = float(i['priceChangePercent'])
        coin_max = dict(sorted(change.items(), key=lambda item: item[1],reverse=True))
        coin_min = dict(sorted(change.items(), key=lambda x: x[1]))
        i=0
        for key, value in coin_max.items():
            i=i+1
            coin_mas1[key] = value
            if i==1:
                coin_max_val = value
            # if i==int(how_mach_coin):
            #     break
        i=0
        for key, value in coin_min.items():
            i=i+1
            coin_mas2[key] = value
            if i==1:
                coin_min_val = value
            # if i== how_mach_coin:
            #     break
        print('Получили монеты')
        if abs(coin_max_val)>abs(coin_min_val):
            result = coin_mas1
        else:
            result = coin_mas2
        return result
    except Exception as e:
        print('Внимание','Ошибка получения активных монет с биржи')

# отчистка фрейма отрисовки
def clean_card_menu(frame):
    for widget in frame.winfo_children():
        widget.forget()

def get_save_df():
    MYDIR_WORKER = '../ROBO_TRADE/pump_str/DF/'
    df = pd.read_csv(f'{MYDIR_WORKER}{result}.csv')


print('Главный поток')
pump_graph(win)


win.mainloop()