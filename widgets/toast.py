import customtkinter as ctk
import pywinstyles

class Toast(ctk.CTkToplevel):
    """
    Creates a toast notification at the top of your screen.
    """
    def __init__(
            self, 
            parent: ctk.CTk, 
            title: str = "", 
            font_title: tuple = ("Inter", 14, "bold"), 
            message: str = "", 
            font_message: tuple = ("Inter", 12, "bold"), 
            duration: int = 3000
        ):
        """
        Creates the toast, then fade it in and out.
        """
        super().__init__(parent, fg_color="#495057")

        # Size of the toast
        width, height = 200, 100
        self.window_scaling = self._get_window_scaling()

        # Creates the position where it will appear
        screen_width = int(self.winfo_screenwidth() * self.window_scaling)
        pos_x = parent.winfo_width() + parent.winfo_x() - width - 20
        pos_y = parent.winfo_y() + 60

        # Sets the geometry and remove the window's border
        self.geometry(f'{width}x{height}+{pos_x}+{pos_y}')
        self.overrideredirect(True)
        
        # Initialize the opacity
        self.duration = duration
        self.current_opacity = 0
        pywinstyles.set_opacity(self, self.current_opacity)

        self.title = ctk.CTkLabel(self, text=title, font=font_title, wraplength=width, justify="left")
        self.title.pack(expand=True, fill="both", padx=3, pady=3)

        self.message = ctk.CTkLabel(self, text=message, font=font_message, wraplength=width, justify="left")
        self.message.pack(expand=True, fill="both", padx=3, pady=3)

        self.fade_in()

    
    def fade_in(self):
        """
        Fade the toast in by recursively calling the function.
        Once the opacity is 1, we wait for the duration and fade out.
        """
        if self.current_opacity == 1:
            self.after(self.duration, self.fade_out)
            return

        self.current_opacity = round(self.current_opacity + 0.1, 2)
        pywinstyles.set_opacity(self, self.current_opacity)
        self.after(20, self.fade_in)
    

    def fade_out(self):
        """
        Fade the toast out by recursively calling the function.
        Once the opacity is 0, we destroy the toast.
        """
        if self.current_opacity == 0:
            self.destroy()
            return

        self.current_opacity = round(self.current_opacity - 0.1, 2)
        pywinstyles.set_opacity(self, self.current_opacity)
        self.after(10, self.fade_out)
