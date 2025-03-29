import customtkinter as ctk
import tkinter as tk
from PIL import Image
from enum import Enum, auto


class Move(Enum):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()
    CLOCK = auto()
    COUNTERCLOCK = auto()


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
        self.width = int(frame_width/self.columns)
        self.height = int(frame_height/self.rows)
        self.tile_image.configure(size=(self.width, self.height))
        self.configure(width=self.width, height=self.height)
    

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
        if self in TileMover.selected_tiles:
            self.unselect_tile()
            return
        
        # Changes the opacity of the image
        self.original_tile_image.putalpha(100)
        self.tile_image.configure(light_image=self.original_tile_image)

        # Selects the tile and and switch tiles if two are selected
        TileMover.selected_tiles.append(self)

        if len(TileMover.selected_tiles) == 2:
            TileMover.switch_selected_tiles()


    def unselect_tile(self):
        """
        Unselect the already selected cell.
        """
        self.original_tile_image.putalpha(255)
        self.tile_image.configure(light_image=self.original_tile_image)

        TileMover.selected_tiles.remove(self)
    

class TileMover():
    """
    Seperated class to keep track of selection, switching, moving and rotating the tiles.
    """
    selected_tiles: list[Tile] = []

    @staticmethod
    def switch_selected_tiles():
        """
        Switches the two selected cells
        """
        cell_1 = TileMover.selected_tiles[0]
        cell_2 = TileMover.selected_tiles[1]

        cell_1.original_tile_image, cell_2.original_tile_image = cell_2.original_tile_image, cell_1.original_tile_image

        cell_1.tile_image.configure(light_image=cell_1.original_tile_image)
        cell_2.tile_image.configure(light_image=cell_2.original_tile_image)

        cell_1.unselect_tile()
        cell_2.unselect_tile()
    

    @staticmethod
    def move_tiles(tiles: list[Tile], direction: Move):
        """
        Moves all the tiles in a given direction.
        """
        vertical_movement = 0
        horizontal_movement = 0
        moved_tiles = []

        match direction:
            case Move.LEFT:
                horizontal_movement = 1
            case Move.RIGHT:
                horizontal_movement = -1
            case Move.UP:
                vertical_movement = 1
            case Move.DOWN:
                vertical_movement = -1
            case _:
                raise ValueError("Invalid direction given")

        for row in range(Tile.rows):
            row = (row + vertical_movement) % Tile.rows
            for col in range(Tile.columns):
                col = (col + horizontal_movement) % Tile.columns
                index = row * Tile.columns + col
                moved_tiles.append(tiles[index].original_tile_image)
        
        for i in range(len(moved_tiles)):
            tiles[i].original_tile_image = moved_tiles[i]
            tiles[i].tile_image.configure(light_image=tiles[i].original_tile_image)


    @staticmethod
    def rotate_tiles(tiles: list[Tile], rotation: Move):
        """
        Rotates all the tiles clockwise or counter-clockwise.
        """
        are_squared = (tiles[0].width == tiles[0].height)
        if Tile.columns != Tile.rows or not are_squared:
            degrees = 180
            col_iterator = range(Tile.columns -1, -1, -1)
            row_iterator = range(Tile.rows - 1, -1, -1)

        elif rotation == Move.CLOCK:
            degrees = -90
            col_iterator = range(Tile.columns)
            row_iterator = range(Tile.rows - 1, -1, -1)

        elif rotation == Move.COUNTERCLOCK:
            degrees = 90
            col_iterator = range(Tile.columns -1, -1, -1)
            row_iterator = range(Tile.rows)
        else:
            raise ValueError("Invalid Rotation given")


        rotated_tiles = []
        if degrees == 180:
            for row in row_iterator:
                for col in col_iterator:
                    index = row * Tile.columns + col
                    rotated_tiles.append(tiles[index].original_tile_image)
        else:
            for col in col_iterator:
                for row in row_iterator:
                    index = row * Tile.columns + col
                    rotated_tiles.append(tiles[index].original_tile_image)
        
        for i in range(len(rotated_tiles)):
            tiles[i].original_tile_image = rotated_tiles[i]
            tiles[i].rotate_cell(degrees)



