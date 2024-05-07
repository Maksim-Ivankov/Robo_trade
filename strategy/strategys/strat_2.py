# стратегия торговли № 2

import numpy as np
import statsmodels.api as sm

MIDDLE_1 = 6
MIDDLE_2 = 12
INDEX_START = 20 # автоматом подсасется из bin. Руками не трогать
MIDDLE_DATA = 3 # сколько шагов назад должны быть одинаковые по сигналу, чтобы сработало изменение
CANAL_MAX = 0.85 # Верх канала
CANAL_MIN = 0.15 # Низ канала
 
data_mas = []

# проверяет, одинаковые ли данные в массиве
def all_the_same(elements):
    return len(elements) == elements.count(elements[0])

def strat_2(df,index_trade,result):
    if index_trade < INDEX_START:
        return 'нет сигнала'
    sum_price = 0
    # вычисляем основную скользящую среднюю в текущей точке
    for i in range(index_trade-int(MIDDLE_1),index_trade):
        sum_price=sum_price+df['close'][i]*(1-(2/(index_trade-i+1))*0.01)
    save_middle_price_1 = sum_price/int(MIDDLE_1)
    sum_price = 0
    # вычесляем отстающую скользящую среднюю в текущей точке
    for i in range(index_trade-int(MIDDLE_2),index_trade):
        sum_price=sum_price+df['close'][i]*(1-(2/(index_trade-i+1))*0.01)
    save_middle_price_2 = sum_price/int(MIDDLE_2)
    data_once = save_middle_price_1<save_middle_price_2
    # закинуть в массив сравнение скользящих средних ха последние N точек
    for j in range(index_trade-MIDDLE_DATA,index_trade):
        sum_price = 0
        for l in range(j-int(MIDDLE_1),j):
            sum_price=sum_price+df['close'][l]*(1-(2/(j-l+1))*0.01)
        save_middle_price_11 = sum_price/int(MIDDLE_1)
        sum_price = 0
        for l in range(j-int(MIDDLE_2),j):
            sum_price=sum_price+df['close'][l]*(1-(2/(j-l+1))*0.01)
        save_middle_price_21 = sum_price/int(MIDDLE_2)
        data_mas.append(save_middle_price_11<save_middle_price_21) 

    prepared_df = PrepareDF(df)
    i=index_trade-2


    if all_the_same(data_mas)==True:
        # если в массиве все одинаковые
        if data_mas[0] == True and data_once==False:
            if prepared_df['position_in_channel'][i-1]<CANAL_MIN: # проверяем, прижаты ли мы к верхней границе канала
                data_mas[:] = []
                return 'short'
        elif data_mas[0] == False and data_once==True:
            if prepared_df['position_in_channel'][i-1]>CANAL_MAX: # проверяем, прижаты ли мы к нижней границе канала
                data_mas[:] = []
                return 'long'
        else:
            data_mas[:] = []
            return 'нет сигнала'
    else:
        data_mas[:] = []
        return 'нет сигнала'



# сгенерируйте фрейм данных со всеми необходимыми данными
def PrepareDF(DF):
    ohlc = DF.iloc[:,[0,1,2,3,4,5]]
    ohlc.columns = ["date","open","high","low","close","VOLUME"]
    ohlc=ohlc.set_index('date')
    df = indATR(ohlc,14).reset_index()
    df['channel_max'] = df['high'].rolling(10).max() # определяем верхний уровень канала
    df['channel_min'] = df['low'].rolling(10).min() # определяем нижний уровень канала
    df['position_in_channel'] = (df['close']-df['channel_min']) / (df['channel_max']-df['channel_min']) # сейчас находимся выше середины канала или ниже
    df = df.set_index('date')
    df = df.reset_index()
    return(df)

# найти локальный максимум
def isHCC(df,i):
    HCC=0
    if df['close'][i]>=df['close'][i+1] and df['close'][i]>=df['close'][i-1] and df['close'][i+1]<df['close'][i-1]:
        #найдена вершина
        HCC = i
    return HCC

# найти локальный минимум
def isLCC(df,i):
    LCC=0
    if df['close'][i]<=df['close'][i+1] and df['close'][i]<=df['close'][i-1] and df['close'][i+1]>df['close'][i-1]:
        #найдено Дно
        LCC = i-1
    return LCC

# Индикатор истинного диапазона и среднего значения истинного диапазона
def indATR(df,n):
    df['H-L']=abs(df['high']-df['low'])
    df['H-PC']=abs(df['high']-df['close'].shift(1))
    df['L-PC']=abs(df['low']-df['close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    df_temp = df.drop(['H-L','H-PC','L-PC'],axis=1)
    return df_temp








































