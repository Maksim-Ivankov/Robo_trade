from tkinter import *
from math import *
import os
import sys
sys.path.insert(1,os.path.join(sys.path[0],'../'))
from imports import *
import strategy.strategys.strat_1 as str_1
import strategy.strategys.strat_2 as str_2
import graph_by.graph_historical as graph
from texttable import Texttable
import progressbar
from CTkTable import *
import models.big_anal as biganal


TF = '5m' # таймфрейм
wait_time = 5 # сколько минут ждать для обновления цены с биржи
TP = 0.012 # Тейк профит, процент
SL = 0.004 # Стоп лосс, процент
DEPOSIT = 100 # Депозит
DEPOSIT_GLOBAL = DEPOSIT
DEPOSIT_START = DEPOSIT_GLOBAL
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
INDEX_START = 20
str_2.INDEX_START = INDEX_START


trend = "нет сигнала"  
how_mach_coin = 10

data_for_table_trade_regime_1 = [['Монета','Шаг','Тренд','TP','SL','Результат','Депозит',]]
set_our_settings = []
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
name_bot_historical = ''
summ_strat = {}
OUR_SETTINGS_MAS_STRAT_1 = []
regime_work = 0

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
def get_trade_VOLUME(get_symbol_price,DEPOSIT,LEVERAGE):
    vol = round(DEPOSIT*LEVERAGE/get_symbol_price)
    return vol

# удаление всех файлов csv в переданной директории
def remove_csv(dir):
    filelist = [ f for f in os.listdir(dir) if f.endswith(".csv") ]
    for f in filelist:
        os.remove(os.path.join(dir, f))
        
# удаление всех файлов txt в переданной директории
def remove_txt(dir):
    filelist = [ f for f in os.listdir(dir) if f.endswith(".txt") ]
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
    f.write('\n'+msg)
    f.close()
    
# создаем файл с торговлей по текущим настройкам для сета настроек
def print_trade_file(number,treyd):
    path =f'DF/hist_strat_1_trade/{number}.txt'
    f = open(path,'a',encoding='utf-8')
    f.write('\n'+treyd)
    f.close()
                
# принтуем в логи гуи
def print_components_log(msg,frame,type):
    global data_print_ad_df
    global number_print_df
    global number_print_ht
    global data_print_ad_ht
    if type == 'DF':
        number_print_df=number_print_df+1
        for widget in frame.winfo_children():
                widget.forget()
        data_print_ad_df.insert(0,customtkinter.CTkLabel(frame, text=str(number_print_df)+'. '+ msg, fg_color="#DAE2EC",text_color='#242424',anchor='w',font=('Arial',12,'normal')))
        for component in data_print_ad_df:
            component.pack(anchor="w")
    # if type == 'HT':
    #     number_print_ht=number_print_ht+1
    #     for widget in frame.winfo_children():
    #             widget.forget()
    #     data_print_ad_ht.insert(0,customtkinter.CTkLabel(frame, text=str(number_print_ht)+'. '+ msg, fg_color="#DAE2EC",text_color='#242424',anchor='w',font=('Arial',12,'normal')))
    #     for component in data_print_ad_ht:
    #         component.pack(anchor="w")          

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
def open_position(trend,value,price,SL,TP):
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
    take_profit_price = get_take_profit(trend,price_trade,TP) # получаем цену тэйк профита
    stop_loss_price = get_stop_loss(trend,price_trade,SL) # получаем цену стоп лосса

# получаем цену тейк профита в зависимости от направления
def get_take_profit(trend,price_trade,TP): 
    if trend == 'long':
        return price_trade*(1+TP)
    if trend == 'short':
        return price_trade*(1-TP)

# получаем цену стоп лосса в зависимости от направления
def get_stop_loss(trend,price_trade,SL): 
    if trend == 'long':
        return price_trade*(1-SL)
    if trend == 'short':
        return price_trade*(1+SL)
    
