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
import itertools

key = 'QIT80MTFskjHSr82dtsteA6bG01CUeODQCg65KoYaQ5LmPcSpYDzyv1Oa7fugW3m'
secret = 'uMLo0WdaCv5FHBauV8QI4LZoDgmmVFf5Jd8TboKYRxHnHx6pmNrhg5bmdBgO54xI'


value_get_data = 480 # 40 часов


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
# settings_window()

# точка входа
def pump_graph():    
    global value_pump_today,dop_data_row_30_daya,dop_data_row_today
    # global value_pump_now
    global value_pump_30_day
    # global frame_table_pump_now
    # global frame_table_pump_today
    # global frame_table_pump_30_day
    
    # frame_pump_our = customtkinter.CTkFrame(frame, corner_radius=0, fg_color="transparent")
    
    # # сейчас
    # frame_pump_now = customtkinter.CTkFrame(frame_pump_our, corner_radius=0)
    # label_title1_1_now = customtkinter.CTkLabel(frame_pump_now, text="Вероятность пампов", fg_color="transparent",anchor='center',font=('Arial',16,'normal'), width = 600)
    # frame_table_pump_now = customtkinter.CTkFrame(frame_pump_now, corner_radius=0)
    # value_pump_now = [['Монета','Вероятность пампа %','% за сегодня']]
    # table_pump_now = CTkTable(master=frame_table_pump_now, row=1, column=3, values=value_pump_now)
    # table_pump_now.pack(expand=True, padx=20, pady=20)
    # frame_pump_now.pack(pady=0)
    # label_title1_1_now.pack()
    # frame_table_pump_now.pack()
    
    # # за 24 часа
    # frame_pump_today_wrap = customtkinter.CTkFrame(frame_pump_our, corner_radius=0)
    # label_title1_1_today = customtkinter.CTkLabel(frame_pump_today_wrap, text="Пампы за 24 часа", fg_color="transparent",anchor='center',font=('Arial',16,'normal'), width = 600)
    # frame_pump_today = customtkinter.CTkScrollableFrame(frame_pump_today_wrap, corner_radius=0, width=700, height=120)
    # frame_table_pump_today = customtkinter.CTkFrame(frame_pump_today, corner_radius=0)
    value_pump_today = [['№','Монета','% роста','Время начала','Длительность']]
    # table_pump_today = CTkTable(master=frame_table_pump_today, row=1, column=4, values=value_pump_today)
    # table_pump_today.pack(expand=True, padx=20, pady=20)
    # frame_pump_today_wrap.pack(pady=20)
    # label_title1_1_today.pack()
    # frame_pump_today.pack()
    # frame_table_pump_today.pack()
    
    # # за 30 дней
    # frame_pump_30_day_wrap = customtkinter.CTkFrame(frame_pump_our, corner_radius=0)
    # label_title1_1_30_day = customtkinter.CTkLabel(frame_pump_30_day_wrap, text="Пампы за 30 дней", fg_color="transparent",anchor='center',font=('Arial',16,'normal'), width = 600)
    # frame_pump_30_day = customtkinter.CTkScrollableFrame(frame_pump_30_day_wrap, corner_radius=0, width=700, height=300)
    # frame_table_pump_30_day = customtkinter.CTkFrame(frame_pump_30_day, corner_radius=0)
    value_pump_30_day = [['№','Дата','Монета','% роста','Время начала','Объём, млн']]
    # table_pump_30_day = CTkTable(master=frame_table_pump_30_day, row=1, column=6, values=value_pump_30_day)
    # table_pump_30_day.pack(expand=True, fill="both", padx=20, pady=20)
    # frame_pump_30_day_wrap.pack()
    # label_title1_1_30_day.pack()
    # frame_pump_30_day.pack(pady=0)
    # frame_table_pump_30_day.pack()
    
    
    # frame_pump_our.pack(pady=[100,0])
    # print('Орисовали графику')
    
    for i,val in enumerate(sett):
        # logger('pump_5min',f'{i+1}/{len(sett)}-----------------------------------------------------------------')
        # logger('pump_5min',f'Настройки - | {val[0]} | {val[1]} | {val[2]} | {val[3]} | {val[4]}')
        search_pump(i,val[0],val[1],val[2],val[3],val[4])
        dop_data_row_30_daya.clear()
        dop_data_row_today.clear()
        value_pump_today[:] = []
        value_pump_30_day[:] = []
        value_pump_today = [['№','Монета','% роста','Время начала','Длительность']]
        value_pump_30_day = [['№','Дата','Монета','% роста','Время начала','Объём, млн']]
        
        
    # thread226 = threading.Thread(target=lambda:search_pump(settings_1,settings_2,settings_3,settings_4,settings_5))
    # thread226.start()

