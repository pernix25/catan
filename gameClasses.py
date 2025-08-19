from utils import *

HEIGHT = 640
WIDTH = 960
hex_size = 75

class Settlement:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

class City:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

class Road:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

class Tile:
    def __init__(self, center, vertices, midpoints, number):
        self.center = center
        self.vertices = vertices
        self.midpoints = midpoints
        self.number = number

class Board:
    def __init__(self) -> None:
        self.reset()

    def reset(self, num_players=4, ) -> None:
        self.structures = []

        # set up tiles
        hex_centers = hexagon_grid((WIDTH//2, HEIGHT//2), hex_size, rings=2)

    def show_board(self, window):
        pass