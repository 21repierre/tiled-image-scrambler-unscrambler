import customtkinter as ctk
from typing import Callable
from settings import *
from widgets.toast import Toast

class ScrambleWindow(ctk.CTkFrame):
    """
    The window that appears when using the scramble functionnalities.
    Allows you to set the settings of the scramble and start it.
    """
    def __init__(self, master):
        """
        Creates the title with the labels and entry fields to start the scramble.
        """
        super().__init__(master, width=400, height=600, corner_radius=0, bg_color="transparent")
        self.title = ctk.CTkLabel(self, text="Scramble Settings:", font=FONT_BIG)
        self.title.pack(expand=True, fill="both", padx=10, pady=20)

        # Label and entry for the rows
        self.label_rows = ctk.CTkLabel(self, text='Rows:', font=FONT)
        self.label_rows.pack(expand=True, fill="both", padx=10)

        self.input_rows = ctk.CTkEntry(self, font=FONT, corner_radius=10)
        self.input_rows.pack(expand=True, fill="both", padx=10, pady=10)
    
        # Label and entry for the columns
        self.label_columns = ctk.CTkLabel(self, text='Columns:', font=FONT)
        self.label_columns.pack(expand=True, fill="both", padx=10)

        self.input_columns = ctk.CTkEntry(self, font=FONT, corner_radius=10)
        self.input_columns.pack(expand=True, fill="both", padx=10, pady=10)

        # Button to decide if we want to add rotations
        self.add_rotations = ctk.BooleanVar(value=False)
        self.rotation_button = ctk.CTkSwitch(self, text="Add rotations", variable=self.add_rotations, font=FONT)
        self.rotation_button.pack(expand=True, fill="both", padx=10, pady=10)

        # Button to split the image
        self.scramble_button = ctk.CTkButton(self, text='Scramble', font=FONT, command=self.verify_scramble_inputs)
        self.scramble_button.pack(expand=True, fill="both", padx=10, pady=10)

        self.start_scramble = self.default_start
    

    def verify_scramble_inputs(self):
        """
        Verifies that the input are positive integers and launch the scramble with it.
        """
        rows = self.input_rows.get()
        columns = self.input_columns.get()

        if not rows.isdigit() or not columns.isdigit():
            Toast(
                parent=self.master,
                title="Invalid settings", 
                message="Rows and columns have to be positive integers", 
            )
            return
        
        self.start_scramble(int(rows), int(columns), self.add_rotations.get())


    def default_start(self, *args, **kwargs):
        """
        Default function to not generate an error if the start_scramble function is not connected.
        """
        print("Start scramble is not connected to any function.")
    

    def connect_start_scramble(self, function: Callable):
        """
        Connects the start_scramble function to the one given in argument.
        """
        self.start_scramble = function