dop_data_row_30_daya = {}
dop_data_row_today = {}

#Логер в файлы
def logger(name_log,msg):
    path = name_log+'_log.txt'
    f = open(path,'a',encoding='utf-8')
    f.write('\n'+time.strftime("%d.%m.%Y | %H:%M:%S | ", time.localtime())+msg)
    f.close()

data = [1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2]

settings = list(itertools.combinations(data, 5))
sett = []

for i,val in enumerate(settings): 
    sett.append(list(val))
    sett.append(list(reversed(val)))


settings_1 = 0.8 # если вторая свеча больше первой больше чем в 2 раза
settings_2 = 2.2 # отношение шпилей к телу 3-ей свечи
settings_3 = 0.8 # объем 3 умноженного на 0.5 больше чем прошлые 10 объёмов по отдельности
settings_4 = 0.8 # если третья свеча больше чем вторая больше чем в n раз
settings_5 = 5 # только больше объема, млн
# -----------
# лучшее - 156/125 = 55%
# settings_1 = 0.8 # если вторая свеча больше первой больше чем в 2 раза
# settings_4 = 0.8 # если третья свеча больше чем вторая больше чем в n раз
# settings_2 = 1.8 # отношение шпилей к телу 3-ей свечи
# settings_3 = 0.8 # объем 3 умноженного на 0.5 больше чем прошлые 10 объёмов по отдельности
# settings_5 = 2 # только больше объема, млн
# -----------



