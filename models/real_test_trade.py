from tkinter import *
from math import *
import os
import sys
sys.path.insert(1,os.path.join(sys.path[0],'../'))
from imports import *
import _thread
from models.tg import *
import strategy.strategys.strat_1 as str_1
import strategy.strategys.strat_2 as str_2


TF = '5m' # таймфрейм
wait_time = 5 # сколько минут ждать для обновления цены с биржи
TP = 0.012 # Тейк профит, процент
SL = 0.004 # Стоп лосс, процент
DEPOSIT = 100 # Депозит
DEPOSIT_START = DEPOSIT
LEVERAGE = 20 # торговое плечо
COMMISSION_MAKER = 0.002 # комиссия на вход
COMMISSION_TAKER = 0.001 # комиссия на выхд
VOLUME = 10 # сколько свечей получить при запросе к бирже
VOLUME_5MIN = 144
CANDLE_COIN_MIN = 200000 # объем торгов за свечку
CANDLE_COIN_MAX = 500000 # объем торгов за свечку
MYDIR_WORKER = '../ROBO_TRADE/DF/worker/'
MYDIR_5MIN = '../ROBO_TRADE/DF/5min/'
MYDIR_COIN = '../ROBO_TRADE/DF/coin.txt'
MYDIR_COIN_PROCENT = '../ROBO_TRADE/DF/coin_procent.txt'
how_mach_coin = 10 # сколько монет торговать
how_mach_candle_get_api = 30

day_trade = round((wait_time*VOLUME)/(60*24),4)
open_sl = False # флаг на открытые позиции
open_position = False # флаг, стоим в позиции или нет
price_trade = 0
signal_trade = ''
coin_trade = ''
symbol = 'btcusdt' 
value_trade = 0
profit = 0
loss = 0
commission = 0
data_numbers = []
count_long_take = 0
count_short_take = 0
count_long_loss = 0
count_short_loss = 0
coin_mas_10=[]
df_our_coin = []
df_our_coin_5min = []
trend = ''
i1 = 0
time_close_tf = 0
coutnt_index_time_df = 0
data_print_ad_df = []
number_print_df = 0
number_print_ht = 0
data_print_ad_ht = []
tg_message = ''
name_bot = ''
client = UMFutures(key=key, secret=secret)
price_now = 0
trend_for_print = ''
stop_real_test_trade_flag = False
width_canvas = 700
height_canvas = 300
flag_trade_real_test = True
summ_strat = {}


# точка входа с main
def start_real_test_trade_model_thread_1(strat_now_rt,strat_mas_real_test,real_test_frame_4,card_trade_menu,name_bot_real_test,sost_tg_message,real_test_frame_3_1_1,real_test_frame_3_2_1):
    global tg_message
    global name_bot
    name_bot = name_bot_real_test
    tg_message = sost_tg_message
    print_components_log(f'Имя бота - {name_bot}\nТаймфрейм {TF}\nТейк {TP}\nСтоп{SL}\nДепозит {DEPOSIT}\nПлечо {LEVERAGE}\n Комиссия на вход {COMMISSION_MAKER}\nКомиссия на выход {COMMISSION_TAKER} Торгуем по {how_mach_coin} топ монетам\nОбъём торгов мин {CANDLE_COIN_MIN}\nОбъём торгов макс {CANDLE_COIN_MAX}',real_test_frame_3_2_1,'OS1')
    print_components_log(f'Стратегии торговли: {strat_now_rt}',real_test_frame_3_2_1,'OS1')
    
    for widget in card_trade_menu.winfo_children(): # чистим табличку
            widget.forget()
    card_trade_menu_1 = customtkinter.CTkFrame(card_trade_menu, corner_radius=5, fg_color="#242424")
    card_trade_menu_2 = customtkinter.CTkFrame(card_trade_menu, corner_radius=5, fg_color="#242424")
    switch_TG_var2 = customtkinter.StringVar(value="on")
    card_trade_menu_1_switch_tg = customtkinter.CTkSwitch(card_trade_menu_1, text="Робот запущен",variable=switch_TG_var2, onvalue="on", offvalue="off")
    card_trade_menu_1.pack()
    card_trade_menu_1_switch_tg.pack(padx=35,pady=5)
    card_trade_menu_2.pack(pady=10)
    
    try:
        thread25 = threading.Thread(target=lambda:start_real_test_trade_model(strat_mas_real_test,real_test_frame_4,card_trade_menu,switch_TG_var2,card_trade_menu_2,real_test_frame_3_1_1,real_test_frame_3_2_1))
        thread25.start()
    except Exception as e:
        messagebox.showinfo('Внимание','Ошибка начала торговли')
    
