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
    coin={}
    coin_mas = []
    coin_mas_10 = []
    for i in data:
        change[i['symbol']] = float(i['priceChangePercent'])
    coin = dict(sorted(change.items(), key=lambda item: item[1],reverse=True))
    for key in coin:
        coin_mas.append(key)
    for x,result in enumerate(coin_mas):
        if x==2:
            break
        coin_mas_10.append(result)
    return coin_mas_10

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
def generate_dataframe(TF,volume,wait_time):
    global coin_mas_10
    coin_mas_10 = get_top_coin() # один раз запускаем функцию, чтобы обновить монету, с которой работаем
    open('../ROBO_TRADE/DF/coin.txt', "w").close()
    fi = open('../ROBO_TRADE/DF/coin.txt','a',encoding='utf-8')
    result_as_list = '|'.join(coin_mas_10)
    fi.write(result_as_list)
    fi.close()
    remove_csv(mydir_worker)
    remove_csv(mydir_5min)
    for x,result in enumerate(coin_mas_10):
        df = get_futures_klines(result,TF,volume)
        df.to_csv(f'{mydir_worker}{result}.csv')
        print(f'{result} - {TF}')
        time.sleep(2)
        df_5m = get_futures_klines(result,'5m',int(volume*wait_time/5))
        df_5m.to_csv(f'{mydir_5min}{result}.csv')
        print(f'{result} - 5 минут')
        time.sleep(2)
    return coin_mas_10

# получить данные с coin.txt

    