# здесь ищем и отрисовываем все пампы, что находим
def search_pump(iter,settings_1,settings_2,settings_3,settings_4,settings_5):
    global dop_data_row_30_daya,dop_data_row_today
    global table_pump_30_day, table_pump_today
    global top_coin
    count_coin = 0
    number_row_table_today = 1
    number_row_table_30_day = 1
    
    for key in top_coin:
        count_coin = count_coin+1
        flag_pump = 0
        # print(f'Обработано {count_coin}/{len(top_coin)} | {key}')
        try:
            df = get_save_df(key)
        except Exception as e:
            time.sleep(1)
            print(f'В сейве монета не найдена - {e}')    
            df = get_futures_klines(key)
            write_save_df(df,key)
        if len(df) != value_get_data: 
            print('Новая монета, нет истории')
            continue
        index_flag_local = -1
        for index, row in df.iterrows():
            if index == (value_get_data-1): break
            if index_flag_local == index : continue
            if index > 9 and row['VOLUME'] != 0:
                
                # и чистим шпили по третей свече
                # и предидущие 10 по объёму не схожи с 3 свечой
                if (float(row['VOLUME'])/float(df['VOLUME'][index-1]) > settings_1 and  # если вторая свеча больше первой больше чем в 2 раза
                    float(row['open'])<float(row['close']) and # и свеча 2 зеленая
                    float(df['open'][index-1])<float(df['close'][index-1])  and # и свеча 1 зеленая
                    float(df['open'][index+1])<float(df['close'][index+1]) and # и свеча 3 зеленая
                    ((float(df['high'][index+1])-float(df['low'][index+1]))/(float(df['close'][index+1])-float(df['open'][index+1])))<settings_2 and # и отношение шпилей к телу меньше 2
                    float(df['VOLUME'][index+1])*settings_3>float(df['VOLUME'][index-2]) and # объем 3 умноженного на 0.5 больше чем прошлые 10 объёмов по отдельности
                    float(df['VOLUME'][index+1])*settings_3>float(df['VOLUME'][index-3]) and 
                    float(df['VOLUME'][index+1])*settings_3>float(df['VOLUME'][index-4]) and 
                    float(df['VOLUME'][index+1])*settings_3>float(df['VOLUME'][index-5]) and 
                    float(df['VOLUME'][index+1])*settings_3>float(df['VOLUME'][index-6]) and 
                    float(df['VOLUME'][index+1])*settings_3>float(df['VOLUME'][index-7]) and 
                    float(df['VOLUME'][index+1])*settings_3>float(df['VOLUME'][index-8]) and 
                    float(df['VOLUME'][index+1])*settings_3>float(df['VOLUME'][index-9])):
                    if float(df['VOLUME'][index+1])/float(row['VOLUME']) > settings_4: # если третья свеча больше чем вторая больше чем в 2.5 раза
                        flag_pump=1
                        index_flag_local = index+1
                        value_candle = round((float(df['VOLUME'][index-1])+float(df['VOLUME'][index])+float(df['VOLUME'][index+1]))*float(df['close'][index])/1000000,0)
                        if value_candle<settings_5:
                            continue
                        value_pump_30_day.append([number_row_table_30_day,datetime.fromtimestamp(int(df['open_time'][index+1]/1000)).strftime('%d.%m.%Y'),key,top_coin[key],datetime.fromtimestamp(int((df['open_time'][index+1]/1000)-10800)).strftime('%H:%M'),value_candle])
                        dop_data_row_30_daya[number_row_table_30_day] = index
                        number_row_table_30_day = number_row_table_30_day + 1 
                        # если нашли памп в последних 6 свечах
                        if index > (value_get_data-8):
                            dop_data_row_today[number_row_table_today] = index
                            value_pump_today.append([number_row_table_today,key,top_coin[key],datetime.fromtimestamp(int((df['open_time'][index+1]/1000)-10800)).strftime('%H:%M'),'???'])
                            number_row_table_today = number_row_table_today + 1
        if flag_pump == 0:
            pass 
    
    
    count_strat_plus = 0
    count_strat_minus = 0
    
    for key,value in enumerate(value_pump_30_day):
        if key == 0:continue
        # шаг пампа - dop_data_row_30_daya[key]+1 на этой свече по цене закрытия нужно входить в сделку
        # value[2] - монета, имя
        df = get_save_df(value[2])
        price_open = df['close'][dop_data_row_30_daya[key]+1] # цена открытия сделки
        # print(f'Цена открытия = {price_open} - {dop_data_row_30_daya[key]+1} | {value[2]}')
        for i in range(dop_data_row_30_daya[key]+2,value_get_data,1):
            if df['close'][i]>price_open and df['low'][i]>price_open: continue
            elif i>dop_data_row_30_daya[key]+2:
                value_pump_30_day[key][3] = round(((float(df['close'][i-1])/float(price_open)) - 1)*100,1)
                break
            else:
                value_pump_30_day[key][3] = round(((float(df['close'][i])/float(price_open)) - 1)*100,1)
                break
              
    # clean_card_menu(frame_table_pump_30_day)
    # table_pump_30_day = CTkTable(master=frame_table_pump_30_day, row=number_row_table_30_day, column=6, values=value_pump_30_day,command = get_data_table_onclick_30_day)
    # table_pump_30_day.pack(expand=True, padx=20, pady=20) 
    # clean_card_menu(frame_table_pump_today)
    # table_pump_today = CTkTable(master=frame_table_pump_today, row=number_row_table_today, column=5, values=value_pump_today, command = get_data_table_onclick_today)
    # table_pump_today.pack(expand=True, padx=20, pady=20) 
    
    for i,val in enumerate(value_pump_30_day):
        if i == 0: continue
        if float(val[3]) < 0:
            count_strat_minus = count_strat_minus+1
            # table_pump_30_day.edit_row(i, fg_color='#EB6D5C')
        else: count_strat_plus= count_strat_plus+1
    print(f'{iter}/{len(sett)}|Сигналов в плюс {count_strat_plus} | в минус {count_strat_minus}')
    if count_strat_plus != 0 and count_strat_minus != 0:
        procent_trade = round((count_strat_plus/(count_strat_plus+count_strat_minus))*100,2)
    elif count_strat_plus == 0 and count_strat_minus != 0:
        procent_trade = -100
    else:
        procent_trade = 0
    logger('pump_5min',f'|{procent_trade}%|{iter}/{len(sett)}|+{count_strat_plus}|-{count_strat_minus}|{count_strat_plus+count_strat_minus} | Настройки - | {settings_1} | {settings_2} | {settings_3} | {settings_4} | {settings_5}')
            
        
            
    