# Получите последние n свечей по n минут для торговой пары, обрабатываем и записывае данные в датафрейм
def get_futures_klines(symbol,TF,VOLUME):
    try:
        time.sleep(2)
        x = requests.get('https://fapi.binance.com/fapi/v1/klines?symbol='+symbol.lower()+'&limit='+str(VOLUME)+'&interval='+TF)
        df=pd.DataFrame(x.json())
        df.columns=['open_time','open','high','low','close','VOLUME','close_time','d1','d2','d3','d4','d5']
        df=df.drop(['d1','d2','d3','d4','d5'],axis=1)
        df['open']=df['open'].astype(float)
        df['high']=df['high'].astype(float)
        df['low']=df['low'].astype(float)
        df['close']=df['close'].astype(float)
        df['VOLUME']=df['VOLUME'].astype(float)
        return(df) # возвращаем датафрейм с подготовленными данными
    except Exception as e:
        messagebox.showinfo('Внимание',f'Ошибка запроса данных с бинанса - {e}')
        print(e)

# Получаем активные монеты на бирже
def get_top_coin():
    try:
        global how_mach_coin
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
            if i==int(how_mach_coin):
                break
        i=0
        for key, value in coin_min.items():
            i=i+1
            coin_mas2[key] = value
            if i==1:
                coin_min_val = value
            if i== how_mach_coin:
                break
        if abs(coin_max_val)>abs(coin_min_val):
            result = coin_mas1
        else:
            result = coin_mas2
        return result
    except Exception as e:
        messagebox.showinfo('Внимание','Ошибка получения активных монет с биржи')

# определяем размер позиции, на которую должны зайти
def get_trade_VOLUME(get_symbol_price):
    try:
        volume = round(float(DEPOSIT)*float(LEVERAGE)/float(get_symbol_price))
        return volume
    except Exception as e:
        messagebox.showinfo('Внимание','Ошибка определения размера позиции')

# логи в прогу
def print_components_log(msg,frame,type):
    global data_print_ad_df
    global number_print_df
    global number_print_ht
    global data_print_ad_ht
    global tg_message
    global name_bot
    if type == 'OS1':
        path ='RT_log.txt'
        f = open(path,'a',encoding='utf-8')
        f.write('\n'+time.strftime("%d.%m.%Y | %H:%M:%S | ", time.localtime())+msg)
        f.close()
        print(msg)
        if tg_message == 'on':
            print_tg(msg)
        number_print_df=number_print_df+1
        for widget in frame.winfo_children():
                widget.forget()
        data_print_ad_df.insert(0,customtkinter.CTkLabel(frame, text=str(number_print_df)+'. '+str(time.strftime("%H:%M:%S", time.localtime()))+' '+msg, fg_color="#DAE2EC",text_color='#242424',anchor='w',font=('Arial',12,'normal')))
        for component in data_print_ad_df:
            component.pack(anchor="w")
    if type == 'WS':
        number_print_ht=number_print_ht+1
        for widget in frame.winfo_children():
                widget.forget()
        data_print_ad_ht.insert(0,customtkinter.CTkLabel(frame, text=str(time.strftime("%H:%M:%S", time.localtime()))+'. '+ msg, fg_color="#DAE2EC",text_color='#242424',anchor='w',font=('Arial',12,'normal')))
        for component in data_print_ad_ht:
            component.pack(anchor="w")

