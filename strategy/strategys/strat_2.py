# стратегия торговли по суммарным сигналам всех индикаторов с трейдинг вью

from tradingview_ta import TA_Handler, Interval, Exchange
 
reccomendation = {}

def get_data(symbol,TF):
    output = TA_Handler(
        symbol=symbol,
        screener="Crypto",
        exchange="Binance",
        interval=TF)
    activiti = output.get_analysis().summary
    activiti['SYMBOL'] = symbol
    return activiti['RECOMMENDATION']
 
def strat_2(symbol,TF):
    global reccomendation
    if symbol not in reccomendation: # если в массиве сигналов нет монеты, значит запускаем первый раз. Просто добавляем в массив и возвращаемся
        reccomendation[symbol] = get_data(symbol,TF)
        return 'нет сигнала'
    if reccomendation[symbol] == get_data(symbol,TF): # если сигнал раньше и сейчас совпадает, то - нет сигнала
        return 'нет сигнала'
    elif get_data(symbol) == 'STRONG_BUY': # сигнал на покупку
         return 'long'
    elif get_data(symbol) == 'STRONG_SELL': # сигнал на ПРОДАЖУ
         return 'short'
    
    






































