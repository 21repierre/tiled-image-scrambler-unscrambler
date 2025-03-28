import tkinter as tk
import customtkinter as ctk
from PIL import Image
import os
import shutil
import random
from widgets.top_menu import TopMenu
from widgets.split_window import SplitWindow
from widgets.scramble_window import ScrambleWindow
from widgets.black_background import BlackBackground
from widgets.tile import Tile
from widgets.toast import Toast
from tkinter import filedialog as fd
from split_image import split_image, reverse_split


class App(ctk.CTk):
    """
    The class containing the main app.
    """
    def __init__(self):
        super().__init__()

        # Sets the title and geometry, get the scaling of the window
        self.title('Tiled image scrambler/unscrambler')
        width, height = 1200, 800
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
        self.top_menu.scramble_button.configure(command=self.show_scramble_window)
        self.top_menu.save_button.configure(command=self.save_result)


        # Creates the frame that will contain the image
        self.image_ratio = 0
        self.image_frame = ctk.CTkFrame(self)
        self.image_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.image_frame.bind("<Configure>", self.on_frame_resize)

        # Empty label that will contain the starting image
        self.image_padding = 10

        self.tile_frame = ctk.CTkFrame(self.image_frame)
        self.tile_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.tiles: list[Tile] = []
        
        self.image_label = ctk.CTkLabel(self.image_frame, text="")
        self.image_label.pack(fill="both", expand=True, padx=self.image_padding, pady=self.image_padding)

        self.mainloop()


    def select_file(self):
        """
        Open the file explorer looking for a png or jpg file.
        """
        filetypes = [('PNG or JPG files', '.png'), ('PNG or JPG files', '.jpg'), ('PNG or JPG files', '.jpeg')]
        self.filepath = fd.askopenfilename(title='Open a PNG or JPG file', initialdir='./', filetypes=filetypes)

        # If an image was selected, we display the image
        if self.filepath != '':
            # If there's tiles, we have to remove them and recreate the image label on top of it
            if len(self.tiles):
                self.remove_tiles()
                self.top_menu.hide_save_button()
                self.image_label.destroy()
                self.image_label = ctk.CTkLabel(self.image_frame, text="")
                self.image_label.pack(fill="both", expand=True, padx=self.image_padding, pady=self.image_padding)

            # Creates the image from the path
            self.original_image = Image.open(self.filepath)
            self.image = ctk.CTkImage(light_image=self.original_image, size=self.original_image.size)

            # Get the ratio and configure the label to display it
            self.image_ratio = round(self.original_image.width / self.original_image.height, 5)
            self.image_label.configure(image=self.image)

            # Resize it properly and display the new available functions
            self.resize_image(self.image_frame.winfo_width(), self.image_frame.winfo_height())
            self.top_menu.show_split_selection()


    def resize_image(self, frame_width: int, frame_height: int):
        """
        Resizes the image or the button frame and keeping the ratio depending on the frame's size.
        """
        # Avoiding the resize of the image if we don't have an image yet
        if not self.image_ratio:
            return
                
        parent_frame_ratio = frame_width / frame_height

        # Calculates the new dimensions of the image/frame, using the image's ratio
        # depending on if the frame is wider or taller than the image
        if parent_frame_ratio > self.image_ratio:
            new_height = (frame_height / self.window_scaling) - (2 * self.image_padding)
            new_width = new_height * self.image_ratio
            new_height_no_scaling = frame_height - (2 * self.image_padding)
            new_width_no_scaling = new_height * self.image_ratio
        else:
            new_width = (frame_width / self.window_scaling) - (2 * self.image_padding)
            new_height = new_width / self.image_ratio
            new_width_no_scaling = frame_width - (2 * self.image_padding)
            new_height_no_scaling = new_width / self.image_ratio
        
        new_height = int(new_height)
        new_width = int(new_width)
        new_height_no_scaling = int(new_height_no_scaling)
        new_width_no_scaling = int(new_width_no_scaling)

        self.image.configure(size=(new_width, new_height))
        self.tile_frame.configure(width=new_width, height=new_height)

        if len(self.tiles):
            for tile in self.tiles:
                tile.resize(new_width, new_height)


    def on_frame_resize(self, event: tk.Event):
        """
        Triggers whenever the frame is resized.
        """
        self.resize_image(event.width, event.height)


    def show_split_window(self):
        """
        Shows the split window when the split button is clicked.
        """
        # Creates the black background
        self.black_background = BlackBackground(self)
        self.black_background.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.black_background.connect_background_click(self.hide_split_window)

        # Creates the split window and place it at the center
        self.split_window = SplitWindow(self)
        self.split_window.place(relx=0.5, rely=0.5, relwidth=0.25, relheight=0.5, anchor="center")
        self.split_window.connect_start_split(self.on_split_image)
        self.is_scrambling = False
    

    def show_scramble_window(self):
        """
        Shows the scramble window when the scramble button is clicked.
        """
        # Creates the black background
        self.black_background = BlackBackground(self)
        self.black_background.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.black_background.connect_background_click(self.hide_scramble_window)

        # Creates the split window and place it at the center
        self.scramble_window = ScrambleWindow(self)
        self.scramble_window.place(relx=0.5, rely=0.5, relwidth=0.25, relheight=0.5, anchor="center")
        self.scramble_window.connect_start_scramble(self.on_scramble_image)
        self.is_scrambling = True
    

    def hide_split_window(self):
        """
        Hides the split window.
        """
        self.black_background.place_forget()
        self.split_window.place_forget()
    

    def hide_scramble_window(self):
        """
        Hides the scramble window.
        """
        self.black_background.place_forget()
        self.scramble_window.place_forget()
    

    def on_split_image(self, rows: int, columns: int):
        """
        Split the image.
        """
        if self.is_scrambling:
            self.hide_scramble_window()
        else:
            self.hide_split_window()
        self.top_menu.show_save_button()

        # Removes all tiles if necessary
        if len(self.tiles):
            self.remove_tiles()

        # Empty the "tiles" folder and make sure it exists
        directory = "tiles"
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)

        # Splits the image
        split_image(image_path=self.filepath, rows=rows, cols=columns, should_square=False, should_cleanup=False, should_quiet=True, output_dir=directory)

        # Remove the image and configure the grid to place the tiles
        self.image_label.pack_forget()
        self.tile_frame.grid_rowconfigure(list(range(rows)), weight=1, uniform="image-frame")
        self.tile_frame.grid_columnconfigure(list(range(columns)), weight=1, uniform="image-frame")

        # Get the file name and the extension
        filename = self.filepath.split("/")[-1]
        file = "".join(filename.split(".")[:-1])
        extension = filename.split(".")[-1]

        # Sets the rows and columns for the Tile class
        Tile.rows = rows
        Tile.columns = columns

        # Creates the tiles
        image_size = self.image._size
        tile_size = (int(image_size[0] / columns), int(image_size[1] / rows))

        for row in range(rows):
            for col in range(columns):
                path = f"{directory}/{file}_{row * columns + col}.{extension}"
                tile_image = Image.open(path).convert("RGBA")
                tile = Tile(self.tile_frame, width=tile_size[0], height=tile_size[1], tile_image=tile_image)
                tile.grid(row=row, column=col, sticky="nsew", padx=0, pady=0, ipadx=0, ipady=0)
                self.tiles.append(tile)
    

    def remove_tiles(self):
        """
        Removes all existing tiles.
        """
        self.tiles = []
        self.tile_frame.destroy()
        self.tile_frame = ctk.CTkFrame(self.image_frame)
        self.tile_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.resize_image(self.image_frame.winfo_width(), self.image_frame.winfo_height())
    

    def save_result(self):
        """
        Saves the result of the splitting.
        """
        # Empty the "tiles" folder and make sure it exists
        directory = "tiles"
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)

        # Extracts the original filename and extension to create the modified path
        original_filename = self.filepath.split("/")[-1]
        filename = "".join(original_filename.split(".")[:-1])
        extension = original_filename.split(".")[-1]
        path = "/".join(self.filepath.split("/")[:-1])
        image_path = f"{path}/{filename}_modified.{extension}"
        path_list = []

        # For each tile, we save the image with the associated index
        for row in range(Tile.rows):
            for col in range(Tile.columns):
                index = row * Tile.columns + col
                tile_path = f"{directory}/tile_{index}.{extension}"
                path_list.append(tile_path)

                # Saves the tile in the "tiles" directory
                current_tile = self.tiles[index]
                if extension == "png":
                    current_tile.original_tile_image.save(tile_path)
                else:
                    current_tile.original_tile_image.convert("RGB").save(tile_path, "JPEG")
        
        # Reverse split to get the result
        reverse_split(paths_to_merge=path_list, rows=Tile.rows, cols=Tile.columns, image_path=image_path, should_cleanup=True, should_quiet=True)
        Toast(self, title="Result saved", message="The result was saved in the image's original directory")
    

    def on_scramble_image(self, rows: int, columns: int, add_rotation: bool):
        """
        Scrambles the image by making random permutation on the tiles and random rotations.
        """
        # Splits the image first
        self.on_split_image(rows=rows, columns=columns)

        # In average, permutes 2 times each tiles
        for i in range(rows * columns * 2):
            tile_1, tile_2 = random.sample(range(rows * columns), 2)
            self.tiles[tile_1].select_tile()
            self.tiles[tile_2].select_tile()
        
        # Stop there if we don't want rotation
        if not add_rotation:
            return
        
        # Rotates each tiles by a random amount of degrees depending on if they're squared or not
        are_squared = (self.tiles[0].width == self.tiles[0].height)
        for i in range(rows * columns):
            if are_squared:
                rotation = random.randint(0, 3) * 90
            else:
                rotation = random.randint(0, 1) * 180
            self.tiles[i].rotate_cell(rotation)


if __name__ == '__main__':
    App()