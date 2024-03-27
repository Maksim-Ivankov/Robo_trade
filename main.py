from imports import *
import models.treayd_historical as bin
import models.main_TV as TV
import strategy.print_settings.strat1 as strat
import strategy.print_settings.strat_real_test as strat_real_test
import strategy.print_settings.strat_historical as strat_historical
import models.real_test_trade as real
import models.treayd_historical_2_bollindger as bin_2
import strategy.strategys.strat_1 as str_1




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
name_bot_real_test = "Версия 1_1"
name_bot_historical = "Версия 1_1"
strat_mas_real_test = ['strat1'] # выбор по умолчанию - 1 вариант
strat_mas_historical = ['strat1'] # выбор по умолчанию - 1 вариант
check_var_real_test = customtkinter.StringVar(value=strat_mas_real_test[0]) # первичный выбор настройки ртт шаг 2
check_var_historical = customtkinter.StringVar(value=strat_mas_historical[0]) # первичный выбор настройки ртт шаг 2
sost_tg_message_real_test = 'off' # первичное состояние кнопки ТГ в РТТ

coin_mas_10 = []
        
#Логер в файлы
def logger(name_log,msg):
    path = name_log+'_log.txt'
    f = open(path,'a',encoding='utf-8')
    f.write('\n'+time.strftime("%d.%m.%Y | %H:%M:%S | ", time.localtime())+msg)
    f.close()
logger('H','------------------------------------------------------------')
logger('H','Открыли Robo_Trade')
#меряем пинг каждую минуту и рисуем круг нужного цвета
def speed_test():
    win.after(60000, speed_test)
    response_list = ping('52.84.150.36', size=40, count=10).rtt_avg_ms
    if response_list>300 and response_list<900:
        indikator_ping.itemconfig(indicator_cicle,fill="#ff921c")
    if response_list>900:
        indikator_ping.itemconfig(indicator_cicle,fill="red")
    if response_list<300:
        indikator_ping.itemconfig(indicator_cicle,fill="green")

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
navigation_frame_time_speed = customtkinter.CTkFrame(navigation_frame, corner_radius=0, fg_color="transparent")
time_now = customtkinter.CTkLabel(navigation_frame_time_speed, text=time.strftime("%d.%m.%Y г. %H:%M:%S", time.localtime()),compound="left", font=customtkinter.CTkFont(size=12, weight="normal"))
indikator_ping = tkinter.Canvas(navigation_frame_time_speed, width=15, height=15, bg="#2B2B2B",border=0,bd=0,highlightthickness=0)
indicator_cicle = indikator_ping.create_oval(4, 4, 15, 15, fill="green")
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
navigation_frame_time_speed.grid(row=10, column=0, sticky="s",pady=20)
time_now.grid(row=0, column=1, sticky="s",pady=10)
indikator_ping.grid(row=0, column=0, sticky="s",pady=20,padx=5)

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
        historical_trade()
    else:
        second_frame.grid_forget()
    if name == "frame_3":
        third_frame.grid(row=0, column=1, sticky="nsew")
        real_test_trade()
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
    try:
        return requests.get('https://api.ipify.org').content.decode('utf8')
    except Exception as e:
        messagebox.showinfo('Внимание','Ошибка работы, нет сети. Подключитесь к интернету.')
    # return requests.get('https://api.ipify.org').content.decode('utf8')
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
    
# --------------------------------- ГЛАВНАЯ ---------------------------------
# рсиуем окно 
def main_page():
    data = TV.get_top_coin() # получили активные монеты слварем
    range_i = math.ceil(len(data)/5) # посчитали, сколько в столбце должно быть штук
    label_title1 = customtkinter.CTkLabel(home_frame, text="", fg_color="transparent",anchor='center',font=('Arial',20,'bold')) # рисуем общую стату
   
    frame_2_set1 = customtkinter.CTkScrollableFrame(home_frame, corner_radius=0,width=700,height=600, fg_color="transparent") # фрейм, где все кнопки лежат с прокруткой
    i = 0
    j = 0
    procent = 0
    for item in data.items(): # рисуем кнопки - монета и процент движения
        procent = float(procent) + float(item[1])
        if i==range_i: 
            j = j+1
            i=0
        element = customtkinter.CTkButton(frame_2_set1, text=f'{item[0]} {item[1]}', fg_color="green", text_color='black',anchor='center',font=('Arial',11,'normal'),corner_radius=0)
        if item[1]>0:
            element.configure(fg_color='green')
        else:
            element.configure(fg_color='red')
        element.grid(row=i, column=j, sticky="ew",padx=1,pady=1)
        i = i+1
    if procent/len(data)>0:
        label_title1.configure( fg_color="green")
        price = f'+ {round(procent/len(data), 2)}'
    else:
        label_title1.configure( fg_color="red")
        price = f'{round(procent/len(data), 2)}'
    label_title1.configure(text=f'Движение рынка сегодня {price} %')
    

    label_title1.pack(anchor='n',pady=[20,0],fill='x')
    frame_2_set1.pack(anchor='n',pady=20)

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
# обработка выбора таймфрейма слежения за ценой в блоке создания датафреймов | слежка, сколько времени работаем, по какому основному таймфрейму
def get_setting_timeframe_slega(data):
    global work_timeframe_HM
    global work_timeframe_str_HM
    work_timeframe_str_HM = data
    work_timeframe_HM = set1_timveframe.get(data) # число 1 или 5
    print(f'work_timeframe_HM - {work_timeframe_HM}')
# обработка выбора времени работы в блоке создания датафреймов
def get_setting_time(data):
    global time_HM
    time_HM = set1_time.get(data) # сколько минут отрабатываем
# кнопка - получить данные, формируем файлы датафреймов
def get_dataframe_with_binance(frame_2_set2_2_1,frame_2_set2_3,input_2_167):
    global work_timeframe_HM
    global timeframe_HM
    global time_HM
    global work_timeframe_str_HM
    bin.VOLUME = int(time_HM/timeframe_HM)
    bin.VOLUME_5MIN = int(time_HM/work_timeframe_HM)
    bin.how_mach_coin = input_2_167.get()
    bin.STEP_5_min_VALUE = bin.VOLUME_5MIN/bin.VOLUME
    
    logger('H','Историческая торговля, формируем датафреймы')
    logger('H',f'Историческая торговля, настройки: рабочий таймфрейм {bin.TF} мин')
    logger('H',f'Историческая торговля, настройки: таймфрейм отслеживания цены {bin.VOLUME_5MIN} мин')
    logger('H',f'Историческая торговля, настройки: Время работы {str(time_HM/60)} часов')
    for widget in frame_2_set2_2_1.winfo_children():
            widget.destroy()
    for widget in frame_2_set2_3.winfo_children():
            widget.destroy()
    bin.number_print_df = 0
    bin.data_print_ad_df[:] = []
    thread7654 = threading.Thread(target=lambda:bin.generate_dataframe(bin.TF,bin.VOLUME,bin.VOLUME_5MIN,frame_2_set2_3,work_timeframe_str_HM,frame_2_set2_2_1))
    thread7654.start()
    time.sleep(1)
        
    
# отрисовка монет из файла, если он не пустой
def get_coin_proc_start(frame_2_set2_2_1):
    global input_2_167
    file = open('../ROBO_TRADE/DF/coin_procent.txt', mode="r")
    bin.coin_mas_10 = file.read().split('|')
    bin.how_mach_coin = len(bin.coin_mas_10)
    # input_2_167.insert(0, bin.how_mach_coin)
    if bin.coin_mas_10:
        i=-1
        for coin in bin.coin_mas_10:
            i=i+1
            customtkinter.CTkButton(frame_2_set2_2_1, text=coin).grid(row=i, column=0, sticky="ew",pady=5)
# отрисовка датафреймов из файла           
def get_dataset_file_start(frame_2_set2_3_1):
    global appearance_mode_menu0_his,appearance_mode_menu1_his,work_timeframe_str_HM,time_HM,appearance_mode_menu2_his
    mypath = '../ROBO_TRADE/DF/5min/'
    filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file
    if len(filenames)!= 0:
        symbol = filenames[0]
        df = pd.read_csv(f'{bin.MYDIR_WORKER}{symbol}')
        time_F = int(df.iloc[1]['open_time'] - df.iloc[0]['open_time'])/60000
        df2 = pd.read_csv(f'{bin.MYDIR_5MIN}{symbol}')
        time_F2 = int(df2.iloc[1]['open_time'] - df2.iloc[0]['open_time'])/60000

        with open(f'{bin.MYDIR_WORKER}{symbol}') as f:
            time_Work_F = sum(1 for line in f)-1
        bin.VOLUME = int(time_Work_F)
        bin.VOLUME_5MIN = int(time_Work_F*time_F)/int(time_F2)
        bin.STEP_5_min_VALUE = (int(time_Work_F*time_F)/int(time_F2))/int(time_Work_F)
        print(bin.VOLUME)
        appearance_mode_menu0_his.set(f'{int(time_F2)}m')
        if int(time_F)==60: 
            appearance_mode_menu1_his.set(f'1h')
            bin.TF = '1h'
        else: 
            appearance_mode_menu1_his.set(f'{int(time_F)}m')
            bin.TF = f'{int(time_F)}m'
        work_timeframe_str_HM = f'{int(time_F2)}m'
        if int(time_Work_F*time_F) == 720: appearance_mode_menu2_his.set('12 часов')
        elif int(time_Work_F*time_F) == 1440: appearance_mode_menu2_his.set('24 часа')
        elif int(time_Work_F*time_F) == 2880: appearance_mode_menu2_his.set('2 дня')
        elif int(time_Work_F*time_F) == 4320: appearance_mode_menu2_his.set('3 дня')
        bin.wait_time = int(time_F)
        
        time_HM = int(time_Work_F*time_F)
        customtkinter.CTkLabel(frame_2_set2_3_1,text=f'Рабочий ТF - {int(time_F)} мин' , fg_color="#DAE2EC",text_color='#242424',anchor='w',font=('Arial',12,'normal')).pack(anchor="w")
        customtkinter.CTkLabel(frame_2_set2_3_1,text=f'Длительность - {int(time_Work_F*time_F/60)} часов' , fg_color="#DAE2EC",text_color='#242424',anchor='w',font=('Arial',12,'normal')).pack(anchor="w")
        customtkinter.CTkLabel(frame_2_set2_3_1,text=f'Следим за ценой - {int(time_F2)} мин' , fg_color="#DAE2EC",text_color='#242424',anchor='w',font=('Arial',12,'normal')).pack(anchor="w")
        for name in filenames:
            customtkinter.CTkLabel(frame_2_set2_3_1,text='Найден датасет '+ name , fg_color="#DAE2EC",text_color='#242424',anchor='w',font=('Arial',12,'normal')).pack(anchor="w")
            symbol=name  
