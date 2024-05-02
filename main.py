import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo


class UploadButton(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        upload_icon = tk.PhotoImage(file="./assets/upload_image.png")
        ttk.Button(self, image=upload_icon, text="Upload", compound=tk.LEFT, command=lambda: showinfo(title="Hello", message="Upload")).pack(expand=True)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tiled image scrambler/unscrambler")
        width, height = 600, 400
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{width}x{height}+{int(screen_width/2 - width/2)}+{int(screen_height/2 - height/2)}")

        upload_button = UploadButton(self)
        upload_button.pack()




if __name__ == "__main__":
    app = App()
    app.mainloop()