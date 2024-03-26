from tkinter import *
from math import *
import os
import sys
sys.path.insert(1,os.path.join(sys.path[0],'../'))
from imports import *
import strategy.strategys.strat_1 as str_1


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
STEP_5_min_VALUE = 5
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

#--------------------

# Следим за ценой {wait_time*VOLUME/VOLUME_5MIN}мин
# Рабочий таймфрейм {wait_time}мин
# Длительность {wait_time*VOLUME/60}ч
# Сколько монет торговать {how_mach_coin}
# Ком мейк {COMMISSION_MAKER*100}%
# Ком тейк {COMMISSION_TAKER*100}%
# Тейк {TP*100}%
# Стоп {SL*100}%
# Депо {DEPOSIT}$
# Плечо {LEVERAGE}
# Объём торгов мин {CANDLE_COIN_MIN}
# Объём торгов макс {CANDLE_COIN_MAX}
# Верх канала {CANAL_MAX*100}%
# Низ канала {CANAL_MIN*100}%
# Угол лонг {CORNER_LONG}
# Угол шорт {CORNER_SHORT}
# 
# 
# 
# 

#--------------------


how_mach_coin = 10

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

summ_strat = {}

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
    global how_mach_coin
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
        if i== int(how_mach_coin):
            break
    i=0
    for key, value in coin_min.items():
        i=i+1
        coin_mas2[key] = value
        if i==1:
            coin_min_val = value
        if i== int(how_mach_coin):
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

# принтуем логи в файл
def print_log(msg):
    global data_print_ad_df
    global number_print_df
    global number_print_ht
    global data_print_ad_ht
    path ='H_log.txt'
    f = open(path,'a',encoding='utf-8')
    f.write('\n'+time.strftime("%d.%m.%Y | %H:%M:%S | ", time.localtime())+msg)
    f.close()
     
                  
# принтуем логи в фрейм в гуи и логи
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

# генерируем фремы в файлы по кнопке с первого этапа
def generate_dataframe(TF,VOLUME,VOLUME_5MIN,frame_2_set2_3,work_timeframe_str_HM,frame_2_set2_2_1):
    global coin_mas_10
    for widget in frame_2_set2_2_1.winfo_children(): # чистим табличку
        widget.destroy()
    print_components_log('Начали сбор данных',frame_2_set2_3,'DF')
    coin_mas_10 = get_top_coin() # один раз запускаем функцию, чтобы обновить монету, с которой работаем
    open(MYDIR_COIN, "w").close()
    open(MYDIR_COIN_PROCENT, "w").close()
    fi1 = open(MYDIR_COIN,'a',encoding='utf-8')
    fi2 = open(MYDIR_COIN_PROCENT,'a',encoding='utf-8')
    arr_coin = []
    arr_coin_procent = []
    i=-1
    for key, value in coin_mas_10.items():
        arr_coin.append(key)
        arr_coin_procent.append(f'{key}: {value}')
        i=i+1
        customtkinter.CTkButton(frame_2_set2_2_1, text=f'{key}: {value}').grid(row=i, column=0, sticky="ew",pady=5)
    result_as_list1 = '|'.join(arr_coin)
    result_as_list2 = '|'.join(arr_coin_procent)
    fi1.write(result_as_list1)
    fi1.close()
    fi2.write(result_as_list2)
    fi2.close()
    # выше записываем файл с монетами роста + монеты роста и проценты
    remove_csv(MYDIR_WORKER)
    remove_csv(MYDIR_5MIN)
    # if coin_mas_10:
    #     i=-1
    #     for coin in coin_mas_10:
    #         i=i+1
    #         customtkinter.CTkButton(frame_2_set2_2_1, text=coin).grid(row=i, column=0, sticky="ew",pady=5)
    for x,result in enumerate(coin_mas_10):
        print(f'{result},{TF},{VOLUME}')
        df = get_futures_klines(result,TF,VOLUME)
        df.to_csv(f'{MYDIR_WORKER}{result}.csv')
        print_components_log(f'{result} - {TF}/{work_timeframe_str_HM} добавлен',frame_2_set2_3,'DF')
        time.sleep(2)
        df_5m = get_futures_klines(result,work_timeframe_str_HM,VOLUME_5MIN)
        df_5m.to_csv(f'{MYDIR_5MIN}{result}.csv')
        time.sleep(2)
    print_components_log(f'Датафреймы добавлены!',frame_2_set2_3,'DF')
    return coin_mas_10