# открывает лонг или шорт
def open_position(trend,value,price,real_test_frame_3_2_1):
    global open_sl
    global price_trade #цена входа
    global signal_trade # тренд
    global coin_trade # монета
    global value_trade # объём
    global take_profit_price
    global stop_loss_price
    price_trade = price
    signal_trade = trend
    coin_trade = symbol
    value_trade = value
    open_sl = True
    print_components_log(f'Открыл {signal_trade}, монета {coin_trade}, цена {price_trade}',real_test_frame_3_2_1,'OS1')
    take_profit_price = get_take_profit(trend,price_trade) # получаем цену тэйк профита
    stop_loss_price = get_stop_loss(trend,price_trade) # получаем цену стоп лосса
    print_components_log(f'Тейк - {take_profit_price} | Стоп - {stop_loss_price}',real_test_frame_3_2_1,'OS1')

# получить тейк профит
def get_take_profit(trend,price_trade): # получаем цену тейк профита в зависимости от направления
    if trend == 'long':
        return float(float(price_trade)*(1+float(TP)))
    if trend == 'short':
        return float(float(price_trade)*(1-float(TP)))

# получить стоп лосс
def get_stop_loss(trend,price_trade): # получаем цену стоп лосса в зависимости от направления
    if trend == 'long':
        return float(float(price_trade)*(1-float(SL)))
    if trend == 'short':
        return float(float(price_trade)*(1+float(SL)))
    
# Закрываем сделку
def close_trade(status,procent,real_test_frame_3_2_1):
    global DEPOSIT
    global open_sl
    global profit
    global loss
    global commission
    if status == '+': # если закрыли в плюс
        profit = profit + LEVERAGE*DEPOSIT*procent
        commission = commission + LEVERAGE*DEPOSIT*(COMMISSION_MAKER+COMMISSION_TAKER)
        DEPOSIT = DEPOSIT + LEVERAGE*DEPOSIT*procent - LEVERAGE*DEPOSIT*(COMMISSION_MAKER+COMMISSION_TAKER) # обновляем размер депо
        open_sl = False
        print_components_log(f'Сработал ТЕЙК|Депо={round(DEPOSIT,1)}, профит={round(profit,1)},ком={round(commission,1)}',real_test_frame_3_2_1,'OS1')
    if status == '-': # если закрыли в минус
        loss = loss + LEVERAGE*DEPOSIT*procent
        commission = commission + LEVERAGE*DEPOSIT*(COMMISSION_MAKER+COMMISSION_TAKER)
        DEPOSIT = DEPOSIT - LEVERAGE*DEPOSIT*procent - LEVERAGE*DEPOSIT*(COMMISSION_MAKER+COMMISSION_TAKER) # обновляем размер депо
        open_sl = False
        print_components_log(f'Сработал СТОП|Депо={round(DEPOSIT,1)}, убыток={round(loss,1)},ком={round(commission,1)}',real_test_frame_3_2_1,'OS1')

# следим за монетой в сделке из вебсокетов - сработал тейк или стоп
def check_trade(price,real_test_frame_3_2_1):
    now_price_trade = price #получаем текущую цену монеты
    global count_long_take
    global count_long_loss
    global count_short_take
    global count_short_loss
    global take_profit_price
    global stop_loss_price
    if signal_trade == 'long':
        if float(now_price_trade)>float(take_profit_price):
            close_trade('+',TP,real_test_frame_3_2_1)
            count_long_take=count_long_take+1
            return 1
        if float(now_price_trade)<float(stop_loss_price):
            count_long_loss = count_long_loss + 1
            close_trade('-',SL,real_test_frame_3_2_1)
            return 1
    if signal_trade == 'short':
        if float(now_price_trade)<float(take_profit_price):
            close_trade('+',TP,real_test_frame_3_2_1)
            count_short_take = count_short_take+1
            return 1
        if float(now_price_trade)>float(stop_loss_price):
            count_short_loss = count_short_loss + 1
            close_trade('-',SL,real_test_frame_3_2_1)
            return 1

