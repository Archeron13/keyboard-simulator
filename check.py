from pynput import keyboard
import sys
import tkinter
from tkinter.messagebox import YES
import customtkinter as ctk
from PIL import Image, ImageTk
import re
import time
from threading import Thread

WIDTH = 1280
HEIGHT = 720

with open("test.txt") as f:             
    sentence = f.read()
    #char_sentence = list(sentence)
    list_sentences = re.split(r'[ \n]',sentence)
    char_sentence = re.split(r'[\n]',sentence)
    print(list_sentences)




class background(tkinter.Canvas):
    def __init__(self, master, *pargs):
        tkinter.Canvas.__init__(self, master, *pargs)

        self.imgBG = Image.open("Images/startBG.jpg")
        self.imgBG_copy = self.imgBG.copy()


        self.imgMain = ImageTk.PhotoImage(self.imgBG)

        self.background = ctk.CTkLabel(self, image=self.imgMain)
        self.background.pack(fill="both", expand=True)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self,event):


        self.imgBG = self.imgBG_copy.resize((event.width, event.height))

        self.imgMain = ImageTk.PhotoImage(self.imgBG)
        self.background.configure(image =  self.imgMain)



class startGUI:

    def __init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme('dark-blue')

        self.root = ctk.CTk()

        self.root.geometry(f'{WIDTH}x{HEIGHT}')
        self.root.title("Keyboard Simulator")

        self.bgCanvas = background(self.root)
        self.bgCanvas.place(x=0,y=0,relwidth=1,relheight=1)

        self.text_var = list_sentences[:15]
        self.input_var = ""

        self.cur_key = ""

        self.mainTextLabel = ctk.CTkLabel(self.root,text = "Keyboard Simulator",text_font = ("Arial50,20"),fg_color=("white","grey"))
        self.mainTextLabel.pack(pady="10",fill="x")

        self.showTextLabel = ctk.CTkLabel(self.root,text =self.text_var,text_font=("Arial50",12),fg_color=("white","gray"))
        self.showTextLabel.pack(side="top",fill="x",expand= True)


        self.inputTextLabel = ctk.CTkLabel(self.root,text =self.input_var,text_font=("Arial50","12"),fg_color=("white","blue"))
        self.inputTextLabel.pack(fill="x",expand = True)

        self.button = ctk.CTkButton(self.root, text="Press to Start", command=Thread(target=self.start_game).start)

        self.button.pack(padx=20, pady=10)

        #STatistics for game
        self.wrong_counter = 0
        self.key_count = 0
        self.char_count = 0
        self.cur_state = ""
        self.cur_keycode = 0
        self.root.mainloop()
    
    def key_press(self,event):
        self.cur_key = event.char
        self.cur_state= event.state
        self.cur_keycode = event.keycode
        print(self.cur_state)
        print(self.cur_keycode)
        self.key_count += 1

    def start_game(self):
        self.root.bind("<KeyPress>",self.key_press)
        for cur_word in char_sentence:
            for curChar in cur_word:
                exit_loop = False
                if (exit_loop):
                    break
                print(f"{curChar} IS THE BUTTON TO PRESS DUMB FUCK")
                while True:
                    if (curChar == self.cur_key):
                        self.char_count += 1
                        break
                    elif (self.cur_state == 17 and self.cur_keycode == 52 ):
                        exit_loop = False
                        break
                    else:
                        pass
        print(f"{self.char_count} cur_count, {self.key_count} key_count, {self.key_count - self.char_count} wrong count")


startGUI()


