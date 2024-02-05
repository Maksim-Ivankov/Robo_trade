import os
import sys
sys.path.insert(1,os.path.join(sys.path[0],'../'))
from imports import *
import _thread
from models.tg import *

TF = '5m' # таймфрейм
wait_time = 5 # сколько минут ждать для обновления цены с биржи
TP = 0.012 # Тейк профит, процент
SL = 0.004 # Стоп лосс, процент
DEPOSIT = 100 # Депозит
DEPOSIT_START = DEPOSIT
LEVERAGE = 20 # торговое плечо
COMMISSION_MAKER = 0.002 # комиссия а вход
COMMISSION_TAKER = 0.001 # комиссия на выхд
VOLUME = 48 # сколько свечей получить при запросе к бирже
VOLUME_5MIN = 144
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
symbol = 'btcusdt' 
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
tg_message = ''
name_bot = ''
client = UMFutures(key=key, secret=secret)

flag_trade_real_test = True


def start_real_test_trade_model_thread_1(name_bot_real_test,sost_tg_message,real_test_frame_3_1_1,real_test_frame_3_2_1):
    global tg_message
    global name_bot
    name_bot = name_bot_real_test
    tg_message = sost_tg_message
    print(f'реал тест имя бота- {name_bot}')
    print(f'реал тест сост тг- {tg_message}')
    try:
        thread25 = threading.Thread(target=lambda:start_real_test_trade_model(real_test_frame_3_1_1,real_test_frame_3_2_1))
        thread25.start()
    except Exception as e:
        messagebox.showinfo('Внимание','Ошибка начала торговли')
    

# Получите последние n свечей по n минут для торговой пары, обрабатываем и записывае данные в датафрейм
def get_futures_klines(symbol,TF,VOLUME):
    try:
        print(symbol)
        print(TF)
        print(VOLUME) 
        time.sleep(2)
        x = requests.get('https://fapi.binance.com/fapi/v1/klines?symbol='+symbol.lower()+'&limit='+str(VOLUME)+'&interval='+TF)
        print(x)
        df=pd.DataFrame(x.json())
        df.columns=['open_time','open','high','low','close','VOLUME','close_time','d1','d2','d3','d4','d5']
        df=df.drop(['d1','d2','d3','d4','d5'],axis=1)
        df['open']=df['open'].astype(float)
        df['high']=df['high'].astype(float)
        df['low']=df['low'].astype(float)
        df['close']=df['close'].astype(float)
        df['VOLUME']=df['VOLUME'].astype(float)
        print(df)
        return(df) # возвращаем датафрейм с подготовленными данными
    except Exception as e:
        messagebox.showinfo('Внимание',f'Ошибка запроса данных с бинанса - {e}')
        print(e)



# Получаем активные монеты на бирже
def get_top_coin():
    try:
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
    except Exception as e:
        messagebox.showinfo('Внимание','Ошибка получения активных монет с биржи')

# определяем размер позиции, на которую должны зайти
def get_trade_VOLUME(get_symbol_price):
    try:
        volume = round(float(DEPOSIT)*float(LEVERAGE)/float(get_symbol_price))
        return volume
    except Exception as e:
        messagebox.showinfo('Внимание','Ошибка определения размера позиции')

