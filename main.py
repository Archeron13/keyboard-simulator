import sys
import tkinter
from tkinter import filedialog
from tkinter.messagebox import YES
import customtkinter as ctk
from PIL import Image, ImageTk
import re
import time
from threading import Thread

WIDTH = 1280
HEIGHT = 720
DEFAULT_TEXT = ("default files/default_input.txt")



#Class for resizing background image
class background(tkinter.Canvas):
    def __init__(self, master, *pargs):
        tkinter.Canvas.__init__(self, master, *pargs)

        self.imgBG = Image.open("default files/startBG.jpg")
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

        self.last_index_of_list = 50 # End index of shown list

        with open(DEFAULT_TEXT) as f:             
            sentence = f.read()
            self.list_sentences = re.split(r'[ \n]',sentence)
            self.char_sentence = sentence.replace("\n"," ")

        self.text_var = self.char_sentence[:self.last_index_of_list]
        self.input_var = ""
        self.cur_key = ""
        self.game_running = False

       # self.mainTextLabel = ctk.CTkLabel(self.root,text = "Keyboard Simulator",text_font = ("Arial50,20"),fg_color=("white","grey"))
        # self.mainTextLabel.pack(pady="10",fill="x")

        #self.text_label = ctk.CTkLabel(self.root, text= "")

        self.showTextLabel = ctk.CTkLabel(self.root,text =self.text_var,text_font=("Arial50",15))
        self.showTextLabel.pack( padx=20, pady= 20,fill="both")

        self.input_label = ctk.CTkLabel(self.root,text="Press Start",text_color="Red",text_font=("Arial50,12"))
        self.input_label.pack(padx=20, pady= 20)

        self.inputTextLabel = ctk.CTkLabel(self.root,text =self.input_var,text_font=("Arial50","15"),text_color="black",fg_color=("white"))
        self.inputTextLabel.pack(padx=20, pady= 20,fill="both")

        self.result_label = ctk.CTkLabel(self.root,text=(f'Keystroke: 0\n'
                                                         f'Wrong Keystroke: 0\n'
                                                         f'Character Per Seconds : 0\n'
                                                         f'Character Per Minute: 0\n'
                                                         f'Accuracy: 0\n' )
                                                         ,text_font=("Arial50,15"))
        self.result_label.pack(side="right", padx=20, pady= 20,)

        self.button_frame = ctk.CTkFrame(self.root)
        self.button_frame.pack(side="left",padx=20,pady=20)

        self.start_button = ctk.CTkButton(self.button_frame, text="Start!", command=Thread(target=self.start_game).start,
                                         fg_color=("grey"),text_color="black",text_font=("Arial50,15"))
        self.start_button.pack(side = "top", padx=20, pady= 20)
        self.browse_button = ctk.CTkButton(self.button_frame,text = "Browse",fg_color=("grey"),text_color="black"
                                          ,text_font=("Arial50,15"),command = self.browse)
        self.browse_button.pack(side="top",padx= 20, pady=20)

        self.restart_button = ctk.CTkButton(self.button_frame, text="Restart",fg_color=("grey"),text_color="black"
                                            ,text_font=("Arial50,15"))
        self.restart_button.pack(side = "bottom",padx=20, pady= 20)



        #STatistics for game
        self.total_counter = 0
        self.correct_count = 0
        self.cur_state = ""
        self.cur_keycode = 0
        self.time_taken = 0
        self.root.mainloop()
    
    def browse(self):
        file = tkinter.filedialog.askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
        if file:
            sentence = file.read()
            self.list_sentences = re.split(r'[ \n]',sentence)
            self.char_sentence = sentence.replace("\n"," ")
            self.showTextLabel.config(text=self.char_sentence[:self.last_index_of_list])



    
    def key_press(self,event):
        self.cur_key = event.char
        self.cur_state= event.state
        self.cur_keycode = event.keycode
        self.total_counter += 1

    def start_game(self):
        self.root.bind("<KeyPress>",self.key_press)
        start_time = time.time()
        word_index = 0 #Used to see which word to remove that has already been iterated
        print(self.char_sentence)
        for cur_word in self.char_sentence:
            self.last_index_of_list += 1
            word_index += 1
            if (len(self.input_var) >= 60):
                for x in range(35,50):
                    print(x)
                    if self.input_var[x] == " ":
                        self.input_var= self.input_var[x:]
                        self.inputTextLabel.configure(text = self.input_var)
                        break
            if (cur_word== " "):
                self.input_label.configure(text = f'Space')
                if (self.last_index_of_list > len(self.char_sentence)):
                    self.last_index_of_list = len(self.char_sentence)
                self.showTextLabel.configure(text = self.char_sentence[word_index:self.last_index_of_list])
            else:
                self.input_label.configure(text = f'{cur_word} ')
            exit_loop = False
            if (exit_loop):
                break
            print(f"{cur_word} IS THE BUTTON TO PRESS DUMB FUCK")
            while True: 
                if (cur_word == self.cur_key):
                    self.correct_count += 1
                    self.input_var+=(cur_word)
                    self.inputTextLabel.configure(text =self.input_var)
                    break
                elif (self.cur_state == 4 and self.cur_keycode == 52 ):
                    exit_loop = False
                    break
                else:
                    pass
        self.time_taken = time.time() - start_time 
        self.result_label.configure(text=(f'Keystroke: {self.correct_count}\n'
                                          f'Wrong Keystroke: {self.total_counter - self.correct_count}\n'
                                          f'Character Per Seconds  {self.correct_count/self.time_taken:.2f}\n'
                                          f'Character Per Minute: {self.correct_count/self.time_taken * 60:.2f}\n'
                                          f'Accuracy: {self.correct_count/self.total_counter * 100:.2f}'))


startGUI()


