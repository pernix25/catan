import pygame
from utils import *
from gameClasses import *

def main():
    pygame.init()
    HEIGHT = 640
    WIDTH = 960
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    HEX_SIZE = 75
    BUFFER = 250

    board = Board()

    # colors
    blue = (0,0,255)
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)

    menu_font = pygame.font.SysFont(None, 24)
    menu_buttons = [
        {"label": "Draw Triangle", "rect": pygame.Rect(10, HEIGHT-60, 120, 40), "action": "triangle"},
        {"label": "Clear", "rect": pygame.Rect(140, HEIGHT-60, 80, 40), "action": "clear"}
    ]

    # camera
    camera_x, camera_y = WIDTH//2, HEIGHT//2

    # compute world bounds
    all_x = [c[0] for c in board.centers]
    all_y = [c[1] for c in board.centers]

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    dragging = False
    last_mouse_pos = (WIDTH//2, HEIGHT//2)
    current_action = None

    running =True
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
                    nearest_vert = board.find_closest_vert((world_x, world_y))
                    board.add_structure(Settlement(nearest_vert, red))
                current_action = None

            # checks if menu is clicked if not drag screen around
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                clicked_on_menu = False
                for button in menu_buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        current_action = button["action"]
                        if current_action == "clear":
                            board.clear_structures()
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

        # Clamp camera so you can't scroll too far
        camera_x = max(min(camera_x, max_x + BUFFER - WIDTH//2), min_x - BUFFER + WIDTH//2)
        camera_y = max(min(camera_y, max_y + BUFFER - HEIGHT//2), min_y - BUFFER + HEIGHT//2)

        # display blue background
        SCREEN.fill(blue)

        # draws the board
        board.print_board(SCREEN, camera_x, camera_y)

        # draws menu
        for button in menu_buttons:
            pygame.draw.rect(SCREEN, (200, 200, 200), button["rect"])  # light gray background
            pygame.draw.rect(SCREEN, black, button["rect"], 2)     # black border
            
            # Draw text centered
            text = menu_font.render(button["label"], True, black)
            text_rect = text.get_rect(center=button["rect"].center)
            SCREEN.blit(text, text_rect)
    
        pygame.display.flip() # updates display

if __name__ == "__main__":
    main()