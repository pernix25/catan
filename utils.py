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

def draw_triangle(window, center, size, color, rotation=0) -> None:
    cx, cy = center
    points = []
    for i in range(3):
        angle = math.radians(120 * i + rotation)
        px = cx + size * math.cos(angle)
        py = cy + size * math.sin(angle)
        points.append((px, py))
    pygame.draw.polygon(window, color, points)

def draw_rotated_rectangle(window, center, angle_deg, color, width=10, height=75):
    """
    Returns the 4 corner points of a rotated rectangle.
    
    :param center: (x, y) center of the rectangle
    :param width: width of the rectangle
    :param height: height of the rectangle
    :param angle_deg: rotation angle in degrees (counterclockwise)
    :return: list of 4 (x, y) tuples for pygame.draw.polygon
    """
    cx, cy = center
    angle_rad = math.radians(angle_deg)

    # Half-dimensions
    w, h = width / 2, height / 2

    # Original corner positions (unrotated)
    corners = [
        (-w, -h),
        ( w, -h),
        ( w,  h),
        (-w,  h)
    ]

    rotated_points = []
    for x, y in corners:
        # Rotation matrix:
        # x' = x*cosθ - y*sinθ
        # y' = x*sinθ + y*cosθ
        xr = x * math.cos(angle_rad) - y * math.sin(angle_rad)
        yr = x * math.sin(angle_rad) + y * math.cos(angle_rad)
        rotated_points.append((cx + xr, cy + yr))

    pygame.draw.polygon(window, color, rotated_points)
    pygame.draw.polygon(window, (0,0,0), rotated_points, 3)

def draw_road(window, ):
    pass