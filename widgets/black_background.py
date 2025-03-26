import customtkinter as ctk
import pywinstyles
from typing import Callable

class BlackBackground(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=200, height=100, fg_color="transparent", bg_color="transparent", corner_radius=0)
        pywinstyles.set_opacity(self, 0.7)
        self.on_background_click = self.default_click
        self.bind("<Button-1>", lambda event: self.on_background_click())


    def default_click(self):
        """
        Default function if the click event wasn't connected
        """
        return


    def connect_background_click(self, function: Callable):
        """
        Connects the background click event to the given function
        """
        self.on_background_click = function
