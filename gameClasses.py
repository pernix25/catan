from utils import *
import random
import pygame

HEIGHT = 640
WIDTH = 960
hex_size = 75

black = (0,0,0)
white = (255,255,255)

pygame.init()
board_font = pygame.font.SysFont(None, 30)

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
    def __init__(self, center, resource, number, vertices) -> None:
        self.center = center
        self.resource = resource
        self.number = number
        self.vertices = vertices
    
    def print_tile(self, window):
        pygame.draw.polygon(window, self.resource, self.vertices) # fill hexagon with white
        pygame.draw.polygon(window, black, self.vertices, 5) # outline hexagon with black

        if self.number != 0:
            # draw circle
                pygame.draw.circle(window, white, self.center, hex_size // 3)

                # draw number centered on circle
                text = board_font.render(str(self.number), True, black)
                text_rect = text.get_rect(center=self.center)
                window.blit(text, text_rect)

class Board:
    def __init__(self) -> None:
        self.reset()

    def reset(self, num_players=4) -> None:
        def find_hexagon_verticies(center, size, points) -> None:
            """Return the 6 vertices of a pointy-topped hexagon."""
            cx, cy = center
            verts = []
            for i in range(6):
                angle = math.radians(60 * i - 30)  # pointy-topped
                x = cx + size * math.cos(angle)
                y = cy + size * math.sin(angle)
                verts.append((x, y))

            points += verts
            return verts
        def find_hexagon_midpoints(points):
            vertices = self.vertices

            # Add midpoints of each side
            for i in range(6):
                x1, y1 = vertices[i]
                x2, y2 = vertices[(i+1) % 6]  # next vertex (wrap around)
                midpoint = ((x1 + x2)/2, (y1 + y2)/2)
                points.append(midpoint)

        self.centers = []
        self.structures = []
        self.tiles = []
        self.vertices = []
        self.midpoints = []
        resource_numbers = [11,3,6,5,4,9,10,8,4,11,12,9,10,8,3,6,2,5]
        resources_ratios = [4,4,3,3,4,1] # wood, wheat, brick, stone, sheep, desert
        tile_colors = [(10,105,14), (237,234,40),(201,69,28),(133,144,153),(71,222,76),(194, 178, 128)] # wood, wheat, brick, stone, sheep, desert

        # compute random tile list
        resource_list = []
        for color, count in zip(tile_colors, resources_ratios):
            resource_list += [color] * count
        random.shuffle(resource_list)

        # set up tiles
        if num_players <= 4:
            hex_centers = hexagon_grid((WIDTH//2, HEIGHT//2), hex_size, rings=2)
            self.centers = hex_centers
        for c in hex_centers:
            color = resource_list.pop()
            if color == (194, 178, 128):
                number = 0
            else:
                number = resource_numbers.pop()

            vertices = find_hexagon_verticies(c, hex_size, self.vertices)
            self.tiles.append(Tile(c, color, number, vertices))
            find_hexagon_midpoints(self.midpoints)

    def add_structure(self, structure):
        pass

    def clear_structures(self):
        self.structures = []

    def print_board(self, window):
        for tile in self.tiles:
            tile.print_tile(window)
        for structure in self.structures:
            structure.print(window)

def main():
    hex_centers = hexagon_grid((WIDTH//2, HEIGHT//2), hex_size, rings=2)
    print(hex_centers)

if __name__ == "__main__":
    main()