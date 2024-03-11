import numpy as np
import time

from binance.client import Client

# обменные операции:
def short_open(symbol, quantity):
    print('Шорт открыли')
    # client.futures_create_order(symbol=symbol, side='SELL', type='MARKET', quantity=quantity)
    
def short_close(symbol, quantity):
    print('Шорт закрыли')
    # client.futures_create_order(symbol=symbol, side='BUY', type='MARKET', quantity=quantity)
    
def long_open(symbol, quantity):
    print('Лонг открыли')
    client.futures_create_order(symbol=symbol, side='BUY', type='MARKET', quantity=quantity)

def long_close(symbol, quantity):
    print('Лонг закрыли')
    # client.futures_create_order(symbol=symbol, side='SELL', type='MARKET', quantity=quantity)

# инициализируйте клиента с помощью ваших API-ключей
api_key = "QIT80MTFskjHSr82dtsteA6bG01CUeODQCg65KoYaQ5LmPcSpYDzyv1Oa7fugW3m"
api_secret = "uMLo0WdaCv5FHBauV8QI4LZoDgmmVFf5Jd8TboKYRxHnHx6pmNrhg5bmdBgO54xI"
client = Client(api_key,  api_secret)


symbol = "ETHUSDT"
prices = []

# списки для хранения всей необходимой статистики
moving_average_values = []
bollinger_band_high_values = []
bollinger_band_low_values = []

# флажки для отслеживания обменов, чтобы избежать дублирования записей
in_short = False
in_long = False

# период полос Боллинджера
period = 3


i = 0
# main loop
while True:
    i=i+1
    print(f'{i}|Цикл')
    
    # если текущая свеча закрылась и текущее время не равно
    # последней записи (чтобы избежать дублирования ценовых записей)
    # if current_time.minute % 5 == 0 and current_time.strftime('%Y-%m-%d %H:%M') != last_time:
    
    # получите последнюю цену на символ
    latest_price = client.futures_symbol_ticker(symbol=symbol)['price']
    latest_price = float(latest_price)
    prices.append(latest_price)
    print(f'{i}|Последняя цена - {latest_price}')
    # напечатать последнюю цену с указанием текущего времени
    # вычислить скользящее среднее и отклонение
    ma = np.mean(prices[-period:])
    moving_average_values.append(ma)
    std = np.std(prices[-period:], ddof=1)
    # рассчитать полосы Боллинджера
    bb_high = ma + 2 * std
    bb_low = ma - 2 * std
    bollinger_band_high_values.append(bb_high)
    bollinger_band_low_values.append(bb_low)
    print(f'{i}|bb_high - {bb_high} | bb_low - {bb_low}')
    # решение о стратегии
    # короткие обмены
    if len(prices)>4:
        if prices[-2] < bollinger_band_high_values[-2] and prices[-1] > bollinger_band_high_values[-1]:
            if not in_short:
                short_open(symbol=symbol, quantity=1)
                in_short = True
        if prices[-2] > moving_average_values[-2] and prices[-1] < moving_average_values[-1]:
            if in_short:
                short_close(symbol=symbol, quantity=1)
                in_short = False
        # длительные условия
        if prices[-1] < bollinger_band_low_values[-1] and prices[-2] > bollinger_band_low_values[-2]:
            if not in_long:
                long_open(symbol=symbol, quantity=1)
                in_long = True

        if prices[-2] < moving_average_values[-2] and prices[-1] > moving_average_values[-1]:
            if in_long:
                long_close(symbol=symbol, quantity=1)
                in_long = False

    time.sleep(5)