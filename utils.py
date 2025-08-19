import math
import pygame
def hexagon_points(center, size) -> list[tuple]:
    x, y = center
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)  # shift so flat sides are left/right
        px = x + size * math.cos(angle)
        py = y + size * math.sin(angle)
        points.append((px, py))
    return points

def hexagon_grid(center, size, rings=2) -> list[tuple]:
    cx, cy = center
    centers = [(cx, cy)]  # start with center

    # axial directions for hex grids
    directions = [(1, 0), (0, 1), (-1, 1),
                  (-1, 0), (0, -1), (1, -1)]

    # step sizes in pixels
    dx = math.sqrt(3) * size
    dy = 1.5 * size

    for r in range(1, rings + 1):
        # Start r steps "up-left"
        q, s = 0, -r
        x = cx + (q * dx) + (s * dx/2)
        y = cy + (s * dy)
        # Walk around the ring
        for dir in directions:
            for _ in range(r):
                centers.append((x, y))
                q += dir[0]
                s += dir[1]
                x = cx + (q * dx) + (s * dx/2)
                y = cy + (s * dy)
    return centers

def draw_triangle(surface, center, size, color, rotation=0):
    cx, cy = center
    points = []
    for i in range(3):
        angle = math.radians(120 * i + rotation)
        px = cx + size * math.cos(angle)
        py = cy + size * math.sin(angle)
        points.append((px, py))
    pygame.draw.polygon(surface, color, points)