# обработка нажатия на строку в таблице 30 дней пампа
def get_data_table_onclick_30_day(data):
    global flag_pricel
    flag_pricel=0
    data_parse = table_pump_30_day.get_row(data['row'])
    df = get_save_df(data_parse[2])
    # table_pump_30_day.select_row(data['row'])
    print_graph(df,int(dop_data_row_30_daya[data_parse[0]])+1)
    
# обработка нажатия на строку в таблице пампов за 24 часа
def get_data_table_onclick_today(data):
    global flag_pricel
    flag_pricel=0
    data_parse = table_pump_today.get_row(data['row'])
    df = get_save_df(data_parse[1])
    # table_pump_today.select_row(data['row'])
    print_graph(df,int(dop_data_row_today[data_parse[0]])+1)

# Получите последние n свечей по n минут для торговой пары, обрабатываем и записывае данные в датафрейм
def get_futures_klines(symbol,TF='5m',VOLUME=value_get_data):
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

# получить датафрейм из файла
def get_save_df(symbol):
    MYDIR_WORKER = '../ROBO_TRADE/pump_str/DF_5min/'
    return pd.read_csv(f'{MYDIR_WORKER}{symbol}.csv')

# записать датафрейм в файл
def write_save_df(df,symbol):
    MYDIR_WORKER = '../ROBO_TRADE/pump_str/DF_5min/'
    df.to_csv(f'{MYDIR_WORKER}{symbol}.csv')


top_coin = get_top_coin()
pump_graph()
# pump_graph(win)















# -------------------------------- РАБОТА С ГРАФИКАМИ -----------------------------------


# первичные настройки окна
def settings_window_graph():
    global win_graph
    win_graph = customtkinter.CTk()
    win_graph.title("Robo_trade")
    w = 690
    h = 600
    ws = win_graph.winfo_screenwidth()
    hs = win_graph.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    win_graph.geometry('%dx%d+%d+%d' % (w, h, x, y))    
    # выстраиваем сетку гридов
    win_graph.grid_rowconfigure(0, weight=1)
    win_graph.grid_columnconfigure(1, weight=1)


height_canvas = 500
width_canvas = 600
width_telo = 3 # Ширина тела свечи
width_spile = 1 # Ширина хвоста, шпиля
flag_pricel = 0 # флаг для логики прицела



# рисуем все свечи по историческим
def paint_bar(iterows,canv,prices,prices_old):
    global OldRange
    global NewRange
    global price_min
    global price_max
    global mass_date_interval_graph
    global mass_date_line
    global NewRange1
    # определяем границы для масштабирования графика цены
    price_max = (prices_old.loc[prices_old['close'] == prices_old['close'].max()].iloc[0]['close'])
    price_min = (prices_old.loc[prices_old['close'] == prices_old['close'].min()].iloc[0]['close'])
    OldRange = (price_max - price_min) 
    NewRange = height_canvas 
    OldRange1 = (value_get_data)  
    NewRange1 = (width_canvas/(144/value_get_data))  
    # определяем границы для масштабирования графика объёмов
    price_max_volume = (prices_old.loc[prices_old['VOLUME'] == prices_old['VOLUME'].max()].iloc[0]['VOLUME'])
    price_min_volume = (prices_old.loc[prices_old['VOLUME'] == prices_old['VOLUME'].min()].iloc[0]['VOLUME'])
    OldRange_volume = (price_max_volume - price_min_volume) 
    NewRange_volume = 110     
    
    
    
    mass_date_interval_graph = {}
    mass_date_line = []
    for i in range(0,3000,20):
        mass_date_line.append(((i * NewRange1) / OldRange1))
    for index, row in prices.iterrows():
        x0 = ((index * NewRange1) / OldRange1)
        mass_date_interval_graph[(x0-2,x0+2)] = datetime.fromtimestamp(int(row['open_time']/1000)).strftime('%d.%m.%Y %H:%M')
        y0 = (((row['open'] - price_min) * NewRange) / OldRange)
        y1 = (((row['close'] - price_min) * NewRange) / OldRange)
        high = (((row['high'] - price_min) * NewRange) / OldRange)
        low = (((row['low'] - price_min) * NewRange) / OldRange)
        if index == iterows:
            paint_candle(canv,x0,y0,y1,high,low,1)
        else:
            paint_candle(canv,x0,y0,y1,high,low)
        
        VOLUME_y = (((row['VOLUME'] - price_min_volume) * NewRange_volume) / OldRange_volume)
        paint_one_volume(canvas_volume,x0,y0,y1,VOLUME_y)