# -------------------------------------- ТОРГОВЛЯ --------------------------------------

# открывает лонг или шорт
def open_position(trend,value,price):
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
    # print_components_log(f'Открыл {signal_trade}, монета {coin_trade}, цена {price_trade}',frame_3_set4_1_1_1,'HT')
    take_profit_price = get_take_profit(trend,price_trade) # получаем цену тэйк профита
    stop_loss_price = get_stop_loss(trend,price_trade) # получаем цену стоп лосса

# получаем цену тейк профита в зависимости от направления
def get_take_profit(trend,price_trade): 
    if trend == 'long':
        return price_trade*(1+TP)
    if trend == 'short':
        return price_trade*(1-TP)

# получаем цену стоп лосса в зависимости от направления
def get_stop_loss(trend,price_trade): 
    if trend == 'long':
        return price_trade*(1-SL)
    if trend == 'short':
        return price_trade*(1+SL)
    
# Закрываем сделку
def close_trade(status,procent):
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
        # print_components_log(f'Сработал ТЕЙК|Депо={round(DEPOSIT,1)}, профит={round(profit,1)},ком={round(commission,1)}',frame_3_set4_1_1_1,'HT')
    if status == '-': # если закрыли в минус
        loss = loss + LEVERAGE*DEPOSIT*procent
        commission = commission + LEVERAGE*DEPOSIT*(COMMISSION_MAKER+COMMISSION_TAKER)
        DEPOSIT = DEPOSIT - LEVERAGE*DEPOSIT*procent - LEVERAGE*DEPOSIT*(COMMISSION_MAKER+COMMISSION_TAKER) # обновляем размер депо
        open_sl = False
        print(f'СТОП В - | {DEPOSIT}')
        # print_components_log(f'Сработал СТОП|Депо={round(DEPOSIT,1)}, убыток={round(loss,1)},ком={round(commission,1)}',frame_3_set4_1_1_1,'HT')

# когда в сделке - чекаем, словили тп или сл
def check_trade(price):
    now_price_trade = price #получаем текущую цену монеты
    global count_long_take
    global count_long_loss
    global count_short_take
    global count_short_loss
    global take_profit_price
    global stop_loss_price
    if signal_trade == 'long':
        if float(now_price_trade)>float(take_profit_price):
            close_trade('+',TP)
            count_long_take=count_long_take+1
            return 1
        if float(now_price_trade)<float(stop_loss_price):
            count_long_loss = count_long_loss + 1
            close_trade('-',SL)
            return 1
    if signal_trade == 'short':
        if float(now_price_trade)<float(take_profit_price):
            close_trade('+',TP)
            count_short_take = count_short_take+1
            return 1
        if float(now_price_trade)>float(stop_loss_price):
            count_short_loss = count_short_loss + 1
            close_trade('-',SL)
            return 1
# # когда в сделке - чекаем, словили тп или сл
# def check_trade(price,frame_3_set4_1_1_1):
#     now_price_trade = price #получаем текущую цену монеты
#     global count_long_take
#     global count_long_loss
#     global count_short_take
#     global count_short_loss
#     global take_profit_price
#     global stop_loss_price
#     if signal_trade == 'long':
#         if float(now_price_trade)>float(take_profit_price):
#             close_trade('+',TP,frame_3_set4_1_1_1)
#             count_long_take=count_long_take+1
#             return 1
#         if float(now_price_trade)<float(stop_loss_price):
#             count_long_loss = count_long_loss + 1
#             close_trade('-',SL,frame_3_set4_1_1_1)
#             return 1
#     if signal_trade == 'short':
#         if float(now_price_trade)<float(take_profit_price):
#             close_trade('+',TP,frame_3_set4_1_1_1)
#             count_short_take = count_short_take+1
#             return 1
#         if float(now_price_trade)>float(stop_loss_price):
#             count_short_loss = count_short_loss + 1
#             close_trade('-',SL,frame_3_set4_1_1_1)
#             return 1
# -------------------------------------- ТОРГОВЛЯ --------------------------------------
# -------------------------------------- СТРАТЕГИЯ --------------------------------------

