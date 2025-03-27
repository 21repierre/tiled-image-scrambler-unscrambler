import customtkinter as ctk
import tkinter as tk
from PIL import Image
from widgets.toast import Toast


class Tile(ctk.CTkLabel):
    """
    The class representing every tile after splitting the image.
    """
    rows = 0
    columns = 0

    def __init__(self, master: ctk.CTkFrame, width: int, height: int, tile_image: Image):
        """
        Creates the image and setup the label, binds the button to selection and rotation.
        """
        self.width = width
        self.height = height
        self.original_tile_image = tile_image
        self.tile_image = ctk.CTkImage(light_image=tile_image, size=(width, height))
        super().__init__(master, width, height, image=self.tile_image, corner_radius=0, text="")
        self.bind("<Button-1>", self.select_tile)
        self.bind("<Button-3>", self.on_right_click)
    

    def resize(self, frame_width: int, frame_height: int):
        """
        Resizes the cell depending on the frame.
        """
        self.tile_image.configure(size=(int(frame_width/self.columns), int(frame_height/self.rows)))
    

    def on_right_click(self, _: tk.Event):
        """
        Rotates the cell on right click.
        """
        if self.width == self.height:
            self.rotate_cell(-90)
        else:
            self.rotate_cell(180)
    

    def rotate_cell(self, degrees: int):
        """
        Rotates the cell by the amuont of degrees given.
        """        
        self.original_tile_image = self.original_tile_image.rotate(degrees)
        self.tile_image.configure(light_image=self.original_tile_image)
    

    def select_tile(self, _: tk.Event = None):
        """
        Selects the cell by making the image transparent and switching two cells if two are selected.
        """
        if self in TileSwitcher.selected_tiles:
            self.unselect_tile()
            return
        
        # Changes the opacity of the image
        self.original_tile_image.putalpha(100)
        self.tile_image.configure(light_image=self.original_tile_image)

        # Selects the tile and and switch tiles if two are selected
        TileSwitcher.selected_tiles.append(self)

        if len(TileSwitcher.selected_tiles) == 2:
            TileSwitcher.switch_selected_tiles()


    def unselect_tile(self):
        """
        Unselect the already selected cell.
        """
        self.original_tile_image.putalpha(255)
        self.tile_image.configure(light_image=self.original_tile_image)

        TileSwitcher.selected_tiles.remove(self)


class TileSwitcher():
    """
    Seperated class to keep track of selection and switching.
    """
    selected_tiles: list[Tile] = []

    @staticmethod
    def switch_selected_tiles():
        """
        Switches the two selected cells
        """
        cell_1 = TileSwitcher.selected_tiles[0]
        cell_2 = TileSwitcher.selected_tiles[1]

        cell_1.original_tile_image, cell_2.original_tile_image = cell_2.original_tile_image, cell_1.original_tile_image

        cell_1.tile_image.configure(light_image=cell_1.original_tile_image)
        cell_2.tile_image.configure(light_image=cell_2.original_tile_image)

        cell_1.unselect_tile()
        cell_2.unselect_tile()