# логи в прогу
def print_components_log(msg,frame,type):
    global data_print_ad_df
    global number_print_df
    global number_print_ht
    global data_print_ad_ht
    global tg_message
    global name_bot
    if type == 'OS1':
        print('Сработали логи')
        if tg_message == 'on':
            print('Отправляем в тг')
            print(f'{name_bot} - {msg}')
            print_tg(name_bot,msg)
        number_print_df=number_print_df+1
        for widget in frame.winfo_children():
                widget.forget()
        data_print_ad_df.insert(0,customtkinter.CTkLabel(frame, text=str(number_print_df)+'. '+str(time.strftime("%H:%M:%S", time.localtime()))+' '+msg, fg_color="#DAE2EC",text_color='#242424',anchor='w',font=('Arial',12,'normal')))
        for component in data_print_ad_df:
            component.pack(anchor="w")
    if type == 'WS':
        number_print_ht=number_print_ht+1
        for widget in frame.winfo_children():
                widget.forget()
        data_print_ad_ht.insert(0,customtkinter.CTkLabel(frame, text=str(time.strftime("%H:%M:%S", time.localtime()))+'. '+ msg, fg_color="#DAE2EC",text_color='#242424',anchor='w',font=('Arial',12,'normal')))
        for component in data_print_ad_ht:
            component.pack(anchor="w")
        

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
def open_position(trend,value,price,real_test_frame_3_2_1):
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
    print_components_log(f'Открыл {signal_trade}, монета {coin_trade}, цена {price_trade}',real_test_frame_3_2_1,'OS1')
    print(f'Открыл {signal_trade}, монета {coin_trade}, цена {price_trade}')
    take_profit_price = get_take_profit(trend,price_trade) # получаем цену тэйк профита
    stop_loss_price = get_stop_loss(trend,price_trade) # получаем цену стоп лосса
    print_components_log(f'Тейк - {take_profit_price} | Стоп - {stop_loss_price}',real_test_frame_3_2_1,'OS1')
    print(f'Тейк - {take_profit_price} | Стоп - {stop_loss_price}')

def get_take_profit(trend,price_trade): # получаем цену тейк профита в зависимости от направления
    if trend == 'long':
        return float(float(price_trade)*(1+float(TP)))
    if trend == 'short':
        return float(float(price_trade)*(1-float(TP)))
def get_stop_loss(trend,price_trade): # получаем цену стоп лосса в зависимости от направления
    if trend == 'long':
        return float(float(price_trade)*(1-float(SL)))
    if trend == 'short':
        return float(float(price_trade)*(1+float(SL)))
    
# Закрываем сделку
def close_trade(status,procent,real_test_frame_3_2_1):
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
        print_components_log(f'Сработал ТЕЙК|Депо={round(DEPOSIT,1)}, профит={round(profit,1)},ком={round(commission,1)}',real_test_frame_3_2_1,'OS1')
        print(f'Сработал ТЕЙК|Депо={round(DEPOSIT,1)}, профит={round(profit,1)},ком={round(commission,1)}')
    if status == '-': # если закрыли в минус
        loss = loss + LEVERAGE*DEPOSIT*procent
        commission = commission + LEVERAGE*DEPOSIT*(COMMISSION_MAKER+COMMISSION_TAKER)
        DEPOSIT = DEPOSIT - LEVERAGE*DEPOSIT*procent - LEVERAGE*DEPOSIT*(COMMISSION_MAKER+COMMISSION_TAKER) # обновляем размер депо
        open_sl = False
        print_components_log(f'Сработал СТОП|Депо={round(DEPOSIT,1)}, убыток={round(loss,1)},ком={round(commission,1)}',real_test_frame_3_2_1,'OS1')

def check_trade(price,real_test_frame_3_2_1):
    now_price_trade = price #получаем текущую цену монеты
    global count_long_take
    global count_long_loss
    global count_short_take
    global count_short_loss
    global take_profit_price
    global stop_loss_price
    if signal_trade == 'long':
        if float(now_price_trade)>float(take_profit_price):
            close_trade('+',TP,real_test_frame_3_2_1)
            count_long_take=count_long_take+1
            return 1
        if float(now_price_trade)<float(stop_loss_price):
            count_long_loss = count_long_loss + 1
            close_trade('-',SL,real_test_frame_3_2_1)
            return 1
    if signal_trade == 'short':
        if float(now_price_trade)<float(take_profit_price):
            close_trade('+',TP,real_test_frame_3_2_1)
            count_short_take = count_short_take+1
            print('лол - 18')
            return 1
        if float(now_price_trade)>float(stop_loss_price):
            count_short_loss = count_short_loss + 1
            close_trade('-',SL,real_test_frame_3_2_1)
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

