import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Robo_trade")
        w = 1000
        h = 800
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

        


