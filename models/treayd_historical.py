from tkinter import *
from math import *
import os
import sys
sys.path.insert(1,os.path.join(sys.path[0],'../'))
from imports import *


TF = '5m' # таймфрейм
wait_time = 5 # сколько минут ждать для обновления цены с биржи
TP = 0.012 # Тейк профит, процент
SL = 0.004 # Стоп лосс, процент
DEPOSIT = 100 # Депозит
DEPOSIT_START = DEPOSIT
LEVERAGE = 20 # торговое плечо
COMMISSION_MAKER = 0.002 # комиссия а вход
COMMISSION_TAKER = 0.001 # комиссия на выхд
VOLUME = 144 # сколько свечей получить при запросе к бирже
VOLUME_5MIN = 720 # сколько свечей получить в режиме слежения за ценой
CANAL_MAX = 0.85 # Верх канала
CANAL_MIN = 0.15 # Низ канала
CORNER_SHORT = 10 # Угол наклона шорт
CORNER_LONG = 10 # Угол наклона лонг
CANDLE_COIN_MIN = 200000 # объем торгов за свечку
CANDLE_COIN_MAX = 500000 # объем торгов за свечку
MYDIR_WORKER = '../ROBO_TRADE/DF/worker/'
MYDIR_5MIN = '../ROBO_TRADE/DF/5min/'
MYDIR_COIN = '../ROBO_TRADE/DF/coin.txt'
MYDIR_COIN_PROCENT = '../ROBO_TRADE/DF/coin_procent.txt'

day_trade = round((wait_time*VOLUME)/(60*24),4)
open_sl = False # флаг на открытые позиции
open_position = False # флаг, стоим в позиции или нет
price_trade = 0
signal_trade = ''
coin_trade = ''
symbol = '' 
value_trade = 0
profit = 0
loss = 0
commission = 0
data_numbers = []
count_long_take = 0
count_short_take = 0
count_long_loss = 0
count_short_loss = 0
coin_mas_10=[]
df_our_coin = []
df_our_coin_5min = []
trend = ''
i1 = 0
time_close_tf = 0
coutnt_index_time_df = 0
data_print_ad_df = []
number_print_df = 0
number_print_ht = 0
data_print_ad_ht = []
work_timeframe_HM = 1
width_canvas = 700
height_canvas = 300
width_telo = 3 # Ширина тела свечи
width_spile = 1 # Ширина хвоста, шпиля

client = UMFutures(key=key, secret=secret)


# Получите последние n свечей по n минут для торговой пары, обрабатываем и записывае данные в датафрейм
def get_futures_klines(symbol,TF,VOLUME):
    print('https://fapi.binance.com/fapi/v1/klines?symbol='+symbol.upper()+'&limit='+str(VOLUME)+'&interval='+TF)
    x = requests.get('https://fapi.binance.com/fapi/v1/klines?symbol='+symbol.upper()+'&limit='+str(VOLUME)+'&interval='+TF)
    df=pd.DataFrame(x.json())
    df.columns=['open_time','open','high','low','close','VOLUME','close_time','d1','d2','d3','d4','d5']
    df=df.drop(['d1','d2','d3','d4','d5'],axis=1)
    df['open']=df['open'].astype(float)
    df['high']=df['high'].astype(float)
    df['low']=df['low'].astype(float)
    df['close']=df['close'].astype(float)
    df['VOLUME']=df['VOLUME'].astype(float)
    return(df) # возвращаем датафрейм с подготовленными данными

# Получаем активные монеты на бирже
def get_top_coin():
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
        if i== 10:
            break
    i=0
    for key, value in coin_min.items():
        i=i+1
        coin_mas2[key] = value
        if i==1:
            coin_min_val = value
        if i== 10:
            break
    if abs(coin_max_val)>abs(coin_min_val):
        result = coin_mas1
    else:
        result = coin_mas2
    return result

# определяем размер позиции, на которую должны зайти
def get_trade_VOLUME(get_symbol_price):
    vol = round(DEPOSIT*LEVERAGE/get_symbol_price)
    return vol

# удаление всех файлов csv в переданной директории
def remove_csv(dir):
    filelist = [ f for f in os.listdir(dir) if f.endswith(".csv") ]
    for f in filelist:
        os.remove(os.path.join(dir, f))

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

