from tkinter import *
from math import *
import os
import sys
sys.path.insert(1,os.path.join(sys.path[0],'../'))
from imports import *
from binance.client import Client




period = 3 # период полос Боллинджера
symbol = "ETHUSDT"
prices = []
# списки для хранения всей необходимой статистики
moving_average_values = []
bollinger_band_high_values = []
bollinger_band_low_values = []
# флажки для отслеживания обменов, чтобы избежать дублирования записей
in_short = False
in_long = False
client = Client(key,secret)
coin_mas_10 = []
width_canvas = 700
height_canvas = 300
width_telo = 3 # Ширина тела свечи
width_spile = 1 # Ширина хвоста, шпиля
bb_high_old = 0
bb_low_old = 0
df_our_coin_5min = []
data_numbers = []
open_sl = False
x_bh0 = 0

def print_components_log(msg,frame,type):
    global data_print_ad_df
    global number_print_df
    global number_print_ht
    global data_print_ad_ht
    path ='H_log.txt'
    f = open(path,'a',encoding='utf-8')
    f.write('\n'+time.strftime("%d.%m.%Y | %H:%M:%S | ", time.localtime())+msg)
    f.close()
    if type == 'DF':
        number_print_df=number_print_df+1
        for widget in frame.winfo_children():
                widget.forget()
        data_print_ad_df.insert(0,customtkinter.CTkLabel(frame, text=str(number_print_df)+'. '+ msg, fg_color="#DAE2EC",text_color='#242424',anchor='w',font=('Arial',12,'normal')))
        for component in data_print_ad_df:
            component.pack(anchor="w")
    if type == 'HT':
        number_print_ht=number_print_ht+1
        for widget in frame.winfo_children():
                widget.forget()
        data_print_ad_ht.insert(0,customtkinter.CTkLabel(frame, text=str(number_print_ht)+'. '+ msg, fg_color="#DAE2EC",text_color='#242424',anchor='w',font=('Arial',12,'normal')))
        for component in data_print_ad_ht:
            component.pack(anchor="w")  

def print_log_his(frame,msg):
    global i1
    i1=i1+1
    customtkinter.CTkLabel(frame, text=msg, fg_color="#DAE2EC",text_color='#242424',anchor='w',justify="left",font=('Arial',12,'normal')).grid(row=i1, column=0, sticky="w",pady=0,padx=5)

# определяем размер позиции, на которую должны зайти
def get_trade_VOLUME(get_symbol_price):
    vol = round(DEPOSIT*LEVERAGE/get_symbol_price)
    return vol

# обменные операции:
def short_open():
    print('Шорт открыли')
    # client.futures_create_order(symbol=symbol, side='SELL', type='MARKET', quantity=quantity)
    
def short_close():
    print('Шорт закрыли')
    # client.futures_create_order(symbol=symbol, side='BUY', type='MARKET', quantity=quantity)
    
def long_open():
    print('Лонг открыли')
    #client.futures_create_order(symbol=symbol, side='BUY', type='MARKET', quantity=quantity)

def long_close():
    print('Лонг закрыли')
    # client.futures_create_order(symbol=symbol, side='SELL', type='MARKET', quantity=quantity)

def get_df_coin(coin):
    global symbol
    for x,result in enumerate(coin_mas_10):
        if result == coin:
            symbol = coin
            return df_our_coin_5min[x]

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

def paint_bar(canv,prices,prices_old,index,bb_high,bb_low):
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
   
    rint_bollindger(canv,index,bb_high,bb_low,price_max,price_min,OldRange,NewRange,OldRange1,NewRange1)
