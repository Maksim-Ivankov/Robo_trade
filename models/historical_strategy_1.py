import os
import sys
sys.path.insert(1,os.path.join(sys.path[0],'../'))
from imports import *


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
    ohlc.columns = ["date","open","high","low","close","volume"]
    ohlc=ohlc.set_index('date')
    df = indATR(ohlc,14).reset_index()
    df['slope'] = indSlope(df['close'],5)
    df['channel_max'] = df['high'].rolling(10).max() # определяем верхний уровень канала
    df['channel_min'] = df['low'].rolling(10).min() # определяем нижний уровень канала
    df['position_in_channel'] = (df['close']-df['channel_min']) / (df['channel_max']-df['channel_min']) # сейчас находимся выше середины канала или ниже
    df = df.set_index('date')
    df = df.reset_index()
    return(df)

































