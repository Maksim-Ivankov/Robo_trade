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

symbol = 'BTCUSDT'
TF = '1h'
VOLUME = 480
MYDIR = '../ROBO_TRADE/graph_by/coin.csv'
height_canvas = 500
width_canvas = 600
width_telo = 3 # Ширина тела свечи
width_spile = 1 # Ширина хвоста, шпиля
flag_pricel = 0 # флаг для логики прицела


frame = customtkinter.CTkFrame(win, corner_radius=0)
frame.pack(pady=[100,0])

# генерируем датафрейм в файл
def generate_dataframe(TF,VOLUME):
    open(MYDIR, "w").close()
    df = get_futures_klines(symbol,TF,VOLUME)
    df.to_csv(f'{MYDIR}.csv')

# Получите последние n свечей по n минут для торговой пары, обрабатываем и записывае данные в датафрейм
def get_futures_klines(symbol,TF,VOLUME):
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

# проверяем дф из файла, если его там нет, то делаем запрос к бирже
def get_df_from_file():
    try:
        print('ДФ найден в файле')
        return pd.read_csv(f'{MYDIR}')
    except:
        print('Генерируем ДФ')
        generate_dataframe(TF,VOLUME)
        return pd.read_csv(f'{MYDIR}')

# рисуем все свечи по историческим
def paint_bar(canv,prices,prices_old):
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
    OldRange1 = (VOLUME)  
    NewRange1 = (width_canvas/(144/VOLUME))  
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
        paint_candle(canv,x0,y0,y1,high,low)
        
        VOLUME_y = (((row['VOLUME'] - price_min_volume) * NewRange_volume) / OldRange_volume)
        paint_one_volume(canvas_volume,x0,y0,y1,VOLUME_y)

# рисуем одну свечу    
def paint_candle(canv,x0,y0,y1,high,low):
    height = height_canvas
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
def draw_graph(df,frame,width=width_canvas,height=height_canvas,bg="#161A1E", title_gr=symbol):
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
    
    paint_bar(canvas,df,df)
    print_setka_from_graph()
    print_tools(canvas_tools)
    
    canvas.xview_moveto(str((abs(-5000)+NewRange1-400)/(abs(-5000)+5000)))
    canvas_volume.xview_moveto(str((abs(-5000)+NewRange1-400)/(abs(-5000)+5000)))
    canvas_date.xview_moveto(str((abs(-5000)+NewRange1-400)/(abs(-5000)+5000)))
    
    
df = get_df_from_file() # получили датафрейм в переменную
draw_graph(df,frame)
 
win.mainloop()











