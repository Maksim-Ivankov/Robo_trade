 label_title1 = customtkinter.CTkLabel(third_frame, text="Реальная тестовая торговля", fg_color="transparent",anchor='center',font=('Arial',20,'bold'))
    frame_2_set1 = customtkinter.CTkFrame(third_frame, corner_radius=10, fg_color="transparent")
    button1 = customtkinter.CTkButton(frame_2_set1, text="Информация")
    button2 = customtkinter.CTkButton(frame_2_set1, text="Инструкция")
    button3 = customtkinter.CTkButton(frame_2_set1, text="История торгов", command = open_real_test_trade_log)
    # ----------
    frame_2_set4_0 = customtkinter.CTkFrame(master=third_frame,width=1100,height=800, corner_radius=10, fg_color="#2B2B2B")
    frame_2_set4_1 = customtkinter.CTkFrame(frame_2_set4_0, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_2 = customtkinter.CTkFrame(frame_2_set4_0, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_25 = customtkinter.CTkFrame(frame_2_set4_0, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_3 = customtkinter.CTkFrame(frame_2_set4_0, corner_radius=0, fg_color="#2B2B2B")
    label_title2_1 = customtkinter.CTkLabel(frame_2_set4_1, text="Имя робота для логов", fg_color="transparent",anchor='center',font=('Arial',12,'bold'),width=200)
    input_2_1 = customtkinter.CTkEntry(frame_2_set4_1, placeholder_text="Версия 1_1",justify="center")
    real_test_trade_frame_1_label_title1_1_1 = customtkinter.CTkLabel(frame_2_set4_25, text="Таймфрейм", fg_color="transparent",anchor='center',font=('Arial',12,'normal'))
    real_test_trade_frame_1_appearance_mode_menu1 = customtkinter.CTkOptionMenu(frame_2_set4_25, values=["5m", "15m", "30m", "1h"],command=get_setting_timeframe_real_test_trad)
    label_title3_1 = customtkinter.CTkLabel(frame_2_set4_2, text="Сколько топ монет торговать", fg_color="transparent",anchor='center',font=('Arial',12,'bold'),width=200)
    input_3_1 = customtkinter.CTkEntry(frame_2_set4_2, placeholder_text="10",justify="center")
    switch_TG_var = customtkinter.StringVar(value="off")
    switch_tg = customtkinter.CTkSwitch(frame_2_set4_3, text="Оповещения в ТГ",variable=switch_TG_var, onvalue="on", offvalue="off")
    # ----------    
    frame_2_set4 = customtkinter.CTkFrame(third_frame, corner_radius=10, fg_color="#2B2B2B")
    label__2_set4 = customtkinter.CTkLabel(frame_2_set4, text="Настройка торговли", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    frame_2_set4_01 = customtkinter.CTkFrame(frame_2_set4, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_11 = customtkinter.CTkFrame(frame_2_set4_01, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_21 = customtkinter.CTkFrame(frame_2_set4_01, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_31 = customtkinter.CTkFrame(frame_2_set4_01, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_41 = customtkinter.CTkFrame(frame_2_set4_01, corner_radius=0, fg_color="#2B2B2B")
    label__2_set4_1_1 = customtkinter.CTkLabel(frame_2_set4_11, text="Выбор стратегии", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    frame_2_set4_1_1 = customtkinter.CTkScrollableFrame(frame_2_set4_11, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=200, height=50)
    radio_var = tkinter.IntVar(value=1)
    radiobutton_1 = customtkinter.CTkRadioButton(frame_2_set4_1_1, text="Канал, тренд, локаль, \nобъём", variable= radio_var, value=1,text_color='#242424',state="disabled")
    radiobutton_2 = customtkinter.CTkRadioButton(frame_2_set4_1_1, text="Скользящие средние", variable= radio_var, value=2,text_color='#242424',state="disabled")
    real_test_trade_frame_2_set4_2_set_1 = customtkinter.CTkEntry(frame_2_set4_21, placeholder_text="0.2",justify="center")
    real_test_trade_frame_2_set4_2_set_2 = customtkinter.CTkEntry(frame_2_set4_21, placeholder_text="0.1",justify="center")
    real_test_trade_frame_2_set4_2_set_3 = customtkinter.CTkEntry(frame_2_set4_21, placeholder_text="1.2",justify="center")
    real_test_trade_frame_2_set4_2_set_4 = customtkinter.CTkEntry(frame_2_set4_21, placeholder_text="0.4",justify="center")
    real_test_trade_label__2_set4_2_set_1 = customtkinter.CTkLabel(frame_2_set4_21, text="Комиссия мейкер, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_trade_label__2_set4_2_set_2 = customtkinter.CTkLabel(frame_2_set4_21, text="Комиссия тейкер, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_trade_label__2_set4_2_set_3 = customtkinter.CTkLabel(frame_2_set4_21, text="Тейк профит, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_trade_label__2_set4_2_set_4 = customtkinter.CTkLabel(frame_2_set4_21, text="Стоп лосс, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_trade_frame_2_set4_3_set_1 = customtkinter.CTkEntry(frame_2_set4_31, placeholder_text="100",justify="center")
    real_test_trade_frame_2_set4_3_set_2 = customtkinter.CTkEntry(frame_2_set4_31, placeholder_text="20",justify="center")
    real_test_trade_frame_2_set4_3_set_3 = customtkinter.CTkEntry(frame_2_set4_31, placeholder_text="85",justify="center")
    real_test_trade_frame_2_set4_3_set_4 = customtkinter.CTkEntry(frame_2_set4_31, placeholder_text="15",justify="center")
    real_test_trade_label__2_set4_3_set_1 = customtkinter.CTkLabel(frame_2_set4_31, text="Деозит, $", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_trade_label__2_set4_3_set_2 = customtkinter.CTkLabel(frame_2_set4_31, text="Плечо", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_trade_label__2_set4_3_set_3 = customtkinter.CTkLabel(frame_2_set4_31, text="Верх канала, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_trade_label__2_set4_3_set_4 = customtkinter.CTkLabel(frame_2_set4_31, text="Низ канала, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_trade_frame_2_set4_4_set_1 = customtkinter.CTkEntry(frame_2_set4_41, placeholder_text="10",justify="center")
    real_test_trade_frame_2_set4_4_set_2 = customtkinter.CTkEntry(frame_2_set4_41, placeholder_text="10",justify="center")
    real_test_trade_frame_2_set4_4_set_3 = customtkinter.CTkEntry(frame_2_set4_41, placeholder_text="200000",justify="center")
    real_test_trade_frame_2_set4_4_set_4 = customtkinter.CTkEntry(frame_2_set4_41, placeholder_text="500000",justify="center")
    real_test_trade_label__2_set4_4_set_1 = customtkinter.CTkLabel(frame_2_set4_41, text="Угол тренда лонг", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_trade_label__2_set4_4_set_2 = customtkinter.CTkLabel(frame_2_set4_41, text="Угол тренда шорт", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_trade_label__2_set4_4_set_3 = customtkinter.CTkLabel(frame_2_set4_41, text="Объём торгов мин", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_trade_label__2_set4_4_set_4 = customtkinter.CTkLabel(frame_2_set4_41, text="Объм торгов макс", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_trade_frame_2_set4_2_set_1.insert(0, "0.2")
    real_test_trade_frame_2_set4_2_set_2.insert(0, "0.1")
    real_test_trade_frame_2_set4_2_set_3.insert(0, "1.2")
    real_test_trade_frame_2_set4_2_set_4.insert(0, "0.4")
    real_test_trade_frame_2_set4_3_set_1.insert(0, "100")
    real_test_trade_frame_2_set4_3_set_2.insert(0, "20")
    real_test_trade_frame_2_set4_3_set_3.insert(0, "85")
    real_test_trade_frame_2_set4_3_set_4.insert(0, "15")
    real_test_trade_frame_2_set4_4_set_1.insert(0, "10")
    real_test_trade_frame_2_set4_4_set_2.insert(0, "10")
    real_test_trade_frame_2_set4_4_set_3.insert(0, "200000")
    real_test_trade_frame_2_set4_4_set_4.insert(0, "500000")
     # --------------------------------
    real_test_frame_2_buttons = customtkinter.CTkFrame(master=third_frame, corner_radius=10, fg_color="transparent")
    start_trade_real_test = customtkinter.CTkButton(real_test_frame_2_buttons, text="Запустить торговлю",command=lambda:start_real_test_trade_btn(input_3_1,real_test_frame_4,input_2_1,switch_TG_var,real_test_frame_3_1_1,real_test_frame_3_2_1,real_test_trade_frame_2_set4_2_set_1,real_test_trade_frame_2_set4_2_set_2,real_test_trade_frame_2_set4_2_set_3,real_test_trade_frame_2_set4_2_set_4,real_test_trade_frame_2_set4_3_set_1,real_test_trade_frame_2_set4_3_set_2,real_test_trade_frame_2_set4_3_set_3,real_test_trade_frame_2_set4_3_set_4,real_test_trade_frame_2_set4_4_set_1,real_test_trade_frame_2_set4_4_set_2,real_test_trade_frame_2_set4_4_set_3,real_test_trade_frame_2_set4_4_set_4))
    stop_trade_real_test = customtkinter.CTkButton(real_test_frame_2_buttons, text="Остановить торговлю", command=stop_real_test_trade)
    # --------------------------------
    real_test_frame_3 = customtkinter.CTkFrame(master=third_frame, corner_radius=10, fg_color="#2B2B2B")
    real_test_frame_3_1 = customtkinter.CTkFrame(real_test_frame_3, corner_radius=0, fg_color="#2B2B2B")
    real_test_frame_3_2 = customtkinter.CTkFrame(real_test_frame_3, corner_radius=0, fg_color="#2B2B2B")
    real_test_label_3_1 = customtkinter.CTkLabel(real_test_frame_3_1, text="Данные по монете в сделке", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_frame_3_1_1 = customtkinter.CTkScrollableFrame(real_test_frame_3_1, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=160, height=260)
    real_test_label_3_2 = customtkinter.CTkLabel(real_test_frame_3_2, text="Логи торговли", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_frame_3_2_1 = customtkinter.CTkScrollableFrame(real_test_frame_3_2, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=460, height=260)
    #----------------------------------
    real_test_frame_4 = customtkinter.CTkFrame(master=third_frame, corner_radius=10, fg_color="transparent")
    input_2_1.insert(0, "Версия 1_1")
    input_3_1.insert(0, "10")
    
    label_title1.pack(pady=20)
    frame_2_set1.pack(pady=10,padx=20)
    button1.grid(row=0, column=0, sticky="ew",padx=10)
    button2.grid(row=0, column=1, sticky="ew",padx=10)
    button3.grid(row=0, column=2, sticky="ew",padx=10)
    frame_2_set4_0.pack(pady=10,ipady = 10,ipadx=5)
    frame_2_set4_1.grid(row=0, column=1, sticky="ew",padx=5)
    frame_2_set4_2.grid(row=0, column=2, sticky="ew",padx=5)
    frame_2_set4_25.grid(row=0, column=3, sticky="ew",padx=[5,15])
    frame_2_set4_3.grid(row=0, column=4, sticky="ew",padx=5)
    real_test_trade_frame_1_label_title1_1_1.pack(pady=[10,0])
    real_test_trade_frame_1_appearance_mode_menu1.pack(pady=0)
    label_title2_1.pack(pady=[10,0])
    input_2_1.pack(pady=0)
    label_title3_1.pack(pady=[10,0])
    input_3_1.pack(pady=0)
    switch_tg.pack(pady=[10,0])
    frame_2_set4.pack(pady=10, padx=20)
    label__2_set4.pack(pady=5)
    frame_2_set4_01.pack(pady=10)
    frame_2_set4_11.grid(row=0, column=1, sticky="ew",padx=10)
    frame_2_set4_21.grid(row=0, column=2, sticky="ew",padx=10)
    frame_2_set4_31.grid(row=0, column=3, sticky="ew",padx=10)
    frame_2_set4_41.grid(row=0, column=4, sticky="ew",padx=10)
    label__2_set4_1_1.pack(pady=4)
    frame_2_set4_1_1.pack(pady=4)
    radiobutton_1.pack(pady=4, anchor='w')
    radiobutton_2.pack(pady=4, anchor='w')
    real_test_trade_label__2_set4_2_set_1.pack(pady=1)
    #!!!
    real_test_trade_frame_2_set4_2_set_1.pack(pady=1)
    real_test_trade_label__2_set4_2_set_2.pack(pady=1)
    real_test_trade_frame_2_set4_2_set_2.pack(pady=1)
    real_test_trade_label__2_set4_2_set_3.pack(pady=1)
    real_test_trade_frame_2_set4_2_set_3.pack(pady=1)
    real_test_trade_label__2_set4_2_set_4.pack(pady=1)
    real_test_trade_frame_2_set4_2_set_4.pack(pady=1)
    real_test_trade_label__2_set4_3_set_1.pack(pady=1)
    real_test_trade_frame_2_set4_3_set_1.pack(pady=1)
    real_test_trade_label__2_set4_3_set_2.pack(pady=1)
    real_test_trade_frame_2_set4_3_set_2.pack(pady=1)
    real_test_trade_label__2_set4_3_set_3.pack(pady=1)
    real_test_trade_frame_2_set4_3_set_3.pack(pady=1)
    real_test_trade_label__2_set4_3_set_4.pack(pady=1)
    real_test_trade_frame_2_set4_3_set_4.pack(pady=1)
    real_test_trade_label__2_set4_4_set_1.pack(pady=1)
    real_test_trade_frame_2_set4_4_set_1.pack(pady=1)
    real_test_trade_label__2_set4_4_set_2.pack(pady=1)
    real_test_trade_frame_2_set4_4_set_2.pack(pady=1)
    real_test_trade_label__2_set4_4_set_3.pack(pady=1)
    real_test_trade_frame_2_set4_4_set_3.pack(pady=1)
    real_test_trade_label__2_set4_4_set_4.pack(pady=1)
    real_test_trade_frame_2_set4_4_set_4.pack(pady=1)
    real_test_frame_2_buttons.pack(pady=[10,0],padx=20)
    start_trade_real_test.grid(row=0, column=0, sticky="ew",padx=10)
    stop_trade_real_test.grid(row=0, column=1, sticky="ew",padx=10)
    #---
    real_test_frame_3.pack(pady=20)
    real_test_frame_3_1.grid(row=0, column=0, sticky="ew",padx=10)
    real_test_frame_3_2.grid(row=0, column=1, sticky="ew",padx=10)
    real_test_label_3_1.pack(pady=0)
    real_test_frame_3_1_1.pack(pady=0)
    real_test_label_3_2.pack(pady=0)
    real_test_frame_3_2_1.pack(pady=0)
    #---
    real_test_frame_4.pack(pady=20)