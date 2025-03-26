import customtkinter as ctk
from settings import *

class TopMenu(ctk.CTkFrame):
    """
    Top Menu of the app containing the buttons to upload, save and split the image.
    """
    def __init__(self, master):
        """
        Creates the widgets and configure the grid.
        """
        super().__init__(master=master)

        self.master = master
        self.grid_rowconfigure(0, weight=1, uniform="topmenu")
        self.grid_columnconfigure([0, 1, 2, 3, 4, 5, 6], weight=1, uniform="topmenu")

        # Upload button to get the image
        self.upload_button = ctk.CTkButton(self, text='Upload', font=FONT)
        self.upload_button.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        # Save button to save the result
        self.save_button = ctk.CTkButton(self, text='Save', font=FONT)

        # Buttons to scramble and split the image
        self.scramble_button = ctk.CTkButton(self, text='Scramble', font=FONT)
        self.split_button = ctk.CTkButton(self, text='Split', font=FONT)


    def show_split_selection(self):
        """
        Shows the button to choose how you want to split your image.
        """
        self.scramble_button.grid(row=0, column=5, padx=10, pady=10, sticky="ns")
        self.split_button.grid(row=0, column=6, padx=10, pady=10, sticky="ns")


    def show_save_button(self):
        """
        Shows the save button once you've splitted the image.
        """
        self.save_button.grid(row=0, column=1, padx=10, pady=10, sticky="ns")