# стартуем историческую торговлю
def start_historical_trade_strat_1():
    # global frame_3_set4_1_1_1_historical,frame_3_set4_1_2_historical,strat_mas_historical,real_test_frame_3_2_1_historical
    print('Начали историческую торговлю по 1 настройке')
    try:
        global thread2922
        logger('RT',f'------------------------------------------------------------------------')
        logger('RT',f'Реальная тестовая торговля | Начали торговлю')
        logger('RT',f'Реальная тестовая торговля | Настройки:')
        logger('RT',f'Реальная тестовая торговля | Комисия мейкер - {bin.COMMISSION_MAKER}, тейкер - {bin.COMMISSION_TAKER}')
        logger('RT',f'Реальная тестовая торговля | Тейк - {bin.TP}, стоп - {bin.SL}')
        logger('RT',f'Реальная тестовая торговля | Депозит - {bin.DEPOSIT}, плечо - {bin.LEVERAGE}')
        logger('RT',f'Реальная тестовая торговля | Канал макс - {str_1.CANAL_MAX}, канал мин - {str_1.CANAL_MIN}')
        logger('RT',f'Реальная тестовая торговля | Угол лонг - {str_1.CORNER_LONG}, угол шорт - {str_1.CORNER_SHORT}')
        logger('RT',f'Реальная тестовая торговля | Объём мин - {bin.CANDLE_COIN_MIN}, макс - {bin.CANDLE_COIN_MAX}')
        logger('RT',f'Реальная тестовая торговля | Название бота - {name_bot_historical}')
        # for widget in real_test_frame_3_1_1.winfo_children():
        #     widget.forget()
        # for widget in real_test_frame_3_2_1.winfo_children():
        #     widget.forget()
        thread2922 = threading.Thread(target=lambda:bin.start_trade_hist_model(strat_mas_historical,bin.COMMISSION_MAKER,bin.COMMISSION_TAKER,bin.TP,bin.SL,bin.DEPOSIT,bin.LEVERAGE,bin.CANDLE_COIN_MIN,bin.CANDLE_COIN_MAX))
        thread2922.start()
    except ValueError: 
        messagebox.showinfo('Внимание','Ошибка запуска торговли')
    
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


strat_mas = ['strat1'] # выбор по умолчанию - 1 вариант
# сохраняет в массив выше выбранные стратегии и удаляет невыбранные
check_var = customtkinter.StringVar(value=strat_mas[0])
def checkbox_event_strat(): 
    global strat_mas
    match check_var.get():
        case '0' : strat_mas.remove('strat1')
        case '1' : strat_mas.remove('strat2')
        case '2' : strat_mas.remove('strat3')
        case '3' : strat_mas.remove('strat4')
        case '4' : strat_mas.remove('strat5')
        case '5' : strat_mas.remove('strat6')
        case '6' : strat_mas.remove('strat7')
        case '7' : strat_mas.remove('strat8')
        case '8' : strat_mas.remove('strat9')
        case '9' : strat_mas.remove('strat10')
        case '10': strat_mas.remove('strat11')
        case '11': strat_mas.remove('strat12')
        case '12': strat_mas.remove('strat13')
        case '13': strat_mas.remove('strat14')
        case '14': strat_mas.remove('strat15')
        case '15': strat_mas.remove('strat16')
        case '16': strat_mas.remove('strat17')
        case '17': strat_mas.remove('strat18')
        case '18': strat_mas.remove('strat19')
        case '19': strat_mas.remove('strat20')
        case '20': strat_mas.remove('strat21')
        case '21': strat_mas.remove('strat22')
        case '22': strat_mas.remove('strat23')
        case '23': strat_mas.remove('strat24')
        case 'strat1' : strat_mas.append('strat1')
        case 'strat2' : strat_mas.append('strat2')
        case 'strat3' : strat_mas.append('strat3')
        case 'strat4' : strat_mas.append('strat4')
        case 'strat5' : strat_mas.append('strat5')
        case 'strat6' : strat_mas.append('strat6')
        case 'strat7' : strat_mas.append('strat7')
        case 'strat8' : strat_mas.append('strat8')
        case 'strat9' : strat_mas.append('strat9')
        case 'strat10': strat_mas.append('strat10')
        case 'strat11': strat_mas.append('strat11')
        case 'strat12': strat_mas.append('strat12')
        case 'strat13': strat_mas.append('strat13')
        case 'strat14': strat_mas.append('strat14')
        case 'strat15': strat_mas.append('strat15')
        case 'strat16': strat_mas.append('strat16')
        case 'strat17': strat_mas.append('strat17')
        case 'strat18': strat_mas.append('strat18')
        case 'strat19': strat_mas.append('strat19')
        case 'strat20': strat_mas.append('strat20')
        case 'strat21': strat_mas.append('strat21')
        case 'strat22': strat_mas.append('strat22')
        case 'strat23': strat_mas.append('strat23')
        case 'strat24': strat_mas.append('strat24')

def start_historical_trade_strat_2_bollindger(frame_2_set2_graph_2):
    try:
        thread25 = threading.Thread(target=lambda:bin_2.main(frame_2_set2_graph_2))
        thread25.start()
    except Exception as e:
        messagebox.showinfo('Внимание','Ошибка начала торговли по стратегии Боллинджера')


# валидация на данные с шага 1
def step_2_historical_trade_prom(frame,frame_2_set4_2_set_1,frame_2_set4_2_set_2,frame_2_set4_2_set_3,frame_2_set4_2_set_4,frame_2_set4_3_set_1,frame_2_set4_3_set_2,frame_2_set4_4_set_3,frame_2_set4_4_set_4,input_2_1,input_2_167):
    global name_bot_historical
    global sost_tg_message_real_test
    if name_bot_historical=='': 
        messagebox.showinfo('Внимание','Введите имя бота')
    elif bin.how_mach_coin=='': 
        messagebox.showinfo('Внимание','Введите количество монет для торговли')
    elif frame_2_set4_2_set_1.get()=='': 
        messagebox.showinfo('Внимание','Введите комиссию мейкер')
    elif frame_2_set4_2_set_2.get()=='': 
        messagebox.showinfo('Внимание','Введите комиссию тейкер')
    elif frame_2_set4_2_set_3.get()=='': 
        messagebox.showinfo('Внимание','Введите тейк профит')
    elif frame_2_set4_2_set_4.get()=='': 
        messagebox.showinfo('Внимание','Введите cтоп лосс')
    elif frame_2_set4_3_set_1.get()=='': 
        messagebox.showinfo('Внимание','Введите депозит')
    elif frame_2_set4_3_set_2.get()=='': 
        messagebox.showinfo('Внимание','Введите плечо')
    elif frame_2_set4_4_set_3.get()=='': 
        messagebox.showinfo('Внимание','Введите объём торгов мин')
    elif frame_2_set4_4_set_4.get()=='': 
        messagebox.showinfo('Внимание','Введите объём торгов макс')
    else:
        bin.COMMISSION_MAKER = float(float(frame_2_set4_2_set_1.get())/100)
        bin.COMMISSION_TAKER = float(float(frame_2_set4_2_set_2.get())/100)
        bin.TP = float(float(frame_2_set4_2_set_3.get())/100)
        bin.SL = float(float(frame_2_set4_2_set_4.get())/100)
        bin.DEPOSIT = float(frame_2_set4_3_set_1.get())
        bin.LEVERAGE = int(frame_2_set4_3_set_2.get())
        bin.CANDLE_COIN_MIN = int(frame_2_set4_4_set_3.get())
        bin.CANDLE_COIN_MAX = int(frame_2_set4_4_set_4.get())
        name_bot_historical = input_2_1.get()
        bin.name_bot_historical = input_2_1.get()
        bin.how_mach_coin = input_2_167.get()
        open_step_2_historical(frame)

# валдиция на данные с шага 2
def step_3_historical_trade_prom(frame):
    global strat_mas_historical
    if len(strat_mas_historical)==0: 
        messagebox.showinfo('Внимание','Выберете хотя бы одну стратегию')
    else:
        open_step_3_historical(frame)

# валидация на данные с шага 3
def step_4_historical_trade_prom(frame):
    global strat_mas_historical
    for i in strat_mas_historical:
        match i:
            case 'strat1' : data_settings_1 = strat_historical.strat1_param()
            case 'strat2' : strat_historical.strat2_param()
            case 'strat3' : strat_historical.strat3()
            case 'strat4' : strat_historical.strat4()
            case 'strat5' : strat_historical.strat5()
            case 'strat6' : strat_historical.strat6()
            case 'strat7' : strat_historical.strat7()
            case 'strat8' : strat_historical.strat8()
            case 'strat9' : strat_historical.strat9()
            case 'strat10': strat_historical.strat10()
            case 'strat11': strat_historical.strat11()
            case 'strat12': strat_historical.strat12()
            case 'strat13': strat_historical.strat13()
            case 'strat14': strat_historical.strat14()
            case 'strat15': strat_historical.strat15()
            case 'strat16': strat_historical.strat16()
            case 'strat17': strat_historical.strat17()
            case 'strat18': strat_historical.strat18()
            case 'strat19': strat_historical.strat19()
            case 'strat20': strat_historical.strat20()
            case 'strat21': strat_historical.strat21()
            case 'strat22': strat_historical.strat22()
            case 'strat23': strat_historical.strat23()
            case 'strat24': strat_historical.strat24()
    if data_settings_1 != None:
        open_step_4_historical(frame,data_settings_1)

