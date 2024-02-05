from imports import *
import models.treayd_historical as bin
import models.real_test_trade as real





set1_timveframe = {"5m":5, "15m":15, "30m":30, "1h":60,"1m":1}
set1_time = {"12 часов":720, "24 часа":1440, "2 дня":2880, "3 дня":4320}
work_timeframe_HM = 1
work_timeframe_str_HM = '1m'
timeframe_HM = 5
time_HM = 720


# открываем по центру
win = customtkinter.CTk()
win.title("Robo_trade")
w = 1020
h = 800
ws = win.winfo_screenwidth()
hs = win.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
win.geometry('%dx%d+%d+%d' % (w, h, x, y))    
# выстраиваем сетку гридов
win.grid_rowconfigure(0, weight=1)
win.grid_columnconfigure(1, weight=1)

coin_mas_10 = []

#Логер в файлы
def logger(name_log,msg):
    path = name_log+'_log.txt'
    f = open(path,'a',encoding='utf-8')
    f.write('\n'+time.strftime("%d.%m.%Y | %H:%M:%S | ", time.localtime())+msg)
    f.close()
logger('H','------------------------------------------------------------')
logger('H','Открыли Robo_Trade')

from component.UI.images.images import * # импорт всех картинок, которые используем здесь

#бработка нажатия по кнопкам
def home_button_event():
    select_frame_by_name("home")
def frame_2_button_event():
    select_frame_by_name("frame_2")
def frame_3_button_event():
    select_frame_by_name("frame_3")
def frame_4_button_event():
    select_frame_by_name("frame_4")
def frame_5_button_event():
    select_frame_by_name("frame_5")
def frame_6_button_event():
    select_frame_by_name("frame_6")
def frame_7_button_event():
    select_frame_by_name("frame_7")
def frame_8_button_event():
    select_frame_by_name("frame_8")
    
# создаем навигацию фреймов - фреймы и кнопки
navigation_frame = customtkinter.CTkFrame(win, corner_radius=0)
navigation_frame_label = customtkinter.CTkLabel(navigation_frame, text="Робо трейд", image=logo_image,compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
home_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Главная",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=home_image, anchor="w", command=home_button_event)
frame_2_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Историческая торговля",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=chat_image_1, anchor="w", command=frame_2_button_event)
frame_3_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Реальная тестовая торговля",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=chat_image_3, anchor="w", command=frame_3_button_event)
frame_4_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Фьючерсы Binance",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=chat_image_2, anchor="w", command=frame_4_button_event)
frame_5_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Торговый робот",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=chat_image_4, anchor="w", command=frame_5_button_event)
frame_6_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="FAQ",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=chat_image_6, anchor="w", command=frame_6_button_event)
frame_7_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Профиль",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=chat_image_5, anchor="w", command=frame_7_button_event)
frame_8_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Настройки программы",fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=chat_image_7, anchor="w", command=frame_8_button_event)
time_now = customtkinter.CTkLabel(navigation_frame, text=time.strftime("%d.%m.%Y г. %H:%M:%S", time.localtime()),compound="left", font=customtkinter.CTkFont(size=12, weight="normal"))
home_frame = customtkinter.CTkFrame(win, corner_radius=0, fg_color="transparent")
second_frame = customtkinter.CTkScrollableFrame(win, corner_radius=0, fg_color="transparent",orientation='vertical')
third_frame = customtkinter.CTkScrollableFrame(win, corner_radius=0, fg_color="transparent",orientation='vertical')
frame_4 = customtkinter.CTkFrame(win, corner_radius=0, fg_color="transparent")
frame_5 = customtkinter.CTkFrame(win, corner_radius=0, fg_color="transparent")
frame_6 = customtkinter.CTkFrame(win, corner_radius=0, fg_color="transparent")
frame_7 = customtkinter.CTkFrame(win, corner_radius=0, fg_color="transparent")
frame_8 = customtkinter.CTkFrame(win, corner_radius=0, fg_color="transparent")
frame_loading = customtkinter.CTkFrame(win, corner_radius=0, fg_color="transparent")
card_trade_menu = customtkinter.CTkFrame(navigation_frame, corner_radius=0, fg_color="transparent")

