import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd

class UploadButton(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.upload_icon = ImageTk.PhotoImage(Image.open('./assets/upload_image_small.jpg'))
        self.filepath = ''

        upload_button = ttk.Button(
            self, 
            image=self.upload_icon, 
            text='Upload', 
            compound=tk.LEFT, 
            command=self.select_file
        )
        upload_button.pack(expand=True)


    def select_file(self):
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
            self.print_file()


    def print_file(self):
        print(self.filepath)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tiled image scrambler/unscrambler')
        width, height = 600, 400
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f'{width}x{height}+{int(screen_width/2 - width/2)}+{int(screen_height/2 - height/2)}')

        upload_button = UploadButton(self)
        upload_button.pack()


if __name__ == '__main__':
    app = App()
    app.mainloop()