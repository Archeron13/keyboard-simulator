import tkinter
import tkinter.simpledialog
import tkinter.filedialog
import re
import os
import time
from threading import Thread
import customtkinter as ctk
from PIL import Image, ImageTk

WIDTH = 1280
HEIGHT = 720
DEFAULT_TEXT = "default files/default_input.txt"
DEFAULT_INDEX = 70

class BackGround(tkinter.Canvas):
    """Class for resizing background image """

    def __init__(self, master, *args):
        tkinter.Canvas.__init__(self, master, *args)

        self.img_bg = Image.open("default files/startBG.jpg")
        self.img_bg_copy = self.img_bg.copy()

        self.img_main = ImageTk.PhotoImage(self.img_bg)

        self.background = ctk.CTkLabel(self, image=self.img_main)
        self.background.pack(fill="both", expand=True)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self, event):
        """Function that resizes image when according to the event"""

        self.img_bg = self.img_bg_copy.resize((event.width, event.height))

        self.img_main = ImageTk.PhotoImage(self.img_bg)
        self.background.configure(image=self.img_main)