def generate_dataframe(TF,VOLUME,VOLUME_5MIN,frame_2_set2_3,work_timeframe_str_HM):
    global coin_mas_10
    print_components_log('Начали сбор данных',frame_2_set2_3,'DF')
    coin_mas_10 = get_top_coin() # один раз запускаем функцию, чтобы обновить монету, с которой работаем
    open(MYDIR_COIN, "w").close()
    open(MYDIR_COIN_PROCENT, "w").close()
    fi1 = open(MYDIR_COIN,'a',encoding='utf-8')
    fi2 = open(MYDIR_COIN_PROCENT,'a',encoding='utf-8')
    arr_coin = []
    arr_coin_procent = []
    for key, value in coin_mas_10.items():
        arr_coin.append(key)
        arr_coin_procent.append(f'{key}: {value}')
    result_as_list1 = '|'.join(arr_coin)
    result_as_list2 = '|'.join(arr_coin_procent)
    fi1.write(result_as_list1)
    fi1.close()
    fi2.write(result_as_list2)
    fi2.close()
    # выше записываем файл с монетами роста + монеты роста и проценты
    remove_csv(MYDIR_WORKER)
    remove_csv(MYDIR_5MIN)
    for x,result in enumerate(coin_mas_10):
        print(f'{result},{TF},{VOLUME}')
        df = get_futures_klines(result,TF,VOLUME)
        df.to_csv(f'{MYDIR_WORKER}{result}.csv')
        print_components_log(f'{result} - {TF} добавлен',frame_2_set2_3,'DF')
        time.sleep(2)
        df_5m = get_futures_klines(result,work_timeframe_str_HM,VOLUME_5MIN)
        df_5m.to_csv(f'{MYDIR_5MIN}{result}.csv')
        print_components_log(f'{result} - {work_timeframe_str_HM} мин добавлен',frame_2_set2_3,'DF')
        time.sleep(2)
    print_components_log(f'Датафреймы добавлены!',frame_2_set2_3,'DF')
    return coin_mas_10

def print_log_his(frame,msg):
    global i1
    i1=i1+1
    customtkinter.CTkLabel(frame, text=msg, fg_color="#DAE2EC",text_color='#242424',anchor='w',justify="left",font=('Arial',12,'normal')).grid(row=i1, column=0, sticky="w",pady=0,padx=5)

# -------------------------------------- ИНДИКАТОРЫ --------------------------------------

