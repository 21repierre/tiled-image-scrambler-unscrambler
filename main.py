import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from widgets.top_menu import TopMenu
from widgets.split_window import SplitWindow
from tkinter import filedialog as fd
import pywinstyles


class BlackBackground(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=200, height=100, fg_color="transparent", bg_color="transparent", corner_radius=0)
        pywinstyles.set_opacity(self, 0.7)


class App(ctk.CTk):
    """
    The class containing the main app.
    """
    def __init__(self):
        super().__init__()

        # Sets the title and geometry, get the scaling of the window
        self.title('Tiled image scrambler/unscrambler')
        width, height = 600, 400
        self.window_scaling = self._get_window_scaling()

        # Calculates the positions depending on the windows' size and scaling
        screen_width = self.winfo_screenwidth() 
        screen_height = self.winfo_screenheight()

        pos_x = int((screen_width/2 - width/2) * self.window_scaling)
        pos_y = int((screen_height/2 - height/2) * self.window_scaling)

        self.geometry(f'{width}x{height}+{pos_x}+{pos_y}')

        # Creates the top menu and linking the upload button to the file selection
        self.top_menu = TopMenu(self)
        self.top_menu.pack(padx=10, pady=10, fill="x")
        self.top_menu.upload_button.configure(command=self.select_file)
        self.top_menu.split_button.configure(command=self.show_split_window)


        # Creates the frame that will contain the image
        self.image_ratio = 0
        self.image_frame = ctk.CTkFrame(self)
        self.image_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.image_frame.bind("<Configure>", self.on_window_resize)

        # Empty label that will contain the starting image
        self.image_padding = 10
        self.image_label = ctk.CTkLabel(self.image_frame, text="")
        self.image_label.pack(fill="both", expand=True, padx=self.image_padding, pady=self.image_padding)

        self.mainloop()


    def select_file(self):
        """
        Open the file explorer looking for a png or jpg file.
        """
        filetypes = [
            ('PNG or JPG files', '.png'),
            ('PNG or JPG files', '.jpg')
        ]

        self.filepath = fd.askopenfilename(
            title='Open a PNG or JPG file',
            initialdir='./',
            filetypes=filetypes
        )

        # If an image was selected, we display the image
        if self.filepath != '':
            self.original_image = Image.open(self.filepath)
            self.image = ctk.CTkImage(light_image=self.original_image, size=self.original_image.size)
            self.image_ratio = self.original_image.width / self.original_image.height
            self.image_label.configure(image=self.image)
            self.resize_image(self.image_frame.winfo_width(), self.image_frame.winfo_height())
            self.top_menu.show_split_selection()
        
    
    def resize_image(self, frame_width: int, frame_height: int):
        """
        Resizes the image and keeping the ratio depending on the frame's size.
        """
        # Avoiding the resize of the image if we don't have an image yet
        if not self.image_ratio:
            return
        
        frame_ratio = frame_width / frame_height

        # Calculates the new dimensions of the image, using the image's ratio
        # depending on if the frame is wider or taller than the image
        if frame_ratio > self.image_ratio:
            new_height = frame_height
            new_width = int(new_height * self.image_ratio)
        else:
            new_width = frame_width
            new_height = int(new_width / self.image_ratio)
        
        # Taking consideration of the scaling and padding
        new_width = int(new_width / self.window_scaling) - (2 * self.image_padding)
        new_height = int(new_height / self.window_scaling) - (2 * self.image_padding)
        self.image.configure(size=(new_width, new_height))


    def on_window_resize(self, event: tk.Event):
        """
        Triggers whenever the window is resized.
        """
        self.resize_image(event.width, event.height)
    

    def show_split_window(self):
        """
        Shows the split window when the split button is clicked.
        """
        self.black_background = BlackBackground(self)
        self.black_background.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.split_window = SplitWindow(self)
        self.split_window.place(relx=0.5, rely=0.5, anchor="center")


if __name__ == '__main__':
    App()