def update_time():
    time_now.configure(text=time.strftime("%d.%m.%Y г. %H:%M:%S", time.localtime()))
    win.after(100, update_time)  # Запланировать выполнение этой же функции через 100 миллисекунд
#рисуем навигацию и фреймы
navigation_frame.grid(row=0, column=0, sticky="nsew")
navigation_frame.grid_rowconfigure(9, weight=1)
navigation_frame_label.grid(row=0, column=0, padx=0, pady=20)
home_button.grid(row=1, column=0, sticky="ew")
frame_2_button.grid(row=2, column=0, sticky="ew")
frame_3_button.grid(row=3, column=0, sticky="ew")
frame_4_button.grid(row=4, column=0, sticky="ew")
frame_5_button.grid(row=5, column=0, sticky="ew")
frame_6_button.grid(row=6, column=0, sticky="ew")
frame_7_button.grid(row=7, column=0, sticky="ew")
frame_8_button.grid(row=8, column=0, sticky="ew")
card_trade_menu.grid(row=9, column=0, sticky="ew")
time_now.grid(row=10, column=0, sticky="s",pady=20)

def select_frame_by_name(name): #выбирает и открывает фрейм
    home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
    frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
    frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
    frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
    frame_5_button.configure(fg_color=("gray75", "gray25") if name == "frame_5" else "transparent")
    frame_6_button.configure(fg_color=("gray75", "gray25") if name == "frame_6" else "transparent")
    frame_7_button.configure(fg_color=("gray75", "gray25") if name == "frame_7" else "transparent")
    frame_8_button.configure(fg_color=("gray75", "gray25") if name == "frame_8" else "transparent")
    # показать выбранный фрейм
    if name == "home":
        home_frame.grid(row=0, column=1, sticky="nsew")
    else:
        home_frame.grid_forget()
    if name == "frame_2":
        second_frame.grid(row=0, column=1, sticky="nsew")
    else:
        second_frame.grid_forget()
    if name == "frame_3":
        third_frame.grid(row=0, column=1, sticky="nsew")
    else:
        third_frame.grid_forget()
    if name == "frame_4":
        frame_4.grid(row=0, column=1, sticky="nsew")
    else:
        frame_4.grid_forget()
    if name == "frame_5":
        frame_5.grid(row=0, column=1, sticky="nsew")
    else:
        frame_5.grid_forget()
    if name == "frame_6":
        frame_6.grid(row=0, column=1, sticky="nsew")
    else:
        frame_6.grid_forget()
    if name == "frame_7":
        frame_7.grid(row=0, column=1, sticky="nsew")
    else:
        frame_7.grid_forget()
    if name == "frame_8":
        frame_8.grid(row=0, column=1, sticky="nsew")
    else:
        frame_8.grid_forget()
    if name == "frame_loading":
        frame_loading.grid(row=0, column=1, sticky="nsew")
    else:
        frame_loading.grid_forget()
        
        

        # создаем страницы фреймов
select_frame_by_name("home")
frame_8.grid_columnconfigure(0, weight=2)

# --------------------------------- НАСТРОЙКИ ПРОГРАММЫ ---------------------------------
# меняем ржим ночной или дневной
def change_appearance_mode_event(new_appearance_mode):
    customtkinter.set_appearance_mode(new_appearance_mode)
# получаем текущий ip c сайта - https://api.ipify.org
def get_my_ip():
    return requests.get('https://api.ipify.org').content.decode('utf8')
