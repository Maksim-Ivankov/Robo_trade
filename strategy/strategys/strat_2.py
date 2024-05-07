# стратегия торговли № 2

MIDDLE_1 = 6
MIDDLE_2 = 12
INDEX_START = 20 # автоматом подсасется из bin. Руками не трогать
MIDDLE_DATA = 3 # сколько шагов назад должны быть одинаковые по сигналу, чтобы сработало изменение
 
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
    if all_the_same(data_mas)==True:
        # если в массиве все одинаковые
        if data_mas[0] == True and data_once==False:
            data_mas[:] = []
            return 'long'
        elif data_mas[0] == False and data_once==True:
            data_mas[:] = []
            return 'short'
        else:
            data_mas[:] = []
            return 'нет сигнала'
    else:
        data_mas[:] = []
        return 'нет сигнала'
    # global reccomendation
    # if symbol not in reccomendation: # если в массиве сигналов нет монеты, значит запускаем первый раз. Просто добавляем в массив и возвращаемся
    #     reccomendation[symbol] = get_data(symbol,TF)
    #     return 'нет сигнала'
    # if reccomendation[symbol] == get_data(symbol,TF): # если сигнал раньше и сейчас совпадает, то - нет сигнала
    #     return 'нет сигнала'
    # elif get_data(symbol) == 'STRONG_BUY': # сигнал на покупку
    #      return 'long'
    # elif get_data(symbol) == 'STRONG_SELL': # сигнал на ПРОДАЖУ
    #      return 'short'
    
    






