def open_step_1_historical(frame):
    global appearance_mode_menu0_his,appearance_mode_menu1_his,appearance_mode_menu2,appearance_mode_menu2_his,input_2_167
    for widget in frame.winfo_children(): # чистим табличку
        widget.destroy()
    label_title112 = customtkinter.CTkLabel(frame, text="Получите данные по монетам для исторической торговли\n с биржи, либо используйте загруженные ранее данные", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    frame_2_set2 = customtkinter.CTkFrame(frame, corner_radius=10, fg_color="#2B2B2B")
    frame_2_set2_1 = customtkinter.CTkFrame(frame_2_set2, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set2_2 = customtkinter.CTkFrame(frame_2_set2, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set2_3 = customtkinter.CTkFrame(frame_2_set2, corner_radius=0, fg_color="#2B2B2B")
    label_title1_1 = customtkinter.CTkLabel(frame_2_set2_1, text="Сбор данных", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    label_title1_1_0 = customtkinter.CTkLabel(frame_2_set2_1, text="Следим за ценой", fg_color="transparent",anchor='center',font=('Arial',12,'normal'))
    appearance_mode_menu0_his = customtkinter.CTkOptionMenu(frame_2_set2_1, values=["1m", "5m"],command=get_setting_timeframe_slega)
    label_title1_1_1 = customtkinter.CTkLabel(frame_2_set2_1, text="Рабочий таймфрейм", fg_color="transparent",anchor='center',font=('Arial',12,'normal'))
    appearance_mode_menu1_his = customtkinter.CTkOptionMenu(frame_2_set2_1, values=["5m", "15m", "30m", "1h"],command=get_setting_timeframe)
    label_title1_1_2 = customtkinter.CTkLabel(frame_2_set2_1, text="Длительность", fg_color="transparent",anchor='center',font=('Arial',12,'normal'))
    appearance_mode_menu2_his = customtkinter.CTkOptionMenu(frame_2_set2_1, values=["12 часов", "24 часа", "2 дня", "3 дня"],command=get_setting_time)
    
    label_title2_167 = customtkinter.CTkLabel(frame_2_set2_1, text="Сколько монет торговать", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    input_2_167 = customtkinter.CTkEntry(frame_2_set2_1, placeholder_text="10",justify="center")
    
    button4 = customtkinter.CTkButton(frame_2_set2_1, text="Получить данные", command=lambda:get_dataframe_with_binance(frame_2_set2_2_1,frame_2_set2_3_1,input_2_167))
    label_title1_2 = customtkinter.CTkLabel(frame_2_set2_2, text="Монеты роста/падения", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    frame_2_set2_2_1 = customtkinter.CTkScrollableFrame(frame_2_set2_2, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=150, height=300)
    label_title1_3_1 = customtkinter.CTkLabel(frame_2_set2_3, text="Датасет с биржи Binance", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    label_title1_3_2 = customtkinter.CTkLabel(frame_2_set2_3, text="                                     ", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    frame_2_set2_3_1 = customtkinter.CTkScrollableFrame(frame_2_set2_3, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=200, height=300)
    
    get_coin_proc_start(frame_2_set2_2_1)
    get_dataset_file_start(frame_2_set2_3_1)
    
    label_title112.pack(pady=20)
    frame_2_set2.pack(pady=10)
    frame_2_set2_1.grid(row=0, column=1, sticky="ew",padx=10)
    frame_2_set2_2.grid(row=0, column=2, sticky="ew",padx=10)
    frame_2_set2_3.grid(row=0, column=3, sticky="ew",padx=10,columnspan = 2)
    label_title1_1.grid(row=0, column=0, sticky="ew")
    label_title1_1_0.grid(row=1, column=0, sticky="ew")
    appearance_mode_menu0_his.grid(row=2, column=0, sticky="ew",pady=[0,5])
    label_title1_1_1.grid(row=3, column=0, sticky="ew")
    appearance_mode_menu1_his.grid(row=4, column=0, sticky="ew",pady=[0,5])
    label_title1_1_2.grid(row=5, column=0, sticky="ew")
    appearance_mode_menu2_his.grid(row=6, column=0, sticky="ew",pady=[0,5])
    label_title2_167.grid(row=7, column=0, sticky="ew")
    input_2_167.grid(row=8, column=0, sticky="ew",pady=[0,5])
    button4.grid(row=9, column=0, sticky="ew",pady=15,padx=20)
    label_title1_2.grid(row=0, column=0, sticky="ew",pady=10)
    frame_2_set2_2_1.grid(row=1, column=0, sticky="ew",pady=[0,20])
    label_title1_3_1.grid(row=0, column=0, sticky="ew",pady=10)
    label_title1_3_2.grid(row=0, column=1, sticky="ew",pady=10)
    frame_2_set2_3_1.grid(row=1, column=0, columnspan=2, sticky="ew",pady=[0,20])
    
    
    label_title112 = customtkinter.CTkLabel(frame, text="Настройте робота для исторической торговли", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    frame_2_set4_0 = customtkinter.CTkFrame(master=frame,width=1100,height=800, corner_radius=10, fg_color="#2B2B2B")
    frame_2_set4_1 = customtkinter.CTkFrame(frame_2_set4_0, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_2 = customtkinter.CTkFrame(frame_2_set4_0, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_25 = customtkinter.CTkFrame(frame_2_set4_0, corner_radius=0, fg_color="#2B2B2B")
    label_title2_1 = customtkinter.CTkLabel(frame_2_set4_1, text="Имя робота для логов", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    input_2_1 = customtkinter.CTkEntry(frame_2_set4_1, placeholder_text="Версия 1_1",justify="center")
    frame_2_set4_2_set_1 = customtkinter.CTkEntry(frame_2_set4_1, placeholder_text="0.2",justify="center")
    frame_2_set4_2_set_2 = customtkinter.CTkEntry(frame_2_set4_1, placeholder_text="0.1",justify="center")
    frame_2_set4_2_set_3 = customtkinter.CTkEntry(frame_2_set4_2, placeholder_text="1.2",justify="center")
    frame_2_set4_2_set_4 = customtkinter.CTkEntry(frame_2_set4_2, placeholder_text="0.4",justify="center")
    label__2_set4_2_set_1 = customtkinter.CTkLabel(frame_2_set4_1, text="Комиссия мейкер, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_2_set_2 = customtkinter.CTkLabel(frame_2_set4_1, text="Комиссия тейкер, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_2_set_3 = customtkinter.CTkLabel(frame_2_set4_2, text="Тейк профит, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_2_set_4 = customtkinter.CTkLabel(frame_2_set4_2, text="Стоп лосс, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    frame_2_set4_3_set_1 = customtkinter.CTkEntry(frame_2_set4_2, placeholder_text="100",justify="center")
    frame_2_set4_3_set_2 = customtkinter.CTkEntry(frame_2_set4_25, placeholder_text="20",justify="center")
    label__2_set4_3_set_1 = customtkinter.CTkLabel(frame_2_set4_2, text="Деозит, $", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_3_set_2 = customtkinter.CTkLabel(frame_2_set4_25, text="Плечо", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    frame_2_set4_4_set_3 = customtkinter.CTkEntry(frame_2_set4_25, placeholder_text="200000",justify="center")
    frame_2_set4_4_set_4 = customtkinter.CTkEntry(frame_2_set4_25, placeholder_text="500000",justify="center")
    label__2_set4_4_set_3 = customtkinter.CTkLabel(frame_2_set4_25, text="Объём торгов мин", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_4_set_4 = customtkinter.CTkLabel(frame_2_set4_25, text="Объм торгов макс", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    button32 = customtkinter.CTkButton(frame, text="Выбрать стратегию торговли",command=lambda:step_2_historical_trade_prom(frame,frame_2_set4_2_set_1,frame_2_set4_2_set_2,frame_2_set4_2_set_3,frame_2_set4_2_set_4,frame_2_set4_3_set_1,frame_2_set4_3_set_2,frame_2_set4_4_set_3,frame_2_set4_4_set_4,input_2_1,input_2_167))
    
    input_2_1.insert(0, name_bot_historical)
    input_2_167.insert(0, bin.how_mach_coin)
    frame_2_set4_2_set_1.insert(0, round(bin.COMMISSION_MAKER*100,3))
    frame_2_set4_2_set_2.insert(0, round(bin.COMMISSION_TAKER*100,3))
    frame_2_set4_2_set_3.insert(0, round(bin.TP*100,3))
    frame_2_set4_2_set_4.insert(0, round(bin.SL*100,3))
    frame_2_set4_3_set_1.insert(0, bin.DEPOSIT)
    frame_2_set4_3_set_2.insert(0, bin.LEVERAGE)
    frame_2_set4_4_set_3.insert(0, bin.CANDLE_COIN_MIN)
    frame_2_set4_4_set_4.insert(0, bin.CANDLE_COIN_MAX)


    label_title112.pack(pady=10,anchor='n')
    frame_2_set4_0.pack(pady=10,ipady = 10,ipadx=5)
    frame_2_set4_1.grid(row=0, column=1, sticky="ew",padx=15)
    frame_2_set4_2.grid(row=0, column=2, sticky="ew",padx=15)
    frame_2_set4_25.grid(row=0, column=3, sticky="ew",padx=15)
    label_title2_1.pack(pady=[10,0])
    input_2_1.pack(pady=[0,1])
    label__2_set4_2_set_1.pack(pady=1)
    frame_2_set4_2_set_1.pack(pady=1)
    label__2_set4_2_set_2.pack(pady=[0,1])
    frame_2_set4_2_set_2.pack(pady=1)
    label__2_set4_2_set_3.pack(pady=1)
    frame_2_set4_2_set_3.pack(pady=1)
    label__2_set4_2_set_4.pack(pady=[0,1])
    frame_2_set4_2_set_4.pack(pady=1)
    label__2_set4_3_set_1.pack(pady=1)
    frame_2_set4_3_set_1.pack(pady=1)
    label__2_set4_3_set_2.pack(pady=[0,1])
    frame_2_set4_3_set_2.pack(pady=1)
    label__2_set4_4_set_3.pack(pady=1)
    frame_2_set4_4_set_3.pack(pady=1)
    label__2_set4_4_set_4.pack(pady=[0,1])
    frame_2_set4_4_set_4.pack(pady=[1,1])
    button32.pack(pady=20)
    
def open_step_2_historical(frame):
    global strat_mas_historical
    for widget in frame.winfo_children(): # чистим табличку
        widget.destroy()
    
    label_title112 = customtkinter.CTkLabel(frame, text="Выберете одну или несколько стратегий реальной тестовой торговли", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    frame_2_set4 = customtkinter.CTkFrame(frame, corner_radius=10, fg_color="#2B2B2B")
    label__2_set4 = customtkinter.CTkLabel(frame_2_set4, text="Выбор стратегии", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    frame_2_set4_0 = customtkinter.CTkFrame(frame_2_set4, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_1 = customtkinter.CTkFrame(frame_2_set4_0, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_1_1 = customtkinter.CTkScrollableFrame(frame_2_set4_1, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=500, height=450)
    radiobutton_1 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat1", offvalue="0",text="Канал, тренд, локаль, объём",text_color='#242424')
    radiobutton_2 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat2", offvalue="1",text="Суммарный тех индикатор TreadingView",text_color='#242424')
    radiobutton_3 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat3", offvalue="2",text="BarUpDn",text_color='#242424')
    radiobutton_4 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat4", offvalue="3",text="Полосы Боллинджера направленные",text_color='#242424')
    radiobutton_5 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat5", offvalue="4",text="Channel BreakOut",text_color='#242424')
    radiobutton_6 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat6", offvalue="5",text="Consecutive Up/Down",text_color='#242424')
    radiobutton_7 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat7", offvalue="6",text="Greedy",text_color='#242424')
    radiobutton_8 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat8", offvalue="7",text="InSide Bar",text_color='#242424')
    radiobutton_9 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat9", offvalue="8",text="Канал Кельтнера",text_color='#242424')
    radiobutton_10 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat10", offvalue="9",text="MACD",text_color='#242424')
    radiobutton_11 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat11", offvalue="10",text="Моментум",text_color='#242424')
    radiobutton_12 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat12", offvalue="11",text="Пересечение двух линий скользящих средних",text_color='#242424')
    radiobutton_13 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat13", offvalue="12",text="Пересечение скользящих средних",text_color='#242424')
    radiobutton_14 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat14", offvalue="13",text="OutSide Bar",text_color='#242424')
    radiobutton_15 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat15", offvalue="14",text="Параболическая остановка и разворот",text_color='#242424')
    radiobutton_16 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat16", offvalue="15",text="Pivot Extension",text_color='#242424')
    radiobutton_17 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat17", offvalue="16",text="Контрольная точка разворота",text_color='#242424')
    radiobutton_18 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat18", offvalue="17",text="Ценовые каналы",text_color='#242424')
    radiobutton_19 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat19", offvalue="18",text="Роб Букер - Прорыв ADX",text_color='#242424')
    radiobutton_20 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat20", offvalue="19",text="RSI",text_color='#242424')
    radiobutton_21 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat21", offvalue="20",text="Медленный стохастик",text_color='#242424')
    radiobutton_22 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat22", offvalue="21",text="Супертренд",text_color='#242424')
    radiobutton_23 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat23", offvalue="22",text="Технический индикатор рынка",text_color='#242424')
    radiobutton_24 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat24", offvalue="23",text="Volty Expan Close",text_color='#242424')
    radiobutton_25 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_historical,variable=check_var_historical, onvalue="strat25", offvalue="24",text="Линии Боллинджера",text_color='#242424')
    frame_2_set412 = customtkinter.CTkFrame(frame, corner_radius=10, fg_color="transparent")
    button3212 = customtkinter.CTkButton(frame_2_set412, text="Назад",command=lambda:historical_trade())
    button3213 = customtkinter.CTkButton(frame_2_set412, text="Настроить стратегию торговли",command=lambda:step_3_historical_trade_prom(frame))
    
    # выбор ранее отмеченных чекбоксов
    for strat in strat_mas_historical:
        match strat:
            case 'strat1' : radiobutton_1.select()
            case 'strat2' : radiobutton_2.select()
            case 'strat3' : radiobutton_3.select()
            case 'strat4' : radiobutton_4.select()
            case 'strat5' : radiobutton_5.select()
            case 'strat6' : radiobutton_6.select()
            case 'strat7' : radiobutton_7.select()
            case 'strat8' : radiobutton_8.select()
            case 'strat9' : radiobutton_9.select()
            case 'strat10': radiobutton_10.select()
            case 'strat11': radiobutton_11.select()
            case 'strat12': radiobutton_12.select()
            case 'strat13': radiobutton_13.select()
            case 'strat14': radiobutton_14.select()
            case 'strat15': radiobutton_15.select()
            case 'strat16': radiobutton_16.select()
            case 'strat17': radiobutton_17.select()
            case 'strat18': radiobutton_18.select()
            case 'strat19': radiobutton_19.select()
            case 'strat20': radiobutton_20.select()
            case 'strat21': radiobutton_21.select()
            case 'strat22': radiobutton_22.select()
            case 'strat23': radiobutton_23.select()
            case 'strat24': radiobutton_24.select()
            case 'strat25': radiobutton_25.select()
    # ----
    label_title112.pack(pady=5)
    frame_2_set4.pack(pady=10, padx=20)
    label__2_set4.pack(pady=5)
    frame_2_set4_0.pack(pady=10)
    frame_2_set4_1.grid(row=0, column=1, sticky="ew",padx=10)
    frame_2_set4_1_1.pack(pady=4)
    radiobutton_1.pack(pady=4, anchor='w')
    radiobutton_2.pack(pady=4, anchor='w')
    radiobutton_3.pack(pady=4, anchor='w')
    radiobutton_4.pack(pady=4, anchor='w')
    radiobutton_5.pack(pady=4, anchor='w')
    radiobutton_6.pack(pady=4, anchor='w')
    radiobutton_7.pack(pady=4, anchor='w')
    radiobutton_8.pack(pady=4, anchor='w')
    radiobutton_9.pack(pady=4, anchor='w')
    radiobutton_10.pack(pady=4, anchor='w')
    radiobutton_11.pack(pady=4, anchor='w')
    radiobutton_12.pack(pady=4, anchor='w')
    radiobutton_13.pack(pady=4, anchor='w')
    radiobutton_14.pack(pady=4, anchor='w')
    radiobutton_15.pack(pady=4, anchor='w')
    radiobutton_16.pack(pady=4, anchor='w')
    radiobutton_17.pack(pady=4, anchor='w')
    radiobutton_18.pack(pady=4, anchor='w')
    radiobutton_19.pack(pady=4, anchor='w')
    radiobutton_20.pack(pady=4, anchor='w')
    radiobutton_21.pack(pady=4, anchor='w')
    radiobutton_22.pack(pady=4, anchor='w')
    radiobutton_23.pack(pady=4, anchor='w')
    radiobutton_24.pack(pady=4, anchor='w')
    radiobutton_25.pack(pady=4, anchor='w')
    frame_2_set412.pack(pady=20, anchor='n')
    button3212.grid(row=0, column=0, sticky="ew",padx=10)
    button3213.grid(row=0, column=1, sticky="ew",padx=10)

def open_step_3_historical(frame):
    global strat_mas_historical
    for widget in frame.winfo_children(): # чистим табличку
        widget.destroy()
    for i in strat_mas_historical:
        match i:
            case 'strat1' : strat_historical.strat1(frame)
            case 'strat2' : strat_historical.strat2(frame)
            case 'strat3' : strat_historical.strat3()
            case 'strat4' : strat_historical.strat4()
            case 'strat5' : strat_historical.strat5()
            case 'strat6' : strat_historical.strat6()
            case 'strat7' : strat_historical.strat7()
            case 'strat8' : strat_historical.strat8()
            case 'strat9' : strat_historical.strat9()
            case 'strat10': strat_historical.strat10()
            case 'strat11': strat_historical.strat11()
            case 'strat12': strat_historical.strat12()
            case 'strat13': strat_historical.strat13()
            case 'strat14': strat_historical.strat14()
            case 'strat15': strat_historical.strat15()
            case 'strat16': strat_historical.strat16()
            case 'strat17': strat_historical.strat17()
            case 'strat18': strat_historical.strat18()
            case 'strat19': strat_historical.strat19()
            case 'strat20': strat_historical.strat20()
            case 'strat21': strat_historical.strat21()
            case 'strat22': strat_historical.strat22()
            case 'strat23': strat_historical.strat23()
            case 'strat24': strat_historical.strat24()
    
    frame_2_set412 = customtkinter.CTkFrame(frame, corner_radius=10, fg_color="transparent")
    button3212 = customtkinter.CTkButton(frame_2_set412, text="Назад",command=lambda:open_step_2_historical(frame))
    button3213 = customtkinter.CTkButton(frame_2_set412, text="Запустить торговлю",command=lambda:step_4_historical_trade_prom(frame))
    
    frame_2_set412.pack(pady=20, anchor='n')
    button3212.grid(row=0, column=0, sticky="ew",padx=10)
    button3213.grid(row=0, column=1, sticky="ew",padx=10)

def open_step_4_historical(frame,data_settings_1=[]):
    for widget in frame.winfo_children(): # чистим табличку
        widget.destroy()
    global name_bot_historical
    global strat_mas_historical,real_test_frame_3_2_1_historical
    strat_now_rt = []
    for i in strat_mas_historical:
        match i:
            case 'strat1' : strat_now_rt.append('Канал, тренд, локаль, объём')
            case 'strat2' : strat_now_rt.append('Суммарный тех индикатор TreadingView')
            case 'strat3' : strat_now_rt.append('BarUpDn')
            case 'strat4' : strat_now_rt.append('Полосы Боллинджера направленные')
            case 'strat5' : strat_now_rt.append('Channel BreakOut')
            case 'strat6' : strat_now_rt.append('Consecutive Up/Down')
            case 'strat7' : strat_now_rt.append('Greedy')
            case 'strat8' : strat_now_rt.append('InSide Bar')
            case 'strat9' : strat_now_rt.append('Канал Кельтнера')
            case 'strat10': strat_now_rt.append('MACD')
            case 'strat11': strat_now_rt.append('Моментум')
            case 'strat12': strat_now_rt.append('Пересечение двух линий скользящих средних')
            case 'strat13': strat_now_rt.append('Пересечение скользящих средних')
            case 'strat14': strat_now_rt.append('OutSide Bar')
            case 'strat15': strat_now_rt.append('Параболическая остановка и разворот')
            case 'strat16': strat_now_rt.append('Pivot Extension')
            case 'strat17': strat_now_rt.append('Контрольная точка разворота')
            case 'strat18': strat_now_rt.append('Ценовые каналы')
            case 'strat19': strat_now_rt.append('Роб Букер - Прорыв ADX')
            case 'strat20': strat_now_rt.append('RSI')
            case 'strat21': strat_now_rt.append('Медленный стохастик')
            case 'strat22': strat_now_rt.append('Супертренд')
            case 'strat23': strat_now_rt.append('Технический индикатор рынка')
            case 'strat24': strat_now_rt.append('Volty Expan Close')
            case 'strat25' : strat_now_rt.append('Линии Боллинджера')
    label_title112 = customtkinter.CTkLabel(frame, text="Проверьте настройки и запустите торговлю", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    frame_2_strat_1= customtkinter.CTkFrame(frame, corner_radius=10, fg_color="#2B2B2B",width=800)
    label_title2_1_0 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Общие настройки робота", fg_color="transparent",text_color='white',anchor='center',font=('Arial',14,'bold'),width=200)
    label_title2_1_1 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Имя робота для логов - {name_bot_historical}", fg_color="transparent",anchor='center',font=('Arial',12,'bold'),width=200)
    label_title2_1_2 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Таймфрейм - {bin.TF}", fg_color="transparent",font=('Arial',12,'bold'),width=200)
    label_title2_1_3 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Сколько топ монет торговать - {bin.how_mach_coin}", fg_color="transparent",anchor='center',font=('Arial',12,'bold'),width=200)
    label_title2_1_41 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Комиссия мейкер, {round(bin.COMMISSION_MAKER*100,3)}%", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label_title2_1_42 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Комиссия тейкер, {round(bin.COMMISSION_TAKER*100,3)}%", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label_title2_1_43 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Тейк профит, {round(bin.TP*100,3)}%", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label_title2_1_44 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Стоп лосс, {round(bin.SL*100,3)}%", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label_title2_1_45 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Деозит, {bin.DEPOSIT}$", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label_title2_1_46 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Плечо {bin.LEVERAGE}", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label_title2_1_47 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Объём торгов мин {bin.CANDLE_COIN_MIN}", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label_title2_1_48 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Объм торгов макс {bin.CANDLE_COIN_MAX}", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label_title2_1_5 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Выбраны стратегии:", fg_color="transparent",anchor='center',font=('Arial',12,'bold'),width=200)
    frame_2_set412 = customtkinter.CTkFrame(frame, corner_radius=10, fg_color="transparent")
    button3212 = customtkinter.CTkButton(frame_2_set412, text="Назад",command=lambda:open_step_3_historical(frame))
    button3213 = customtkinter.CTkButton(frame_2_set412, text="Запустить торговлю",command = lambda:start_historical_trade_strat_1())
    stop_trade_real_test = customtkinter.CTkButton(frame_2_set412, text="Остановить торговлю", command=stop_real_test_trade)
    real_test_frame_3 = customtkinter.CTkFrame(master=frame, corner_radius=10, fg_color="#2B2B2B")
    real_test_frame_3_2 = customtkinter.CTkFrame(real_test_frame_3, corner_radius=0, fg_color="#2B2B2B")
    
    
    
    real_test_label_3_2 = customtkinter.CTkLabel(real_test_frame_3_2, text="Логи торговли", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_frame_3_2_1_historical = customtkinter.CTkScrollableFrame(real_test_frame_3_2, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=460, height=260)
    real_test_frame_4 = customtkinter.CTkFrame(master=frame, corner_radius=10, fg_color="transparent") # графики
    
    label_title112.pack(pady=0, anchor='n')
    frame_2_strat_1.pack(pady=10, anchor='n')
    label_title2_1_0.grid(row=0, column=0,columnspan=2, sticky="ew",padx=10)
    label_title2_1_1.grid(row=1, column=0, sticky="w",padx=10)
    label_title2_1_2.grid(row=1, column=1, sticky="w",padx=10)
    label_title2_1_3.grid(row=2, column=0, sticky="w",padx=10)
    label_title2_1_41.grid(row=3, column=0, sticky="w",padx=10)
    label_title2_1_42.grid(row=3, column=1, sticky="w",padx=10)
    label_title2_1_43.grid(row=4, column=0, sticky="w",padx=10)
    label_title2_1_44.grid(row=4, column=1, sticky="w",padx=10)
    label_title2_1_45.grid(row=5, column=0, sticky="w",padx=10)
    label_title2_1_46.grid(row=5, column=1, sticky="w",padx=10)
    label_title2_1_47.grid(row=6, column=0, sticky="w",padx=10)
    label_title2_1_48.grid(row=6, column=1, sticky="w",padx=10)
    label_title2_1_5.grid(row=7, column=0,columnspan=2, sticky="ew",padx=10)
    for ind, i in enumerate(strat_now_rt):
        customtkinter.CTkLabel(frame_2_strat_1, text=i, fg_color="transparent",anchor='center',font=('Arial',12,'bold'),width=200).grid(row=8+ind, column=0,columnspan=2, sticky="ew",padx=10)
    if len(data_settings_1)!=0:
        frame_2_strat_122= customtkinter.CTkFrame(frame, corner_radius=10, fg_color="#2B2B2B",width=800)
        frame_2_strat_122.pack(pady=10, anchor='n')
        customtkinter.CTkLabel(frame_2_strat_122, text='Настройки стратегии - Канал, тренд, локаль, объём', fg_color="transparent",text_color='white',anchor='center',font=('Arial',14,'bold'),width=200).grid(row=0, column=0,columnspan=2, sticky="ew",padx=10)
        customtkinter.CTkLabel(frame_2_strat_122, text=f"Верх канала, {round(float(data_settings_1[6])*100,3)} %", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).grid(row=1, column=0, sticky="w",padx=10)
        customtkinter.CTkLabel(frame_2_strat_122, text=f"Низ канала, {round(float(data_settings_1[7])*100,3)} %", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).grid(row=2, column=0, sticky="w",padx=10)
        customtkinter.CTkLabel(frame_2_strat_122, text=f"Угол тренда лонг {data_settings_1[8]}", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).grid(row=3, column=0, sticky="w",padx=10)
        customtkinter.CTkLabel(frame_2_strat_122, text=f"Угол тренда шорт {data_settings_1[9]}", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).grid(row=4, column=0, sticky="w",padx=10)
    frame_2_set412.pack(pady=20, anchor='n')
    button3212.grid(row=0, column=0, sticky="ew",padx=10)
    button3213.grid(row=0, column=1, sticky="ew",padx=10)
    stop_trade_real_test.grid(row=0, column=2, sticky="ew",padx=10)
    #------------
    
    # условие на вывод торговли по сету готовых настроек
    if strat_mas_historical[0] == 'strat1' and len(strat_mas_historical)==1:
        frame_2_strat_1_settings = customtkinter.CTkFrame(frame, corner_radius=10, fg_color="#2B2B2B",width=800)
        label_title112_settings = customtkinter.CTkLabel(frame_2_strat_1_settings, text="Торговля стартегией 'Канал, тренд, локаль, объём'\nпо готовому сету настроек", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
        frame_2_strat_122_settings = customtkinter.CTkFrame(frame_2_strat_1_settings, corner_radius=10, fg_color="#2B2B2B")
        button3213_settings = customtkinter.CTkButton(frame_2_strat_122_settings, text="Загрузить сет настрорек",command = lambda:open_history_trade_strat_1_set())
        button32132_settings = customtkinter.CTkButton(frame_2_strat_122_settings, text="Начать торговлю",command = lambda:start_historical_trade_strat_1_set_validation())
        
        frame_2_strat_1_settings.pack(pady=20,ipadx=12)
        label_title112_settings.pack(pady=20)
        frame_2_strat_122_settings.pack(pady=[0,20])
        button3213_settings.grid(row=0, column=0,padx=10)
        button32132_settings.grid(row=0, column=1,padx=10)
    
    #---
    real_test_frame_3.pack(pady=20)
    real_test_frame_3_2.grid(row=0, column=1, sticky="ew",padx=10)
    real_test_label_3_2.pack(pady=0)
    real_test_frame_3_2_1_historical.pack(pady=0)
    #---
    
    real_test_frame_4.pack(pady=20)

# Валидация на начало торговли по сету настроек на первой стратегии - если есть данные в файле и они правильные
def start_historical_trade_strat_1_set_validation():
    # Проверить, есть ли данные в файле и они правильные
    try:
        thread29221 = threading.Thread(target=lambda:bin.start_trade_hist_model(strat_mas_historical,bin.COMMISSION_MAKER,bin.COMMISSION_TAKER,bin.TP,bin.SL,bin.DEPOSIT,bin.LEVERAGE,bin.CANDLE_COIN_MIN,bin.CANDLE_COIN_MAX,1,'111'))
        thread29221.start()
    except Exception as e:
        print('ОШИБКА начала исторической торговли по сету настроек')

# открываем блокнот дл янастроект 1 стратегии в сете
def open_history_trade_strat_1_set():
    print('Открыли файл для сохранения настроек')
    os.system("notepad strat_1_set.txt")

# функция отработки нажатия чекбоксов в шаге 2
def checkbox_event_strat_historical(): 
    global strat_mas_historical
    match check_var_historical.get():
        case '0' : strat_mas_historical.remove('strat1')
        case '1' : strat_mas_historical.remove('strat2')
        case '2' : strat_mas_historical.remove('strat3')
        case '3' : strat_mas_historical.remove('strat4')
        case '4' : strat_mas_historical.remove('strat5')
        case '5' : strat_mas_historical.remove('strat6')
        case '6' : strat_mas_historical.remove('strat7')
        case '7' : strat_mas_historical.remove('strat8')
        case '8' : strat_mas_historical.remove('strat9')
        case '9' : strat_mas_historical.remove('strat10')
        case '10': strat_mas_historical.remove('strat11')
        case '11': strat_mas_historical.remove('strat12')
        case '12': strat_mas_historical.remove('strat13')
        case '13': strat_mas_historical.remove('strat14')
        case '14': strat_mas_historical.remove('strat15')
        case '15': strat_mas_historical.remove('strat16')
        case '16': strat_mas_historical.remove('strat17')
        case '17': strat_mas_historical.remove('strat18')
        case '18': strat_mas_historical.remove('strat19')
        case '19': strat_mas_historical.remove('strat20')
        case '20': strat_mas_historical.remove('strat21')
        case '21': strat_mas_historical.remove('strat22')
        case '22': strat_mas_historical.remove('strat23')
        case '23': strat_mas_historical.remove('strat24')
        case '24': strat_mas_historical.remove('strat25')
        case 'strat1' : strat_mas_historical.append('strat1')
        case 'strat2' : strat_mas_historical.append('strat2')
        case 'strat3' : strat_mas_historical.append('strat3')
        case 'strat4' : strat_mas_historical.append('strat4')
        case 'strat5' : strat_mas_historical.append('strat5')
        case 'strat6' : strat_mas_historical.append('strat6')
        case 'strat7' : strat_mas_historical.append('strat7')
        case 'strat8' : strat_mas_historical.append('strat8')
        case 'strat9' : strat_mas_historical.append('strat9')
        case 'strat10': strat_mas_historical.append('strat10')
        case 'strat11': strat_mas_historical.append('strat11')
        case 'strat12': strat_mas_historical.append('strat12')
        case 'strat13': strat_mas_historical.append('strat13')
        case 'strat14': strat_mas_historical.append('strat14')
        case 'strat15': strat_mas_historical.append('strat15')
        case 'strat16': strat_mas_historical.append('strat16')
        case 'strat17': strat_mas_historical.append('strat17')
        case 'strat18': strat_mas_historical.append('strat18')
        case 'strat19': strat_mas_historical.append('strat19')
        case 'strat20': strat_mas_historical.append('strat20')
        case 'strat21': strat_mas_historical.append('strat21')
        case 'strat22': strat_mas_historical.append('strat22')
        case 'strat23': strat_mas_historical.append('strat23')
        case 'strat24': strat_mas_historical.append('strat24')
        case 'strat25': strat_mas_historical.append('strat25')
    
# отрисовка страницы - историческая торговля
def historical_trade():
    
    for widget in second_frame.winfo_children(): # чистим табличку
        widget.destroy()    
    
    label_title1 = customtkinter.CTkLabel(second_frame, text="Торговля по историческим данным", fg_color="transparent",anchor='center',font=('Arial',20,'bold'))
    frame_2_set1 = customtkinter.CTkFrame(second_frame, corner_radius=10, fg_color="transparent")
    button1 = customtkinter.CTkButton(frame_2_set1, text="Информация")
    button2 = customtkinter.CTkButton(frame_2_set1, text="Инструкция")
    button3 = customtkinter.CTkButton(frame_2_set1, text="История торгов",command=open_history_trade_log)
    frame_2_set1_step1 = customtkinter.CTkFrame(second_frame, corner_radius=10, fg_color="transparent")
    
    
    
    label_title1.pack(pady=20)
    frame_2_set1.pack(pady=10,padx=20)
    button1.grid(row=0, column=0, sticky="ew",padx=10)
    button2.grid(row=0, column=1, sticky="ew",padx=10)
    button3.grid(row=0, column=2, sticky="ew",padx=10)
    frame_2_set1_step1.pack()
    
    open_step_1_historical(frame_2_set1_step1)
    
   
    
# --------------------------------- РЕАЛЬНАЯ ТЕСТОВАЯ ТОРГОВЛЯ ---------------------------------    
real.wait_time = int(set1_timveframe.get(bin.TF))
# открываем логи торгов в блокноте
def open_real_test_trade_log():
    print('Открыли логи реальная тестовая торговля')
    os.system("notepad RT_log.txt")

# получаем таймфрейм 1 шаг
def get_setting_timeframe_real_test_trad(data):
    timeframe = set1_timveframe.get(data)
    real.TF = data
    real.wait_time = timeframe
    logger('RT',f'Реальная тестовая торговля | Таймфрейм- {real.TF}')

# стартуем реальную тестовую торговлю
def start_real_test_trade_btn(strat_now_rt,real_test_frame_4,real_test_frame_3_1_1,real_test_frame_3_2_1,card_trade_menu,strat_mas_real_test):
    try:
        global thread2
        logger('RT',f'------------------------------------------------------------------------')
        logger('RT',f'Реальная тестовая торговля | Начали торговлю')
        logger('RT',f'Реальная тестовая торговля | Настройки:')
        logger('RT',f'Реальная тестовая торговля | Комисия мейкер - {real.COMMISSION_MAKER}, тейкер - {real.COMMISSION_TAKER}')
        logger('RT',f'Реальная тестовая торговля | Тейк - {real.TP}, стоп - {real.SL}')
        logger('RT',f'Реальная тестовая торговля | Депозит - {real.DEPOSIT}, плечо - {real.LEVERAGE}')
        logger('RT',f'Реальная тестовая торговля | Канал макс - {str_1.CANAL_MAX}, канал мин - {str_1.CANAL_MIN}')
        logger('RT',f'Реальная тестовая торговля | Угол лонг - {str_1.CORNER_LONG}, угол шорт - {str_1.CORNER_SHORT}')
        logger('RT',f'Реальная тестовая торговля | Объём мин - {real.CANDLE_COIN_MIN}, макс - {real.CANDLE_COIN_MAX}')
        logger('RT',f'Реальная тестовая торговля | Название бота - {name_bot_real_test}')
        logger('RT',f'Реальная тестовая торговля | Галка тг- {sost_tg_message_real_test}')
        for widget in real_test_frame_3_1_1.winfo_children():
            widget.forget()
        for widget in real_test_frame_3_2_1.winfo_children():
            widget.forget()
        thread2 = threading.Thread(target=lambda:real.start_real_test_trade_model_thread_1(strat_now_rt,strat_mas_real_test,real_test_frame_4,card_trade_menu,name_bot_real_test,sost_tg_message_real_test,real_test_frame_3_1_1,real_test_frame_3_2_1))
        thread2.start()
    except ValueError: 
        messagebox.showinfo('Внимание','Ошибка запуска торговли')

# состояние кнопки остановить торговлю
def stop_real_test_trade():
    print('Нажали на кнопку - завершить торговлю, но пока поток не завершился')
    real.stop_real_test_trade_flag = True

# функция отработки нажатия чекбоксов в шаге 2
def checkbox_event_strat_real_test(): 
    global strat_mas_real_test
    match check_var_real_test.get():
        case '0' : strat_mas_real_test.remove('strat1')
        case '1' : strat_mas_real_test.remove('strat2')
        case '2' : strat_mas_real_test.remove('strat3')
        case '3' : strat_mas_real_test.remove('strat4')
        case '4' : strat_mas_real_test.remove('strat5')
        case '5' : strat_mas_real_test.remove('strat6')
        case '6' : strat_mas_real_test.remove('strat7')
        case '7' : strat_mas_real_test.remove('strat8')
        case '8' : strat_mas_real_test.remove('strat9')
        case '9' : strat_mas_real_test.remove('strat10')
        case '10': strat_mas_real_test.remove('strat11')
        case '11': strat_mas_real_test.remove('strat12')
        case '12': strat_mas_real_test.remove('strat13')
        case '13': strat_mas_real_test.remove('strat14')
        case '14': strat_mas_real_test.remove('strat15')
        case '15': strat_mas_real_test.remove('strat16')
        case '16': strat_mas_real_test.remove('strat17')
        case '17': strat_mas_real_test.remove('strat18')
        case '18': strat_mas_real_test.remove('strat19')
        case '19': strat_mas_real_test.remove('strat20')
        case '20': strat_mas_real_test.remove('strat21')
        case '21': strat_mas_real_test.remove('strat22')
        case '22': strat_mas_real_test.remove('strat23')
        case '23': strat_mas_real_test.remove('strat24')
        case '24': strat_mas_real_test.remove('strat25')
        case 'strat1' : strat_mas_real_test.append('strat1')
        case 'strat2' : strat_mas_real_test.append('strat2')
        case 'strat3' : strat_mas_real_test.append('strat3')
        case 'strat4' : strat_mas_real_test.append('strat4')
        case 'strat5' : strat_mas_real_test.append('strat5')
        case 'strat6' : strat_mas_real_test.append('strat6')
        case 'strat7' : strat_mas_real_test.append('strat7')
        case 'strat8' : strat_mas_real_test.append('strat8')
        case 'strat9' : strat_mas_real_test.append('strat9')
        case 'strat10': strat_mas_real_test.append('strat10')
        case 'strat11': strat_mas_real_test.append('strat11')
        case 'strat12': strat_mas_real_test.append('strat12')
        case 'strat13': strat_mas_real_test.append('strat13')
        case 'strat14': strat_mas_real_test.append('strat14')
        case 'strat15': strat_mas_real_test.append('strat15')
        case 'strat16': strat_mas_real_test.append('strat16')
        case 'strat17': strat_mas_real_test.append('strat17')
        case 'strat18': strat_mas_real_test.append('strat18')
        case 'strat19': strat_mas_real_test.append('strat19')
        case 'strat20': strat_mas_real_test.append('strat20')
        case 'strat21': strat_mas_real_test.append('strat21')
        case 'strat22': strat_mas_real_test.append('strat22')
        case 'strat23': strat_mas_real_test.append('strat23')
        case 'strat24': strat_mas_real_test.append('strat24')
        case 'strat25': strat_mas_real_test.append('strat25')
    print(strat_mas_real_test)

# валидация на данные с шага 1
def step_2_real_test_trade_prom(frame,switch_TG_var,input_2_1,input_3_1,frame_2_set4_2_set_1,frame_2_set4_2_set_2,frame_2_set4_2_set_3,frame_2_set4_2_set_4,frame_2_set4_3_set_1,frame_2_set4_3_set_2,frame_2_set4_4_set_3,frame_2_set4_4_set_4):
    global name_bot_real_test
    global sost_tg_message_real_test
    if name_bot_real_test=='': 
        messagebox.showinfo('Внимание','Введите имя бота')
    elif real.how_mach_coin=='': 
        messagebox.showinfo('Внимание','Введите количество монет для торговли')
    elif frame_2_set4_2_set_1.get()=='': 
        messagebox.showinfo('Внимание','Введите комиссию мейкер')
    elif frame_2_set4_2_set_2.get()=='': 
        messagebox.showinfo('Внимание','Введите комиссию тейкер')
    elif frame_2_set4_2_set_3.get()=='': 
        messagebox.showinfo('Внимание','Введите тейк профит')
    elif frame_2_set4_2_set_4.get()=='': 
        messagebox.showinfo('Внимание','Введите cтоп лосс')
    elif frame_2_set4_3_set_1.get()=='': 
        messagebox.showinfo('Внимание','Введите депозит')
    elif frame_2_set4_3_set_2.get()=='': 
        messagebox.showinfo('Внимание','Введите плечо')
    elif frame_2_set4_4_set_3.get()=='': 
        messagebox.showinfo('Внимание','Введите объём торгов мин')
    elif frame_2_set4_4_set_4.get()=='': 
        messagebox.showinfo('Внимание','Введите объём торгов макс')
    else:
        real.COMMISSION_MAKER = float(float(frame_2_set4_2_set_1.get())/100)
        real.COMMISSION_TAKER = float(float(frame_2_set4_2_set_2.get())/100)
        real.TP = float(float(frame_2_set4_2_set_3.get())/100)
        real.SL = float(float(frame_2_set4_2_set_4.get())/100)
        real.DEPOSIT = int(frame_2_set4_3_set_1.get())
        real.LEVERAGE = int(frame_2_set4_3_set_2.get())
        real.CANDLE_COIN_MIN = int(frame_2_set4_4_set_3.get())
        real.CANDLE_COIN_MAX = int(frame_2_set4_4_set_4.get())
        sost_tg_message_real_test = switch_TG_var.get()
        name_bot_real_test = input_2_1.get()
        real.how_mach_coin = input_3_1.get()
        step_2_real_test_trade(frame)

# валидация на данные с шага 2
def step_3_real_test_trade_prom(frame):
    global strat_mas_real_test
    if len(strat_mas_real_test)==0: 
        messagebox.showinfo('Внимание','Выберете хотя бы одну стратегию')
    else:
        step_3_real_test_trade(frame)

# валидация на данные с шага 3
def step_4_real_test_trade_prom(frame):
    global strat_mas_real_test
    for i in strat_mas_real_test:
        match i:
            case 'strat1' : data_settings_1 = strat_real_test.strat1_param()
            case 'strat2' : strat_real_test.strat2_param()
            case 'strat3' : strat_real_test.strat3()
            case 'strat4' : strat_real_test.strat4()
            case 'strat5' : strat_real_test.strat5()
            case 'strat6' : strat_real_test.strat6()
            case 'strat7' : strat_real_test.strat7()
            case 'strat8' : strat_real_test.strat8()
            case 'strat9' : strat_real_test.strat9()
            case 'strat10': strat_real_test.strat10()
            case 'strat11': strat_real_test.strat11()
            case 'strat12': strat_real_test.strat12()
            case 'strat13': strat_real_test.strat13()
            case 'strat14': strat_real_test.strat14()
            case 'strat15': strat_real_test.strat15()
            case 'strat16': strat_real_test.strat16()
            case 'strat17': strat_real_test.strat17()
            case 'strat18': strat_real_test.strat18()
            case 'strat19': strat_real_test.strat19()
            case 'strat20': strat_real_test.strat20()
            case 'strat21': strat_real_test.strat21()
            case 'strat22': strat_real_test.strat22()
            case 'strat23': strat_real_test.strat23()
            case 'strat24': strat_real_test.strat24()
    print(data_settings_1)
    if data_settings_1 != None:
        step_4_real_test_trade(frame,data_settings_1)

# первичные настройки робота в ртт
def step_1_real_test_trade(frame):
    
    label_title112 = customtkinter.CTkLabel(frame, text="Настройте робота для дальнейшей реальной тестовой торговли", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    frame_2_set4_0 = customtkinter.CTkFrame(master=frame,width=1100,height=800, corner_radius=10, fg_color="#2B2B2B")
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
    switch_TG_var = customtkinter.StringVar(value=sost_tg_message_real_test)
    switch_tg = customtkinter.CTkSwitch(frame_2_set4_3, text="Оповещения в ТГ",variable=switch_TG_var, onvalue="on", offvalue="off")
    frame_2_set4_2_set_1 = customtkinter.CTkEntry(frame_2_set4_1, placeholder_text="0.2",justify="center")
    frame_2_set4_2_set_2 = customtkinter.CTkEntry(frame_2_set4_1, placeholder_text="0.1",justify="center")
    frame_2_set4_2_set_3 = customtkinter.CTkEntry(frame_2_set4_2, placeholder_text="1.2",justify="center")
    frame_2_set4_2_set_4 = customtkinter.CTkEntry(frame_2_set4_2, placeholder_text="0.4",justify="center")
    label__2_set4_2_set_1 = customtkinter.CTkLabel(frame_2_set4_1, text="Комиссия мейкер, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_2_set_2 = customtkinter.CTkLabel(frame_2_set4_1, text="Комиссия тейкер, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_2_set_3 = customtkinter.CTkLabel(frame_2_set4_2, text="Тейк профит, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_2_set_4 = customtkinter.CTkLabel(frame_2_set4_2, text="Стоп лосс, %", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    frame_2_set4_3_set_1 = customtkinter.CTkEntry(frame_2_set4_25, placeholder_text="100",justify="center")
    frame_2_set4_3_set_2 = customtkinter.CTkEntry(frame_2_set4_25, placeholder_text="20",justify="center")
    label__2_set4_3_set_1 = customtkinter.CTkLabel(frame_2_set4_25, text="Деозит, $", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_3_set_2 = customtkinter.CTkLabel(frame_2_set4_25, text="Плечо", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    frame_2_set4_4_set_3 = customtkinter.CTkEntry(frame_2_set4_3, placeholder_text="200000",justify="center")
    frame_2_set4_4_set_4 = customtkinter.CTkEntry(frame_2_set4_3, placeholder_text="500000",justify="center")
    label__2_set4_4_set_3 = customtkinter.CTkLabel(frame_2_set4_3, text="Объём торгов мин", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label__2_set4_4_set_4 = customtkinter.CTkLabel(frame_2_set4_3, text="Объм торгов макс", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    button32 = customtkinter.CTkButton(frame, text="Выбрать стратегию торговли",command=lambda:step_2_real_test_trade_prom(frame,switch_TG_var,input_2_1,input_3_1,frame_2_set4_2_set_1,frame_2_set4_2_set_2,frame_2_set4_2_set_3,frame_2_set4_2_set_4,frame_2_set4_3_set_1,frame_2_set4_3_set_2,frame_2_set4_4_set_3,frame_2_set4_4_set_4))
    
    input_2_1.insert(0, name_bot_real_test)
    input_3_1.insert(0, real.how_mach_coin)
    real_test_trade_frame_1_appearance_mode_menu1.set(real.TF)
    frame_2_set4_2_set_1.insert(0, round(real.COMMISSION_MAKER*100,3))
    frame_2_set4_2_set_2.insert(0, round(real.COMMISSION_TAKER*100,3))
    frame_2_set4_2_set_3.insert(0, round(real.TP*100,3))
    frame_2_set4_2_set_4.insert(0, round(real.SL*100,3))
    frame_2_set4_3_set_1.insert(0, real.DEPOSIT)
    frame_2_set4_3_set_2.insert(0, real.LEVERAGE)
    frame_2_set4_4_set_3.insert(0, real.CANDLE_COIN_MIN)
    frame_2_set4_4_set_4.insert(0, real.CANDLE_COIN_MAX)


    label_title112.pack(pady=10,anchor='n')
    frame_2_set4_0.pack(pady=10,ipady = 10,ipadx=5)
    frame_2_set4_1.grid(row=0, column=1, sticky="ew",padx=5)
    frame_2_set4_2.grid(row=0, column=2, sticky="ew",padx=5)
    frame_2_set4_25.grid(row=0, column=3, sticky="ew",padx=[5,15])
    frame_2_set4_3.grid(row=0, column=4, sticky="ew",padx=5)
    real_test_trade_frame_1_label_title1_1_1.pack(pady=[10,0])
    real_test_trade_frame_1_appearance_mode_menu1.pack(pady=[0,15])
    label_title2_1.pack(pady=[10,0])
    input_2_1.pack(pady=[0,15])
    label_title3_1.pack(pady=[10,0])
    input_3_1.pack(pady=[0,15])
    switch_tg.pack(pady=[20,30],ipady=12)
    label__2_set4_2_set_1.pack(pady=1)
    frame_2_set4_2_set_1.pack(pady=1)
    label__2_set4_2_set_2.pack(pady=[0,15])
    frame_2_set4_2_set_2.pack(pady=1)
    label__2_set4_2_set_3.pack(pady=1)
    frame_2_set4_2_set_3.pack(pady=1)
    label__2_set4_2_set_4.pack(pady=[0,15])
    frame_2_set4_2_set_4.pack(pady=1)
    label__2_set4_3_set_1.pack(pady=1)
    frame_2_set4_3_set_1.pack(pady=1)
    label__2_set4_3_set_2.pack(pady=[0,15])
    frame_2_set4_3_set_2.pack(pady=1)
    label__2_set4_4_set_3.pack(pady=1)
    frame_2_set4_4_set_3.pack(pady=1)
    label__2_set4_4_set_4.pack(pady=[0,15])
    frame_2_set4_4_set_4.pack(pady=[1,20])
    button32.pack(pady=10,anchor='n')

# выбор стратегий для торговли
def step_2_real_test_trade(frame):
    global strat_mas_real_test
    for widget in frame.winfo_children(): # чистим табличку
        widget.destroy()
    print('1')
    
    label_title112 = customtkinter.CTkLabel(frame, text="Выберете одну или несколько стратегий реальной тестовой торговли", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    frame_2_set4 = customtkinter.CTkFrame(frame, corner_radius=10, fg_color="#2B2B2B")
    label__2_set4 = customtkinter.CTkLabel(frame_2_set4, text="Выбор стратегии", fg_color="transparent",anchor='center',font=('Arial',14,'bold'))
    frame_2_set4_0 = customtkinter.CTkFrame(frame_2_set4, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_1 = customtkinter.CTkFrame(frame_2_set4_0, corner_radius=0, fg_color="#2B2B2B")
    frame_2_set4_1_1 = customtkinter.CTkScrollableFrame(frame_2_set4_1, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=500, height=450)
    radiobutton_1 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat1", offvalue="0",text="Канал, тренд, локаль, объём",text_color='#242424')
    radiobutton_2 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat2", offvalue="1",text="Суммарный тех индикатор TreadingView",text_color='#242424')
    radiobutton_3 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat3", offvalue="2",text="BarUpDn",text_color='#242424')
    radiobutton_4 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat4", offvalue="3",text="Полосы Боллинджера направленные",text_color='#242424')
    radiobutton_5 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat5", offvalue="4",text="Channel BreakOut",text_color='#242424')
    radiobutton_6 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat6", offvalue="5",text="Consecutive Up/Down",text_color='#242424')
    radiobutton_7 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat7", offvalue="6",text="Greedy",text_color='#242424')
    radiobutton_8 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat8", offvalue="7",text="InSide Bar",text_color='#242424')
    radiobutton_9 = customtkinter.CTkCheckBox(frame_2_set4_1_1,  command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat9", offvalue="8",text="Канал Кельтнера",text_color='#242424')
    radiobutton_10 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat10", offvalue="9",text="MACD",text_color='#242424')
    radiobutton_11 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat11", offvalue="10",text="Моментум",text_color='#242424')
    radiobutton_12 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat12", offvalue="11",text="Пересечение двух линий скользящих средних",text_color='#242424')
    radiobutton_13 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat13", offvalue="12",text="Пересечение скользящих средних",text_color='#242424')
    radiobutton_14 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat14", offvalue="13",text="OutSide Bar",text_color='#242424')
    radiobutton_15 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat15", offvalue="14",text="Параболическая остановка и разворот",text_color='#242424')
    radiobutton_16 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat16", offvalue="15",text="Pivot Extension",text_color='#242424')
    radiobutton_17 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat17", offvalue="16",text="Контрольная точка разворота",text_color='#242424')
    radiobutton_18 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat18", offvalue="17",text="Ценовые каналы",text_color='#242424')
    radiobutton_19 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat19", offvalue="18",text="Роб Букер - Прорыв ADX",text_color='#242424')
    radiobutton_20 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat20", offvalue="19",text="RSI",text_color='#242424')
    radiobutton_21 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat21", offvalue="20",text="Медленный стохастик",text_color='#242424')
    radiobutton_22 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat22", offvalue="21",text="Супертренд",text_color='#242424')
    radiobutton_23 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat23", offvalue="22",text="Технический индикатор рынка",text_color='#242424')
    radiobutton_24 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat24", offvalue="23",text="Volty Expan Close",text_color='#242424')
    radiobutton_25 = customtkinter.CTkCheckBox(frame_2_set4_1_1, command=checkbox_event_strat_real_test,variable=check_var_real_test, onvalue="strat25", offvalue="24",text="Линии Боллинджера",text_color='#242424')
    frame_2_set412 = customtkinter.CTkFrame(frame, corner_radius=10, fg_color="transparent")
    button3212 = customtkinter.CTkButton(frame_2_set412, text="Назад",command=lambda:real_test_trade())
    button3213 = customtkinter.CTkButton(frame_2_set412, text="Настроить стратегию торговли",command=lambda:step_3_real_test_trade_prom(frame))
    
    # выбор ранее отмеченных чекбоксов
    for strat in strat_mas_real_test:
        match strat:
            case 'strat1' : radiobutton_1.select()
            case 'strat2' : radiobutton_2.select()
            case 'strat3' : radiobutton_3.select()
            case 'strat4' : radiobutton_4.select()
            case 'strat5' : radiobutton_5.select()
            case 'strat6' : radiobutton_6.select()
            case 'strat7' : radiobutton_7.select()
            case 'strat8' : radiobutton_8.select()
            case 'strat9' : radiobutton_9.select()
            case 'strat10': radiobutton_10.select()
            case 'strat11': radiobutton_11.select()
            case 'strat12': radiobutton_12.select()
            case 'strat13': radiobutton_13.select()
            case 'strat14': radiobutton_14.select()
            case 'strat15': radiobutton_15.select()
            case 'strat16': radiobutton_16.select()
            case 'strat17': radiobutton_17.select()
            case 'strat18': radiobutton_18.select()
            case 'strat19': radiobutton_19.select()
            case 'strat20': radiobutton_20.select()
            case 'strat21': radiobutton_21.select()
            case 'strat22': radiobutton_22.select()
            case 'strat23': radiobutton_23.select()
            case 'strat24': radiobutton_24.select()
            case 'strat25': radiobutton_25.select()
    # ----
    label_title112.pack(pady=5)
    frame_2_set4.pack(pady=10, padx=20)
    label__2_set4.pack(pady=5)
    frame_2_set4_0.pack(pady=10)
    frame_2_set4_1.grid(row=0, column=1, sticky="ew",padx=10)
    frame_2_set4_1_1.pack(pady=4)
    radiobutton_1.pack(pady=4, anchor='w')
    radiobutton_2.pack(pady=4, anchor='w')
    radiobutton_3.pack(pady=4, anchor='w')
    radiobutton_4.pack(pady=4, anchor='w')
    radiobutton_5.pack(pady=4, anchor='w')
    radiobutton_6.pack(pady=4, anchor='w')
    radiobutton_7.pack(pady=4, anchor='w')
    radiobutton_8.pack(pady=4, anchor='w')
    radiobutton_9.pack(pady=4, anchor='w')
    radiobutton_10.pack(pady=4, anchor='w')
    radiobutton_11.pack(pady=4, anchor='w')
    radiobutton_12.pack(pady=4, anchor='w')
    radiobutton_13.pack(pady=4, anchor='w')
    radiobutton_14.pack(pady=4, anchor='w')
    radiobutton_15.pack(pady=4, anchor='w')
    radiobutton_16.pack(pady=4, anchor='w')
    radiobutton_17.pack(pady=4, anchor='w')
    radiobutton_18.pack(pady=4, anchor='w')
    radiobutton_19.pack(pady=4, anchor='w')
    radiobutton_20.pack(pady=4, anchor='w')
    radiobutton_21.pack(pady=4, anchor='w')
    radiobutton_22.pack(pady=4, anchor='w')
    radiobutton_23.pack(pady=4, anchor='w')
    radiobutton_24.pack(pady=4, anchor='w')
    radiobutton_25.pack(pady=4, anchor='w')
    frame_2_set412.pack(pady=20, anchor='n')
    button3212.grid(row=0, column=0, sticky="ew",padx=10)
    button3213.grid(row=0, column=1, sticky="ew",padx=10)

# шаг 3 - настройки выбранных стратегий
def step_3_real_test_trade(frame):
    global strat_mas_real_test
    for widget in frame.winfo_children(): # чистим табличку
        widget.destroy()
    for i in strat_mas_real_test:
        match i:
            case 'strat1' : strat_real_test.strat1(frame)
            case 'strat2' : strat_real_test.strat2(frame)
            case 'strat3' : strat_real_test.strat3()
            case 'strat4' : strat_real_test.strat4()
            case 'strat5' : strat_real_test.strat5()
            case 'strat6' : strat_real_test.strat6()
            case 'strat7' : strat_real_test.strat7()
            case 'strat8' : strat_real_test.strat8()
            case 'strat9' : strat_real_test.strat9()
            case 'strat10': strat_real_test.strat10()
            case 'strat11': strat_real_test.strat11()
            case 'strat12': strat_real_test.strat12()
            case 'strat13': strat_real_test.strat13()
            case 'strat14': strat_real_test.strat14()
            case 'strat15': strat_real_test.strat15()
            case 'strat16': strat_real_test.strat16()
            case 'strat17': strat_real_test.strat17()
            case 'strat18': strat_real_test.strat18()
            case 'strat19': strat_real_test.strat19()
            case 'strat20': strat_real_test.strat20()
            case 'strat21': strat_real_test.strat21()
            case 'strat22': strat_real_test.strat22()
            case 'strat23': strat_real_test.strat23()
            case 'strat24': strat_real_test.strat24()
    
    frame_2_set412 = customtkinter.CTkFrame(frame, corner_radius=10, fg_color="transparent")
    button3212 = customtkinter.CTkButton(frame_2_set412, text="Назад",command=lambda:step_2_real_test_trade(frame))
    button3213 = customtkinter.CTkButton(frame_2_set412, text="Запустить торговлю",command=lambda:step_4_real_test_trade_prom(frame))
    
    frame_2_set412.pack(pady=20, anchor='n')
    button3212.grid(row=0, column=0, sticky="ew",padx=10)
    button3213.grid(row=0, column=1, sticky="ew",padx=10)

# шаг 4 - проверка настроек и запуск торговли
def step_4_real_test_trade(frame,data_settings_1=[]):
    for widget in frame.winfo_children(): # чистим табличку
        widget.destroy()
    global name_bot_real_test
    global sost_tg_message_real_test
    global strat_mas_real_test
    strat_now_rt = []
    for i in strat_mas_real_test:
        match i:
            case 'strat1' : strat_now_rt.append('Канал, тренд, локаль, объём')
            case 'strat2' : strat_now_rt.append('Суммарный тех индикатор TreadingView')
            case 'strat3' : strat_now_rt.append('BarUpDn')
            case 'strat4' : strat_now_rt.append('Полосы Боллинджера направленные')
            case 'strat5' : strat_now_rt.append('Channel BreakOut')
            case 'strat6' : strat_now_rt.append('Consecutive Up/Down')
            case 'strat7' : strat_now_rt.append('Greedy')
            case 'strat8' : strat_now_rt.append('InSide Bar')
            case 'strat9' : strat_now_rt.append('Канал Кельтнера')
            case 'strat10': strat_now_rt.append('MACD')
            case 'strat11': strat_now_rt.append('Моментум')
            case 'strat12': strat_now_rt.append('Пересечение двух линий скользящих средних')
            case 'strat13': strat_now_rt.append('Пересечение скользящих средних')
            case 'strat14': strat_now_rt.append('OutSide Bar')
            case 'strat15': strat_now_rt.append('Параболическая остановка и разворот')
            case 'strat16': strat_now_rt.append('Pivot Extension')
            case 'strat17': strat_now_rt.append('Контрольная точка разворота')
            case 'strat18': strat_now_rt.append('Ценовые каналы')
            case 'strat19': strat_now_rt.append('Роб Букер - Прорыв ADX')
            case 'strat20': strat_now_rt.append('RSI')
            case 'strat21': strat_now_rt.append('Медленный стохастик')
            case 'strat22': strat_now_rt.append('Супертренд')
            case 'strat23': strat_now_rt.append('Технический индикатор рынка')
            case 'strat24': strat_now_rt.append('Volty Expan Close')
            case 'strat25' : strat_now_rt.append('Линии Боллинджера')
    label_title112 = customtkinter.CTkLabel(frame, text="Проверьте настройки и запустите торговлю", fg_color="transparent",anchor='center',font=('Arial',14,'normal'))
    frame_2_strat_1= customtkinter.CTkFrame(frame, corner_radius=10, fg_color="#2B2B2B",width=800)
    label_title2_1_0 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Общие настройки робота", fg_color="transparent",text_color='white',anchor='center',font=('Arial',14,'bold'),width=200)
    label_title2_1_1 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Имя робота для логов - {name_bot_real_test}", fg_color="transparent",anchor='center',font=('Arial',12,'bold'),width=200)
    label_title2_1_2 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Таймфрейм - {real.TF}", fg_color="transparent",font=('Arial',12,'bold'),width=200)
    label_title2_1_3 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Сколько топ монет торговать - {real.how_mach_coin}", fg_color="transparent",anchor='center',font=('Arial',12,'bold'),width=200)
    label_title2_1_4 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Оповещения в ТГ - {'да' if sost_tg_message_real_test=='on' else 'нет'}", fg_color="transparent",font=('Arial',12,'bold'),width=200)
    label_title2_1_41 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Комиссия мейкер, {round(real.COMMISSION_MAKER*100,3)}%", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label_title2_1_42 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Комиссия тейкер, {round(real.COMMISSION_TAKER*100,3)}%", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label_title2_1_43 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Тейк профит, {round(real.TP*100,3)}%", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label_title2_1_44 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Стоп лосс, {round(real.SL*100,3)}%", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label_title2_1_45 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Деозит, {real.DEPOSIT}$", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label_title2_1_46 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Плечо {real.LEVERAGE}", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label_title2_1_47 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Объём торгов мин {real.CANDLE_COIN_MIN}", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label_title2_1_48 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Объм торгов макс {real.CANDLE_COIN_MAX}", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    label_title2_1_5 = customtkinter.CTkLabel(frame_2_strat_1, text=f"Выбраны стратегии:", fg_color="transparent",anchor='center',font=('Arial',12,'bold'),width=200)
    frame_2_set412 = customtkinter.CTkFrame(frame, corner_radius=10, fg_color="transparent")
    button3212 = customtkinter.CTkButton(frame_2_set412, text="Назад",command=lambda:step_3_real_test_trade(frame))
    button3213 = customtkinter.CTkButton(frame_2_set412, text="Запустить торговлю",command = lambda:start_real_test_trade_btn(strat_now_rt,real_test_frame_4,real_test_frame_3_1_1,real_test_frame_3_2_1,card_trade_menu,strat_mas_real_test))
    stop_trade_real_test = customtkinter.CTkButton(frame_2_set412, text="Остановить торговлю", command=stop_real_test_trade)
    real_test_frame_3 = customtkinter.CTkFrame(master=frame, corner_radius=10, fg_color="#2B2B2B")
    real_test_frame_3_1 = customtkinter.CTkFrame(real_test_frame_3, corner_radius=0, fg_color="#2B2B2B")
    real_test_frame_3_2 = customtkinter.CTkFrame(real_test_frame_3, corner_radius=0, fg_color="#2B2B2B")
    real_test_label_3_1 = customtkinter.CTkLabel(real_test_frame_3_1, text="Данные по монете в сделке", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_frame_3_1_1 = customtkinter.CTkScrollableFrame(real_test_frame_3_1, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=160, height=260)
    real_test_label_3_2 = customtkinter.CTkLabel(real_test_frame_3_2, text="Логи торговли", fg_color="transparent",anchor='center',font=('Arial',12,'bold'))
    real_test_frame_3_2_1 = customtkinter.CTkScrollableFrame(real_test_frame_3_2, corner_radius=5, fg_color="#DAE2EC",orientation='vertical', width=460, height=260)
    real_test_frame_4 = customtkinter.CTkFrame(master=frame, corner_radius=10, fg_color="transparent") # графики
    
    label_title112.pack(pady=0, anchor='n')
    frame_2_strat_1.pack(pady=10, anchor='n')
    label_title2_1_0.grid(row=0, column=0,columnspan=2, sticky="ew",padx=10)
    label_title2_1_1.grid(row=1, column=0, sticky="w",padx=10)
    label_title2_1_2.grid(row=1, column=1, sticky="w",padx=10)
    label_title2_1_3.grid(row=2, column=0, sticky="w",padx=10)
    label_title2_1_4.grid(row=2, column=1, sticky="w",padx=10)
    label_title2_1_41.grid(row=3, column=0, sticky="w",padx=10)
    label_title2_1_42.grid(row=3, column=1, sticky="w",padx=10)
    label_title2_1_43.grid(row=4, column=0, sticky="w",padx=10)
    label_title2_1_44.grid(row=4, column=1, sticky="w",padx=10)
    label_title2_1_45.grid(row=5, column=0, sticky="w",padx=10)
    label_title2_1_46.grid(row=5, column=1, sticky="w",padx=10)
    label_title2_1_47.grid(row=6, column=0, sticky="w",padx=10)
    label_title2_1_48.grid(row=6, column=1, sticky="w",padx=10)
    label_title2_1_5.grid(row=7, column=0,columnspan=2, sticky="ew",padx=10)
    for ind, i in enumerate(strat_now_rt):
        customtkinter.CTkLabel(frame_2_strat_1, text=i, fg_color="transparent",anchor='center',font=('Arial',12,'bold'),width=200).grid(row=8+ind, column=0,columnspan=2, sticky="ew",padx=10)
    if len(data_settings_1)!=0:
        frame_2_strat_122= customtkinter.CTkFrame(frame, corner_radius=10, fg_color="#2B2B2B",width=800)
        frame_2_strat_122.pack(pady=10, anchor='n')
        customtkinter.CTkLabel(frame_2_strat_122, text='Настройки стратегии - Канал, тренд, локаль, объём', fg_color="transparent",text_color='white',anchor='center',font=('Arial',14,'bold'),width=200).grid(row=0, column=0,columnspan=2, sticky="ew",padx=10)
        customtkinter.CTkLabel(frame_2_strat_122, text=f"Верх канала, {round(float(data_settings_1[6])*100,3)} %", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).grid(row=1, column=0, sticky="w",padx=10)
        customtkinter.CTkLabel(frame_2_strat_122, text=f"Низ канала, {round(float(data_settings_1[7])*100,3)} %", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).grid(row=2, column=0, sticky="w",padx=10)
        customtkinter.CTkLabel(frame_2_strat_122, text=f"Угол тренда лонг {data_settings_1[8]}", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).grid(row=3, column=0, sticky="w",padx=10)
        customtkinter.CTkLabel(frame_2_strat_122, text=f"Угол тренда шорт {data_settings_1[9]}", fg_color="transparent",anchor='center',font=('Arial',12,'bold')).grid(row=4, column=0, sticky="w",padx=10)
    frame_2_set412.pack(pady=20, anchor='n')
    button3212.grid(row=0, column=0, sticky="ew",padx=10)
    button3213.grid(row=0, column=1, sticky="ew",padx=10)
    stop_trade_real_test.grid(row=0, column=2, sticky="ew",padx=10)
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

# показывается при нажатии на вкладку меню
def real_test_trade():
    for widget in third_frame.winfo_children(): # чистим табличку
        widget.destroy()    
    label_title1 = customtkinter.CTkLabel(third_frame, text="Реальная тестовая торговля", fg_color="transparent",anchor='center',font=('Arial',20,'bold'))
    frame_2_set1 = customtkinter.CTkFrame(third_frame, corner_radius=10, fg_color="transparent")
    button1 = customtkinter.CTkButton(frame_2_set1, text="Информация")
    button2 = customtkinter.CTkButton(frame_2_set1, text="Инструкция")
    button3 = customtkinter.CTkButton(frame_2_set1, text="История торгов", command = open_real_test_trade_log)
    frame_2_set1_step1 = customtkinter.CTkFrame(third_frame, corner_radius=10, fg_color="transparent")
    
    
    label_title1.pack(pady=20)
    frame_2_set1.pack(pady=10,padx=20)
    button1.grid(row=0, column=0, sticky="ew",padx=10)
    button2.grid(row=0, column=1, sticky="ew",padx=10)
    button3.grid(row=0, column=2, sticky="ew",padx=10)
    frame_2_set1_step1.pack()
    
    step_1_real_test_trade(frame_2_set1_step1)


speed_test()
update_time()
settings_prog()
profile()
main_page()

win.mainloop()