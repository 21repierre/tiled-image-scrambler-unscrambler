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
        self.grid_columnconfigure([0, 1, 8, 9], weight=2, uniform="topmenu")
        self.grid_columnconfigure([2, 3, 4, 5, 6, 7], weight=1, uniform="topmenu")

        # Upload button to get the image
        self.upload_button = ctk.CTkButton(self, text='Upload', font=FONT)
        self.upload_button.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        # Save button to save the result
        self.save_button = ctk.CTkButton(self, text='Save', font=FONT)

        # Buttons to scramble and split the image
        self.scramble_button = ctk.CTkButton(self, text='Scramble', font=FONT)
        self.split_button = ctk.CTkButton(self, text='Split', font=FONT)

        # Buttons to move and rotate the image
        self.up_button = ctk.CTkButton(self, width=40, height=40, text='⭡', font=FONT_BIG)
        self.down_button = ctk.CTkButton(self, width=40, height=40, text='⭣', font=FONT_BIG)
        self.left_button = ctk.CTkButton(self, width=40, height=40, text='⭠', font=FONT_BIG)
        self.right_button = ctk.CTkButton(self, width=40, height=40, text='⭢', font=FONT_BIG)
        self.clock_button = ctk.CTkButton(self, width=40, height=40, text='⭮', font=FONT_BIG)
        self.counterclock_button = ctk.CTkButton(self, width=40, height=40, text='⭯', font=FONT_BIG)


    def show_split_selection(self):
        """
        Shows the button to choose how you want to split your image.
        """
        self.scramble_button.grid(row=0, column=8, padx=10, pady=10, sticky="ns")
        self.split_button.grid(row=0, column=9, padx=10, pady=10, sticky="ns")


    def show_tool_buttons(self):
        """
        Shows the tool buttons once you've splitted the image.
        """
        self.save_button.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
        self.up_button.grid(row=0, column=2, padx=10, pady=10)
        self.down_button.grid(row=0, column=3, padx=10, pady=10)
        self.left_button.grid(row=0, column=4, padx=10, pady=10)
        self.right_button.grid(row=0, column=5, padx=10, pady=10)
        self.clock_button.grid(row=0, column=6, padx=10, pady=10)
        self.counterclock_button.grid(row=0, column=7, padx=10, pady=10)
    

    def hide_tool_buttons(self):
        """
        hides the tool buttons when uploading a new image.
        """
        self.save_button.grid_forget()
        self.up_button.grid_forget()
        self.down_button.grid_forget()
        self.left_button.grid_forget()
        self.right_button.grid_forget()
        self.clock_button.grid_forget()
        self.counterclock_button.grid_forget()