# точка входа в стратегии
def check_if_signal(prices,index,strat_mas_historical):
    global TF
    global summ_strat,DEPOSIT
    for strat in strat_mas_historical: # перебор по id выбранных стратегий
        match strat:
            case 'strat1' : summ_strat['Канал, тренд, локаль, объём'] = get_strat_1(prices,index)
            case 'strat2' : pass
            case 'strat3' : pass
            case 'strat4' : pass
            case 'strat5' : pass
            case 'strat6' : pass
            case 'strat7' : pass
            case 'strat8' : pass
            case 'strat9' : pass
            case 'strat10': pass
            case 'strat11': pass
            case 'strat12': pass
            case 'strat13': pass
            case 'strat14': pass
            case 'strat15': pass
            case 'strat16': pass
            case 'strat17': pass
            case 'strat18': pass
            case 'strat19': pass
            case 'strat20': pass
            case 'strat21': pass
            case 'strat22': pass
            case 'strat23': pass
            case 'strat24': pass
            case 'strat25': pass
    # print_components_log(f'Рекомендации стратегий - {summ_strat}',real_test_frame_3_2_1,'OS1')
    strat_long = 0
    strat_short = 0
    strat_neutral = 0
    for trend in summ_strat.values():
        if trend == 'long': 
            strat_long = strat_long + 1
        if trend == 'short': 
            strat_short = strat_short + 1
        if trend == 'нет сигнала': 
            strat_neutral = strat_neutral + 1
    # print(f'Лонг - {strat_long} | Шорт - {strat_short} | Нейтрально - {strat_neutral}')
    # print_components_log(f'Лонг - {strat_long} | Шорт - {strat_short} | Нейтрально - {strat_neutral}',real_test_frame_3_2_1,'OS1')
    print(f'Шаг - {index} | Депозит {DEPOSIT} | Лонг - {strat_long} | Шорт - {strat_short} | Нейтрально - {strat_neutral}')
    if strat_long == len(summ_strat): return 'long'
    elif strat_short == len(summ_strat): return 'short'
    else : return 'нет сигнала'
    
    
def get_strat_1(prices,index):
    try:
        return str_1.strat_1(prices,index) 
    except Exception as e:
        # print_components_log(f'Ошибка работы стратегии Канал, тренд, локаль, объём! - {e}',real_test_frame_3_2_1,'OS1')
        return 'нет сигнала'
# -------------------------------------- СТРАТЕГИЯ --------------------------------------

# удаление всех файлов csv в переданной директории
def remove_csv(dir):
    filelist = [ f for f in os.listdir(dir) if f.endswith(".csv") ]
    for f in filelist:
        os.remove(os.path.join(dir, f))
        
# получаем датафрейм по монете из обзего массива датафреймов
def get_df_coin(coin):
    global symbol
    for x,result in enumerate(coin_mas_10):
        if result == coin:
            symbol = coin
            return df_our_coin[x]

# получаем цену закрытия из фрейма по монете в сделке по индексу фрейма
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