# рисуем одну свечу    
def paint_candle(canv,x0,y0,y1,high,low,pump=0):
    height = height_canvas
    if pump == 1:
        canv.tag_lower(canv.create_line(x0+2,height-high,x0+2,height-y0,width=1,fill="#F68B44"))
        canv.tag_lower(canv.create_rectangle(x0, height-y0, x0+width_telo, height-y1,outline="#F68B44", fill="#F68B44"))
        canv.tag_lower(canv.create_line(x0+2,height-low,x0+2,height-y1,width=1,fill="#F68B44"))
    if y0>=y1:
        canv.tag_lower(canv.create_line(x0+2,height-high,x0+2,height-y0,width=1,fill="#F6465D"))
        canv.tag_lower(canv.create_rectangle(x0, height-y0, x0+width_telo, height-y1,outline="#F6465D", fill="#F6465D"))
        canv.tag_lower(canv.create_line(x0+2,height-low,x0+2,height-y1,width=1,fill="#F6465D"))
    if y0<y1:
        canv.tag_lower(canv.create_line(x0+2,height-high,x0+2,height-y0,width=1,fill="#0ECB81"))
        canv.tag_lower(canv.create_rectangle(x0, height-y0, x0+width_telo, height-y1,outline="#0ECB81", fill="#0ECB81"))
        canv.tag_lower(canv.create_line(x0+2,height-low,x0+2,height-y1,width=1,fill="#0ECB81"))

# рисуем один объём
def paint_one_volume(canv,x0,y0,y1,VOLUME_y):
    if y0>=y1: # красный
        canv.tag_lower(canv.create_rectangle(x0, 80-VOLUME_y, x0+width_telo, 80,outline="#F6465D", fill="#F6465D"))
    if y0<y1: # зеленый
        canv.tag_lower(canv.create_rectangle(x0, 80-VOLUME_y, x0+width_telo, 80,outline="#0ECB81", fill="#0ECB81"))
        
# перемещение канваса мышкой старт
def move_start(event):
    canvas.scan_mark(event.x, event.y)
    canvas_price.scan_mark(0, event.y)
    canvas_date.scan_mark(event.x, 0)
    canvas_volume.scan_mark(event.x, 60)
    
# перемещение канваса мышкой отпускание 
def move_move(event):
    canvas.scan_dragto(event.x, event.y, gain=1)
    canvas_price.scan_dragto(0, event.y, gain=1)
    canvas_date.scan_dragto(event.x, 0, gain=1)
    canvas_volume.scan_dragto(event.x, 60, gain=1)

# зум колесиком мыши
def zoomer(event):
    true_x = canvas.canvasx(event.x)
    true_y = canvas.canvasy(event.y)  
    if (event.delta > 0):
        canvas.scale("all", true_x, true_y, 1.1, 1.1)
        canvas_price.scale("all", 20, true_y, 1.1, 1.1)
        canvas_date.scale("all", true_x, 14, 1.1, 1.1)
        canvas_volume.scale("all", true_x, 80, 1.1, 1.1)
    elif (event.delta < 0):
        canvas.scale("all", true_x, true_y, 0.9, 0.9)
        canvas_price.scale("all", 20, true_y, 0.9, 0.9)
        canvas_date.scale("all", true_x, 14, 0.9, 0.9)
        canvas_volume.scale("all", true_x, 80, 0.9, 0.9)
    #canvas_date.configure(scrollregion = canvas_date.bbox("all"))