# получаем таблицу бесплатных прокси с сайта - https://free-proxy-list.net/
def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # получаем ответ HTTP и создаем объект soup
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    host = []
    for row in soup.find("table", attrs={"class": "table"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            kod = tds[2].text.strip()
            country = tds[3].text.strip()
            anon = tds[4].text.strip()
            google = tds[5].text.strip()
            Https = tds[6].text.strip()
            time_ago = tds[7].text.strip()
            host = f"{ip}|{port}|{kod}|{country}|{anon}|{google}|{Https}|{time_ago}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies
# подставляем занчения выбранного прокси
def install_proxy_to_empty(input_2_1,input_2_2,ip,port):
    input_2_1.delete(0, len(input_2_1.get()))
    input_2_2.delete(0, len(input_2_2.get()))
    input_2_1.insert(0,ip)
    input_2_2.insert(0,port)
# выбираем строку в таблице
def update_item(tv,input_2_1,input_2_2):
    selected = tv.focus()
    temp = tv.item(selected, 'values')
    install_proxy_to_empty(input_2_1,input_2_2,temp[0],temp[1])   
# показываем окно с таблицей бесплатных прокси
def create_window_proxy(input_2_1,input_2_2):
    
    window_proxy = customtkinter.CTk()
    window_proxy.title("Бесплатные прокси")
    w = 800
    h = 400
    ws = window_proxy.winfo_screenwidth()
    hs = window_proxy.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window_proxy.geometry('%dx%d+%d+%d' % (w, h, x, y)) 
    
    #-------------------Отрисовка окна-----------------------
    customtkinter.CTkLabel(window_proxy, text="Список бесплатных прокси", fg_color="transparent",anchor='center',font=('Arial',20,'bold')).pack(pady=10)
    frame_data = customtkinter.CTkScrollableFrame(window_proxy, corner_radius=10, fg_color="transparent", orientation='vertical', height=240, width=720)
    frame_data.pack(pady=10)
    tv = ttk.Treeview(frame_data, columns=(1,2,3,4,5,6), show='headings',height=14)
    tv.pack()
    tv.heading(1, text="IP адрес")
    tv.heading(2, text="Порт")
    tv.heading(3, text="Страна")
    tv.heading(4, text="Анонимность")
    tv.heading(5, text="Https")
    tv.heading(6, text="Время проверки")
    count=0
    for i in get_free_proxies():
        ip_one = i.split("|")
        tv.insert(parent='', index=count, iid=count, values=(ip_one[0],ip_one[1],ip_one[3],ip_one[4],ip_one[6],ip_one[7]))
        count=count+1
    customtkinter.CTkButton(window_proxy, text="Выбрать прокси",width=30, command = lambda:update_item(tv,input_2_1,input_2_2)).pack(pady=10)
    window_proxy.mainloop()
# Создаём сессию
def get_session(proxies):
    # создать HTTP‑сеанс
    session = requests.Session()
    session.proxies = {"http": proxies, "https": proxies}
    return session
#запускаем прокси
def start_proxy():
    
    s = get_session('91.243.61.168:14552')
    print("Страница запроса с IP:", s.get("https://icanhazip.com", timeout=1.5).text.strip())
    # try:
    #     if switch_TG_var2.get()=='1':
    #         ses = str(input_2_1.get())+':'+str(int(input_2_2.get()))
    #         print(ses)
    #         s = get_session('114.156.77.107:8080')
    #         print("Страница запроса с IP:", s.get("http://icanhazip.com", timeout=1.5).text.strip())
    #     else:
    #         print('Ошибка подкчлюения')
    #         switch_TG_var2.set('0')
    # except Exception as e: 
    #     # messagebox.showinfo('Внимание','Введите правильные значения в ip и порте прокси')
    #     print('ошибка')
    #     switch_TG_var2.set('0')
# рисуем страницу с настройками
def settings_prog():
    label_title1 = customtkinter.CTkLabel(frame_8, text="Настройки программы", fg_color="transparent",anchor='center',font=('Arial',20,'bold'))
    frame_2_set1 = customtkinter.CTkFrame(frame_8, corner_radius=10, fg_color="transparent")
    button1 = customtkinter.CTkButton(frame_2_set1, text="Информация")
    button2 = customtkinter.CTkButton(frame_2_set1, text="Инструкция")
    button3 = customtkinter.CTkButton(frame_2_set1, text="Стартовые настройки")
    frame_8_set = customtkinter.CTkFrame(frame_8, corner_radius=0, fg_color="transparent")
    label_title2 = customtkinter.CTkLabel(frame_8_set, text="Оформление программы", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    appearance_mode_menu = customtkinter.CTkOptionMenu(frame_8_set, values=["Dark", "Light", "System"],command=change_appearance_mode_event)
    frame_2_set2 = customtkinter.CTkFrame(frame_8, corner_radius=10, fg_color="#2B2B2B")
    label_title_8_1 = customtkinter.CTkLabel(frame_2_set2, text="Использовать прокси", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    label_title_8_2 = customtkinter.CTkLabel(frame_2_set2, text="", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    label_title_8_2.configure(text=f'Мой ip адрес - {get_my_ip()}')
    frame_2_set2_2 = customtkinter.CTkFrame(frame_2_set2, corner_radius=10, fg_color="#2B2B2B")
    frame_2_set2_2_1 = customtkinter.CTkFrame(frame_2_set2_2, corner_radius=10, fg_color="#2B2B2B")
    frame_2_set2_2_2 = customtkinter.CTkFrame(frame_2_set2_2, corner_radius=10, fg_color="#2B2B2B")
    label_title_8_3 = customtkinter.CTkLabel(frame_2_set2_2_1, text="Адрес", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label_title_8_4 = customtkinter.CTkLabel(frame_2_set2_2_2, text="Порт", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    input_2_1 = customtkinter.CTkEntry(frame_2_set2_2_1, placeholder_text="139.162.78.109",justify="center")
    input_2_2 = customtkinter.CTkEntry(frame_2_set2_2_2, placeholder_text="3128",justify="center")
    switch_TG_var2 = customtkinter.StringVar(value="0")
    switch_tg2 = customtkinter.CTkSwitch(frame_2_set2, text="Включить прокси",variable=switch_TG_var2, onvalue="1", offvalue="0",command=lambda:start_proxy())
    button_settings_prog_3_1 = customtkinter.CTkButton(frame_2_set2, text="Список бесплатных прокси", command=lambda:create_window_proxy(input_2_1,input_2_2))
    
    
    label_title1.pack(pady=20)
    frame_2_set1.pack(pady=[10,20],padx=20)
    button1.grid(row=0, column=0, sticky="ew",padx=10)
    button2.grid(row=0, column=1, sticky="ew",padx=10)
    button3.grid(row=0, column=2, sticky="ew",padx=10)
    frame_8_set.pack()
    label_title2.grid(row=0, column=0, sticky="ew",padx=20)
    appearance_mode_menu.grid(row=0, column=1, sticky="ew")
    frame_2_set2.pack(pady=20)
    label_title_8_2.grid(row=1, column=0, sticky="ew",padx=20)
    label_title_8_1.grid(row=0, column=0, sticky="ew",padx=20,pady=20)
    frame_2_set2_2.grid(row=2, column=0, sticky="ew",padx=20)
    frame_2_set2_2_1.grid(row=0, column=0, sticky="ew",padx=20)
    frame_2_set2_2_2.grid(row=0, column=1, sticky="ew",padx=20)
    label_title_8_3.pack(pady=10)
    label_title_8_4.pack(pady=10)
    input_2_1.pack(pady=0)
    input_2_2.pack(pady=0)
    switch_tg2.grid(row=3, column=0,padx=20,pady=20,columnspan=2)
    button_settings_prog_3_1.grid(row=4, column=0,padx=20,pady=[0,20],columnspan=2)
    
# --------------------------------- ПРОФИЛЬ ---------------------------------

def profile():
    label_title1 = customtkinter.CTkLabel(frame_7, text="Профиль", fg_color="transparent",anchor='center',font=('Arial',20,'bold'))
    frame_7_set1 = customtkinter.CTkFrame(frame_7, corner_radius=10, fg_color="#2B2B2B")
    label_title2 = customtkinter.CTkLabel(frame_7_set1, text="Логин", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    label_title3 = customtkinter.CTkLabel(frame_7_set1, text=NAME, fg_color="transparent", text_color='#1F6AA5',anchor='center',font=('Arial',14,'normal'))
    label_title4 = customtkinter.CTkLabel(frame_7_set1, text="Ключ шифрования", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    label_title5 = customtkinter.CTkLabel(frame_7_set1, text=API_KEY, fg_color="transparent", text_color='#1F6AA5',anchor='center',font=('Arial',14,'normal'))
    label_title6 = customtkinter.CTkLabel(frame_7_set1, text="Email", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    label_title7 = customtkinter.CTkLabel(frame_7_set1, text='MaksimIvankov26@yandex.ru', fg_color="transparent", text_color='#1F6AA5',anchor='center',font=('Arial',14,'normal'))
    frame_7_set2 = customtkinter.CTkScrollableFrame(frame_7, corner_radius=10, fg_color="#2B2B2B", orientation='horizontal', width=600, height=140)
    label_title8 = customtkinter.CTkLabel(frame_7_set2, text="API_KEY_BINANCE", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    label_title9 = customtkinter.CTkLabel(frame_7_set2, text=key, fg_color="transparent", text_color='#1F6AA5',anchor='center',font=('Arial',14,'normal'))
    label_title10 = customtkinter.CTkLabel(frame_7_set2, text="API_SECRET_KEY_BINANCE", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    label_title11 = customtkinter.CTkLabel(frame_7_set2, text=secret, fg_color="transparent", text_color='#1F6AA5',anchor='center',font=('Arial',14,'normal'))
    label_title12 = customtkinter.CTkLabel(frame_7_set2, text="API_KEY_TELEGRAM", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    label_title13 = customtkinter.CTkLabel(frame_7_set2, text=TG_API, fg_color="transparent", text_color='#1F6AA5',anchor='center',font=('Arial',14,'normal'))
    label_title14 = customtkinter.CTkLabel(frame_7_set2, text="ID_TELEGRAM", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    label_title15 = customtkinter.CTkLabel(frame_7_set2, text=TG_ID, fg_color="transparent", text_color='#1F6AA5',anchor='center',font=('Arial',14,'normal'))

    label_title1.pack(pady=20)
    frame_7_set1.pack(pady=10)
    label_title2.grid(row=0, column=0, sticky="w",padx=20)
    label_title3.grid(row=0, column=1, sticky="w",padx=20)
    label_title4.grid(row=1, column=0, sticky="w",padx=20)
    label_title5.grid(row=1, column=1, sticky="w",padx=20)
    label_title6.grid(row=2, column=0, sticky="w",padx=20)
    label_title7.grid(row=2, column=1, sticky="w",padx=20)
    frame_7_set2.pack(pady=10,padx=20)
    label_title8.grid(row=0, column=0, sticky="w",padx=20)
    label_title9.grid(row=0, column=1, sticky="w",padx=20)
    label_title10.grid(row=1, column=0, sticky="w",padx=20)
    label_title11.grid(row=1, column=1, sticky="w",padx=20)
    label_title12.grid(row=2, column=0, sticky="w",padx=20)
    label_title13.grid(row=2, column=1, sticky="w",padx=20)
    label_title14.grid(row=3, column=0, sticky="w",padx=20)
    label_title15.grid(row=3, column=1, sticky="w",padx=20)

# --------------------------------- ИСТОРИЧЕСКАЯ ТОРГОВЛЯ ---------------------------------

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
def start_historical_trade(frame_2_set2_graph,frame_3_set4_1_2,frame_3_set4_1_1_1,frame_2_set4_2_set_1,frame_2_set4_2_set_2,frame_2_set4_2_set_3,frame_2_set4_2_set_4,frame_2_set4_3_set_1,frame_2_set4_3_set_2,frame_2_set4_3_set_3,frame_2_set4_3_set_4,frame_2_set4_4_set_1,frame_2_set4_4_set_2,frame_2_set4_4_set_3,frame_2_set4_4_set_4):
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
        thread = threading.Thread(target=lambda:bin.start_trade_hist_model(frame_2_set2_graph,frame_3_set4_1_1_1,frame_3_set4_1_2))
        thread.start()
    except ValueError: 
        messagebox.showinfo('Внимание','Введите правильные значения в настройках торговли')
# открываем логи торгов в блокноте
def open_history_trade_log():
    print('Открыли логи истор торгов')
    os.system("notepad H_log.txt")
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
    # --------------------------------------
    frame_2_set4 = customtkinter.CTkFrame(second_frame, corner_radius=10, fg_color="#2B2B2B")
    label__2_set4 = customtkinter.CTkLabel(frame_2_set4, text="Настройка торговли", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    frame_2_set4_0 = customtkinter.CTkFrame(frame_2_set4, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_1 = customtkinter.CTkFrame(frame_2_set4_0, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_2 = customtkinter.CTkFrame(frame_2_set4_0, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_3 = customtkinter.CTkFrame(frame_2_set4_0, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_4 = customtkinter.CTkFrame(frame_2_set4_0, corner_radius=0, fg_color="#2B2B2B")
    label__2_set4_1_1 = customtkinter.CTkLabel(frame_2_set4_1, text="Выбор стратегии", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    frame_2_set4_1_1 = customtkinter.CTkScrollableFrame(frame_2_set4_1, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=200, height=50)
    radio_var = tkinter.IntVar(value=1)
    radiobutton_1 = customtkinter.CTkRadioButton(frame_2_set4_1_1, text="Канал, тренд, локаль, \nобъём", variable= radio_var, value=1,text_color='#242424',state="disabled")
    radiobutton_2 = customtkinter.CTkRadioButton(frame_2_set4_1_1, text="Скользящие средние", variable= radio_var, value=2,text_color='#242424',state="disabled")
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
    # --------------------------------
    button6 = customtkinter.CTkButton(second_frame, text="Запустить торговлю",command=lambda:start_historical_trade(frame_2_set2_graph,frame_3_set4_1_2,frame_3_set4_1_1_1,frame_2_set4_2_set_1,frame_2_set4_2_set_2,frame_2_set4_2_set_3,frame_2_set4_2_set_4,frame_2_set4_3_set_1,frame_2_set4_3_set_2,frame_2_set4_3_set_3,frame_2_set4_3_set_4,frame_2_set4_4_set_1,frame_2_set4_4_set_2,frame_2_set4_4_set_3,frame_2_set4_4_set_4))
    # --------------------------------
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
    # -----------------------------------
    frame_2_set2_graph = customtkinter.CTkFrame(second_frame, corner_radius=10, fg_color="transparent")  
    
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
    frame_2_set4_2.grid(row=0, column=2, sticky="ew",padx=10)
    frame_2_set4_3.grid(row=0, column=3, sticky="ew",padx=10)
    frame_2_set4_4.grid(row=0, column=4, sticky="ew",padx=10)
    label__2_set4_1_1.pack(pady=4)
    frame_2_set4_1_1.pack(pady=4)
    radiobutton_1.pack(pady=4, anchor='w')
    radiobutton_2.pack(pady=4, anchor='w')
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
    button6.pack(pady=[10,10])
    frame_3_set4_1.pack(pady=[10,10],padx=20)
    frame_3_set4_1_1.grid(row=0, column=1, sticky="ew",padx=10)
    frame_3_set4_1_2.grid(row=0, column=2, sticky="ew",padx=10)
    label__3_set4_1_1_set_1.pack(pady=5)
    frame_3_set4_1_1_1.pack(pady=[5,20])
    frame_2_set2_graph.pack(pady=[0,20],padx=20)

# --------------------------------- Реальная тестовая торговля ---------------------------------    
real.wait_time = int(set1_timveframe.get(bin.TF))
# получаем таймфрейм
def get_setting_timeframe_real_test_trad(data):
    timeframe = set1_timveframe.get(data)
    real.TF = data
    real.wait_time = timeframe
# запускаем реальную тестовую торговлю            
def start_real_test_trade_btn(input_2_1,switch_TG_var,real_test_frame_3_1_1,real_test_frame_3_2_1,real_test_trade_frame_2_set4_2_set_1,real_test_trade_frame_2_set4_2_set_2,real_test_trade_frame_2_set4_2_set_3,real_test_trade_frame_2_set4_2_set_4,real_test_trade_frame_2_set4_3_set_1,real_test_trade_frame_2_set4_3_set_2,real_test_trade_frame_2_set4_3_set_3,real_test_trade_frame_2_set4_3_set_4,real_test_trade_frame_2_set4_4_set_1,real_test_trade_frame_2_set4_4_set_2,real_test_trade_frame_2_set4_4_set_3,real_test_trade_frame_2_set4_4_set_4):
    try:
        global name_bot_real_test
        real.COMMISSION_MAKER = float(float(real_test_trade_frame_2_set4_2_set_1.get())/100)
        real.COMMISSION_TAKER = float(float(real_test_trade_frame_2_set4_2_set_2.get())/100)
        real.TP = float(float(real_test_trade_frame_2_set4_2_set_3.get())/100)
        real.SL = float(float(real_test_trade_frame_2_set4_2_set_4.get())/100)
        real.DEPOSIT = int(real_test_trade_frame_2_set4_3_set_1.get())
        real.LEVERAGE = int(real_test_trade_frame_2_set4_3_set_2.get())
        real.CANAL_MAX = float(float(real_test_trade_frame_2_set4_3_set_3.get())/100)
        real.CANAL_MIN = float(float(real_test_trade_frame_2_set4_3_set_4.get())/100)
        real.CORNER_LONG = int(real_test_trade_frame_2_set4_4_set_1.get())
        real.CORNER_SHORT = int(real_test_trade_frame_2_set4_4_set_2.get())
        real.CANDLE_COIN_MIN = int(real_test_trade_frame_2_set4_4_set_3.get())
        real.CANDLE_COIN_MAX = int(real_test_trade_frame_2_set4_4_set_4.get())
        sost_tg_message = switch_TG_var.get()
        name_bot_real_test = input_2_1.get()
        print(f'main галка тг- {sost_tg_message}')
        print(f'main имя бота- {name_bot_real_test}')
        for widget in real_test_frame_3_1_1.winfo_children():
            widget.forget()
        for widget in real_test_frame_3_2_1.winfo_children():
            widget.forget()
        thread2 = threading.Thread(target=lambda:real.start_real_test_trade_model_thread_1(card_trade_menu,name_bot_real_test,sost_tg_message,real_test_frame_3_1_1,real_test_frame_3_2_1))
        thread2.start()
    except ValueError: 
        messagebox.showinfo('Внимание','Введите правильные значения в настройках торговли')
# рсиуем окно реальной тестовой торговли
def real_test_trade():
    label_title1 = customtkinter.CTkLabel(third_frame, text="Реальная тестовая торговля", fg_color="transparent",anchor='center',font=('Arial',20,'bold'))
    frame_2_set1 = customtkinter.CTkFrame(third_frame, corner_radius=10, fg_color="transparent")
    button1 = customtkinter.CTkButton(frame_2_set1, text="Информация")
    button2 = customtkinter.CTkButton(frame_2_set1, text="Инструкция")
    button3 = customtkinter.CTkButton(frame_2_set1, text="История торгов")
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
    start_trade_real_test = customtkinter.CTkButton(real_test_frame_2_buttons, text="Запустить торговлю",command=lambda:start_real_test_trade_btn(input_2_1,switch_TG_var,real_test_frame_3_1_1,real_test_frame_3_2_1,real_test_trade_frame_2_set4_2_set_1,real_test_trade_frame_2_set4_2_set_2,real_test_trade_frame_2_set4_2_set_3,real_test_trade_frame_2_set4_2_set_4,real_test_trade_frame_2_set4_3_set_1,real_test_trade_frame_2_set4_3_set_2,real_test_trade_frame_2_set4_3_set_3,real_test_trade_frame_2_set4_3_set_4,real_test_trade_frame_2_set4_4_set_1,real_test_trade_frame_2_set4_4_set_2,real_test_trade_frame_2_set4_4_set_3,real_test_trade_frame_2_set4_4_set_4))
    stop_trade_real_test = customtkinter.CTkButton(real_test_frame_2_buttons, text="Остановить торговлю")
    # --------------------------------
    real_test_frame_3 = customtkinter.CTkFrame(master=third_frame, corner_radius=10, fg_color="#2B2B2B")
    real_test_frame_3_1 = customtkinter.CTkFrame(real_test_frame_3, corner_radius=0, fg_color="#2B2B2B")
    real_test_frame_3_2 = customtkinter.CTkFrame(real_test_frame_3, corner_radius=0, fg_color="#2B2B2B")
    real_test_label_3_1 = customtkinter.CTkLabel(real_test_frame_3_1, text="Данные по монете в сделке", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_frame_3_1_1 = customtkinter.CTkScrollableFrame(real_test_frame_3_1, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=160, height=260)
    real_test_label_3_2 = customtkinter.CTkLabel(real_test_frame_3_2, text="Логи торговли", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_frame_3_2_1 = customtkinter.CTkScrollableFrame(real_test_frame_3_2, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=460, height=260)
    
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




update_time()
real_test_trade()
historical_trade()
settings_prog()
profile()

win.mainloop()