# точка входа
def start_trade_hist_model(strat_mas_historical):
    global coin_mas_10,symbol,time_close_tf,STEP_5_min_VALUE,DEPOSIT,open_sl,data_numbers,DEPOSIT
    open_sl = False
    DEPOSIT = 100
    print(f'{VOLUME} | {VOLUME_5MIN} | {STEP_5_min_VALUE} | CANDLE_COIN_MIN - {CANDLE_COIN_MIN} | CANDLE_COIN_MAX - {CANDLE_COIN_MAX}')
    data_numbers = []
    fi = open(MYDIR_COIN,'r') # открываем файл с монетами
    coin_mas_10 = fi.read().split('|') # записываем омнеты массивом сюда
    fi.close()
    for index in range(VOLUME):
        print(f'Шаг - {index} | Депозит {DEPOSIT}')
        data_numbers.append(index) # добавляем в массив номера итераций - 0,1,2,3 - имитируем реальную торговлю
        if index>10: # начинаем не с нуля, а с 5-ой свечи
            if open_sl == False: # если нет позиции
                for x,result in enumerate(coin_mas_10):
                    df = pd.read_csv(f'{MYDIR_WORKER}{result}.csv') # получили датафрейм из файла
                    prices = df.iloc[data_numbers]
                    # print(f"{prices['VOLUME'][index]}>{CANDLE_COIN_MIN} and {prices['VOLUME'][index]}<{CANDLE_COIN_MAX}")
                    if prices['VOLUME'][index]>CANDLE_COIN_MIN and prices['VOLUME'][index]<CANDLE_COIN_MAX:
                        trend = check_if_signal(prices,index,strat_mas_historical) # определяем тренд - стратегия
                        if trend != 'нет сигнала': # если есть сигнал
                            symbol = result # сохраняем монету с сигналом
                            time_close_tf = prices['close_time'][index]
                            break
                        else:
                            trend = "нет сигнала"  
                    else:
                        trend = "нет сигнала"  
                        print('Не прошли по объёму')
                # если получили сигнал и объём за свечку больше минимального объема (настройка) и меншье максимального объёма (настройка)  
                if trend != "нет сигнала":
                    # если есть сигнал, то открываем позицию - направление, объём, цена входа, 
                    print('СДЕЛКА!!!!!')
                    open_position(trend,get_trade_VOLUME(prices['close'][index]),prices['close'][index])   
            else: #если есть позиция
                df = pd.read_csv(f'{MYDIR_WORKER}{symbol}.csv') # получили датафрейм из файла
                prices = df.iloc[data_numbers]
                df_mal = pd.read_csv(f'{MYDIR_5MIN}{result}.csv') # получили датафрейм мини из файла
                for index2, row in df_mal.iterrows(): # находим индекс, с которого начгнем следить за ценой
                    if row['close_time'] == prices['close_time'][index]:
                        if int(index2)>int(VOLUME_5MIN)-int(STEP_5_min_VALUE)-5:
                            print('В сделке, но в конце массива, выходим из сделки')
                            break
                        for i in range(int(index2),int(index2)+int(STEP_5_min_VALUE),1):
                            # print(f'{i} - {df_mal['close'][i]}|{price_trade} | {(float(df_mal['close'][i])/float(price_trade))*100}%')
                            if check_trade(df_mal['close'][i]): break # чекаем монету по шагам итерации между большим и мальеньким фреймом
            if float(DEPOSIT)/float(DEPOSIT_START) < 0.4:
                print('Слили депозит! Торговля закончена')
                break
    print('Закончили')
                    