# отображает перекрестье на графике, изменяет цену и время
def mmove(event):
    global flag_pricel
    global canvas_id
    global canvas_id2
    global canvas_id3
    x0 = canvas.canvasx(0)
    y0 = canvas.canvasy(0)
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)  
    
    if flag_pricel!=0:
        # прицел
        canvas.coords(canvas_id,x, -1000, x, 10000)
        canvas_volume.coords(canvas_id3,x, -1000, x, 10000)
        canvas.coords(canvas_id2,0, y, 10000, y)
        # цена
        canvas_price.coords(price_rectangle,0, y-7,46, y+7)
        canvas_price.coords(price_rectangle_text,22, y)
        text_price = round(float((((height_canvas-y)*OldRange)/NewRange)+price_min),1)
        canvas_price.itemconfigure(price_rectangle_text, text=text_price)
        # дата
        canvas_date.coords(date_rectangle_text,x, 14)
        canvas_date.itemconfigure(date_rectangle_text, text=get_all_values(x))
        # canvas.coords(price_rectangle_polosa,x0+width_canvas-46, y0, x0+width_canvas, y0+height_canvas)
        
        return
    canvas_id = canvas.create_line(x, 0, x, 10000, width=1, fill='#424747')
    canvas_id3 = canvas_volume.create_line(x, 0, x, 10000, width=1, fill='#424747')
    canvas_id2 = canvas.create_line(0, y, 10000, y, width=1, fill='#424747')
    
    print_real_price_x(x,y)
    flag_pricel = 1

# находим дату по интервалу
def get_all_values(age):
   for key, value in mass_date_interval_graph.items():
      if (age >= key[0] and age <= key[1]):
        return value

# рисует прямоугольник с ценой справа графика и временем внизу
def print_real_price_x(x,y):
    global price_rectangle
    global price_rectangle_text
    global date_rectangle_text
    price_rectangle = canvas_price.create_rectangle(x+0, y+0, x+60, y+30, fill="#363A45",outline='#363A45')
    price_rectangle_text = canvas_price.create_text(100,10,fill="#DADBDD",font=('Purisa',8),text='124112')
    date_rectangle_text = canvas_date.create_text(100,10,fill="#DADBDD",font=('Purisa',8),text='124112')
    pass

# фугкция округления - принимает цену, которую хоим округлить и разряд
def price_round(price,digit):
    x = price
    n = digit
    return n * round(x/n)

# рисуем сетку
def print_setka_from_graph():
    mass_setka_price = []
    digit = 1000
    prise_mas_min = price_round(price_min,digit)
    prise_mas_max = price_round(price_max,digit)
    for i in range(prise_mas_min,prise_mas_min-30*digit,-1000):
        mass_setka_price.append(i)
    for i in range(prise_mas_max,prise_mas_max+30*digit,1000):
        mass_setka_price.append(i)
    for i in range(prise_mas_min,prise_mas_max,1000):
        mass_setka_price.append(i)
    for i in mass_setka_price:
        y = (((i - price_min) * NewRange) / OldRange)   
        canvas.tag_lower(canvas.create_line(-1000,height_canvas- y, 5000, height_canvas-y, width=1, fill='#1B1F24'))
        canvas_price.create_text(20,height_canvas-y,fill="#707985",font=('Purisa',8),text=i)
    for i in mass_date_line:
        canvas.tag_lower(canvas.create_line(i,-1000, i, 5000, width=1, fill='#1B1F24'))
        canvas_volume.tag_lower(canvas_volume.create_line(i,-1000, i, 5000, width=1, fill='#1B1F24'))

