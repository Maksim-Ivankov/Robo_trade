from tkinter import *
from math import *
import os
import sys
sys.path.insert(1,os.path.join(sys.path[0],'../'))
from imports import *
from CTkTable import *

TF = '5m' # таймфрейм
VOLUME = 144 # сколько свечей получить при запросе к бирже
VOLUME_5MIN = 720 # сколько свечей получить в режиме слежения за ценой
how_mach_coin = 10
STEP_5_min_VALUE = 5
MYDIR_WORKER = '../ROBO_TRADE/DF/big_anal/worker/'
MYDIR_COIN_PROCENT = '../ROBO_TRADE/DF/big_anal/coin_procent.txt'
MYDIR_5MIN = '../ROBO_TRADE/DF/big_anal/mini/'
MYDIR_COIN = '../ROBO_TRADE/DF/big_anal/coin.txt'

wait_time = 5 # сколько минут ждать для обновления цены с биржи
coin_mas_10 = []
data_print_ad_df = []

client = UMFutures(key=key, secret=secret)

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

# удаление всех файлов csv в переданной директории
def remove_csv(dir):
    filelist = [ f for f in os.listdir(dir) if f.endswith(".csv") ]
    for f in filelist:
        os.remove(os.path.join(dir, f))

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