# проверяем, есть ли сигнал на монету - точка входа работы стратегий
def check_if_signal(strat_mas_real_test,symbol,real_test_frame_3_2_1):
    global TF
    global how_mach_candle_get_api
    global summ_strat
    for strat in strat_mas_real_test:
        match strat:
            case 'strat1' : summ_strat['Канал, тренд, локаль, объём'] = get_strat_1(symbol,TF,how_mach_candle_get_api,real_test_frame_3_2_1)
            case 'strat2' : summ_strat['Скользящие средние'] = get_strat_2(symbol,TF,real_test_frame_3_2_1)
            case 'strat3' : pass
            case 'strat4' : pass
            case 'strat5' : pass
            case 'strat6' : pass
            case 'strat7' : pass
            case 'strat8' : pass
            case 'strat9' : pass
            case 'strat10': pass
            case 'strat11': pass
            case 'strat12': pass
            case 'strat13': pass
            case 'strat14': pass
            case 'strat15': pass
            case 'strat16': pass
            case 'strat17': pass
            case 'strat18': pass
            case 'strat19': pass
            case 'strat20': pass
            case 'strat21': pass
            case 'strat22': pass
            case 'strat23': pass
            case 'strat24': pass
            case 'strat25': pass
    print_components_log(f'Рекомендации стратегий - {summ_strat}',real_test_frame_3_2_1,'OS1')
    strat_long = 0
    strat_short = 0
    strat_neutral = 0
    for trend in summ_strat.values():
        if trend == 'long': 
            strat_long = strat_long + 1
        if trend == 'short': 
            strat_short = strat_short + 1
        if trend == 'нет сигнала': 
            strat_neutral = strat_neutral + 1
    print_components_log(f'Лонг - {strat_long} | Шорт - {strat_short} | Нейтрально - {strat_neutral}',real_test_frame_3_2_1,'OS1')
    if strat_long == len(summ_strat): return 'long'
    elif strat_short == len(summ_strat): return 'short'
    else : return 'нет сигнала'
        
def get_strat_1(symbol,TF,how_mach_candle_get_api,real_test_frame_3_2_1): # 1 стратегия
    try:
        prices = get_futures_klines(symbol,TF,how_mach_candle_get_api)
        return str_1.strat_1(prices,how_mach_candle_get_api) 
    except Exception as e:
        print_components_log(f'Ошибка работы стратегии Канал, тренд, локаль, объём! - {e}',real_test_frame_3_2_1,'OS1')
        return 'нет сигнала'

def get_strat_2(symbol,TF,real_test_frame_3_2_1): # 2 стратегия
    try:
      return str_2.strat_2(symbol,TF) 
    except Exception as e:
      print_components_log(f'Ошибка работы стратегии сум индикаторов TV! - {e}',real_test_frame_3_2_1,'OS1')
      return 'нет сигнала'
    
# получаем цену монеты сейчас
def get_price_now_coin(symbol):
    try:
        key = "https://fapi.binance.com/fapi/v1/ticker/price?symbol="+symbol
        data = requests.get(key)   
        data = data.json() 
        price = data['price']
        return price
    except Exception as e:
        print(f'Ошибка запроса цены для открытия сделки - {e}')
     