# Индикатор истинного диапазона и среднего значения истинного диапазона
def indATR(source_DF,n):
    df = source_DF.copy()
    df['H-L']=abs(df['high']-df['low'])
    df['H-PC']=abs(df['high']-df['close'].shift(1))
    df['L-PC']=abs(df['low']-df['close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    df_temp = df.drop(['H-L','H-PC','L-PC'],axis=1)
    return df_temp

# Определяем наклон ценовой линии
def indSlope(series,n):
    array_sl = [j*0 for j in range(n-1)]
    for j in range(n,len(series)+1):
        y = series[j-n:j]
        x = np.array(range(n))
        x_sc = (x - x.min())/(x.max() - x.min())
        y_sc = (y - y.min())/(y.max() - y.min())
        x_sc = sm.add_constant(x_sc)
        model = sm.OLS(y_sc,x_sc)
        results = model.fit()
        array_sl.append(results.params[-1])
    slope_angle = (np.rad2deg(np.arctan(np.array(array_sl))))
    return np.array(slope_angle)

# найти локальный минимум
def isLCC(DF,i):
    df=DF.copy()
    LCC=0
    if df['close'][i]<=df['close'][i+1] and df['close'][i]<=df['close'][i-1] and df['close'][i+1]>df['close'][i-1]:
        #найдено Дно
        LCC = i-1
    return LCC

# найти локальный максимум
def isHCC(DF,i):
    df=DF.copy()
    HCC=0
    if df['close'][i]>=df['close'][i+1] and df['close'][i]>=df['close'][i-1] and df['close'][i+1]<df['close'][i-1]:
        #найдена вершина
        HCC = i
    return HCC

# сгенерируйте фрейм данных со всеми необходимыми данными
def PrepareDF(DF):
    ohlc = DF.iloc[:,[0,1,2,3,4,5]]
    ohlc.columns = ["date","open","high","low","close","VOLUME"]
    ohlc=ohlc.set_index('date')
    df = indATR(ohlc,14).reset_index()
    df['slope'] = indSlope(df['close'],5)
    df['channel_max'] = df['high'].rolling(10).max() # определяем верхний уровень канала
    df['channel_min'] = df['low'].rolling(10).min() # определяем нижний уровень канала
    df['position_in_channel'] = (df['close']-df['channel_min']) / (df['channel_max']-df['channel_min']) # сейчас находимся выше середины канала или ниже
    df = df.set_index('date')
    df = df.reset_index()
    return(df)

# -------------------------------------- ИНДИКАТОРЫ --------------------------------------
# -------------------------------------- ТОРГОВЛЯ --------------------------------------

# открывает лонг или шорт
def open_position(trend,value,price,frame_3_set4_1_1_1):
    global open_sl
    global price_trade
    global signal_trade
    global coin_trade
    global value_trade
    global take_profit_price
    global stop_loss_price
    price_trade = price
    signal_trade = trend
    coin_trade = symbol
    value_trade = value
    open_sl = True
    print_components_log(f'Открыл {signal_trade}, монета {coin_trade}, цена {price_trade}',frame_3_set4_1_1_1,'HT')
    take_profit_price = get_take_profit(trend,price_trade) # получаем цену тэйк профита
    stop_loss_price = get_stop_loss(trend,price_trade) # получаем цену стоп лосса

def get_take_profit(trend,price_trade): # получаем цену тейк профита в зависимости от направления
    if trend == 'long':
        return price_trade*(1+TP)
    if trend == 'short':
        return price_trade*(1-TP)
def get_stop_loss(trend,price_trade): # получаем цену стоп лосса в зависимости от направления
    if trend == 'long':
        return price_trade*(1-SL)
    if trend == 'short':
        return price_trade*(1+SL)
    
# Закрываем сделку
def close_trade(status,procent,frame_3_set4_1_1_1):
    global DEPOSIT
    global open_sl
    global profit
    global loss
    global commission
    if status == '+': # если закрыли в плюс
        profit = profit + LEVERAGE*DEPOSIT*procent
        commission = commission + LEVERAGE*DEPOSIT*(COMMISSION_MAKER+COMMISSION_TAKER)
        DEPOSIT = DEPOSIT + LEVERAGE*DEPOSIT*procent - LEVERAGE*DEPOSIT*(COMMISSION_MAKER+COMMISSION_TAKER) # обновляем размер депо
        open_sl = False
        print(f'ТЕЙК в + | {DEPOSIT}')
        print_components_log(f'Сработал ТЕЙК|Депо={round(DEPOSIT,1)}, профит={round(profit,1)},ком={round(commission,1)}',frame_3_set4_1_1_1,'HT')
    if status == '-': # если закрыли в минус
        loss = loss + LEVERAGE*DEPOSIT*procent
        commission = commission + LEVERAGE*DEPOSIT*(COMMISSION_MAKER+COMMISSION_TAKER)
        DEPOSIT = DEPOSIT - LEVERAGE*DEPOSIT*procent - LEVERAGE*DEPOSIT*(COMMISSION_MAKER+COMMISSION_TAKER) # обновляем размер депо
        open_sl = False
        print(f'СТОП В - | {DEPOSIT}')
        print_components_log(f'Сработал СТОП|Депо={round(DEPOSIT,1)}, убыток={round(loss,1)},ком={round(commission,1)}',frame_3_set4_1_1_1,'HT')

def check_trade(price,frame_3_set4_1_1_1):
    now_price_trade = price #получаем текущую цену монеты
    global count_long_take
    global count_long_loss
    global count_short_take
    global count_short_loss
    global take_profit_price
    global stop_loss_price
    print('лол - 12')
    if signal_trade == 'long':
        print('лол - 13')
        
        print(f'сейчас - {now_price_trade}')
        print(f'тейк - {take_profit_price}')
        print(f'стоп - {stop_loss_price}')
        if float(now_price_trade)>float(take_profit_price):
            close_trade('+',TP,frame_3_set4_1_1_1)
            count_long_take=count_long_take+1
            print('лол - 16')
            return 1
        if float(now_price_trade)<float(stop_loss_price):
            count_long_loss = count_long_loss + 1
            close_trade('-',SL,frame_3_set4_1_1_1)
            print('лол - 17')
            return 1
    if signal_trade == 'short':
        print('лол - 14')
        if float(now_price_trade)<float(take_profit_price):
            close_trade('+',TP,frame_3_set4_1_1_1)
            count_short_take = count_short_take+1
            print('лол - 18')
            return 1
        if float(now_price_trade)>float(stop_loss_price):
            count_short_loss = count_short_loss + 1
            close_trade('-',SL,frame_3_set4_1_1_1)
            print('лол - 19')
            return 1
# -------------------------------------- ТОРГОВЛЯ --------------------------------------
# -------------------------------------- СТРАТЕГИЯ --------------------------------------

def check_if_signal(ohlc,index):
    prepared_df = PrepareDF(ohlc)
    signal="нет сигнала" # возвращаемый сигнал, лонг или шорт
    i=index-2 # 99 - текущая свеча, которая не закрыта, 98 - последняя закрытая свеча, нам нужно 97, чтобы проверить, нижняя она или верхняя
    if isHCC(prepared_df,i-1)>0: # если у нас локальный минимум
        if prepared_df['position_in_channel'][i-1]>CANAL_MAX: # проверяем, прижаты ли мы к нижней границе канала
            if prepared_df['slope'][i-1]>CORNER_SHORT: # смотрим, какой у нас наклон графика
                signal='short'
    if isLCC(prepared_df,i-1)>0: # если у нас локальный максимум
        if prepared_df['position_in_channel'][i-1]<CANAL_MIN: # проверяем, прижаты ли мы к верхней границе канала
            if prepared_df['slope'][i-1]<CORNER_LONG: # смотрим, какой наклон графика
                signal='long'
    return signal
    
# -------------------------------------- СТРАТЕГИЯ --------------------------------------

# удаление всех файлов csv в переданной директории
def remove_csv(dir):
    filelist = [ f for f in os.listdir(dir) if f.endswith(".csv") ]
    for f in filelist:
        os.remove(os.path.join(dir, f))
        
        
def get_df_coin(coin):
    global symbol
    for x,result in enumerate(coin_mas_10):
        if result == coin:
            symbol = coin
            return df_our_coin[x]

def get_df_coin_now_price(index):
    for x,result in enumerate(coin_mas_10):
        if str(result) == str(symbol):
            if int(index) > int(VOLUME_5MIN-1):
                return 0
            return df_our_coin_5min[x].iloc[index]['close']
        
# возвращаем список индексов таймфреймов 1м внутри 5м по цене закрытия на текущем шаге итерации
def get_price_5min(time):
    for x,result in enumerate(coin_mas_10):
        global coutnt_index_time_df
        if str(result) == str(symbol):
            df_new = df_our_coin_5min[x][df_our_coin_5min[x]['close_time'] == time].index[0]
            index_time_df = []
            for i in range(df_new+coutnt_index_time_df*int(wait_time/work_timeframe_HM),df_new+int(wait_time/work_timeframe_HM)+coutnt_index_time_df*int(wait_time/work_timeframe_HM)):
                index_time_df.append(i)
            coutnt_index_time_df = coutnt_index_time_df+1
            return index_time_df

# -------------------------------------- Перебор по датафрейму --------------------------------------


# рисуем треугольники лонга и шорта
def paint_trade(canv,trend,index,prices,prices_old):
    height = height_canvas
    price_max = (prices_old.loc[prices_old['close'] == prices_old['close'].max()].iloc[0]['close'])*1.05
    price_min = (prices_old.loc[prices_old['close'] == prices_old['close'].min()].iloc[0]['close'])*0.95
    OldRange = (price_max - price_min) 
    NewRange = height_canvas 
    OldRange1 = (VOLUME)  
    NewRange1 = (width_canvas/(144/VOLUME))
    if trend == 'long':
        x0 = ((index * NewRange1) / OldRange1)+10
        y0 = height-(((prices - price_min) * NewRange) / OldRange)
        canv.lift(canv.create_polygon([x0+5+2,y0+10],[x0-5+2,y0+10],[x0+2,y0],fill="green", outline="black"))
        
    if trend == 'short':
        x0 = ((index * NewRange1) / OldRange1)+10
        y0 = height-(((prices - price_min) * NewRange) / OldRange)
        canv.lift(canv.create_polygon([x0+5+2,y0-10],[x0-5+2,y0-10],[x0+2,y0],fill="red", outline="black"))
        
    
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


def start_trade_hist_model(frame_2_set2_graph,frame_3_set4_1_1_1,frame_3_set4_1_2):
    global coin_mas_10
    global symbol
    global coutnt_index_time_df
    global trend
    global time_close_tf
    
    print_components_log('Начали торговлю',frame_3_set4_1_1_1,'HT')
    print_components_log(f'Настройки:\nДепозит:{DEPOSIT} | Плечо:{LEVERAGE} | Комиссия покупка:{COMMISSION_MAKER}\nКомиссия продажа:{COMMISSION_TAKER} | Тейк:{TP} | Стоп:{SL} | Канал верх:{CANAL_MAX}\nКанал низ:{CANAL_MIN} | Угол лонг:{CORNER_LONG} | Угол шорт:{CORNER_SHORT} | Объём мин:{CANDLE_COIN_MIN}\nОбъём макс:{CANDLE_COIN_MAX} | Объём основа:{VOLUME} | Объём 5 мин: {VOLUME_5MIN}',frame_3_set4_1_1_1,'HT')
    
    fi = open(MYDIR_COIN,'r')
    coin_mas_10 = fi.read().split('|')
    fi.close()
    canvas_mas = []
    count_mas = 0
    for x,result in enumerate(coin_mas_10):
        df = pd.read_csv(f'{MYDIR_WORKER}{result}.csv')
        df_our_coin.append(df)
        df_5min = pd.read_csv(f'{MYDIR_5MIN}{result}.csv')
        df_our_coin_5min.append(df_5min)
        canvas_mas.insert(count_mas, Canvas(frame_2_set2_graph, width = width_canvas, height = height_canvas, bg = "#2B2B2B", cursor = "pencil",border=0,bd=0,highlightthickness=0))
        customtkinter.CTkLabel(frame_2_set2_graph, text=result, fg_color="transparent",anchor='center',font=('Arial',14,'bold')).pack(pady=1, anchor='w')
        canvas_mas[count_mas].pack(pady=10)	
        canvas_mas[count_mas].create_line(10,height_canvas,10,0,width=1,arrow=LAST) 
        canvas_mas[count_mas].create_line(0,height_canvas-10,width_canvas,height_canvas-10,width=1,arrow=LAST) 
        count_mas = count_mas+1
        
    for index in range(VOLUME):
        data_numbers.append(index)
        if index>4: # начинаем не с нуля, а с 5-ой свечи
            if open_sl == False: # если нет позиции
                coutnt_index_time_df = 0
                for x,result in enumerate(coin_mas_10):
                    prices_old = get_df_coin(result)
                    prices = prices_old.iloc[data_numbers] # берем из фрема свечи по текущий шаг итерации
                    paint_bar(canvas_mas[x],prices.iloc[-1:],prices_old)
                    trend = check_if_signal(prices,index)
                    if trend != 'нет сигнала':
                        canvas_coin = canvas_mas[x]
                        symbol = result  
                        time_close_tf = prices.iloc[[index]]['close_time'][index]
                        break
                    else:
                        trend = "нет сигнала"                
                if trend != "нет сигнала" and prices.iloc[index]['VOLUME']>CANDLE_COIN_MIN and prices.iloc[index]['VOLUME']<CANDLE_COIN_MAX:
                    paint_trade(canvas_coin,trend,index,prices.iloc[index]['close'],prices_old)
                    open_position(trend,get_trade_VOLUME(prices.iloc[index]['close']),prices.iloc[index]['close'],frame_3_set4_1_1_1) # если есть сигнал и мы не стоим в позиции, то открываем позицию
            if open_sl == True:
                for x,result in enumerate(coin_mas_10):
                    prices_old = get_df_coin(result)
                    prices = prices_old.iloc[data_numbers]
                    paint_bar(canvas_mas[x],prices.iloc[-1:],prices_old)
                for index_5min in get_price_5min(time_close_tf):
                    price_now = get_df_coin_now_price(index_5min)
                    if price_now != 0:
                        if check_trade(price_now,frame_3_set4_1_1_1): # следим за монетой, отрабатываем тп и сл
                            break
                    else:
                        break       
        if DEPOSIT < 40:
            break
    for x,result in enumerate(coin_mas_10):
        prices_old = get_df_coin(result)
        paint_bar(canvas_mas[x],prices_old,prices_old)
    print_components_log('Закончил торговлю',frame_3_set4_1_1_1,'HT')
    for widget in frame_3_set4_1_2.winfo_children():
        widget.forget()
    customtkinter.CTkLabel(frame_3_set4_1_2, text=f"Начальный депозит: {DEPOSIT_START}$", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
    customtkinter.CTkLabel(frame_3_set4_1_2, text=f"Конечный депозит: {round(DEPOSIT,1)}$", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
    customtkinter.CTkLabel(frame_3_set4_1_2, text=f"Процент торговли: {round(float((float(DEPOSIT/DEPOSIT_START)-1)*100),1)}", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
    customtkinter.CTkLabel(frame_3_set4_1_2, text=f"Сделок совершено: {count_long_take+count_long_loss+count_short_take+count_short_loss}", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
    customtkinter.CTkLabel(frame_3_set4_1_2, text=f"+ в лонг: {count_long_take} | + в шорт: {count_short_take}", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
    customtkinter.CTkLabel(frame_3_set4_1_2, text=f"- в лонг: {count_long_loss} | - в шорт: {count_short_loss}", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
    customtkinter.CTkLabel(frame_3_set4_1_2, text=f"Прибыль от сделок: {round(profit,1)}$", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
    customtkinter.CTkLabel(frame_3_set4_1_2, text=f"Убыток от сделок: {round(loss,1)}$", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
    customtkinter.CTkLabel(frame_3_set4_1_2, text=f"Комиссия биржи: {round(commission,1)}$", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')   













