
# обработка выбора рабочег о таймфрейма в блоке создания датафреймов
def get_setting_timeframe(data):
    global timeframe_HM
    timeframe_HM = set1_timveframe.get(data) # число 5,15,30,60
    bin.TF = data
    print(time_HM)
# обработка выбора таймфрейма слежения за ценой в блоке создания датафреймов | слежка, сколько времени работаем, по какому основному таймфрейму
def get_setting_timeframe_slega(data):
    global work_timeframe_HM
    global work_timeframe_str_HM
    work_timeframe_str_HM = data
    work_timeframe_HM = set1_timveframe.get(data) # число 1 или 5
    print(work_timeframe_HM)
# обработка выбора времени работы в блоке создания датафреймов
def get_setting_time(data):
    global time_HM
    time_HM = set1_time.get(data) # сколько минут отрабатываем
    print(timeframe_HM)
# кнопка - получить данные, формируем файлы датафреймов
def get_dataframe_with_binance(frame_2_set2_2_1,frame_2_set2_3):
    global work_timeframe_HM
    global timeframe_HM
    global time_HM
    global work_timeframe_str_HM
    bin.VOLUME = int(time_HM/timeframe_HM)
    bin.VOLUME_5MIN = int(time_HM/work_timeframe_HM)

    logger('H','Историческая торговля, формируем датафреймы')
    logger('H',f'Историческая торговля, настройки: рабочий таймфрейм {bin.TF} мин')
    logger('H',f'Историческая торговля, настройки: таймфрейм отслеживания цены {bin.VOLUME_5MIN} мин')
    logger('H',f'Историческая торговля, настройки: Время работы {str(time_HM/60)} часов')
    for widget in frame_2_set2_2_1.winfo_children():
            widget.destroy()
    for widget in frame_2_set2_3.winfo_children():
            widget.destroy()
    thread = threading.Thread(target=lambda:bin.generate_dataframe(bin.TF,bin.VOLUME,bin.VOLUME_5MIN,frame_2_set2_3,work_timeframe_str_HM))
    thread.start()
    time.sleep(3)
    file = open('../ROBO_TRADE/DF/coin_procent.txt', mode="r")
    bin.coin_mas_10 = file.read().split('|')
    i=-1
    for coin in bin.coin_mas_10:
        i=i+1
        customtkinter.CTkButton(frame_2_set2_2_1, text=coin).grid(row=i, column=0, sticky="ew",pady=5)
        
    
    select_frame_by_name("frame_2")
# отрисовка монет из файла, если он не пустой
def get_coin_proc_start(frame_2_set2_2_1):
    file = open('../ROBO_TRADE/DF/coin_procent.txt', mode="r")
    bin.coin_mas_10 = file.read().split('|')
    if bin.coin_mas_10:
        i=-1
        for coin in bin.coin_mas_10:
            i=i+1
            customtkinter.CTkButton(frame_2_set2_2_1, text=coin).grid(row=i, column=0, sticky="ew",pady=5)
# отрисовка датафреймов из файла           
def get_dataset_file_start(frame_2_set2_3_1):
    mypath = '../ROBO_TRADE/DF/5min/'
    filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file
    symbol = filenames[0]
    df = pd.read_csv(f'{bin.MYDIR_WORKER}{symbol}')
    time_F = int(df.iloc[1]['open_time'] - df.iloc[0]['open_time'])/60000
    df2 = pd.read_csv(f'{bin.MYDIR_5MIN}{symbol}')
    time_F2 = int(df2.iloc[1]['open_time'] - df2.iloc[0]['open_time'])/60000

    with open(f'{bin.MYDIR_WORKER}{symbol}') as f:
        time_Work_F = sum(1 for line in f)-1
    bin.VOLUME = int(time_Work_F)
    print(bin.VOLUME)
    customtkinter.CTkLabel(frame_2_set2_3_1,text=f'Рабочий ТF - {int(time_F)} мин' , fg_color="#DAE2EC",text_color='#242424',anchor='w',font=('Arial',12,'normal')).pack(anchor="w")
    customtkinter.CTkLabel(frame_2_set2_3_1,text=f'Длительность - {int(time_Work_F*time_F/60)} часов' , fg_color="#DAE2EC",text_color='#242424',anchor='w',font=('Arial',12,'normal')).pack(anchor="w")
    customtkinter.CTkLabel(frame_2_set2_3_1,text=f'Следим за ценой - {int(time_F2)} мин' , fg_color="#DAE2EC",text_color='#242424',anchor='w',font=('Arial',12,'normal')).pack(anchor="w")
    for name in filenames:
        customtkinter.CTkLabel(frame_2_set2_3_1,text='Найден датасет '+ name , fg_color="#DAE2EC",text_color='#242424',anchor='w',font=('Arial',12,'normal')).pack(anchor="w")
        symbol=name  