# Закрываем сделку
def close_trade(status,procent,COMMISSION_MAKER,COMMISSION_TAKER,DEPOSIT,LEVERAGE):
    global open_sl
    global profit
    global loss
    global commission
    global status_trade_close,DEPOSIT_GLOBAL,place_open_position_profit
    status_trade_close = status
    if status == '+': # если закрыли в плюс
        profit = profit + LEVERAGE*DEPOSIT_GLOBAL*procent
        commission = commission + LEVERAGE*DEPOSIT_GLOBAL*(COMMISSION_MAKER+COMMISSION_TAKER)
        DEPOSIT_GLOBAL = DEPOSIT_GLOBAL + LEVERAGE*DEPOSIT_GLOBAL*procent - LEVERAGE*DEPOSIT_GLOBAL*(COMMISSION_MAKER+COMMISSION_TAKER) # обновляем размер депо
        DEPOSIT_GLOBAL = round(DEPOSIT_GLOBAL,2)
        open_sl = False
        place_open_position_profit = round(LEVERAGE*DEPOSIT_GLOBAL*procent-LEVERAGE*DEPOSIT_GLOBAL*(COMMISSION_MAKER+COMMISSION_TAKER),2)
        # print_components_log(f'Сработал ТЕЙК|Депо={round(DEPOSIT,1)}, профит={round(profit,1)},ком={round(commission,1)}',frame_3_set4_1_1_1,'HT')
    if status == '-': # если закрыли в минус
        loss = loss + LEVERAGE*DEPOSIT_GLOBAL*procent
        commission = commission + LEVERAGE*DEPOSIT_GLOBAL*(COMMISSION_MAKER+COMMISSION_TAKER)
        DEPOSIT_GLOBAL = DEPOSIT_GLOBAL - LEVERAGE*DEPOSIT_GLOBAL*procent - LEVERAGE*DEPOSIT_GLOBAL*(COMMISSION_MAKER+COMMISSION_TAKER) # обновляем размер депо
        DEPOSIT_GLOBAL = round(DEPOSIT_GLOBAL,2)
        open_sl = False
        place_open_position_profit = round(-LEVERAGE*DEPOSIT_GLOBAL*procent-LEVERAGE*DEPOSIT_GLOBAL*(COMMISSION_MAKER+COMMISSION_TAKER),2)
    

        # print_components_log(f'Сработал СТОП|Депо={round(DEPOSIT,1)}, убыток={round(loss,1)},ком={round(commission,1)}',frame_3_set4_1_1_1,'HT')

# когда в сделке - чекаем, словили тп или сл
def check_trade(price,COMMISSION_MAKER,COMMISSION_TAKER,TP,SL,DEPOSIT,LEVERAGE):
    now_price_trade = price #получаем текущую цену монеты
    global count_long_take
    global count_long_loss
    global count_short_take
    global count_short_loss
    global take_profit_price
    global stop_loss_price, signal_for_logs_regime_0
    if signal_trade == 'long':
        if float(now_price_trade)>float(take_profit_price):
            signal_for_logs_regime_0 = 'Тейк'
            close_trade('+',TP,COMMISSION_MAKER,COMMISSION_TAKER,DEPOSIT,LEVERAGE)
            count_long_take=count_long_take+1
            return 1
        if float(now_price_trade)<float(stop_loss_price):
            signal_for_logs_regime_0 = 'Стоп'
            count_long_loss = count_long_loss + 1
            close_trade('-',SL,COMMISSION_MAKER,COMMISSION_TAKER,DEPOSIT,LEVERAGE)
            return 1
    if signal_trade == 'short':
        if float(now_price_trade)<float(take_profit_price):
            signal_for_logs_regime_0 = 'Тейк'
            close_trade('+',TP,COMMISSION_MAKER,COMMISSION_TAKER,DEPOSIT,LEVERAGE)
            count_short_take = count_short_take+1
            return 1
        if float(now_price_trade)>float(stop_loss_price):
            signal_for_logs_regime_0 = 'Стоп'
            count_short_loss = count_short_loss + 1
            close_trade('-',SL,COMMISSION_MAKER,COMMISSION_TAKER,DEPOSIT,LEVERAGE)
            return 1

