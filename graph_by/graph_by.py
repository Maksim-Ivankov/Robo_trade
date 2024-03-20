import customtkinter
import time
import requests
import pandas as pd
from tkinter import *
import tkinter as tk

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
    # определяем границы для масштабирования графика
    price_max = (prices_old.loc[prices_old['close'] == prices_old['close'].max()].iloc[0]['close'])*1.05
    price_min = (prices_old.loc[prices_old['close'] == prices_old['close'].min()].iloc[0]['close'])*0.95
    OldRange = (price_max - price_min) 
    NewRange = height_canvas 
    OldRange1 = (VOLUME)  
    NewRange1 = (width_canvas/(144/VOLUME))  
    for index, row in prices.iterrows():
        x0 = ((index * NewRange1) / OldRange1)+10
        y0 = (((row['open'] - price_min) * NewRange) / OldRange)
        y1 = (((row['close'] - price_min) * NewRange) / OldRange)
        high = (((row['high'] - price_min) * NewRange) / OldRange)
        low = (((row['low'] - price_min) * NewRange) / OldRange)
        paint_candle(canv,x0,y0,y1,high,low)

# рисуем одну свечу    
def paint_candle(canv,x0,y0,y1,high,low):
    height = height_canvas
    if y0>=y1:
        canv.tag_lower(canv.create_line(x0+2,height-high,x0+2,height-y0,width=1,fill="#ff2b2b"))
        canv.tag_lower(canv.create_rectangle(x0, height-y0, x0+width_telo, height-y1,outline="#ff2b2b", fill="#ff2b2b"))
        canv.tag_lower(canv.create_line(x0+2,height-low,x0+2,height-y1,width=1,fill="#ff2b2b"))
    if y0<y1:
        canv.tag_lower(canv.create_line(x0+2,height-high,x0+2,height-y0,width=1,fill="#45f757"))
        canv.tag_lower(canv.create_rectangle(x0, height-y0, x0+width_telo, height-y1,outline="#45f757", fill="#45f757"))
        canv.tag_lower(canv.create_line(x0+2,height-low,x0+2,height-y1,width=1,fill="#45f757"))

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


# рисовать график по историческим данным
def draw_graph(df,frame=win,width=width_canvas,height=height_canvas,bg="#2B2B2B", title_gr=symbol):
    global canvas
    canvas = Canvas(frame, width = width, height = height, bg = bg,border=0,bd=0,highlightthickness=0)
    # canvas = Canvas(frame, width = width, height = height, bg = bg)
    xsb = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
    ysb = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
    canvas.configure(scrollregion=(0,0,10000,5000))
    
    canvas.grid(row=0, column=0,padx=[100,0])
    
    # Это то, что позволяет использовать мышь
    canvas.bind("<ButtonPress-1>", lambda event: move_start(event))
    canvas.bind("<B1-Motion>", lambda event:move_move(event))
    canvas.bind("<MouseWheel>",lambda event:zoomer(event))
    
    paint_bar(canvas,df,df)

x_mouse = 0
y_mouse = 0    

def mmove(event):
    global canvas_id
    global canvas_id2
    x = event.x
    y = event.y
    canvas_id = canvas.create_line(x, 0, x, 1000, width=1, fill='red')
    canvas_id2 = canvas.create_line(0, y, 1000, y, width=1, fill='red')
    # time.sleep(0.1)
    # b2()
    
def b2():
	canvas.delete(canvas_id)
	canvas.delete(canvas_id2)    

win.bind('<Motion>', mmove)



df = get_df_from_file() # получили датафрейм в переменную
draw_graph(df)



win.mainloop()