# рисуем панель инструментов
def print_tools(frame):
    global img_cursor_canvas,img_line_trend_canvas,img_horiz_line_canvas,img_kanal_canvas,img_kist_canvas,img_korzina_canvas 
    global img_cursor,img_line_trend,img_horiz_line,img_kanal,img_kist,img_korzina 

    img_cursor = PhotoImage(file=sys.path[0] + "\image\png\cursor.png") 
    img_line_trend = PhotoImage(file=sys.path[0] + "\image\png\line_trend.png") 
    img_horiz_line = PhotoImage(file=sys.path[0] + "\image\png\horiz_line.png") 
    img_kanal = PhotoImage(file=sys.path[0] + "\image\png\kanal.png") 
    img_kist = PhotoImage(file=sys.path[0] + "\image\png\kist.png") 
    img_korzina = PhotoImage(file=sys.path[0] + "\image\png\korzina.png") 
    
    img_cursor_canvas = Button(frame, command=img_cursor_enter,image=img_cursor,relief = 'flat',background ='#121619',border=0,width=25,height=25)
    img_line_trend_canvas = Button(frame, command=img_line_trend_enter,image=img_line_trend,relief = 'flat',background ='#121619',border=0,width=25,height=25)
    img_horiz_line_canvas = Button(frame, command=img_horiz_line_enter,image=img_horiz_line,relief = 'flat',background ='#121619',border=0,width=25,height=25)
    img_kanal_canvas = Button(frame, command=img_kanal_enter,image=img_kanal,relief = 'flat',background ='#121619',border=0,width=25,height=25)
    img_kist_canvas = Button(frame, command=img_kist_enter,image=img_kist,relief = 'flat',background ='#121619',border=0,width=25,height=25)
    img_korzina_canvas = Button(frame, command=img_korzina_enter,image=img_korzina,relief = 'flat',background ='#121619',border=0,width=25,height=25)
    
    
   
    img_cursor_canvas.pack(padx=5,pady=5)
    img_line_trend_canvas.pack(padx=5,pady=5)
    img_horiz_line_canvas.pack(padx=5,pady=5)
    img_kanal_canvas.pack(padx=5,pady=5)
    img_kist_canvas.pack(padx=5,pady=5)
    img_korzina_canvas.pack(padx=5,pady=5)
    
    # 0 кнопка
    img_cursor_canvas.bind("<Enter>", img_cursor_canvas_on_focus)
    img_cursor_canvas.bind("<Leave>", img_cursor_canvas_off_focus)
    # 1 кнопка
    img_line_trend_canvas.bind("<Enter>", img_line_trend_on_focus)
    img_line_trend_canvas.bind("<Leave>", img_line_trend_off_focus)
    # 2 кнопка
    img_horiz_line_canvas.bind("<Enter>", img_horiz_line_on_focus)
    img_horiz_line_canvas.bind("<Leave>", img_horiz_line_off_focus)
    # 3 кнопка
    img_kanal_canvas.bind("<Enter>", img_kanal_on_focus)
    img_kanal_canvas.bind("<Leave>", img_kanal_off_focus)
    # 4 кнопка
    img_kist_canvas.bind("<Enter>", img_kist_on_focus)
    img_kist_canvas.bind("<Leave>", img_kist_off_focus)
    # 5 кнопка
    img_korzina_canvas.bind("<Enter>", img_korzina_on_focus)
    img_korzina_canvas.bind("<Leave>", img_korzina_off_focus)
    
# 0 кнопка фокус
def img_cursor_canvas_on_focus(e):
    img_cursor_canvas['background'] = '#2A2E39'
# 0 кнопка дизфокус
def img_cursor_canvas_off_focus(e):
    img_cursor_canvas['background'] = '#121619'
#----------------------
# 1 кнопка фокус
def img_line_trend_on_focus(e):
    img_line_trend_canvas['background'] = '#2A2E39'
# 1 кнопка дизфокус
def img_line_trend_off_focus(e):
    img_line_trend_canvas['background'] = '#121619'
#----------------------
# 2 кнопка фокус
def img_horiz_line_on_focus(e):
    img_horiz_line_canvas['background'] = '#2A2E39'
# 2 кнопка дизфокус
def img_horiz_line_off_focus(e):
    img_horiz_line_canvas['background'] = '#121619'
#----------------------
# 3 кнопка фокус
def img_kanal_on_focus(e):
    img_kanal_canvas['background'] = '#2A2E39'