# -------------------------------------- ТОРГОВЛЯ --------------------------------------
# -------------------------------------- СТРАТЕГИЯ --------------------------------------

# точка входа в стратегии
def check_if_signal(prices,index,strat_mas_historical,result):
    global summ_strat
    for strat in strat_mas_historical: # перебор по id выбранных стратегий
        match strat:
            case 'strat1' : summ_strat['Канал, тренд, локаль, объём'] = get_strat_1(prices,index)
            case 'strat2' : summ_strat['Скользящие средние'] = get_strat_2(prices,index,result)
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
    if strat_long == len(summ_strat): return 'long'
    elif strat_short == len(summ_strat): return 'short'
    else : return 'нет сигнала'
    
# если есть первая стратегия
def get_strat_1(prices,index):
    try:
        return str_1.strat_1(prices,index) 
    except Exception as e:
        # print_components_log(f'Ошибка работы стратегии Канал, тренд, локаль, объём! - {e}',real_test_frame_3_2_1,'OS1')
        return 'нет сигнала'
    
# если вторая стратегия
def get_strat_2(prices,index,result):
    try:
        return str_2.strat_2(prices,index,result) 
    except Exception as e:
        print(f'Ошибка работы стратегии - {e}')
        return 'нет сигнала'
# -------------------------------------- СТРАТЕГИЯ --------------------------------------

# удаление всех файлов csv в переданной директории
def remove_csv(dir):
    filelist = [ f for f in os.listdir(dir) if f.endswith(".csv") ]
    for f in filelist:
        os.remove(os.path.join(dir, f))
        
# -------------------------------------- Перебор по датафрейму --------------------------------------

# отчистка фрейма
def clear_frame(frame):
    for widget in frame.winfo_children():
            widget.forget()

flag_set_ferst_once = 0

