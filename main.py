import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo, showerror
from tkinter import filedialog as fd


class InputWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Input Integers")
        self.geometry("300x150")
        
        self.label1 = tk.Label(self, text="Enter first integer:")
        self.label1.pack(pady=5)
        self.entry1 = tk.Entry(self)
        self.entry1.pack(pady=5)
        
        self.label2 = tk.Label(self, text="Enter second integer:")
        self.label2.pack(pady=5)
        self.entry2 = tk.Entry(self)
        self.entry2.pack(pady=5)
        
        self.submit_button = tk.Button(self, text="Submit", command=self.validate_input)
        self.submit_button.pack(pady=10)
        
    def validate_input(self):
        try:
            first_int = int(self.entry1.get())
            second_int = int(self.entry2.get())
            showinfo("Success", f"First integer: {first_int}\nSecond integer: {second_int}")
            self.destroy()
        except ValueError:
            showerror("Error", "Please enter valid integers.")


class UploadButton(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.container = container
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
            self.container.get_tiled_image(self.filepath)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tiled image scrambler/unscrambler')
        width, height = 600, 400
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f'{width}x{height}+{int(screen_width/2 - width/2)}+{int(screen_height/2 - height/2)}')

        self.upload_button = UploadButton(self)
        self.upload_button.pack()

        self.image_label = ttk.Label(self, padding=5)
        self.image_label.pack()

    def get_tiled_image(self, filepath):
        self.input_box = InputWindow(self)

    def display_image(self, filepath):
        self.image = ImageTk.PhotoImage(Image.open(filepath))
        self.image_label.configure(image=self.image)



if __name__ == '__main__':
    app = App()
    app.mainloop()