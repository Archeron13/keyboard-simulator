import tkinter
import tkinter.simpledialog
import tkinter.filedialog
import re
import os
import time
import numpy as np
from kbhmap import Heatmap
from threading import Thread
import customtkinter as ctk
from PIL import Image, ImageTk
from background import BackGround

WIDTH = 1280
HEIGHT = 720
DEFAULT_TEXT = "default files/default_input.txt"
DEFAULT_INDEX = 70


class StartGUI:
    """The GUI class for our keyboard simulator"""

    def __init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme('dark-blue')

        self.root = ctk.CTk()

        self.root.geometry(f'{WIDTH}x{HEIGHT}')
        self.root.title("Keyboard Simulator")

        self.bg_canvas = BackGround(self.root)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        with open(DEFAULT_TEXT) as file:
            sentence = file.read()
            self.list_sentences = re.split(r'[ \n]', sentence)
            self.char_sentence = sentence.replace("\n", " ")

        self.last_index_of_list = DEFAULT_INDEX   # End index of shown list
        self.text_var = self.char_sentence[:self.last_index_of_list]
        self.input_var = ""
        self.cur_key = ""
        self.game_running = False
        self.iterator = 0
        self.word_index = 0
        self.game_thread = 0
        self.not_saved = True
        self.change_save = False
        self.name = None
        self.exit_loop = False

        self.show_text_label = ctk.CTkLabel(self.root, text=self.text_var,
                                            text_font=("Arial50", 15))
        self.show_text_label.pack(padx=20, pady=20, fill="both")

        self.input_label = ctk.CTkLabel(self.root, text="Press Start", text_color="Green",
                                        text_font="Arial50,12")
        self.input_label.pack(padx=20, pady=20)

        self.input_text_label = ctk.CTkLabel(self.root, text=self.input_var,
                                             text_font=("Arial50", "15"),
                                             text_color="black", fg_color="white")
        self.input_text_label.pack(padx=20, pady=20, fill="both")

        self.result_label = ctk.CTkLabel(self.root, text=(f'Keystroke: 0\n'
                                                          f'Wrong Keystroke: 0\n'
                                                          f'Character Per Seconds : 0\n'
                                                          f'Character Per Minute: 0\n'
                                                          f'Accuracy: 0\n'), text_font="Arial50,15")
        self.result_label.pack(side="right", padx=20, pady=20, )

        self.button_frame = ctk.CTkFrame(self.root)
        self.button_frame.pack(side="left", padx=20, pady=20)

        self.start_button = ctk.CTkButton(self.button_frame, text="Start",
                                          command=self.start_game, fg_color='grey',
                                          text_color="black", text_font="Arial50,15")
        self.start_button.pack(side="top", padx=20, pady=20)

        self.stop_button = ctk.CTkButton(self.button_frame,text="End Game",
                                         command = self.end_game, fg_color="grey",
                                         text_color="black", text_font ="Arial50,15")
        self.stop_button.pack(side="top",padx=20,pady=20)

        self.browse_button = ctk.CTkButton(self.button_frame, text="Browse",
                                           fg_color="grey", text_color="black",
                                           text_font="Arial50,15", command=self.browse)
        self.browse_button.pack(side="top", padx=20, pady=20)

        self.restart_button = ctk.CTkButton(self.button_frame, text="Restart",
                                            fg_color="grey", text_color="black",
                                            text_font="Arial50,15", command=self.restart)
        self.restart_button.pack(side="top", padx=20, pady=20)

        self.exit_button = ctk.CTkButton(self.button_frame, text="Exit",
                                         fg_color="grey", text_color="black",
                                         text_font="Arial50,15", command=self.root.destroy)
        self.exit_button.pack(side="bottom", padx=20, pady=20)

        # Statistics for game
        self.total_counter = 0
        self.correct_count = 0
        self.cur_state = ""
        self.cur_keycode = 0
        self.time_taken = 0
        self.cur_word = 0
        self.root.mainloop()

    def start_game(self):
        """ Function that starts the thread on which keystroke detection is done"""
        if not self.game_running:
            self.name = tkinter.simpledialog.askstring(
                "Name", "Please enter your name!", parent=self.root)
            self.game_thread = Thread(target=self.start_game_thread)
            self.game_thread.start()
            self.game_running = True
        else:
            tkinter.messagebox.showerror("Error", "Game is already running!. \
                                            Press the restart button to restart the game")

    def end_game(self):
        if self.game_running:
            self.exit_loop = True
        else:
            tkinter.messagebox.showerror("Error", "Game is not running!. \
                                            Press the start button to start the game")


    def browse(self):
        """Function for browsing text file to play the game"""
        file = tkinter.filedialog.askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
        if file:
            sentence = file.read()
            self.list_sentences = re.split(r'[ \n]', sentence)
            self.char_sentence = sentence.replace("\n", " ")
            if self.game_running:
                self.restart()
            self.text_var = self.char_sentence[:self.last_index_of_list]
            self.show_text_label.configure(text=self.text_var)

    def restart(self):
        """Function for restarting the game"""
        if not self.game_running:
            tkinter.messagebox.showerror("Error", "Game is not running!. \
                                            Press the start button to start the game")
            return None

        # Resetting everything to their default state
        self.total_counter = 0
        self.correct_count = 0
        self.cur_state = ""
        self.cur_keycode = 0
        self.time_taken = 0
        self.last_index_of_list = DEFAULT_INDEX   # End index of shown list
        self.text_var = self.char_sentence[:self.last_index_of_list]
        self.show_text_label.configure(text=self.text_var)
        self.input_text_label.configure(text="")
        self.result_label.configure(text=(f'Keystroke: 0\n'
                                          f'Wrong Keystroke: 0\n'
                                          f'Character Per Seconds : 0\n'
                                          f'Character Per Minute: 0\n'
                                          f'Accuracy: 0\n'))
        self.input_var = ""
        self.cur_key = ""
        self.iterator = 0
        self.word_index = 0
        self.cur_word = self.char_sentence[0]
        self.input_label.configure(text=f'{self.cur_word}')
        self.change_save = True
        self.exit_loop = False
        return None

    def key_press(self, event):
        """Function for registering every keypress"""
        self.cur_key = event.char
        self.cur_state = event.state
        self.cur_keycode = event.keycode
        if (self.cur_word) != self.cur_key:
            with open("keystroke.txt","a") as file:
                file.write(self.cur_word)
        self.total_counter += 1

    def heatmap_window(self):
        heatmap = tkinter.PhotoImage(file = "temp.png")
        heatmap_label = ctk.CTkLabel(heatmap_window,image = heatmap)
        heatmap_label.pack()
        heatmap_window.mainloop()

    def start_game_thread(self):
        """Function which will be started as a thread for playing the game"""
        self.root.bind("<KeyPress>", self.key_press)
        start_time = time.time()
        self.show_text_label.configure(text=self.text_var)
        self.word_index = 0  # Used to see which word to remove that has already been iterated
        while True:
            while self.iterator < len(self.char_sentence) and not self.exit_loop:
                if self.change_save:
                    self.not_saved = True
                self.cur_word = self.char_sentence[self.iterator]
                self.last_index_of_list += 1
                self.word_index += 1
                if len(self.input_var) >= 60:  # To reset input_text_label if it gets too big
                    for x in range(35, 50):
                        if self.input_var[x] == " ":
                            self.input_var = self.input_var[x:]
                            self.input_text_label.configure(text=self.input_var)
                            break
                if self.cur_word == " ":
                    self.input_label.configure(text=f'Space')
                    if self.last_index_of_list > len(self.char_sentence):
                        self.last_index_of_list = len(self.char_sentence)
                    self.show_text_label.configure(
                        text=self.char_sentence[self.word_index:self.last_index_of_list])
                else:
                    self.input_label.configure(text=f'{self.cur_word} ')
                while True:
                    if not self.game_running or self.exit_loop:
                        break

                    if self.cur_word == self.cur_key:
                        self.correct_count += 1
                        self.input_var += self.cur_word
                        self.input_text_label.configure(text=self.input_var)
                        break


                self.iterator += 1
                self.time_taken = time.time() - start_time
            self.result_label.configure(text=(f'Keystroke: {self.total_counter}\n'
                                              f'Wrong Keystroke: {self.total_counter - self.correct_count}\n'
                                              f'Character Per Seconds  {self.correct_count / self.time_taken:.2f}\n'
                                              f'Character Per Minute: {self.correct_count / self.time_taken * 60:.2f}\n'
                                              f'Accuracy: {self.correct_count / self.total_counter * 100:.2f}'))
            save_score = False
            if self.not_saved:
                save_score = tkinter.messagebox.askyesno(
                    "Save score", "Would you like to save your score?")
                show_heatmap = tkinter.messagebox.askyesno(
                    "Save score", "Would you like to save the heatmap of your the letter you get wrong the most?")
                self.not_saved = False
            if save_score:
                save_score = False
                with open("score.txt", "a+") as file:
                    if os.stat("score.txt").st_size == 0:
                        # If file is empty writing the header
                        file.write("Name,CPM,Accuracy,Score")
                    file.write(f'\n{self.name},{self.correct_count / self.time_taken * 60:.2f}')
                    file.write(f',{self.correct_count / self.total_counter * 100:.2f}')
                    score = self.correct_count / self.total_counter * 100 * \
                            (self.correct_count / self.time_taken * 60)
                    file.write(f',{score:.2f}')
            if show_heatmap:
                show_heatmap = False
                HMQ = Heatmap('qwerty')
                char_dict = []
                with open("keystroke.txt","r") as chars:
                    unique,count = np.unique([char for char in chars.read()],return_counts=True)
                    char_dict = dict(zip(unique,count))
                HMQ.make_heatmap(char_dict,layout='qwerty',cmap='YlGnBu',sigmas=2)
                directory = tkinter.filedialog.askdirectory(initialdir="./")
                print(directory)
                save_name = self.name + str(time.time())
                HMQ.save(f'{save_name}.png',directory)
                tkinter.messagebox.showinfo(title="Heatmap",message = f'Heatmap {save_name} successfully saved in {directory}')


            if os.path.exists("keystroke.txt"):
                os.remove("keystroke.txt")
            #if os.path.exists("temp.png"):
             #   os.remove("temp.png")


