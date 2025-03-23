import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog as fd


class UploadButton(ctk.CTkFrame):
    """
    A button to upload the image you want to split.
    """
    def __init__(self, container):
        super().__init__(container)

        # Defines the container of the frame and get the upload logo
        self.container = container
        self.upload_icon = ImageTk.PhotoImage(Image.open('./assets/upload_image_small.jpg'))
        self.filepath = ''

        # Creates the button itself, linked to the file selection
        upload_button = ctk.CTkButton(
            self, 
            image=self.upload_icon, 
            text='Upload', 
            compound=tk.LEFT, 
            command=self.select_file
        )
        upload_button.pack(expand=True)


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

        if self.filepath != '':
            self.container.get_tiled_image(self.filepath)

