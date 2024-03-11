from tkinter import *
from math import *
import os
import sys
sys.path.insert(1,os.path.join(sys.path[0],'../'))
from imports import *

client = UMFutures(key=key, secret=secret)

# Получаем активные монеты на бирже
def get_top_coin():
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
        
    i=0
    for key, value in coin_min.items():
        i=i+1
        coin_mas2[key] = value
        if i==1:
            coin_min_val = value
        
    if abs(coin_max_val)>abs(coin_min_val):
        result = coin_mas1
    else:
        result = coin_mas2
    return result