# точка входа
def start_trade_hist_model(real_test_frame_indicator_hist,frame_osnova,frame_log,strat_mas_historical,COMMISSION_MAKER,COMMISSION_TAKER,TP,SL,DEPOSIT,LEVERAGE,CANDLE_COIN_MIN,CANDLE_COIN_MAX,regime = 0,number_iteration_history_str=''):
    global regime_work,coin_mas_10,symbol,time_close_tf,STEP_5_min_VALUE,open_sl,data_numbers,profit,loss,commission,count_long_take,count_long_loss,count_short_take,count_short_loss,DEPOSIT_GLOBAL,wait_time,name_bot_historical,DEPOSIT_START,OUR_SETTINGS_MAS_STRAT_1,flag_set_ferst_once,set_our_settings,signal_for_logs_regime_0,place_open_position_step,place_open_position_trend,place_open_position_profit,take_profit_price,stop_loss_price,table_strat_1_settings_trade_for_historical
    open_sl = False # всегда при старте функции, мы не стоим в сделке
    DEPOSIT_GLOBAL = DEPOSIT
    data_numbers = []
    profit = 0  # Обнуляем профит сделки при старте функции
    loss = 0  # Обнуляем размер лося на стедку при страте функции
    commission = 0 # обнуляем комиссию на сделку при страте функции
    count_long_take = 0 # обнуляем количество лонговых позиций в плюс при старте функции
    count_long_loss = 0 # обнуляем количество лонговых позиций в минус при старте функции
    count_short_take = 0 # обнуляем количество шортовых позиций в плюс при старте функции
    count_short_loss = 0 # обнуляем количество шортовых позиций в минус при старте функции
    if regime==0:
        fi = open(MYDIR_COIN,'r') # открываем файл с монетами
        coin_mas_10 = fi.read().split('|') # записываем омнеты массивом сюда
    if regime==1:
        fi = open(MYDIR_COIN,'r') # открываем файл с монетами
        coin_mas_10 = fi.read().split('|') # записываем омнеты массивом сюда
    if regime==5:
        fi = open(biganal.MYDIR_COIN_2,'r') # открываем файл с монетами
        biganal.coin_mas_10_2 = fi.read().split('|') # записываем омнеты массивом сюда


    
    fi.close()
    t = Texttable()
    if regime==0:
        bar = progressbar.ProgressBar(maxval=VOLUME).start()
        VOLUME_NOW = VOLUME
    if regime==1:
        bar = progressbar.ProgressBar(maxval=VOLUME).start()
        VOLUME_NOW = VOLUME
    if regime==5:
        bar = progressbar.ProgressBar(maxval=biganal.VOLUME).start()
        VOLUME_NOW = biganal.VOLUME
    number_iteration_history = 0
    
    clear_frame(real_test_frame_indicator_hist)

    regime_work = regime
    
    progressbar_hist_once = customtkinter.CTkProgressBar(real_test_frame_indicator_hist, orientation="horizontal",width=600)
    progressbar_hist_once.pack()
    
    if regime==1 and flag_set_ferst_once==0:
        print_components_log(f'Торговля по сету настроек, начинаем',frame_log,'DF')
        flag_set_ferst_once = 1
    if regime==0:
        print_components_log(f'Торговля по заданным найстройкам, начинаем',frame_log,'DF')
    if regime==5 and flag_set_ferst_once==0:
        print_components_log(f'Торговля по заданным найстройкам BIG TRADE, начинаем',frame_log,'DF')
        flag_set_ferst_once = 1
    for index in range(VOLUME_NOW):
        progressbar_hist_once.set(index/VOLUME_NOW)
        bar.update(index)
        data_numbers.append(index) # добавляем в массив номера итераций - 0,1,2,3 - имитируем реальную торговлю
        if index>INDEX_START: # начинаем не с нуля, а с 20-ой свечи
            if open_sl == False: # если нет позиции
                try:
                    if regime==0:
                        coin_mas = coin_mas_10
                    if regime==1:
                        coin_mas = coin_mas_10
                    if regime==5:
                        coin_mas = biganal.coin_mas_10_2
                    for x,result in enumerate(coin_mas):
                        if regime==0:
                            df = pd.read_csv(f'{MYDIR_WORKER}{result}.csv') # получили датафрейм из файла
                            if len(df) != VOLUME : continue
                        if regime==1:
                            df = pd.read_csv(f'{MYDIR_WORKER}{result}.csv') # получили датафрейм из файла
                            if len(df) != VOLUME : continue
                        if regime==5:
                            df = pd.read_csv(f'{biganal.MYDIR_WORKER_2}{result}.csv') # получили датафрейм из файла
                            if len(df) != int(biganal.VOLUME) : continue

                        prices = df.iloc[data_numbers]
                        # print(f"{prices['VOLUME'][index]}>{CANDLE_COIN_MIN} and {prices['VOLUME'][index]}<{CANDLE_COIN_MAX}")
                        if prices['VOLUME'][index]>CANDLE_COIN_MIN and prices['VOLUME'][index]<CANDLE_COIN_MAX:
                            trend = check_if_signal(prices,index,strat_mas_historical,result) # определяем тренд - стратегия
                            if trend != 'нет сигнала': # если есть сигнал
                                symbol = result # сохраняем монету с сигналом
                                time_close_tf = prices['close_time'][index]
                                place_open_position_step = index
                                place_open_position_trend = trend
                                break
                            else:
                                trend = "нет сигнала"  
                        else:
                            trend = "нет сигнала"  
                    # если получили сигнал и объём за свечку больше минимального объема (настройка) и меншье максимального объёма (настройка)  
                    if trend != "нет сигнала":
                        # если есть сигнал, то открываем позицию - направление, объём, цена входа, 
                        if regime==0: print_components_log(f'Открываем позицию в {trend} | Монета {symbol} | цена входа {prices['close'][index]}',frame_log,'DF')
                        open_position(trend,get_trade_VOLUME(prices['close'][index],DEPOSIT,LEVERAGE),prices['close'][index],SL,TP)   
                except Exception as e:
                    print(f'Ошибка основного цикла | Определение сгнала не работает - {e}')
            else: #если есть позиция
                if regime==0:
                    df = pd.read_csv(f'{MYDIR_WORKER}{symbol}.csv') # получили датафрейм из файла
                    prices = df.iloc[data_numbers]
                    df_mal = pd.read_csv(f'{MYDIR_5MIN}{result}.csv') # получили датафрейм мини из файла
                if regime==1:
                    df = pd.read_csv(f'{MYDIR_WORKER}{symbol}.csv') # получили датафрейм из файла
                    prices = df.iloc[data_numbers]
                    df_mal = pd.read_csv(f'{MYDIR_5MIN}{result}.csv') # получили датафрейм мини из файла
                if regime==5:
                    df = pd.read_csv(f'{biganal.MYDIR_WORKER_2}{symbol}.csv') # получили датафрейм из файла
                    prices = df.iloc[data_numbers]
                    df_mal = pd.read_csv(f'{biganal.MYDIR_5MIN}{result}.csv') # получили датафрейм мини из файла
                
                for index2, row in df_mal.iterrows(): # находим индекс, с которого начгнем следить за ценой
                    if row['close_time'] == prices['close_time'][index]:
                        if regime==0:
                            if int(index2)>int(VOLUME_5MIN)-int(STEP_5_min_VALUE)-5:
                                break
                        if regime==1:
                            if int(index2)>int(VOLUME_5MIN)-int(STEP_5_min_VALUE)-5:
                                break
                        if regime==5:
                            if int(index2)>int(biganal.VOLUME_5MIN)-int(biganal.STEP_5_min_VALUE)-5:
                                break
                        for i in range(int(index2),int(index2)+int(STEP_5_min_VALUE),1):
                            if check_trade(df_mal['close'][i],COMMISSION_MAKER,COMMISSION_TAKER,TP,SL,DEPOSIT,LEVERAGE):
                                if regime==0: 
                                    if take_profit_price>1:
                                        take_profit_price = round(take_profit_price,3)
                                        stop_loss_price = round(stop_loss_price,3)
                                    data_for_table_trade_regime_1.append([symbol,place_open_position_step,place_open_position_trend,round(take_profit_price,2),stop_loss_price,place_open_position_profit,DEPOSIT_GLOBAL]) 
                                    print_components_log(f'{signal_for_logs_regime_0}! Закрыли позицию, депозит - {DEPOSIT_GLOBAL}',frame_log,'DF')
                                if regime==1:
                                    number = number_iteration_history_str.split('/')[0]
                                    take_profit_price = round(take_profit_price,3)
                                    stop_loss_price = round(stop_loss_price,3)
                                    treyd = f'{symbol},{place_open_position_step},{place_open_position_trend},{round(take_profit_price,2)},{stop_loss_price},{place_open_position_profit},{DEPOSIT_GLOBAL}'
                                    print_trade_file(number,treyd)
                                if regime==5:
                                    number = number_iteration_history_str.split('/')[0]
                                    take_profit_price = round(take_profit_price,3)
                                    stop_loss_price = round(stop_loss_price,3)
                                    treyd = f'{symbol},{place_open_position_step},{place_open_position_trend},{round(take_profit_price,2)},{stop_loss_price},{place_open_position_profit},{DEPOSIT_GLOBAL}'
                                    print_trade_file(number,treyd)
                                break # чекаем монету по шагам итерации между большим и мальеньким фреймом
            if float(DEPOSIT_GLOBAL)/float(DEPOSIT_START) < 0.4:
                break
    if regime == 0: 
        number_iteration_history = 1
        print_components_log(f'Закончили торговлю, депозит - {DEPOSIT_GLOBAL}',frame_log,'DF')
        # рисуем таблицу для нажатия и вывода графика
        table_strat_1_settings_trade_for_historical = CTkTable(master=frame_osnova, row=1+len(data_for_table_trade_regime_1), column=7, values=data_for_table_trade_regime_1,font=('Arial',10,'bold'),command = onclick_stroka_table_trade_str_1_set)
        table_strat_1_settings_trade_for_historical.pack(expand=True, padx=20, pady=20)
        progressbar_hist_once.set(1)
        
    if regime == 1: 
        progressbar_hist_once.set(1)
        number_iteration_history = number_iteration_history_str
        if count_long_take+count_short_take+count_long_loss+count_short_loss==0:
            procent_trade_plus = 0
        else:
            procent_trade_plus = ((count_long_take+count_short_take)/(count_long_take+count_short_take+count_long_loss+count_short_loss))*100
        
        print_components_log(f'Обработано {number_iteration_history} | ИТОГ: {round(profit-loss-commission,2)} $',frame_log,'DF')
        print_log('---------------------------------------------------------------------------------------------------------------------------')

        if strat_mas_historical[0] == 'strat1':
            t.add_rows([[f'Дата {time.strftime("%d.%m.%Y", time.localtime())}',f'Время {time.strftime("%H:%M:%S", time.localtime())}',f'Имя бота {name_bot_historical}',f'{number_iteration_history}'],
                        [f'Следим за ценой {int(wait_time*VOLUME/VOLUME_5MIN)} мин',f'Ком мейк {COMMISSION_MAKER*100} %',f'Депо {int(DEPOSIT)} $',f'Верх канала {str_1.CANAL_MAX*100} %'],
                        [f'Рабочий таймфрейм {wait_time} мин',f'Ком тейк {COMMISSION_TAKER*100} %',f'Плечо {LEVERAGE}',f'Низ канала {str_1.CANAL_MIN*100} %'],
                        [f'Длительность {int(wait_time*VOLUME/60)} ч',f'Тейк {TP*100} %',f'Объём торгов мин {CANDLE_COIN_MIN}',f'Угол лонг {str_1.CORNER_LONG}'],
                        [f'Сколько монет торговать {how_mach_coin}',f'Стоп {SL*100} %',f'Объём торгов макс {CANDLE_COIN_MAX}',f'Угол шорт {str_1.CORNER_SHORT}'],
                        [f'Процент сделок в + {procent_trade_plus} %',f'Сделок в + {count_long_take+count_short_take}',f'Седлок в - {count_long_loss+count_short_loss}',f'Всего сделок {count_long_take+count_short_take+count_long_loss+count_short_loss}'],
                        [f'Общий профит {profit} $',f'Общий убыток {loss} $',f'Комиссия {commission} $',f'ИТОГ: {round(profit-loss-commission,2)} $'],
                        [f'Депо ИТОГ: {DEPOSIT_GLOBAL} $',f'Депо старт {DEPOSIT_START} $',f'Депо ИТОГ,%: {round(((DEPOSIT_GLOBAL/DEPOSIT_START)-1)*100,2)}',f'']])
        if strat_mas_historical[0] == 'strat2':
            t.add_rows([[f'Дата {time.strftime("%d.%m.%Y", time.localtime())}',f'Время {time.strftime("%H:%M:%S", time.localtime())}',f'Имя бота {name_bot_historical}',f'{number_iteration_history}'],
                        [f'Следим за ценой {int(wait_time*VOLUME/VOLUME_5MIN)} мин',f'Ком мейк {COMMISSION_MAKER*100} %',f'Депо {int(DEPOSIT)} $',f'Верх канала {str_2.CANAL_MAX*100} %'],
                        [f'Рабочий таймфрейм {wait_time} мин',f'Ком тейк {COMMISSION_TAKER*100} %',f'Плечо {LEVERAGE}',f'Низ канала {str_2.CANAL_MIN*100} %'],
                        [f'Длительность {int(wait_time*VOLUME/60)} ч',f'Тейк {TP*100} %',f'Объём торгов мин {CANDLE_COIN_MIN}',f'Угол лонг -'],
                        [f'Сколько монет торговать {how_mach_coin}',f'Стоп {SL*100} %',f'Объём торгов макс {CANDLE_COIN_MAX}',f'Угол шорт -'],
                        [f'Процент сделок в + {procent_trade_plus} %',f'Сделок в + {count_long_take+count_short_take}',f'Седлок в - {count_long_loss+count_short_loss}',f'Всего сделок {count_long_take+count_short_take+count_long_loss+count_short_loss}'],
                        [f'Общий профит {profit} $',f'Общий убыток {loss} $',f'Комиссия {commission} $',f'ИТОГ: {round(profit-loss-commission,2)} $'],
                        [f'Депо ИТОГ: {DEPOSIT_GLOBAL} $',f'Депо старт {DEPOSIT_START} $',f'Депо ИТОГ,%: {round(((DEPOSIT_GLOBAL/DEPOSIT_START)-1)*100,2)}',f'']])
        print(t.draw())
        print_log(t.draw())
        set_our_settings.append([TP,SL,DEPOSIT,LEVERAGE,CANDLE_COIN_MIN,CANDLE_COIN_MAX,str_1.CANAL_MAX,str_1.CANAL_MIN,str_1.CORNER_SHORT,str_1.CORNER_LONG,number_iteration_history_str])
        OUR_SETTINGS_MAS_STRAT_1.append([number_iteration_history,round(profit-loss-commission,2),count_long_take+count_short_take+count_long_loss+count_short_loss,count_long_take+count_short_take,count_long_loss+count_short_loss,round(profit,1),round(loss,1),round(commission,1)])
        # print(set_our_settings)
    if regime == 5: 
        progressbar_hist_once.set(1)
        number_iteration_history = number_iteration_history_str
        if count_long_take+count_short_take+count_long_loss+count_short_loss==0:
            procent_trade_plus = 0
        else:
            procent_trade_plus = ((count_long_take+count_short_take)/(count_long_take+count_short_take+count_long_loss+count_short_loss))*100
        
        print_components_log(f'Обработано {number_iteration_history} | ИТОГ: {round(profit-loss-commission,2)} $',frame_log,'DF')
        print_log('---------------------------------------------------------------------------------------------------------------------------')
        if strat_mas_historical[0] == 'strat1':
            t.add_rows([[f'Дата {time.strftime("%d.%m.%Y", time.localtime())}',f'Время {time.strftime("%H:%M:%S", time.localtime())}',f'Имя бота {name_bot_historical}',f'{number_iteration_history}'],
                        [f'Следим за ценой {int(biganal.wait_time*biganal.VOLUME/biganal.VOLUME_5MIN)} мин',f'Ком мейк {biganal.COMMISSION_MAKER*100} %',f'Депо {int(DEPOSIT)} $',f'Верх канала {str_1.CANAL_MAX*100} %'],
                        [f'Рабочий таймфрейм {biganal.wait_time} мин',f'Ком тейк {biganal.COMMISSION_TAKER*100} %',f'Плечо {LEVERAGE}',f'Низ канала {str_1.CANAL_MIN*100} %'],
                        [f'Длительность {int(biganal.wait_time*biganal.VOLUME/60)} ч',f'Тейк {TP*100} %',f'Объём торгов мин {CANDLE_COIN_MIN}',f'Угол лонг {str_1.CORNER_LONG}'],
                        [f'Сколько монет торговать {biganal.how_mach_coin}',f'Стоп {SL*100} %',f'Объём торгов макс {CANDLE_COIN_MAX}',f'Угол шорт {str_1.CORNER_SHORT}'],
                        [f'Процент сделок в + {procent_trade_plus} %',f'Сделок в + {count_long_take+count_short_take}',f'Седлок в - {count_long_loss+count_short_loss}',f'Всего сделок {count_long_take+count_short_take+count_long_loss+count_short_loss}'],
                        [f'Общий профит {profit} $',f'Общий убыток {loss} $',f'Комиссия {commission} $',f'ИТОГ: {round(profit-loss-commission,2)} $'],
                        [f'Депо ИТОГ: {DEPOSIT_GLOBAL} $',f'Депо старт {DEPOSIT_START} $',f'Депо ИТОГ,%: {round(((DEPOSIT_GLOBAL/DEPOSIT_START)-1)*100,2)}',f'']])
        if strat_mas_historical[0] == 'strat2':
            t.add_rows([[f'Дата {time.strftime("%d.%m.%Y", time.localtime())}',f'Время {time.strftime("%H:%M:%S", time.localtime())}',f'Имя бота {name_bot_historical}',f'{number_iteration_history}'],
                        [f'Следим за ценой {int(biganal.wait_time*biganal.VOLUME/biganal.VOLUME_5MIN)} мин',f'Ком мейк {biganal.COMMISSION_MAKER*100} %',f'Депо {int(DEPOSIT)} $',f'Верх канала {str_2.CANAL_MAX*100} %'],
                        [f'Рабочий таймфрейм {biganal.wait_time} мин',f'Ком тейк {biganal.COMMISSION_TAKER*100} %',f'Плечо {LEVERAGE}',f'Низ канала {str_2.CANAL_MIN*100} %'],
                        [f'Длительность {int(biganal.wait_time*biganal.VOLUME/60)} ч',f'Тейк {TP*100} %',f'Объём торгов мин {CANDLE_COIN_MIN}',f'Угол лонг -'],
                        [f'Сколько монет торговать {biganal.how_mach_coin}',f'Стоп {SL*100} %',f'Объём торгов макс {CANDLE_COIN_MAX}',f'Угол шорт -'],
                        [f'Процент сделок в + {procent_trade_plus} %',f'Сделок в + {count_long_take+count_short_take}',f'Седлок в - {count_long_loss+count_short_loss}',f'Всего сделок {count_long_take+count_short_take+count_long_loss+count_short_loss}'],
                        [f'Общий профит {profit} $',f'Общий убыток {loss} $',f'Комиссия {commission} $',f'ИТОГ: {round(profit-loss-commission,2)} $'],
                        [f'Депо ИТОГ: {DEPOSIT_GLOBAL} $',f'Депо старт {DEPOSIT_START} $',f'Депо ИТОГ,%: {round(((DEPOSIT_GLOBAL/DEPOSIT_START)-1)*100,2)}',f'']])
        print(t.draw())
        print_log(t.draw())
        set_our_settings.append([TP,SL,DEPOSIT,LEVERAGE,CANDLE_COIN_MIN,CANDLE_COIN_MAX,str_1.CANAL_MAX,str_1.CANAL_MIN,str_1.CORNER_SHORT,str_1.CORNER_LONG,number_iteration_history_str])
        OUR_SETTINGS_MAS_STRAT_1.append([number_iteration_history,round(profit-loss-commission,2),count_long_take+count_short_take+count_long_loss+count_short_loss,count_long_take+count_short_take,count_long_loss+count_short_loss,round(profit,1),round(loss,1),round(commission,1)])
        # print(set_our_settings)
        
    if regime == 0:
        pass
    


def onclick_stroka_table_trade_str_1_set(data):
    global regime_work
    global table_strat_1_settings_trade_for_historical
    data_parse = table_strat_1_settings_trade_for_historical.get_row(data['row'])
    # for key,val in enumerate(bin.set_our_settings):
    print_graph_historical_of_once_settings(data_parse[0],data_parse[1],data_parse[2],data_parse[3],data_parse[4],regime_work)

def print_graph_historical_of_once_settings(symbol,step_input,trend,TP,SL,regime):
    if regime==0:
        df = pd.read_csv(f'{MYDIR_WORKER}{symbol}.csv')
    if regime==1:
        df = pd.read_csv(f'{MYDIR_WORKER}{symbol}.csv')
    if regime==5:
        df = pd.read_csv(f'{biganal.MYDIR_WORKER}{symbol}.csv')
    graph.draw_graph(df,VOLUME,step_input,trend,TP,SL)








