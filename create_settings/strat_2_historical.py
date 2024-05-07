import random

# 0.012,0.004,100,20,200000,5000000,0.85,0.15,10,10
# Ниже число, сколько настроек создать
how_mach_settings = 100

# принтуем логи в файл
def print_log(msg):
    path ='create_settings/strat_2_historical_settings.txt'
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
    MIDDLE_1 = random.choice([2,3,4,5,6,7,8,9,10,11,12,13,14])
    MIDDLE_2 = random.choice([2,3,4,5,6,7,8,9,10,11,12,13,14])
    MIDDLE_DATA = random.choice([1,2,3,4,5,6,7,8,9,10])
    str_settings=f'{TP},{SL},{DEPOSIT},{LEVERAGE},{CANDLE_COIN_MIN},{CANDLE_COIN_MAX},{MIDDLE_1},{MIDDLE_2},{MIDDLE_DATA}'
    print_log(str_settings)