def get_price_now_coin(symbol):
    try:
        key = "https://fapi.binance.com/fapi/v1/ticker/price?symbol="+symbol
        data = requests.get(key)   
        data = data.json() 
        price = data['price']
        print(f'{symbol} - {price}')
        return price
    except Exception as e:
        print('Ошибка запроса цены для открытия сделки')
        print(e)
         

def websocket_trade(real_test_frame_3_1_1,real_test_frame_3_2_1):
    try:
        url = 'wss://fstream.binance.com/stream?streams='+symbol.lower()+'@miniTicker'
        with connect(url) as ws:
            while True:        
                try:
                    data = json.loads(ws.recv())['data']
                    print_components_log(data['c'],real_test_frame_3_1_1,'WS')
                    if check_trade(data['c'],real_test_frame_3_2_1): # следим за монетой, отрабатываем тп и сл
                        print_components_log('----------------',real_test_frame_3_1_1,'WS')
                        break
                except websockets.exceptions.ConnectionClosed:
                    break
    except Exception as e:
        messagebox.showinfo('Внимание','Ошибка работы вебсокетов')

# -------------------------------------- Перебор по датафрейму --------------------------------------



def start_real_test_trade_model(real_test_frame_3_1_1,real_test_frame_3_2_1):
    try:
        print_components_log(f'Начали торговлю',real_test_frame_3_2_1,'OS1')
        print('Стартуем')
        global coin_mas_10
        global symbol
        event = threading.Event()
        coin_mas_10 = get_top_coin()
        while True:
            try:     
                if open_sl == False:
                    for x,result in enumerate(coin_mas_10):
                        prices = get_futures_klines(result,TF,30)
                        time.sleep(2)
                        trend = check_if_signal(prices,30)
                        time.sleep(2) # Интервал в 2 секунд, чтобы бинанс не долбить
                        print_components_log(f'Монета - {result}, {trend}',real_test_frame_3_2_1,'OS1')
                        if trend != 'нет сигнала':
                            symbol = result
                            print('СИГНАЛ!')
                            break
                    if trend == "нет сигнала":
                        print_components_log(f'Нет сигналов. Ждём {wait_time*2} минут',real_test_frame_3_2_1,'OS1')
                        # timeout = time.time() + wait_time*2*60  # время, которое будет работать скрипт
                        # while time.time()< timeout:
                        #     event.wait()    
                        # event.set()
                        time.sleep(120)
                        # time.sleep(wait_time*2) # Двойной интервал, если нет сигнала
                    else:
                        print('Сделка!')
                        price__now = get_price_now_coin(symbol)
                        print(price__now)
                        vol_trade = get_trade_VOLUME(price__now)
                        print(vol_trade)
                        open_position(trend,vol_trade,price__now,real_test_frame_3_2_1) # если есть сигнал и мы не стоим в позиции, то открываем позицию
                if open_sl == True:  
                    websocket_trade(real_test_frame_3_1_1,real_test_frame_3_2_1)
                    print_components_log(f'Ждём {wait_time*2} минут',real_test_frame_3_2_1,'OS1')
                    # timeout = time.time() + wait_time*2*60  # время, которое будет работать скрипт
                    # while time.time()< timeout:
                    #     event.wait()    
                    # event.set()    
                    time.sleep(120)
                if DEPOSIT < 40:
                    break
            except KeyboardInterrupt: #
                print_components_log(f'Завершили торговлю',real_test_frame_3_2_1,'OS1')
                print("СЛОМАЛИ!!!!!!!!!!")
                break
    except Exception as e:
        messagebox.showinfo('Внимание',f'Ошибка работы основного цикла торговли - - {e}')
        print(e)
            
            
            