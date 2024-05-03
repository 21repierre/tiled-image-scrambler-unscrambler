from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


def select_file():
        filetypes = (
            ('PNG or JPG files', '.png'),
            ('PNG or JPG files', '.jpg')
        )

        filename = fd.askopenfilename(
            title='Open a PNG or JPG file',
            initialdir='./',
            filetypes=filetypes
        )

        showinfo(title="Selected file", message=filename)