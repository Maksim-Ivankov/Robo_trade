
# переменные историческа торговля
work_timeframe_HM = 1 # истор следим за ценой таймфрейм
timeframe_HM = 5 # рабочий тайфрейм
wait_time = 5 # сколько минут ждать для обновления цены с биржи
COMMISSION_MAKER = 0.002 # комиссия а вход
COMMISSION_TAKER = 0.001 # комиссия на выхд
TP = 0.012 # Тейк профит, процент
SL = 0.004 # Стоп лосс, процент
DEPOSIT = 100 # Депозит
LEVERAGE = 20 # торговое плечо
CANAL_MAX = 0.85 # Верх канала
CANAL_MIN = 0.15 # Низ канала
CORNER_SHORT = 10 # Угол наклона шорт
CORNER_LONG = 10 # Угол наклона лонг
CANDLE_COIN_MIN = 200000 # объем торгов за свечку
CANDLE_COIN_MAX = 500000 # объем торгов за свечку
MYDIR_WORKER = '../ROBO_TRADE/DF/worker/'
MYDIR_5MIN = '../ROBO_TRADE/DF/5min/'
MYDIR_COIN = '../ROBO_TRADE/DF/coin.txt'
MYDIR_COIN_PROCENT = '../ROBO_TRADE/DF/coin_procent.txt'
VOLUME = 144 # сколько свечей получить при запросе к бирже
VOLUME_5MIN = 720 # сколько свечей получить в режиме слежения за ценой