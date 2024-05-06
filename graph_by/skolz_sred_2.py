import customtkinter
import time
import requests
import pandas as pd
from tkinter import *
import tkinter as tk
from datetime import datetime
import os   
import sys
sys.path.insert(1,os.path.join(sys.path[0],'../../../'))

INDEX_START=20
VOLUME = 480

MIDDLE_1 = 6
MIDDLE_2 = 12
INDEX_START = 20
MIDDLE_DATA = 3

def all_the_same(elements):
    return len(elements) == elements.count(elements[0])

def check_if_signal(df,index_trade):
    if index_trade < INDEX_START:
        return 'нет сигнала'
    else:
        sum_price = 0
        data_mas = []
        # вычисляем основную скользящую среднюю в текущей точке
        for i in range(index_trade-MIDDLE_1,index_trade):
            sum_price=sum_price+df['close'][i]*(1-(2/(index_trade-i+1))*0.01)
        save_middle_price_1 = sum_price/MIDDLE_1
        sum_price = 0
        # вычесляем отстающую скользящую среднюю в текущей точке
        for i in range(index_trade-MIDDLE_2,index_trade):
            sum_price=sum_price+df['close'][i]*(1-(2/(index_trade-i+1))*0.01)
        save_middle_price_2 = sum_price/MIDDLE_2
        data_once = save_middle_price_1<save_middle_price_2
        # закинуть в массив сравнение скользящих средних ха последние N точек
        for j in range(index_trade-MIDDLE_DATA,index_trade):
            sum_price = 0
            for l in range(j-MIDDLE_1,j):
                sum_price=sum_price+df['close'][l]*(1-(2/(j-l+1))*0.01)
            save_middle_price_11 = sum_price/MIDDLE_1
            sum_price = 0
            for l in range(j-MIDDLE_2,j):
                sum_price=sum_price+df['close'][l]*(1-(2/(j-l+1))*0.01)
            save_middle_price_21 = sum_price/MIDDLE_2
            data_mas.append(save_middle_price_11<save_middle_price_21)
        # print(f'{index_trade}|{data_mas}')
        
        if all_the_same(data_mas)==TRUE:
            # если в массиве все одинаковые
            if data_mas[0] == TRUE and data_once==FALSE:
                return 'long'
            elif data_mas[0] == FALSE and data_once==TRUE:
                return 'short'
            else:
                return 'нет сигнала'
        else:
            return 'нет сигнала'


        # print(save_middle_price_1>save_middle_price_2)
    # else:
    #     for index, row in df.iterrows():
    #         if index==index_trade:
    #             sum_price = 0
    #             for i in range(index-MIDDLE_1,index):
    #                 sum_price=sum_price+df['close'][i]*(1-(2/(index-i+1))*0.01)
    #             middle_price_1 = sum_price/MIDDLE_1
    #             for i in range(index-MIDDLE_2,index):
    #                 sum_price=sum_price+df['close'][i]*(1-(2/(index-i+1))*0.01)
    #             middle_price_2 = sum_price/MIDDLE_2
    #             sum_price = 0
    #             for i in range(index-MIDDLE_1-1,index-1):
    #                 sum_price=sum_price+df['close'][i]*(1-(2/(index-i))*0.01)
    #             middle_price_0_1 = sum_price/MIDDLE_1
    #             for i in range(index-MIDDLE_2-1,index-1):
    #                 sum_price=sum_price+df['close'][i]*(1-(2/(index-i))*0.01)
    #             middle_price_0_2 = sum_price/MIDDLE_2
    #     print(f'{middle_price_1>middle_price_2}')
    #     if middle_price_1<=middle_price_2 and middle_price_0_1>middle_price_0_2:
    #         signal =  'long'
    #     elif middle_price_1>=middle_price_2 and middle_price_0_1<middle_price_0_2:
    #         signal = 'short'
    #     else:
    #         signal = 'нет сигнала'
    #     return signal

def main():
    data_numbers = []
    for index in range(VOLUME):
        data_numbers.append(index) # добавляем в массив номера итераций - 0,1,2,3 - имитируем реальную торговлю
        if index>INDEX_START: # начинаем не с нуля, а с 20-ой свечи
            df = pd.read_csv(f'graph_by/coin.csv')
            prices = df.iloc[data_numbers]
            trend = check_if_signal(prices,index)
            print(f'{index}|{trend}')



main()















