# 3 кнопка дизфокус
def img_kanal_off_focus(e):
    img_kanal_canvas['background'] = '#121619'
#----------------------
# 4 кнопка фокус
def img_kist_on_focus(e):
    img_kist_canvas['background'] = '#2A2E39'
# 4 кнопка дизфокус
def img_kist_off_focus(e):
    img_kist_canvas['background'] = '#121619'
#----------------------
# 5 кнопка фокус
def img_korzina_on_focus(e):
    img_korzina_canvas['background'] = '#2A2E39'
# 5 кнопка дизфокус
def img_korzina_off_focus(e):
    img_korzina_canvas['background'] = '#121619'
    
# 0 кнопка нажата
def img_cursor_enter():
    print("0")
# 1 кнопка нажата
def img_line_trend_enter():
    print("1")
# 2 кнопка нажата
def img_horiz_line_enter():
    print("2")
# 3 кнопка нажата
def img_kanal_enter():
    print("3")
# 4 кнопка нажата
def img_kist_enter():
    print("4")
# 5 кнопка нажата
def img_korzina_enter():
    print("5")
    
# рисовать график по историческим данным - главное, точка входа
def draw_graph(iterows,df,frame,width=width_canvas,height=height_canvas,bg="#161A1E"):
    global canvas
    global canvas_price
    global canvas_date
    global canvas_volume
    global canvas_tools
    
    canvas = Canvas(frame, width = width, height = height, bg = bg,border=0,bd=0,highlightthickness=0)
    canvas_price = Canvas(frame, width = 46, height = height, bg = '#121619',border=0,bd=0,highlightthickness=0)
    canvas_date = Canvas(frame, width = width_canvas, height = 30, bg = '#121619',border=0,bd=0,highlightthickness=0)
    canvas_volume = Canvas(frame, width = width_canvas, height = 80, bg = bg,border=0,bd=0,highlightthickness=0)
    canvas_settings = Canvas(frame, width = 46, height = 110, bg = '#121619',border=0,bd=0,highlightthickness=0)
    canvas_tools = customtkinter.CTkFrame(frame, corner_radius=0,fg_color='#121619',width=40)
    xsb = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
    ysb = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
    canvas.configure(scrollregion=(-5000,-5000,5000,5000))
    canvas_volume.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
    canvas_volume.configure(scrollregion=(-5000,-5000,5000,5000))
    canvas_date.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
    canvas_date.configure(scrollregion=(-5000,-5000,5000,5000))
    
    canvas.grid(row=0, column=1)
    canvas_price.grid(row=0, column=2,padx=0,sticky='w')
    canvas_volume.grid(row=1, column=1,padx=0,sticky='w')
    canvas_date.grid(row=2, column=1,padx=0,sticky='w')
    canvas_settings.grid(row=1, column=2,padx=0,sticky='ns',rowspan=2)
    canvas_tools.grid(row=0, column=0,rowspan=3,sticky='ns')  
    
    # Это то, что позволяет использовать мышь
    canvas.bind("<ButtonPress-1>", lambda event: move_start(event))
    canvas.bind("<B1-Motion>", lambda event:move_move(event))
    canvas.bind("<MouseWheel>",lambda event:zoomer(event))
    canvas.bind('<Motion>', lambda event:mmove(event))
    
    paint_bar(iterows,canvas,df,df)
    print_setka_from_graph()
    #print_tools(canvas_tools)
    
    canvas.xview_moveto(str((abs(-5000)+(width_canvas/(144/iterows))-400)/(abs(-5000)+5000)))
    canvas_volume.xview_moveto(str((abs(-5000)+(width_canvas/(144/iterows))-400)/(abs(-5000)+5000)))
    canvas_date.xview_moveto(str((abs(-5000)+(width_canvas/(144/iterows))-400)/(abs(-5000)+5000)))
    
 
def print_graph(df,iterows):
    settings_window_graph()
    frame = customtkinter.CTkFrame(win_graph, corner_radius=0)
    frame.pack(pady=[0,0])
    draw_graph(iterows,df,frame)
    win_graph.mainloop()
 





# win.mainloop()



















