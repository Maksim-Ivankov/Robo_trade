# это файл первой стратегии - Канал, тренд, локаль, объём

import numpy as np
import statsmodels.api as sm


CANAL_MAX = 0.85 # Верх канала
CANAL_MIN = 0.15 # Низ канала
CORNER_SHORT = 10 # Угол наклона шорт
CORNER_LONG = 10 # Угол наклона лонг

# функцифя ниже - точка входа
def strat_1(ohlc,index):
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

# найти локальный максимум
def isHCC(DF,i):
    df=DF.copy()
    HCC=0
    if df['close'][i]>=df['close'][i+1] and df['close'][i]>=df['close'][i-1] and df['close'][i+1]<df['close'][i-1]:
        #найдена вершина
        HCC = i
    return HCC

# найти локальный минимум
def isLCC(DF,i):
    df=DF.copy()
    LCC=0
    if df['close'][i]<=df['close'][i+1] and df['close'][i]<=df['close'][i-1] and df['close'][i+1]>df['close'][i-1]:
        #найдено Дно
        LCC = i-1
    return LCC

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