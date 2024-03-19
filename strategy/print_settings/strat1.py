import customtkinter


def strat1(frame,open_step_2_historical):
    label_title112 = customtkinter.CTkLabel(frame, text="Настройте стратегии и запустите торговлю", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    frame_2_strat_1= customtkinter.CTkFrame(frame, corner_radius=0, fg_color="#2B2B2B")
    label__2_set4_2_set_1_title = customtkinter.CTkLabel(frame_2_strat_1, text="Канал, тренд, локаль, объём", fg_color="transparent",anchor='center',font=('Arial',15,'bold'))
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
    frame_2_set412 = customtkinter.CTkFrame(frame, corner_radius=10, fg_color="transparent")
    button3212 = customtkinter.CTkButton(frame_2_set412, text="Назад",command=lambda:open_step_2_historical(frame))
    button3213 = customtkinter.CTkButton(frame_2_set412, text="Запустить торговлю")
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
    label_title112.pack(pady=0, anchor='n')
    frame_2_strat_1.pack(pady=20, anchor='n')
    label__2_set4_2_set_1_title.grid(row=0, column=0, sticky="ew",padx=10,columnspan = 3,pady=10)
    frame_2_set4_2.grid(row=1, column=0, sticky="ew",padx=10)
    frame_2_set4_3.grid(row=1, column=1, sticky="ew",padx=10)
    frame_2_set4_4.grid(row=1, column=2, sticky="ew",padx=10)
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
    frame_2_set4_4_set_4.pack(pady=20)
    frame_2_set412.pack(pady=20, anchor='n')
    button3212.grid(row=0, column=0, sticky="ew",padx=10)
    button3213.grid(row=0, column=1, sticky="ew",padx=10)
    # button6 = customtkinter.CTkButton(frame_2_strat_1, text="Запустить торговлю")
    # button6 = customtkinter.CTkButton(frame_2_strat_1, text="Запустить торговлю",command=lambda:start_historical_trade_strat_1(frame_2_set2_graph,frame_3_set4_1_2,frame_3_set4_1_1_1,frame_2_set4_2_set_1,frame_2_set4_2_set_2,frame_2_set4_2_set_3,frame_2_set4_2_set_4,frame_2_set4_3_set_1,frame_2_set4_3_set_2,frame_2_set4_3_set_3,frame_2_set4_3_set_4,frame_2_set4_4_set_1,frame_2_set4_4_set_2,frame_2_set4_4_set_3,frame_2_set4_4_set_4))
    # button6.grid(row=1, column=1, sticky="ew",padx=10,pady=15)
    