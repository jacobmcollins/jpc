# General Imports
import time
import tkinter as tk
from PIL import ImageTk,Image

w = 'initial'


class Display(tk.Canvas):
    def __init__(self,  parent, *args, **kwargs):
        self.parent = parent
        tk.Canvas.__init__(self, parent, *args, **kwargs)

    def current_play(self, option):
        if option == 'initial':
            self.initial_display()
        elif option == 'n' or option == 's':
            self.ns_display()

    def initial_display(self):
        self.set_image("temp")

    def set_image(self, file):
        self.im = Image.open(file)
        self.im = self.im.resize((self.winfo_screenwidth(),self.winfo_screenheight()), Image.ANTIALIAS)
        self.photo_image = ImageTk.PhotoImage(self.im)
        self.demo = self.create_image(0, 0, image=self.photo_image, anchor='nw')
        self.update()


class start_gui(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self,parent, *args, **kwargs)
        # create canvas
        self.canvas = Display(parent, width=parent.winfo_screenwidth(), height=parent.winfo_screenheight(), background="white")
        self.message_text = tk.StringVar()
        self.message_text.set("Welcome")
        self.label = tk.Label(parent, textvariable=self.message_text,font=("Helvetica", 50), wraplength=500)
        self.label.pack(expand=True)
        self.canvas.pack()
        self.canvas.current_play(w)

    def set_message(self, message):
        self.message_text.set(message)
        for i in range(0,10):
            self.flash_screen("yellow")
            time.sleep(.1)
            self.flash_screen("red")
            time.sleep(.1)
        self.flash_screen("white")
        self.update()

    def set_image(self, file):
        self.canvas.set_image(file)

    def flash_screen(self, color):
        self.label.configure(background=color)
        self.configure(background=color)
        self.update()


class JPCClientGUI:
    def __init__(self):
        self.root = tk.Tk()
        #self.root.attributes("-fullscreen", True)
        self.g = start_gui(self.root)
        self.root.update()

    def start(self):
        self.root.update()

    def set_message(self, message):
        self.g.set_message(message)

    def set_image(self, file):
        self.g.set_image(file)