# стартуем историческую торговлю
def start_historical_trade_strat_1(frame_2_set2_graph,frame_3_set4_1_2,frame_3_set4_1_1_1,frame_2_set4_2_set_1,frame_2_set4_2_set_2,frame_2_set4_2_set_3,frame_2_set4_2_set_4,frame_2_set4_3_set_1,frame_2_set4_3_set_2,frame_2_set4_3_set_3,frame_2_set4_3_set_4,frame_2_set4_4_set_1,frame_2_set4_4_set_2,frame_2_set4_4_set_3,frame_2_set4_4_set_4):
    try:
        global work_timeframe_HM
        bin.work_timeframe_HM = work_timeframe_HM
        bin.wait_time = int(set1_timveframe.get(bin.TF))
        bin.COMMISSION_MAKER = float(float(frame_2_set4_2_set_1.get())/100)
        bin.COMMISSION_TAKER = float(float(frame_2_set4_2_set_2.get())/100)
        bin.TP = float(float(frame_2_set4_2_set_3.get())/100)
        bin.SL = float(float(frame_2_set4_2_set_4.get())/100)
        bin.DEPOSIT = int(frame_2_set4_3_set_1.get())
        bin.LEVERAGE = int(frame_2_set4_3_set_2.get())
        bin.CANAL_MAX = float(float(frame_2_set4_3_set_3.get())/100)
        bin.CANAL_MIN = float(float(frame_2_set4_3_set_4.get())/100)
        bin.CORNER_LONG = int(frame_2_set4_4_set_1.get())
        bin.CORNER_SHORT = int(frame_2_set4_4_set_2.get())
        bin.CANDLE_COIN_MIN = int(frame_2_set4_4_set_3.get())
        bin.CANDLE_COIN_MAX = int(frame_2_set4_4_set_4.get())
        logger('H','Начинаем историческую торговлю')
        logger('H',f'Настройки ИТ: Комиссия мейкер {bin.COMMISSION_MAKER} | Комиссия тейкер {bin.COMMISSION_TAKER}')
        logger('H',f'Настройки ИТ: Тейк профит {bin.TP} | Стоп лосс {bin.SL}')
        logger('H',f'Настройки ИТ: Депозит {bin.DEPOSIT} | Плечо {bin.LEVERAGE}')
        logger('H',f'Настройки ИТ: Верх канала {bin.CANAL_MAX} | Низ канала {bin.CANAL_MIN}')
        logger('H',f'Настройки ИТ: Угол лонг {bin.CORNER_LONG} | Угол шорт {bin.CORNER_SHORT}')
        logger('H',f'Настройки ИТ: Объём мин {bin.CANDLE_COIN_MIN} | Объём макс {bin.CANDLE_COIN_MAX}')
        for widget in frame_3_set4_1_1_1.winfo_children(): # чистим логи тоговли
            widget.forget()
        for widget in frame_2_set2_graph.winfo_children(): # чистим табличку
            widget.forget()
        thread = threading.Thread(target=lambda:bin.start_trade_hist_model(frame_2_set2_graph,frame_3_set4_1_1_1,frame_3_set4_1_2))
        thread.start()
    except ValueError: 
        messagebox.showinfo('Внимание','Введите правильные значения в настройках торговли')
# открываем логи торгов в блокноте
def open_history_trade_log():
    print('Открыли логи истор торгов')
    os.system("notepad H_log.txt")
