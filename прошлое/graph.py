import time
import requests
import pandas as pd

symbol = 'BTCUSDT'
TF = '1h'
VOLUME = 120

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


df = get_futures_klines(symbol,TF,VOLUME)












