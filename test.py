import customtkinter as ctk

def show_invisible_label():
    # Invisible frame
    global root
    frame = ctk.CTkFrame(root, width=200, height=100, fg_color="transparent")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Example child widget (still visible)
    label = ctk.CTkLabel(frame, text="I am inside an invisible frame")
    label.pack()


root = ctk.CTk()
root.geometry("400x300")

button = ctk.CTkButton(root, text="My cool button", command=show_invisible_label)
button.pack()


root.mainloop()
