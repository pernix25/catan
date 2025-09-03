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
    
    def print_structure(self, window, camera_x, camera_y):
        cx,cy = self.pos
        draw_x = cx - camera_x + WIDTH//2
        draw_y = cy - camera_y + HEIGHT//2
        draw_triangle(window, (draw_x, draw_y), 30, self.color) # 30 = size

class City:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    def print_structure(self, window, camera_x, camera_y):
        cx,cy = self.pos
        draw_x = cx - camera_x + WIDTH//2
        draw_y = cy - camera_y + HEIGHT//2
        draw_triangle(window, (draw_x, draw_y), 30, self.color) # 30 = size

class Road:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    def print_structure(self, window, camera_x, camera_y):
        cx,cy = self.pos
        draw_x = cx - camera_x + WIDTH//2
        draw_y = cy - camera_y + HEIGHT//2
        draw_triangle(window, (draw_x, draw_y), 30, self.color) # 30 = size

class Tile:
    def __init__(self, center, resource, number, vertices) -> None:
        self.center = center
        self.resource = resource
        self.number = number
        self.vertices = vertices
    
    def print_tile(self, window, camera_x, camera_y):
        cx,cy = self.center
        draw_x = cx - camera_x + WIDTH//2
        draw_y = cy - camera_y + HEIGHT//2
        hexagon = hexagon_points((draw_x, draw_y), hex_size)
        pygame.draw.polygon(window, self.resource, hexagon) # fill hexagon with white
        pygame.draw.polygon(window, black, hexagon, 5) # outline hexagon with black

        if self.number != 0:
            # draw circle
                pygame.draw.circle(window, white, (int(draw_x), int(draw_y)), hex_size // 3)

                # draw number centered on circle
                text = board_font.render(str(self.number), True, black)
                text_rect = text.get_rect(center=(draw_x, draw_y))
                window.blit(text, text_rect)

class Board:
    def __init__(self) -> None:
        self.reset()

    def reset(self, num_players=4) -> None:
        def find_hexagon_verticies(center, size) -> None:
            """Return the 6 vertices of a pointy-topped hexagon."""
            cx, cy = center
            verts = []
            for i in range(6):
                angle = math.radians(60 * i - 30)  # pointy-topped
                x = cx + size * math.cos(angle)
                y = cy + size * math.sin(angle)
                verts.append((x, y))

            find_hexagon_midpoints(verts)
            self.vertices += verts
            return verts
        def find_hexagon_midpoints(verts):
            # Add midpoints of each side
            for i in range(6):
                x1, y1 = verts[i]
                x2, y2 = verts[(i+1) % 6]  # next vertex (wrap around)
                midpoint = ((x1 + x2)/2, (y1 + y2)/2)
                self.midpoints.append(midpoint)

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

            vertices = find_hexagon_verticies(c, hex_size)
            self.tiles.append(Tile(c, color, number, vertices))

    def add_structure(self, structure) -> None:
        self.structures.append(structure)

    def clear_structures(self):
        self.structures = []
    
    def find_closest_vert(self, point):
        nearest_vert = None
        min_distance = float("inf")
        px,py = point

        for vert in self.vertices:
            vx,vy = vert
            dist = ((px - vx)**2 + (py - vy)**2) ** 0.5  # Euclidean distance
            if dist < min_distance:
                min_distance = dist
                nearest_vert = (vx, vy)
        
        return nearest_vert
    
    def find_closest_midpoint(self, point):
        nearest_mid = None
        min_distance = float("inf")
        px,py = point

        for mid in self.midpoints:
            mx,my = mid
            dist = ((px - mx)**2 + (py - my)**2) ** 0.5  # Euclidean distance
            if dist < min_distance:
                min_distance = dist
                nearest_mid = (mx,my)
        
        return nearest_mid

    def print_board(self, window, camera_x, camera_y):
        for tile in self.tiles:
            tile.print_tile(window, camera_x, camera_y)
        for structure in self.structures:
            structure.print_structure(window, camera_x, camera_y)

def main():
    hex_centers = hexagon_grid((WIDTH//2, HEIGHT//2), hex_size, rings=2)
    print(hex_centers)

if __name__ == "__main__":
    main()