# запускаем вебсокеты, когда вошли в сделку, следим за монетой, рисуем график и данные в реальном времени    
async def websocket_trade(switch_TG_var2,real_test_frame_4,card_trade_menu_2,real_test_frame_3_1_1,real_test_frame_3_2_1):
    try:
        global price_trade #цена входа
        global signal_trade # тренд
        global coin_trade # монета
        global value_trade # объём
        global take_profit_price
        global stop_loss_price
        global DEPOSIT
        clean_card_menu(card_trade_menu_2)
        customtkinter.CTkLabel(card_trade_menu_2, text="В позиции", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=0)
        card_trade_menu_2_1 = customtkinter.CTkFrame(card_trade_menu_2,  fg_color="transparent")
        card_trade_menu_2_1.pack()
        customtkinter.CTkLabel(card_trade_menu_2_1, text=symbol, fg_color="transparent",anchor='w',font=('Arial',12,'bold')).grid(row=0,column=0,padx=10)
        if signal_trade == 'long':
            customtkinter.CTkLabel(card_trade_menu_2_1, text='Лонг', fg_color="transparent",text_color='#0AFF89',anchor='w',font=('Arial',12,'bold')).grid(row=0,column=1,padx=[40,50])
        if signal_trade == 'short':
            customtkinter.CTkLabel(card_trade_menu_2_1, text='Шорт', fg_color="transparent",text_color='#DA1010',anchor='w',font=('Arial',12,'bold')).grid(row=0,column=1,padx=[40,50])
        customtkinter.CTkLabel(card_trade_menu_2, text=f"Цена входа: {price_trade}", fg_color="transparent",anchor='w',font=('Arial',12,'bold')).pack(pady=0,anchor="w",padx=10)
        card_trade_menu_2_2 = customtkinter.CTkFrame(card_trade_menu_2,  fg_color="transparent")
        card_trade_menu_2_2.pack()
        comission = round(float(value_trade)*float(price_trade)*(COMMISSION_MAKER+COMMISSION_TAKER))
        customtkinter.CTkLabel(card_trade_menu_2_2, text=f"TP: {round(take_profit_price,4)}", fg_color="transparent",justify="left", anchor="w",font=('Arial',12,'bold')).grid(row=0,column=0,sticky='w' ,padx=0)
        customtkinter.CTkLabel(card_trade_menu_2_2, text=f"SL: {round(stop_loss_price,4)}", fg_color="transparent",anchor='w',font=('Arial',12,'bold')).grid(row=0,column=1,padx=10)
        customtkinter.CTkLabel(card_trade_menu_2, text=f"Комиссия: {comission}", fg_color="transparent",anchor='w',font=('Arial',12,'bold')).pack(pady=0,anchor="w",padx=10)
        price_now_ws = customtkinter.CTkLabel(card_trade_menu_2, text=f"Текущая цена: ", fg_color="transparent",anchor='w',font=('Arial',12,'bold'))
        price_now_ws.pack(pady=0,anchor="w",padx=10)
        card_trade_menu_2_pnl = customtkinter.CTkLabel(card_trade_menu_2, text=f"P&L: ", fg_color="transparent",anchor='w',font=('Arial',12,'bold'),text_color='white')
        card_trade_menu_2_pnl.pack(pady=0,anchor="w",padx=10)
        card_trade_menu_2_balance = customtkinter.CTkLabel(card_trade_menu_2, text=f"Баланс: ", fg_color="transparent",anchor='w',font=('Arial',12,'bold'))
        card_trade_menu_2_balance.pack(pady=0,anchor="w",padx=10)
        
        price_max = float(take_profit_price)
        price_min = float(stop_loss_price)
        OldRange = (price_max - price_min) 
        NewRange = height_canvas-20 
        OldRange1 = 170  
        NewRange1 = int((width_canvas-20)/170)
        index = 1

        canvas_trade = Canvas(real_test_frame_4, width = width_canvas, height = height_canvas, bg = "#2B2B2B", cursor = "pencil",border=0,bd=0,highlightthickness=0)
        if signal_trade == 'long':
            h_center = height_canvas*(1-1/(float(TP)/float(SL) + 1))
            canvas_trade.create_line(10,10,width_canvas-10,10,width=2,fill="#5dff3e")
            canvas_trade.create_line(10,height_canvas-10,width_canvas-10,height_canvas-10,width=2,fill="#ff4040")
            x_old = int((index * NewRange1))+10
            y_old = int(round(height_canvas-(((float(price_trade) - price_min) * NewRange) / OldRange),0))-10
        if signal_trade == 'short':
            h_center = height_canvas - height_canvas*(1-1/(float(TP)/float(SL) + 1))
            canvas_trade.create_line(10,10,width_canvas-10,10,width=2,fill="#ff4040")
            canvas_trade.create_line(10,height_canvas-10,width_canvas-10,height_canvas-10,width=2,fill="#5dff3e")
            x_old = int((index * NewRange1))+10
            y_old = int(round((((float(price_trade) - price_min) * NewRange) / OldRange),0))-10
        canvas_trade.create_line(10,h_center,width_canvas-10,h_center,width=2,fill="black")
        canvas_trade.pack(pady=10)
        
        url = 'wss://fstream.binance.com/stream?streams='+symbol.lower()+'@miniTicker'
        async with websockets.connect(url) as ws:
            while True:        
                try:
                    if x_old>680:
                        print('Переполнили канвас!')
                        index=1
                        x_old = x_old - 680
                        canvas_trade.delete("all")
                        if signal_trade == 'long':
                            canvas_trade.create_line(10,10,width_canvas-10,10,width=2,fill="#5dff3e")
                            canvas_trade.create_line(10,height_canvas-10,width_canvas-10,height_canvas-10,width=2,fill="#ff4040")
                        if signal_trade == 'short':
                            canvas_trade.create_line(10,10,width_canvas-10,10,width=2,fill="#ff4040") # красный
                            canvas_trade.create_line(10,height_canvas-10,width_canvas-10,height_canvas-10,width=2,fill="#5dff3e") # зеленый
                        canvas_trade.create_line(10,h_center,width_canvas-10,h_center,width=2,fill="black") # точка входа
                    
                    if signal_trade == 'long':
                        
                        index = index+1
                        data = json.loads(await ws.recv())['data']
                        pnl_proc = round((float(data['c'])/float(price_trade)-1)*100,4)
                        pnl_dol = round(float(value_trade)*float(price_trade)*float(pnl_proc)/100,4)
                        print_components_log(data['c'],real_test_frame_3_1_1,'WS')
                        price_now_ws.configure(text=f"Текущая цена: {data['c']}")
                        x = int((index * NewRange1))+10
                        y = int(round(height_canvas - (((float(data['c']) - price_min) * NewRange) / OldRange),0))-10
                        canvas_trade.create_line(x_old,y_old,x,y,width=1,fill="white") 
                        x_old = x
                        y_old = y
                        
                        if pnl_proc>=0:  # в плюс
                            card_trade_menu_2_pnl.configure(text=f"P&L: {pnl_proc} | {pnl_dol}$",text_color='#0AFF89')
                            card_trade_menu_2_pnl.configure(text_color='#0AFF89')
                        if pnl_proc<0:  # в минус
                            card_trade_menu_2_pnl.configure(text=f"P&L: {pnl_proc}% | {pnl_dol}$",text_color='#DA1010')
                            card_trade_menu_2_pnl.configure(text_color='#DA1010')
                        card_trade_menu_2_balance.configure(text=f"Баланс: {round(DEPOSIT+pnl_dol-comission,4)}$")
                    if signal_trade == 'short':
                        
                        index = index+1
                        data = json.loads(await ws.recv())['data']
                        pnl_proc = round((float(data['c'])/float(price_trade)-1)*100,4)
                        pnl_dol = round(float(value_trade)*float(price_trade)*float(pnl_proc)/100,4)
                        print_components_log(data['c'],real_test_frame_3_1_1,'WS')
                        price_now_ws.configure(text=f"Текущая цена: {data['c']}")
                        x = int((index * NewRange1))+10
                        y = int(round((((float(data['c']) - price_min) * NewRange) / OldRange),0))-10
                        canvas_trade.create_line(x_old,y_old,x,y,width=1,fill="white") 
                        x_old = x
                        y_old = y
                        
                        if pnl_proc<=0: # в минус
                            card_trade_menu_2_pnl.configure(text=f"P&L: {-pnl_proc} | {-pnl_dol}$",text_color='#0AFF89')
                            card_trade_menu_2_pnl.configure(text_color='#0AFF89')
                        if pnl_proc>0: # в плюс
                            card_trade_menu_2_pnl.configure(text=f"P&L: {-pnl_proc}% | {-pnl_dol}$",text_color='#DA1010')
                            card_trade_menu_2_pnl.configure(text_color='#DA1010')
                        card_trade_menu_2_balance.configure(text=f"Баланс: {round(DEPOSIT-pnl_dol-comission,4)}$") 
                    if stop_real_test_trade_flag: break
                    if switch_TG_var2.get()=='off': break
                    if check_trade(data['c'],real_test_frame_3_2_1): # следим за монетой, отрабатываем тп и сл
                        print_components_log('----------------',real_test_frame_3_1_1,'WS')
                        break
                except websockets.exceptions.ConnectionClosed:
                    break
    except Exception as e:
        messagebox.showinfo('Внимание','Ошибка работы вебсокетов')
        print(e)
        
