import pygame
import sys

# Constants
WIDTH = 1300
HEIGHT = 800
DRY = (160, 82, 45)  # Dry dirt
WET = (101, 67, 33)  # Watered dirt
PLANTED = (0, 200, 0)  # Planted (green)
WATERED_PLANT = (0, 128, 0)  # Watered plant (brighter green)

# Game states
MENU = 0
GAME = 1
current_state = MENU

# Tabla
BORDER = pygame.Rect(60, 60, 160, HEIGHT - 100)
HOUSE = pygame.Rect(1095, 120, 190, 130)

GRID_START_X = 343
GRID_START_Y = 200
TILE_SIZE = 60
GRID_WIDTH = 5
GRID_HEIGHT = 9
INTERACTION_RANGE = 130 

tiles = [[{'watered': False, 'planted': False, 'watered_plant': False, 'watered_time': 0} for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Character settings
CHARACTER_WIDTH = 100
CHARACTER_HEIGHT = 90
MOVEMENT_SPEED = 5

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ECOCULTIVO")
clock = pygame.time.Clock()

# Load menu assets
menu_bg = pygame.image.load("assets/menu.png").convert()
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

play_button_img = pygame.image.load("assets/play_button.png").convert_alpha()
play_button_img = pygame.transform.scale(play_button_img, (200, 80))
play_button_rect = play_button_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Load game assets
game_bg = pygame.image.load("assets/background.png").convert()
game_bg = pygame.transform.scale(game_bg, (WIDTH, HEIGHT))

# Load character images
standing_img = pygame.image.load("assets/farmer.png").convert_alpha()
down_img = pygame.image.load("assets/farmer_down.png").convert_alpha()
regadera_img = pygame.image.load("assets/regadera.png").convert_alpha()
regadera_down_img = pygame.image.load("assets/regadera_down.png").convert_alpha()
regadera_down_surf = pygame.transform.scale(regadera_down_img, (CHARACTER_WIDTH - 5, CHARACTER_HEIGHT + 10))
standing_surf = pygame.transform.scale(standing_img, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
down_surf = pygame.transform.scale(down_img, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
regadera_surf = pygame.transform.scale(regadera_img, (CHARACTER_WIDTH - 5, CHARACTER_HEIGHT + 10))

# Character state
character_x = WIDTH // 2
character_y = HEIGHT // 2
current_character_surf = standing_surf
is_standing = True
regadera = False

def get_nearest_tile(char_x, char_y):
    min_dist = float('inf')
    nearest = None
    char_center_x = char_x + CHARACTER_WIDTH // 2
    char_center_y = char_y + CHARACTER_HEIGHT // 2
    
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            tile_center_x = GRID_START_X + (col + 0.5) * TILE_SIZE
            tile_center_y = GRID_START_Y + (row + 0.5) * TILE_SIZE
            dist = ((char_center_x - tile_center_x) ** 2 + (char_center_y - tile_center_y) ** 2) ** 0.5
            if dist < min_dist and dist <= INTERACTION_RANGE:
                min_dist = dist
                nearest = (col, row)
    
    return nearest

def draw_menu():
    # Draw the main menu background and play button.
    screen.blit(menu_bg, (0, 0))
    screen.blit(play_button_img, play_button_rect)

def draw_game():
    # Draw the game background and character.
    pygame.draw.rect(screen, (196, 160, 146), BORDER)
    pygame.draw.rect(screen, (0, 0, 0), HOUSE)
    screen.blit(game_bg, (0, 0))

    current_time = pygame.time.get_ticks()
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            rect = pygame.Rect(GRID_START_X + col * TILE_SIZE, GRID_START_Y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            tile = tiles[row][col]
            if tile['planted']:
                if tile['watered_plant'] and current_time - tile['watered_time'] < 30000:
                    color = WATERED_PLANT
                else:
                    color = PLANTED
                    tile['watered_plant'] = False
            elif tile['watered']:
                color = WET
            else:
                color = DRY
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2) 
    
    screen.blit(current_character_surf, (character_x, character_y))

def update_character_movement():
    # Handle continuous keyboard input for character movement and boundaries.
    global character_x, character_y
    keys = pygame.key.get_pressed()
    
    dx = 0
    dy = 0
    
    # Calculate intended movement
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        dy -= MOVEMENT_SPEED
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        dy += MOVEMENT_SPEED
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        dx -= MOVEMENT_SPEED
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        dx += MOVEMENT_SPEED
    
    # Attempt horizontal movement with collision check
    new_x = character_x + dx
    test_rect_x = pygame.Rect(new_x, character_y, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    if not test_rect_x.colliderect(HOUSE):
        character_x = new_x
    
    # Attempt vertical movement with collision check
    new_y = character_y + dy
    test_rect_y = pygame.Rect(character_x, new_y, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    if not test_rect_y.colliderect(HOUSE):
        character_y = new_y
    
    # Keep character within screen bounds
    character_x = max(BORDER.width + 30, min(character_x, WIDTH - CHARACTER_WIDTH))
    character_y = max(0, min(character_y, HEIGHT - CHARACTER_HEIGHT))

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and current_state == MENU:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(mouse_pos):
                    current_state = GAME
        
        elif event.type == pygame.KEYDOWN and current_state == GAME:
            if event.key == pygame.K_ESCAPE:
                current_state = MENU
            elif event.key == pygame.K_l:
                # Toggle between standing and down poses
                if regadera:  # If in regadera mode
                    if is_standing:
                        current_character_surf = regadera_down_surf  # Use regadera down sprite
                        is_standing = False
                    else:
                        current_character_surf = regadera_surf  # Keep regadera sprite
                        is_standing = True
                else:  # Regular mode
                    if is_standing:
                        current_character_surf = down_surf  # Use regular down sprite
                        is_standing = False
                    else:
                        current_character_surf = standing_surf  # Use regular standing sprite
                        is_standing = True
            elif event.key == pygame.K_r:
                if regadera:
                    current_character_surf = standing_surf
                    regadera = False
                else:
                    current_character_surf = regadera_surf
                    regadera = True
            elif event.key == pygame.K_SPACE and regadera:
                # Water the nearest tile if possible
                nearest = get_nearest_tile(character_x, character_y)
                if nearest:
                    col, row = nearest
                    tile = tiles[row][col]
                    if tile['planted']:
                        tile['watered_plant'] = True
                        tile['watered_time'] = pygame.time.get_ticks()
                    elif not tile['watered']:
                        tile['watered'] = True
            elif event.key == pygame.K_p and not regadera:
                # Plant on the nearest watered, unplanted tile if possible
                nearest = get_nearest_tile(character_x, character_y)
                if nearest:
                    col, row = nearest
                    if tiles[row][col]['watered'] and not tiles[row][col]['planted']:
                        tiles[row][col]['planted'] = True
    
    # Update game state (only for game mode)
    if current_state == GAME:
        update_character_movement()
    
    # Draw everything
    if current_state == MENU:
        draw_menu()
    elif current_state == GAME:
        draw_game()
    
    # Update display and cap FPS
    pygame.display.flip()
    clock.tick(60)

# Cleanup
pygame.quit()
sys.exit()