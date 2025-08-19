import pygame
from utils import *
import random

def main():
    pygame.init()
    HEIGHT = 640
    WIDTH = 960
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    board_font = pygame.font.SysFont(None, 30)
    BUFFER = 250

    #menu stuff
    menu_font = pygame.font.SysFont(None, 24)
    menu_buttons = [
        {"label": "Draw Triangle", "rect": pygame.Rect(10, HEIGHT-60, 120, 40), "action": "triangle"},
        {"label": "Clear", "rect": pygame.Rect(140, HEIGHT-60, 80, 40), "action": "clear"}
    ]

    # colors
    blue = (0,0,255)
    white = (255,255,255)
    black = (0,0,0)

    # world data
    hex_size = 75
    hex_centers = hexagon_grid((WIDTH//2, HEIGHT//2), hex_size, rings=2)
    resources_ratios = [4,4,3,3,4,1] # wood, wheat, brick, stone, sheep, desert
    tile_colors = [(10,105,14), (237,234,40),(201,69,28),(133,144,153),(71,222,76),(194, 178, 128)] # wood, wheat, brick, stone, sheep, desert
    resource_numbers = [11,3,6,5,4,9,10,8,4,11,12,9,10,8,3,6,2,5]

    # compute random tile list
    resource_list = []
    for color, count in zip(tile_colors, resources_ratios):
        resource_list += [color] * count
    random.shuffle(resource_list)

    # compute world bounds
    all_x = [c[0] for c in hex_centers]
    all_y = [c[1] for c in hex_centers]

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    world_width = (max_x - min_x) + hex_size * 2
    world_height = (max_y - min_y) + hex_size * 2

    # camera
    camera_x, camera_y = WIDTH//2, HEIGHT//2
    scroll_speed = 10

    # mouse drag state
    dragging = False
    last_mouse_pos = (0,0)

    # player structures
    triangles = []

    current_action = None
    clicked_on_menu = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            # preforms action on mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and current_action:
                mouse_pos = event.pos
                if current_action == "triangle":
                    world_x = mouse_pos[0] + camera_x - WIDTH//2
                    world_y = mouse_pos[1] + camera_y - HEIGHT//2
                    triangles.append((world_x, world_y, 30, (255, 0, 0)))  # size=30, red
                current_action = None

            # checks if menu is clicked if not drag screen around
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                clicked_on_menu = False
                for button in menu_buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        current_action = button["action"]
                        if current_action == "clear":
                            triangles.clear()
                            current_action = None
                        else:
                            clicked_on_menu = True
                        break
                
                # If click is NOT on a menu, start dragging or perform action
                if not clicked_on_menu:
                    dragging = True
                    last_mouse_pos = mouse_pos


            # mouse released
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False

            # mouse moved
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mx, my = event.pos
                    dx = mx - last_mouse_pos[0]
                    dy = my - last_mouse_pos[1]
                    camera_x -= dx   # subtract to "drag the world"
                    camera_y -= dy
                    last_mouse_pos = (mx, my)
        
        # keyboard movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            camera_x -= scroll_speed
        if keys[pygame.K_RIGHT]:
            camera_x += scroll_speed
        if keys[pygame.K_UP]:
            camera_y -= scroll_speed
        if keys[pygame.K_DOWN]:
            camera_y += scroll_speed

        # Clamp camera so you can't scroll too far
        camera_x = max(min(camera_x, max_x + BUFFER - WIDTH//2), min_x - BUFFER + WIDTH//2)
        camera_y = max(min(camera_y, max_y + BUFFER - HEIGHT//2), min_y - BUFFER + HEIGHT//2)

        # display blue background
        SCREEN.fill(blue) 

        desert_offset = False
        for i,c in enumerate(hex_centers):
            cx,cy = c
            draw_x = cx - camera_x + WIDTH//2
            draw_y = cy - camera_y + HEIGHT//2
            hexagon = hexagon_points((draw_x, draw_y), hex_size)
            pygame.draw.polygon(SCREEN, resource_list[i], hexagon) # fill hexagon with white
            pygame.draw.polygon(SCREEN, black, hexagon, 5) # outline hexagon with black

            if desert_offset:
                # draw circle
                pygame.draw.circle(SCREEN, white, (int(draw_x), int(draw_y)), hex_size // 3)

                # draw number centered on circle
                text = board_font.render(str(resource_numbers[i-1]), True, black)
                text_rect = text.get_rect(center=(draw_x, draw_y))
                SCREEN.blit(text, text_rect)
            elif resource_list[i] != (194, 178, 128):
                # draw circle
                pygame.draw.circle(SCREEN, white, (int(draw_x), int(draw_y)), hex_size // 3)

                # draw number centered on circle
                text = board_font.render(str(resource_numbers[i]), True, black)
                text_rect = text.get_rect(center=(draw_x, draw_y))
                SCREEN.blit(text, text_rect)
            else:
                desert_offset = True

        # draws menu
        for button in menu_buttons:
            pygame.draw.rect(SCREEN, (200, 200, 200), button["rect"])  # light gray background
            pygame.draw.rect(SCREEN, (0, 0, 0), button["rect"], 2)     # black border
            
            # Draw text centered
            text = menu_font.render(button["label"], True, (0, 0, 0))
            text_rect = text.get_rect(center=button["rect"].center)
            SCREEN.blit(text, text_rect)

        # draws all triangles
        for t in triangles:
            world_x, world_y, size, color = t
            draw_x = world_x - camera_x + WIDTH//2
            draw_y = world_y - camera_y + HEIGHT//2
            draw_triangle(SCREEN, (draw_x, draw_y), size, color)

        pygame.display.flip() # updates display
            
    
    pygame.quit()



if __name__ == "__main__":
    main()