frame_2_strat_1 = customtkinter.CTkFrame(win)
frame_2_strat_2 = customtkinter.CTkFrame(win)
frame_2_set2_graph_2 = customtkinter.CTkFrame(win)
frame_2_set2_graph = customtkinter.CTkFrame(win)
frame_3_set4_1 = customtkinter.CTkFrame(win)
frame_3_set4_1_trat_2 = customtkinter.CTkFrame(win)
def start_historical_trade_strat_2_bollindger(frame_2_set2_graph_2):
    try:
        thread25 = threading.Thread(target=lambda:bin_2.main(frame_2_set2_graph_2))
        thread25.start()
    except Exception as e:
        messagebox.showinfo('Внимание','Ошибка начала торговли по стратегии Боллинджера')
def get_strategy_HT(frame_2_set4_0,radio_var):
    print(radio_var.get())
    global frame_2_strat_1
    global frame_2_strat_2
    global frame_2_set2_graph_2
    global frame_2_set2_graph
    global frame_3_set4_1
    global frame_3_set4_1_trat_2
    # первая стратегия
    if radio_var.get() == 1:
        frame_2_strat_1= customtkinter.CTkFrame(frame_2_set4_0, corner_radius=0, fg_color="#2B2B2B")
        frame_2_strat_2.destroy()
        frame_2_set4_2 = customtkinter.CTkFrame(frame_2_strat_1, corner_radius=0, fg_color="#2B2B2B")
        frame_2_set4_3 = customtkinter.CTkFrame(frame_2_strat_1, corner_radius=0, fg_color="#2B2B2B")
        frame_2_set4_4 = customtkinter.CTkFrame(frame_2_strat_1, corner_radius=0, fg_color="#2B2B2B")
        frame_2_set4_2_set_1 = customtkinter.CTkEntry(frame_2_set4_2, placeholder_text="0.2",justify="center")
        frame_2_set4_2_set_2 = customtkinter.CTkEntry(frame_2_set4_2, placeholder_text="0.1",justify="center")
        frame_2_set4_2_set_3 = customtkinter.CTkEntry(frame_2_set4_2, placeholder_text="1.2",justify="center")
        frame_2_set4_2_set_4 = customtkinter.CTkEntry(frame_2_set4_2, placeholder_text="0.4",justify="center")
        label__2_set4_2_set_1 = customtkinter.CTkLabel(frame_2_set4_2, text="Комиссия мейкер, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
        label__2_set4_2_set_2 = customtkinter.CTkLabel(frame_2_set4_2, text="Комиссия тейкер, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
        label__2_set4_2_set_3 = customtkinter.CTkLabel(frame_2_set4_2, text="Тейк профит, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
        label__2_set4_2_set_4 = customtkinter.CTkLabel(frame_2_set4_2, text="Стоп лосс, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
        frame_2_set4_3_set_1 = customtkinter.CTkEntry(frame_2_set4_3, placeholder_text="100",justify="center")
        frame_2_set4_3_set_2 = customtkinter.CTkEntry(frame_2_set4_3, placeholder_text="20",justify="center")
        frame_2_set4_3_set_3 = customtkinter.CTkEntry(frame_2_set4_3, placeholder_text="85",justify="center")
        frame_2_set4_3_set_4 = customtkinter.CTkEntry(frame_2_set4_3, placeholder_text="15",justify="center")
        label__2_set4_3_set_1 = customtkinter.CTkLabel(frame_2_set4_3, text="Деозит, $", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
        label__2_set4_3_set_2 = customtkinter.CTkLabel(frame_2_set4_3, text="Плечо", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
        label__2_set4_3_set_3 = customtkinter.CTkLabel(frame_2_set4_3, text="Верх канала, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
        label__2_set4_3_set_4 = customtkinter.CTkLabel(frame_2_set4_3, text="Низ канала, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
        frame_2_set4_4_set_1 = customtkinter.CTkEntry(frame_2_set4_4, placeholder_text="10",justify="center")
        frame_2_set4_4_set_2 = customtkinter.CTkEntry(frame_2_set4_4, placeholder_text="10",justify="center")
        frame_2_set4_4_set_3 = customtkinter.CTkEntry(frame_2_set4_4, placeholder_text="200000",justify="center")
        frame_2_set4_4_set_4 = customtkinter.CTkEntry(frame_2_set4_4, placeholder_text="500000",justify="center")
        label__2_set4_4_set_1 = customtkinter.CTkLabel(frame_2_set4_4, text="Угол тренда лонг", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
        label__2_set4_4_set_2 = customtkinter.CTkLabel(frame_2_set4_4, text="Угол тренда шорт", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
        label__2_set4_4_set_3 = customtkinter.CTkLabel(frame_2_set4_4, text="Объём торгов мин", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
        label__2_set4_4_set_4 = customtkinter.CTkLabel(frame_2_set4_4, text="Объм торгов макс", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
        frame_2_set4_2_set_1.insert(0, "0.2")
        frame_2_set4_2_set_2.insert(0, "0.1")
        frame_2_set4_2_set_3.insert(0, "1.2")
        frame_2_set4_2_set_4.insert(0, "0.4")
        frame_2_set4_3_set_1.insert(0, "100")
        frame_2_set4_3_set_2.insert(0, "20")
        frame_2_set4_3_set_3.insert(0, "85")
        frame_2_set4_3_set_4.insert(0, "15")
        frame_2_set4_4_set_1.insert(0, "10")
        frame_2_set4_4_set_2.insert(0, "10")
        frame_2_set4_4_set_3.insert(0, "200000")
        frame_2_set4_4_set_4.insert(0, "500000")
        frame_2_strat_1.grid(row=0, column=2, sticky="ew",padx=10)
        frame_2_set4_2.grid(row=0, column=0, sticky="ew",padx=10)
        frame_2_set4_3.grid(row=0, column=1, sticky="ew",padx=10)
        frame_2_set4_4.grid(row=0, column=2, sticky="ew",padx=10)
        label__2_set4_2_set_1.pack(pady=1)
        frame_2_set4_2_set_1.pack(pady=1)
        label__2_set4_2_set_2.pack(pady=1)
        frame_2_set4_2_set_2.pack(pady=1)
        label__2_set4_2_set_3.pack(pady=1)
        frame_2_set4_2_set_3.pack(pady=1)
        label__2_set4_2_set_4.pack(pady=1)
        frame_2_set4_2_set_4.pack(pady=1)
        label__2_set4_3_set_1.pack(pady=1)
        frame_2_set4_3_set_1.pack(pady=1)
        label__2_set4_3_set_2.pack(pady=1)
        frame_2_set4_3_set_2.pack(pady=1)
        label__2_set4_3_set_3.pack(pady=1)
        frame_2_set4_3_set_3.pack(pady=1)
        label__2_set4_3_set_4.pack(pady=1)
        frame_2_set4_3_set_4.pack(pady=1)
        label__2_set4_4_set_1.pack(pady=1)
        frame_2_set4_4_set_1.pack(pady=1)
        label__2_set4_4_set_2.pack(pady=1)
        frame_2_set4_4_set_2.pack(pady=1)
        label__2_set4_4_set_3.pack(pady=1)
        frame_2_set4_4_set_3.pack(pady=1)
        label__2_set4_4_set_4.pack(pady=1)
        frame_2_set4_4_set_4.pack(pady=1)
        button6 = customtkinter.CTkButton(frame_2_strat_1, text="Запустить торговлю",command=lambda:start_historical_trade_strat_1(frame_2_set2_graph,frame_3_set4_1_2,frame_3_set4_1_1_1,frame_2_set4_2_set_1,frame_2_set4_2_set_2,frame_2_set4_2_set_3,frame_2_set4_2_set_4,frame_2_set4_3_set_1,frame_2_set4_3_set_2,frame_2_set4_3_set_3,frame_2_set4_3_set_4,frame_2_set4_4_set_1,frame_2_set4_4_set_2,frame_2_set4_4_set_3,frame_2_set4_4_set_4))
        button6.grid(row=1, column=1, sticky="ew",padx=10,pady=15)
        frame_3_set4_1 = customtkinter.CTkFrame(second_frame, corner_radius=10, fg_color="#2B2B2B")
        frame_3_set4_1_1 = customtkinter.CTkFrame(frame_3_set4_1, corner_radius=0, fg_color="#2B2B2B")
        frame_3_set4_1_2 = customtkinter.CTkFrame(frame_3_set4_1, corner_radius=0, fg_color="#2B2B2B")
        label__3_set4_1_1_set_1 = customtkinter.CTkLabel(frame_3_set4_1_1, text="Логи торговли", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
        frame_3_set4_1_1_1 = customtkinter.CTkScrollableFrame(frame_3_set4_1_1, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=460, height=260)
        customtkinter.CTkLabel(frame_3_set4_1_2, text="Начальный депозит:                         ", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
        customtkinter.CTkLabel(frame_3_set4_1_2, text="Конечный депозит:", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
        customtkinter.CTkLabel(frame_3_set4_1_2, text="Процент торговли:", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
        customtkinter.CTkLabel(frame_3_set4_1_2, text="Сделок совершено:", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
        customtkinter.CTkLabel(frame_3_set4_1_2, text="+ в лонг:  | + в шорт: ", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
        customtkinter.CTkLabel(frame_3_set4_1_2, text="- в лонг:  | - в шорт: ", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
        customtkinter.CTkLabel(frame_3_set4_1_2, text="Прибыль от сделок:", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
        customtkinter.CTkLabel(frame_3_set4_1_2, text="Убыток от сделок:", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
        customtkinter.CTkLabel(frame_3_set4_1_2, text="Комиссия биржи:", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')  
        frame_3_set4_1.pack(pady=[10,10],padx=20)
        frame_3_set4_1_1.grid(row=0, column=1, sticky="ew",padx=10)
        frame_3_set4_1_2.grid(row=0, column=2, sticky="ew",padx=10)
        label__3_set4_1_1_set_1.pack(pady=5)
        frame_3_set4_1_1_1.pack(pady=[5,2])
        frame_2_set2_graph = customtkinter.CTkFrame(second_frame, corner_radius=10, fg_color="transparent") 
        frame_2_set2_graph.pack(pady=[0,20],padx=20)
        for widget in frame_2_set2_graph_2.winfo_children(): # чистим табличку
            widget.forget()
        for widget in frame_3_set4_1_trat_2.winfo_children(): # чистим табличку
            widget.forget()
        frame_2_set2_graph_2.destroy()
        frame_3_set4_1_trat_2.destroy()
        
    # стратегия - линии Боллинджера
    if radio_var.get() == 2:
        frame_2_strat_2= customtkinter.CTkFrame(frame_2_set4_0, corner_radius=0, fg_color="#2B2B2B")
        for widget in frame_2_strat_1.winfo_children(): # чистим табличку
            widget.forget()
        for widget in frame_2_set2_graph.winfo_children(): # чистим табличку
            widget.forget()
        for widget in frame_3_set4_1.winfo_children(): # чистим табличку
            widget.forget()
        frame_2_strat_1.destroy()
        frame_2_set2_graph.destroy()
        frame_3_set4_1.destroy()
        frame_2_strat_2.grid(row=0, column=2, sticky="ew",padx=10)
        frame_2_set4_2 = customtkinter.CTkFrame(frame_2_strat_2, corner_radius=0, fg_color="#2B2B2B")
        frame_2_set4_3 = customtkinter.CTkFrame(frame_2_strat_2, corner_radius=0, fg_color="#2B2B2B")
        frame_2_set4_4 = customtkinter.CTkFrame(frame_2_strat_2, corner_radius=0, fg_color="#2B2B2B")
        frame_2_set4_2.grid(row=0, column=0, sticky="ew",padx=10)
        frame_2_set4_3.grid(row=0, column=1, sticky="ew",padx=10)
        frame_2_set4_4.grid(row=0, column=2, sticky="ew",padx=10)
        button6 = customtkinter.CTkButton(frame_2_set4_3, text="Запустить торговлю",command=lambda:start_historical_trade_strat_2_bollindger(frame_2_set2_graph_2))
        button6.grid(row=0, column=0, sticky="ew",padx=10,pady=15)
        frame_3_set4_1_trat_2 = customtkinter.CTkFrame(second_frame, corner_radius=10, fg_color="#2B2B2B")
        frame_3_set4_1_1 = customtkinter.CTkFrame(frame_3_set4_1_trat_2, corner_radius=0, fg_color="#2B2B2B")
        frame_3_set4_1_2 = customtkinter.CTkFrame(frame_3_set4_1_trat_2, corner_radius=0, fg_color="#2B2B2B")
        label__3_set4_1_1_set_1 = customtkinter.CTkLabel(frame_3_set4_1_1, text="Логи торговли", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
        frame_3_set4_1_1_1 = customtkinter.CTkScrollableFrame(frame_3_set4_1_1, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=460, height=260)
        customtkinter.CTkLabel(frame_3_set4_1_2, text="Начальный депозит:                         ", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
        customtkinter.CTkLabel(frame_3_set4_1_2, text="Конечный депозит:", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
        customtkinter.CTkLabel(frame_3_set4_1_2, text="Процент торговли:", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
        customtkinter.CTkLabel(frame_3_set4_1_2, text="Сделок совершено:", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
        customtkinter.CTkLabel(frame_3_set4_1_2, text="+ в лонг:  | + в шорт: ", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
        customtkinter.CTkLabel(frame_3_set4_1_2, text="- в лонг:  | - в шорт: ", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
        customtkinter.CTkLabel(frame_3_set4_1_2, text="Прибыль от сделок:", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
        customtkinter.CTkLabel(frame_3_set4_1_2, text="Убыток от сделок:", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')
        customtkinter.CTkLabel(frame_3_set4_1_2, text="Комиссия биржи:", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).pack(pady=1, anchor='w')  
        frame_3_set4_1_trat_2.pack(pady=[10,10],padx=20)
        frame_3_set4_1_1.grid(row=0, column=1, sticky="ew",padx=10)
        frame_3_set4_1_2.grid(row=0, column=2, sticky="ew",padx=10)
        label__3_set4_1_1_set_1.pack(pady=5)
        frame_3_set4_1_1_1.pack(pady=[5,2])
        frame_2_set2_graph_2 = customtkinter.CTkFrame(second_frame, corner_radius=10, fg_color="transparent") 
        frame_2_set2_graph_2.pack(pady=[0,20],padx=20)   
# отрисовка страницы - историческая торговля
def historical_trade():
    label_title1 = customtkinter.CTkLabel(second_frame, text="Торговля по историческим данным", fg_color="transparent",anchor='center',font=('Arial',20,'bold'))
    frame_2_set1 = customtkinter.CTkFrame(second_frame, corner_radius=10, fg_color="transparent")
    button1 = customtkinter.CTkButton(frame_2_set1, text="Информация")
    button2 = customtkinter.CTkButton(frame_2_set1, text="Инструкция")
    button3 = customtkinter.CTkButton(frame_2_set1, text="История торгов",command=open_history_trade_log)
    frame_2_set2 = customtkinter.CTkFrame(second_frame, corner_radius=10, fg_color="#2B2B2B")
    frame_2_set2_1 = customtkinter.CTkFrame(frame_2_set2, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set2_2 = customtkinter.CTkFrame(frame_2_set2, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set2_3 = customtkinter.CTkFrame(frame_2_set2, corner_radius=0, fg_color="#2B2B2B")
    #----
    label_title1_1 = customtkinter.CTkLabel(frame_2_set2_1, text="Сбор данных", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    label_title1_1_0 = customtkinter.CTkLabel(frame_2_set2_1, text="Следим за ценой", fg_color="transparent",anchor='center',font=('Arial',12,'normal'))
    appearance_mode_menu0 = customtkinter.CTkOptionMenu(frame_2_set2_1, values=["1m", "5m"],command=get_setting_timeframe_slega)
    label_title1_1_1 = customtkinter.CTkLabel(frame_2_set2_1, text="Рабочий таймфрейм", fg_color="transparent",anchor='center',font=('Arial',12,'normal'))
    appearance_mode_menu1 = customtkinter.CTkOptionMenu(frame_2_set2_1, values=["5m", "15m", "30m", "1h"],command=get_setting_timeframe)
    label_title1_1_2 = customtkinter.CTkLabel(frame_2_set2_1, text="Длительность", fg_color="transparent",anchor='center',font=('Arial',12,'normal'))
    appearance_mode_menu2 = customtkinter.CTkOptionMenu(frame_2_set2_1, values=["12 часов", "24 часа", "2 дня", "3 дня"],command=get_setting_time)
    button4 = customtkinter.CTkButton(frame_2_set2_1, text="Получить данные", command=lambda:get_dataframe_with_binance(frame_2_set2_2_1,frame_2_set2_3_1))
    #----
    label_title1_2 = customtkinter.CTkLabel(frame_2_set2_2, text="Монеты роста/падения", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    frame_2_set2_2_1 = customtkinter.CTkScrollableFrame(frame_2_set2_2, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=150, height=50)
    # ----
    label_title1_3_1 = customtkinter.CTkLabel(frame_2_set2_3, text="Датасет с биржи Binance", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    label_title1_3_2 = customtkinter.CTkLabel(frame_2_set2_3, text="                                     ", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    frame_2_set2_3_1 = customtkinter.CTkScrollableFrame(frame_2_set2_3, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=200, height=50)
    # ----
    frame_2_set4 = customtkinter.CTkFrame(second_frame, corner_radius=10, fg_color="#2B2B2B")
    label__2_set4 = customtkinter.CTkLabel(frame_2_set4, text="Настройка торговли", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    frame_2_set4_0 = customtkinter.CTkFrame(frame_2_set4, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_1 = customtkinter.CTkFrame(frame_2_set4_0, corner_radius=0, fg_color="#2B2B2B")
    label__2_set4_1_1 = customtkinter.CTkLabel(frame_2_set4_1, text="Выбор стратегии", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    frame_2_set4_1_1 = customtkinter.CTkScrollableFrame(frame_2_set4_1, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=200, height=250)
    radio_var = tkinter.IntVar(value=1)
    radiobutton_1 = customtkinter.CTkRadioButton(frame_2_set4_1_1, text="Канал, тренд, локаль, \nобъём", variable= radio_var, value=1,text_color='#242424',command = lambda:get_strategy_HT(frame_2_set4_0,radio_var))
    radiobutton_2 = customtkinter.CTkRadioButton(frame_2_set4_1_1, text="Линии Боллинджера", variable= radio_var, value=2,text_color='#242424',command = lambda:get_strategy_HT(frame_2_set4_0,radio_var))
    # ----

    get_coin_proc_start(frame_2_set2_2_1)
    get_dataset_file_start(frame_2_set2_3_1)
    label_title1.pack(pady=20)
    frame_2_set1.pack(pady=10,padx=20)
    button1.grid(row=0, column=0, sticky="ew",padx=10)
    button2.grid(row=0, column=1, sticky="ew",padx=10)
    button3.grid(row=0, column=2, sticky="ew",padx=10)
    frame_2_set2.pack(pady=10)
    frame_2_set2_1.grid(row=0, column=1, sticky="ew",padx=10)
    frame_2_set2_2.grid(row=0, column=2, sticky="ew",padx=10)
    frame_2_set2_3.grid(row=0, column=3, sticky="ew",padx=10,columnspan = 2)
    label_title1_1.grid(row=0, column=0, sticky="ew")
    label_title1_1_0.grid(row=1, column=0, sticky="ew")
    appearance_mode_menu0.grid(row=2, column=0, sticky="ew",pady=[0,5])
    label_title1_1_1.grid(row=3, column=0, sticky="ew")
    appearance_mode_menu1.grid(row=4, column=0, sticky="ew",pady=[0,5])
    label_title1_1_2.grid(row=5, column=0, sticky="ew")
    appearance_mode_menu2.grid(row=6, column=0, sticky="ew",pady=[0,5])
    button4.grid(row=7, column=0, sticky="ew",pady=15,padx=20)
    label_title1_2.grid(row=0, column=0, sticky="ew",pady=10)
    frame_2_set2_2_1.grid(row=1, column=0, sticky="ew",pady=[0,20])
    label_title1_3_1.grid(row=0, column=0, sticky="ew",pady=10)
    label_title1_3_2.grid(row=0, column=1, sticky="ew",pady=10)
    frame_2_set2_3_1.grid(row=1, column=0, columnspan=2, sticky="ew",pady=[0,20])
    frame_2_set4.pack(pady=10, padx=20)
    label__2_set4.pack(pady=5)
    frame_2_set4_0.pack(pady=10)
    frame_2_set4_1.grid(row=0, column=1, sticky="ew",padx=10)
    label__2_set4_1_1.pack(pady=4)
    frame_2_set4_1_1.pack(pady=4)
    radiobutton_1.pack(pady=4, anchor='w')
    radiobutton_2.pack(pady=4, anchor='w')
    get_strategy_HT(frame_2_set4_0,radio_var)
    