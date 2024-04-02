import random

# 0.012,0.004,100,20,200000,5000000,0.85,0.15,10,10
# Ниже число, сколько настроек создать
how_mach_settings = 3

# принтуем логи в файл
def print_log(msg):
    path ='create_settings/strat_1_historical_settings.txt'
    f = open(path,'a',encoding='utf-8')
    f.write('\n'+msg)
    f.close()


for i in range(0,how_mach_settings):
    TP = random.choice([0.004,0.005,0.006,0.007,0.008,0.009,0.01,0.011,0.012,0.013,0.014,0.015])
    SL = random.choice([0.004,0.005,0.006,0.007,0.008,0.009,0.01,0.011,0.012,0.013,0.014,0.015])
    DEPOSIT = random.choice([100])
    LEVERAGE = random.choice([20])
    CANDLE_COIN_MIN = random.choice([0,20000,200000,50000,100000,1000,10000])
    CANDLE_COIN_MAX = random.choice([500000,700000,900000,1000000,1200000,1400000,1600000,1800000,2000000])
    CANAL_MAX = random.choice([0.7,0.71,0.72,0.73,0.74,0.75,0.76,0.77,0.78,0.79,0.8,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.9])
    CANAL_MIN = random.choice([0.7,0.71,0.72,0.73,0.74,0.75,0.76,0.77,0.78,0.79,0.8,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.9])
    CORNER_SHORT = random.choice([7,8,9,10,11,12,13])
    CORNER_LONG = random.choice([7,8,9,10,11,12,13])
    str_settings=f'{TP},{SL},{DEPOSIT},{LEVERAGE},{CANDLE_COIN_MIN},{CANDLE_COIN_MAX},{CANAL_MAX},{CANAL_MIN},{CORNER_SHORT},{CORNER_LONG}'
    print_log(str_settings)





