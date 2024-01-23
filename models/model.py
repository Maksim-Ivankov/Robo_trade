import os
import sys
sys.path.insert(1,os.path.join(sys.path[0],'../'))
from imports import *


client = UMFutures(key=key, secret=secret)

# Получите последние n свечей по n минут для торговой пары, обрабатываем и записывае данные в датафрейм
def get_futures_klines(symbol,TF,volume):
    x = requests.get('https://binance.com/fapi/v1/klines?symbol='+symbol.lower()+'&limit='+str(volume)+'&interval='+TF)
    df=pd.DataFrame(x.json())
    df.columns=['open_time','open','high','low','close','volume','close_time','d1','d2','d3','d4','d5']
    df=df.drop(['d1','d2','d3','d4','d5'],axis=1)
    df['open']=df['open'].astype(float)
    df['high']=df['high'].astype(float)
    df['low']=df['low'].astype(float)
    df['close']=df['close'].astype(float)
    df['volume']=df['volume'].astype(float)
    return(df) # возвращаем датафрейм с подготовленными данными

# Получаем активные монеты на бирже
def get_top_coin():
    data = client.ticker_24hr_price_change()
    change={}
    coin_max={}
    coin_min={}
    coin_mas1 = {}
    coin_mas2 = {}
    coin_mas_10 = []
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
def get_trade_volume(get_symbol_price,DEPOSIT,Leverage):
    volume = round(DEPOSIT*Leverage/get_symbol_price)
    return volume

# удаление всех файлов csv в переданной директории
def remove_csv(dir):
    filelist = [ f for f in os.listdir(dir) if f.endswith(".csv") ]
    for f in filelist:
        os.remove(os.path.join(dir, f))
        
coin_mas_10=[]
df_our_coin = []
df_our_coin_5min = []
mydir_worker = '../ROBO_TRADE/DF/worker/'
mydir_5min = '../ROBO_TRADE/DF/5min/'
def generate_dataframe(TF,volume,wait_time,frame_2_set2_3):
    global coin_mas_10
    coin_mas_10 = get_top_coin() # один раз запускаем функцию, чтобы обновить монету, с которой работаем
    open('../ROBO_TRADE/DF/coin.txt', "w").close()
    open('../ROBO_TRADE/DF/coin_procent.txt', "w").close()
    fi1 = open('../ROBO_TRADE/DF/coin.txt','a',encoding='utf-8')
    fi2 = open('../ROBO_TRADE/DF/coin_procent.txt','a',encoding='utf-8')
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
    remove_csv(mydir_worker)
    remove_csv(mydir_5min)
    i=-1
    for x,result in enumerate(coin_mas_10):
        df = get_futures_klines(result,TF,volume)
        df.to_csv(f'{mydir_worker}{result}.csv')
        print(f'{result} - {TF}')
        i=i+1
        customtkinter.CTkLabel(frame_2_set2_3, text=f'{i}. {result} - {TF} добавлен', fg_color="#DAE2EC",text_color='#242424',anchor='center',font=('Arial',12,'normal')).grid(row=i, column=0, sticky="w",pady=1)
        time.sleep(2)
        df_5m = get_futures_klines(result,'5m',int(volume*wait_time/5))
        df_5m.to_csv(f'{mydir_5min}{result}.csv')
        print(f'{result} - 5 минут')
        i=i+1
        customtkinter.CTkLabel(frame_2_set2_3, text=f'{i}. {result} - 5 мин добавлен', fg_color="#DAE2EC",text_color='#242424',anchor='center',font=('Arial',12,'normal')).grid(row=i, column=0, sticky="w",pady=1)
        time.sleep(2)
    i=i+1
    customtkinter.CTkLabel(frame_2_set2_3, text=f'Датафреймы добавлены', fg_color="#DAE2EC",text_color='#242424',anchor='center',font=('Arial',12,'normal')).grid(row=i, column=0, sticky="w",pady=1)
    return coin_mas_10

# получить данные с coin.txt   frame_2_set2_3



    












