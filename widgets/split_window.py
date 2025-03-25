import customtkinter as ctk
from settings import *

class SplitWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=200, height=100, corner_radius=10, bg_color="transparent")
        self.button = ctk.CTkButton(self, text="Button")
        self.button.place(relx=0.5, rely=0.5, anchor="center")