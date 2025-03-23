import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo, showerror


class InputWindow(tk.Frame):
    """
    Window asking the grid size for spliting the image.
    """
    def __init__(self, master):
        super().__init__(master)

        # Labels and entries to ask the dimensions
        self.label1 = tk.Label(self, text="Enter first integer:")
        self.label1.pack(pady=5)
        self.entry1 = tk.Entry(self)
        self.entry1.pack(pady=5)
        
        self.label2 = tk.Label(self, text="Enter second integer:")
        self.label2.pack(pady=5)
        self.entry2 = tk.Entry(self)
        self.entry2.pack(pady=5)
        
        # Submit button linked to the validation
        self.submit_button = tk.Button(self, text="Submit", command=self.validate_input)
        self.submit_button.pack(pady=10)
        

    def validate_input(self):
        """
        Get the two entries and verify that they're integers.
        """
        try:
            first_int = int(self.entry1.get())
            second_int = int(self.entry2.get())
            showinfo("Success", f"First integer: {first_int}\nSecond integer: {second_int}")
            self.destroy()
        except ValueError:
            showerror("Error", "Please enter valid integers.")