x_bollindger = 0  
x0_bol = 0
y0_bol = 0
y0_bol_l = 0
def rint_bollindger(canv,index,bb_high,bb_low,price_max,price_min,OldRange,NewRange,OldRange1,NewRange1):
    global x_bollindger
    global x0_bol
    global y0_bol
    global y0_bol_l
    if x_bollindger == 0:  
        x0_bol = ((index * NewRange1) / OldRange1)+10
        y0_bol = height_canvas-(((bb_high - price_min) * NewRange) / OldRange)
        y0_bol_l = height_canvas-(((bb_low - price_min) * NewRange) / OldRange)
        x_bollindger = 1
        return
    x = ((index * NewRange1) / OldRange1)+10
    y = height_canvas-(((bb_high - price_min) * NewRange) / OldRange)
    y_l = height_canvas-(((bb_low - price_min) * NewRange) / OldRange)
    canv.create_line(x0_bol,y0_bol,x,y,width=1,fill="green")
    canv.create_line(x0_bol,y0_bol_l,x,y_l,width=1,fill="red")
    x0_bol = x
    y0_bol = y
    y0_bol_l = y_l
    


# main loop
def main(frame_2_set2_graph):
    global coin_mas_10
    global in_long
    global in_short
    fi = open(MYDIR_COIN,'r')
    coin_mas_10 = fi.read().split('|')
    fi.close()
    canvas_mas = []
    count_mas = 0
    for x,result in enumerate(coin_mas_10):
        df_5min = pd.read_csv(f'{MYDIR_WORKER}{result}.csv')
        VOLUME_TRADE = len(df_5min)
        df_our_coin_5min.append(df_5min)
        canvas_mas.insert(count_mas, Canvas(frame_2_set2_graph, width = width_canvas, height = height_canvas, bg = "#2B2B2B", cursor = "pencil",border=0,bd=0,highlightthickness=0))
        customtkinter.CTkLabel(frame_2_set2_graph, text=result, fg_color="transparent",anchor='center',font=('Arial',14,'bold')).pack(pady=1, anchor='w')
        canvas_mas[count_mas].pack(pady=10)	
        canvas_mas[count_mas].create_line(10,height_canvas,10,0,width=1,arrow=LAST) 
        canvas_mas[count_mas].create_line(0,height_canvas-10,width_canvas,height_canvas-10,width=1,arrow=LAST) 
        count_mas = count_mas+1
    for index in range(VOLUME_TRADE):
    # for index in range(VOLUME_TRADE):
        data_numbers.append(index)   
        if open_sl == False: # если нет позиции
            for x,result in enumerate(coin_mas_10):
                prices_old = get_df_coin(result)
                latest_price = prices_old.iloc[data_numbers] # берем из фрема свечи по текущий шаг итерации
                prices = latest_price['close'].to_numpy()
                # вычислить скользящее среднее и отклонение
                ma = np.mean(prices[-period:])
                moving_average_values.append(ma)
                std = np.std(prices[-period:], ddof=1)
                # рассчитать полосы Боллинджера
                bb_high = ma + 2 * std
                bb_low = ma - 2 * std
                bollinger_band_high_values.append(bb_high)
                bollinger_band_low_values.append(bb_low)
                #if x==0:print(f'{index}|bb_low - {bb_low}|bb_high - {bb_high}|prices = {prices[-1]}')
                # решение о стратегии
                # короткие обмены
                if len(prices)>4:
                    paint_bar(canvas_mas[x],latest_price.iloc[-1:],prices_old,index,bb_high,bb_low)
                    if float(prices[-2]) < bollinger_band_high_values[-2] and float(prices[-1]) > bollinger_band_high_values[-1]:
                        print('111')
                        if not in_short:
                            print('222')
                            short_open()
                            in_short = True
                    if float(prices[-2]) > moving_average_values[-2] and float(prices[-1]) < moving_average_values[-1]:
                        if in_short:
                            short_close()
                            in_short = False
                    # длительные условия
                    if float(prices[-1]) < bollinger_band_low_values[-1] and float(prices[-2]) > bollinger_band_low_values[-2]:
                        if not in_long:
                            long_open()
                            in_long = True
                    if float(prices[-2]) < moving_average_values[-2] and float(prices[-1]) > moving_average_values[-1]:
                        if in_long:
                            long_close()
                            in_long = False
                    
                    
                    
                    
                    
     
    
    
    
    

            
            
            