# точка входа
def start_trade_hist_model2(strat_mas_historical):
    global coin_mas_10
    global symbol
    global coutnt_index_time_df
    global trend
    global time_close_tf
    print('Начали торговлю')
    # print_components_log('Начали торговлю',frame_3_set4_1_1_1,'HT')
    # print_components_log(f'Настройки:\nДепозит:{DEPOSIT} | Плечо:{LEVERAGE} | Комиссия покупка:{COMMISSION_MAKER}\nКомиссия продажа:{COMMISSION_TAKER} | Тейк:{TP} | Стоп:{SL} | Канал верх:{CANAL_MAX}\nКанал низ:{CANAL_MIN} | Угол лонг:{CORNER_LONG} | Угол шорт:{CORNER_SHORT} | Объём мин:{CANDLE_COIN_MIN}\nОбъём макс:{CANDLE_COIN_MAX} | Объём основа:{VOLUME} | Объём 5 мин: {VOLUME_5MIN}',frame_3_set4_1_1_1,'HT')
    
    fi = open(MYDIR_COIN,'r') # открываем файл с монетами
    coin_mas_10 = fi.read().split('|') # записываем омнеты массивом сюда
    fi.close()
    count_mas = 0
    for x,result in enumerate(coin_mas_10): # В цикле сохраняем ДФ всех монет в обзем массиве
        df = pd.read_csv(f'{MYDIR_WORKER}{result}.csv') # получили датафрейм из файла
        df_our_coin.append(df) # добавили в массив всех фреймов
        df_5min = pd.read_csv(f'{MYDIR_5MIN}{result}.csv') # получили датафрйм слежения за ценой по текущей монете
        df_our_coin_5min.append(df_5min) # и так же сохранили его в файл
        count_mas = count_mas+1
    for index in range(VOLUME):  # перебор по клдичеству свечей в фрейме
        data_numbers.append(index) # добавляем в массив номера итераций - 0,1,2,3 - имитируем реальную торговлю
        if index>4: # начинаем не с нуля, а с 5-ой свечи
            if open_sl == False: # если нет позиции
                coutnt_index_time_df = 0
                for x,result in enumerate(coin_mas_10): # снова бежим по монетам
                    prices_old = get_df_coin(result) # получеам датафрейм по текущей монете
                    prices = prices_old.iloc[data_numbers] # берем из фрема свечи по текущий шаг итерации
                    trend = check_if_signal(prices,index,strat_mas_historical) # определяем тренд - стратегия
                    if trend != 'нет сигнала': # если есть сигнал
                        # canvas_coin = canvas_mas[x]
                        symbol = result # сохраняем монету с сигналом
                        time_close_tf = prices['close_time'][index]
                        break
                    else:
                        trend = "нет сигнала"           
                # если получили сигнал и объём за свечку больше минимального объема (настройка) и меншье максимального объёма (настройка)  
                if trend != "нет сигнала" and prices['VOLUME'][index]>CANDLE_COIN_MIN and prices['VOLUME'][index]<CANDLE_COIN_MAX:
                    # если есть сигнал, то открываем позицию - направление, объём, цена входа, 
                    print('СДЕЛКА!!!!!')
                    open_position(trend,get_trade_VOLUME(prices['close'][index]),prices['close'][index]) 
            if open_sl == True:
                for x,result in enumerate(coin_mas_10): # еще раз получаем фрейм по монете по текущий шаг (зачем?)
                    prices_old = get_df_coin(result)
                    prices = prices_old.iloc[data_numbers]
                for index_5min in get_price_5min(time_close_tf): # дальше какое-то волшебство
                    price_now = get_df_coin_now_price(index_5min)
                    if price_now != 0:
                        if check_trade(price_now): # следим за монетой, отрабатываем тп и сл
                            break
                    else:
                        break       
        if float(DEPOSIT)/float(DEPOSIT_START) < 0.4:
            break
    print('Закончили торговлю')
    # print_components_log('Закончил торговлю',frame_3_set4_1_1_1,'HT')
    # for widget in frame_3_set4_1_2.winfo_children():
    #     widget.forget()
    # customtkinter.CTkLabel(frame_3_set4_1_2, text=f"Начальный депозит: {DEPOSIT_START}$", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
    # customtkinter.CTkLabel(frame_3_set4_1_2, text=f"Конечный депозит: {round(DEPOSIT,1)}$", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
    # customtkinter.CTkLabel(frame_3_set4_1_2, text=f"Процент торговли: {round(float((float(DEPOSIT/DEPOSIT_START)-1)*100),1)}", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
    # customtkinter.CTkLabel(frame_3_set4_1_2, text=f"Сделок совершено: {count_long_take+count_long_loss+count_short_take+count_short_loss}", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
    # customtkinter.CTkLabel(frame_3_set4_1_2, text=f"+ в лонг: {count_long_take} | + в шорт: {count_short_take}", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
    # customtkinter.CTkLabel(frame_3_set4_1_2, text=f"- в лонг: {count_long_loss} | - в шорт: {count_short_loss}", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
    # customtkinter.CTkLabel(frame_3_set4_1_2, text=f"Прибыль от сделок: {round(profit,1)}$", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
    # customtkinter.CTkLabel(frame_3_set4_1_2, text=f"Убыток от сделок: {round(loss,1)}$", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
    # customtkinter.CTkLabel(frame_3_set4_1_2, text=f"Комиссия биржи: {round(commission,1)}$", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')   