# отчистка ферйма для отрисовки        
def clean_card_menu(frame):
    for widget in frame.winfo_children():
        widget.forget()

# главный цикл работы программы
def start_real_test_trade_model(strat_mas_real_test,real_test_frame_4,card_trade_menu,switch_TG_var2,card_trade_menu_2,real_test_frame_3_1_1,real_test_frame_3_2_1):
    try:
        print_components_log(f'Начали торговлю',real_test_frame_3_2_1,'OS1')
        global coin_mas_10
        global symbol
        global trend_for_print
        global stop_real_test_trade_flag
        global open_sl
        global trend
        global data_print_ad_df
        global how_mach_coin
        global how_mach_candle_get_api
        event = threading.Event()
        coin_mas_10 = get_top_coin()
        stop_real_test_trade_flag = False
        switch_TG_var2.set('on')
        open_sl = False
        while stop_real_test_trade_flag == False or switch_TG_var2.get()=='on':
            try:     
                if open_sl == False:
                    clean_card_menu(card_trade_menu_2)
                    customtkinter.CTkLabel(card_trade_menu_2, text="Нет активных позиций", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=[10,160],padx=35)
                    for x,result in enumerate(coin_mas_10):
                        if stop_real_test_trade_flag: break
                        if switch_TG_var2.get()=='off': break
                        time.sleep(2)
                        trend = check_if_signal(strat_mas_real_test,result,real_test_frame_3_2_1)
                        time.sleep(2) # Интервал в 2 секунд, чтобы бинанс не долбить
                        print_components_log(f'{int(x)+1}({how_mach_coin}) Монета - {result}, {trend}',real_test_frame_3_2_1,'OS1')
                        trend_for_print = trend
                        if int(x) == int(how_mach_coin): break
                        if trend != 'нет сигнала':
                            symbol = result
                            break
                    if trend == "нет сигнала":
                        if stop_real_test_trade_flag: break
                        if switch_TG_var2.get()=='off': break
                        print_components_log(f'Нет сигналов. Ждём {wait_time} минут',real_test_frame_3_2_1,'OS1')
                        time.sleep(wait_time*60)
                    else:
                        price__now = get_price_now_coin(symbol)
                        vol_trade = get_trade_VOLUME(price__now)
                        open_position(trend,vol_trade,price__now,real_test_frame_3_2_1) # если есть сигнал и мы не стоим в позиции, то открываем позицию
                if open_sl == True:  
                    if stop_real_test_trade_flag: break
                    if switch_TG_var2.get()=='off': break
                    loop22 = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop22)
                    loop22 = asyncio.get_event_loop()
                    loop22.run_until_complete(websocket_trade(switch_TG_var2,real_test_frame_4,card_trade_menu_2,real_test_frame_3_1_1,real_test_frame_3_2_1)) 
                    for widget in real_test_frame_4.winfo_children(): # чистим график вебсокетов
                        widget.forget()
                    clean_card_menu(card_trade_menu_2)
                    customtkinter.CTkLabel(card_trade_menu_2, text="Нет активных позиций", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=[10,160],padx=35)
                    # print_components_log(f'Ждём {wait_time*2} минут',real_test_frame_3_2_1,'OS1')
                    # time.sleep(wait_time*2*60)
                if int(DEPOSIT) < 40:
                    break
            except KeyboardInterrupt: #
                
                print_components_log(f'Завершили торговлю',real_test_frame_3_2_1,'OS1')
                break
        print('Нажали на кнопку - завершить торговлю, поток завершился')
        time.sleep(3)
        for widget in card_trade_menu.winfo_children(): # чистим табличку
            widget.forget()
        print_components_log(f'Завершили торговлю',real_test_frame_3_2_1,'OS1')
        data_print_ad_df = []
        open_sl = False # флаг на открытые позиции
        trend = ""
    except Exception as e:
        messagebox.showinfo('Внимание',f'Ошибка работы основного цикла торговли - {e}')
        print_components_log(f'Что то нахуй стомалось - {e}',real_test_frame_3_2_1,'OS1')
        print(e)
            
            
            