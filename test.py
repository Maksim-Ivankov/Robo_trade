from imports import *
import websocket

# открываем по центру
win = customtkinter.CTk()
win.title("Robo_trade")
w = 200 
h = 200
ws = win.winfo_screenwidth()
hs = win.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
win.geometry('%dx%d+%d+%d' % (w, h, x, y))    
# выстраиваем сетку гридов
win.grid_rowconfigure(0, weight=1)
win.grid_columnconfigure(1, weight=1)

def start():
    print('Стартуем на кнопку')
    thread2 = threading.Thread(target=start_real_test_trade_model_thread_1)
    thread2.start()
    
    
def start_real_test_trade_model_thread_1():
    print('Вошли в первый поток')
    try:
        thread25 = threading.Thread(target=start_real_test_trade_model)
        thread25.start()
    except Exception as e:
        messagebox.showinfo('Внимание','Ошибка начала торговли')
        
def start_real_test_trade_model():
    print('Вошли во второй поток')
    loop22 = asyncio.new_event_loop()
    asyncio.set_event_loop(loop22)
    loop22 = asyncio.get_event_loop()
    loop22.run_until_complete(websocket_trade()) 
   
    print('После сокетов')

async def websocket_trade():
    print('внутри вебсокетов 1')
    url = "wss://fstream.binance.com/stream?streams=btcusdt@miniTicker"
    async with websockets.connect(url) as client:
        while True:
            data = json.loads(await client.recv())['data']
            print(data['c'])
    
    

button1 = customtkinter.CTkButton(win, text="Запускаем вебсокеты", command=start)

button1.pack(pady=20)
# async def main():
#     url = "wss://stream.binance.com:9443/stream?streams=btcusdt@miniTicker"
#     async with websockets.connect(url) as client:
#         while True:
#             data = json.loads(await client.recv())['data']
#             print(data['c'])
            
  
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())        
























win.mainloop()