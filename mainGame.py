import pygame
import sys
import random

# Constants
WIDTH = 1300
HEIGHT = 800
DRY = (160, 82, 45)  # Dry dirt
WET = (101, 67, 33)  # Watered dirt
PLANTED = (0, 200, 0)  # Planted (green)
WATERED_PLANT = (0, 128, 0)  # Watered plant (brighter green)
HARVEST_READY = (255, 215, 0)  # Gold for harvest-ready

# Game states
MENU = 0
GAME = 1
MAP = 2
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

tiles = [[{'watered': False, 'planted': False, 'watered_plant': False, 'watered_time': 0, 'water_count': 0, 'harvest_ready': False} for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Character settings
CHARACTER_WIDTH = 100
CHARACTER_HEIGHT = 90
MOVEMENT_SPEED = 5

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ECOCULTIVO")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Load menu assets
menu_bg = pygame.image.load("assets/menu.png").convert()
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))
map_bg = pygame.image.load("assets/map_bg.png").convert()
map_bg = pygame.transform.scale(map_bg, (WIDTH, HEIGHT))

play_button_img = pygame.image.load("assets/play_button.png").convert_alpha()
play_button_img = pygame.transform.scale(play_button_img, (200, 80))
play_button_rect = play_button_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Load game assets
tropical_bg = pygame.image.load("assets/tropical_bg.png").convert()
tropical_bg = pygame.transform.scale(tropical_bg, (WIDTH, HEIGHT))
cold_bg = pygame.image.load("assets/cold_bg.png").convert()
cold_bg = pygame.transform.scale(cold_bg, (WIDTH, HEIGHT))

# Backgrounds list for switching
backgrounds = [tropical_bg, cold_bg]
current_bg_index = 0

# Map buttons for tropical and cold (centered in map view)
tropical_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 50)
cold_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)

# Load button images
tropical_button_img = pygame.image.load("assets/tropical_button.png").convert_alpha()
tropical_button_img = pygame.transform.scale(tropical_button_img, (200, 80))
cold_button_img = pygame.image.load("assets/cold_button.png").convert_alpha()
cold_button_img = pygame.transform.scale(cold_button_img, (200, 80))

# Load character images
standing_img = pygame.image.load("assets/farmer.png").convert_alpha()
down_img = pygame.image.load("assets/farmer_down.png").convert_alpha()
regadera_img = pygame.image.load("assets/regadera.png").convert_alpha()
regadera_down_img = pygame.image.load("assets/regadera_down.png").convert_alpha()
regadera_down_surf = pygame.transform.scale(regadera_down_img, (CHARACTER_WIDTH - 5, CHARACTER_HEIGHT + 10))
standing_surf = pygame.transform.scale(standing_img, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
down_surf = pygame.transform.scale(down_img, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
regadera_surf = pygame.transform.scale(regadera_img, (CHARACTER_WIDTH - 5, CHARACTER_HEIGHT + 10))

# Cow settings (integrated from the first script)
cow_image = pygame.image.load("assets/cow.png").convert_alpha()
cow_surf = pygame.transform.scale(cow_image, (100, 110))
cow_x = 750
cow_y = 260
cow_speed = 1
cow_velx = random.uniform(cow_speed, cow_speed)
cow_vely = 0
cow_left_bound = 730
cow_right_bound = 900

# Character state
character_x = WIDTH // 2
character_y = HEIGHT // 2
current_character_surf = standing_surf
is_standing = True
regadera = False

def reset_tiles():
    global tiles
    tiles = [[{'watered': False, 'planted': False, 'watered_plant': False, 'watered_time': 0, 'water_count': 0, 'harvest_ready': False} for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

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

def update_cow_movement():
    global cow_x, cow_y, cow_velx, cow_vely  # Add cow_y here
    cow_x += cow_velx
    cow_y += cow_vely  # Vely is 0, so y stays fixed
    if cow_x <= cow_left_bound or cow_x >= cow_right_bound:
        cow_velx = -cow_velx

def draw_menu():
    # Draw the main menu background and play button.
    screen.blit(menu_bg, (0, 0))
    screen.blit(play_button_img, play_button_rect)

def draw_game():
    pygame.draw.rect(screen, (196, 160, 146), BORDER)
    pygame.draw.rect(screen, (0, 0, 0), HOUSE)
    screen.blit(backgrounds[current_bg_index], (0, 0))

    current_time = pygame.time.get_ticks()
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            rect = pygame.Rect(GRID_START_X + col * TILE_SIZE, GRID_START_Y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            tile = tiles[row][col]
            if tile['harvest_ready']:
                color = HARVEST_READY
            elif tile['planted']:
                if tile['watered_plant'] and current_time - tile['watered_time'] < 30000:
                    color = WATERED_PLANT
                else:
                    color = PLANTED
                    tile['watered_plant'] = False
            elif tile['watered']:
                color = WET
            else:
                color = DRY
            
            # Draw tile with adjusted opacity (more opaque for similarity)
            tile_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            tile_surf.fill(color)
            alpha = 255  # Fully opaque for both biomes to make them similar and more visible
            tile_surf.set_alpha(alpha)
            screen.blit(tile_surf, rect.topleft)
            
            pygame.draw.rect(screen, (0, 0, 0), rect, 2) 
    
    screen.blit(cow_surf, (cow_x, cow_y))
    screen.blit(current_character_surf, (character_x, character_y))
    # Draw the cow

def draw_map():
    screen.blit(map_bg, (0, 0))
    
    # Draw tropical button
    screen.blit(tropical_button_img, tropical_button_rect)
    if current_bg_index == 0:
        pygame.draw.rect(screen, (0, 255, 0), tropical_button_rect, 3)  # Green border for selected
    else:
        pygame.draw.rect(screen, (0, 0, 0), tropical_button_rect, 2)  # Default border
    
    # Draw cold button
    screen.blit(cold_button_img, cold_button_rect)
    if current_bg_index == 1:
        pygame.draw.rect(screen, (0, 255, 0), cold_button_rect, 3)  # Green border for selected
    else:
        pygame.draw.rect(screen, (0, 0, 0), cold_button_rect, 2)  # Default border

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
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == MENU:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if play_button_rect.collidepoint(mouse_pos):
                        current_state = GAME
            elif current_state == MAP:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos
                    if tropical_button_rect.collidepoint(mouse_pos):
                        if current_bg_index != 0:
                            reset_tiles()
                        current_bg_index = 0
                    elif cold_button_rect.collidepoint(mouse_pos):
                        if current_bg_index != 1:
                            reset_tiles()
                        current_bg_index = 1
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if current_state == GAME or current_state == MAP:
                    current_state = MENU
            elif event.key == pygame.K_m:
                if current_state == GAME:
                    current_state = MAP
                elif current_state == MAP:
                    current_state = GAME
            elif current_state == GAME:
                if event.key == pygame.K_l:
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
                            if not tile['harvest_ready']:
                                tile['water_count'] += 1
                                tile['watered_plant'] = True
                                tile['watered_time'] = pygame.time.get_ticks()
                                if tile['water_count'] >= 3:
                                    tile['harvest_ready'] = True
                                    tile['watered_plant'] = False
                        elif not tile['watered']:
                            tile['watered'] = True
                elif event.key == pygame.K_h:
                    # Harvest the nearest harvest-ready tile if possible
                    nearest = get_nearest_tile(character_x, character_y)
                    if nearest:
                        col, row = nearest
                        tile = tiles[row][col]
                        if tile['harvest_ready']:
                            tile['watered'] = False
                            tile['planted'] = False
                            tile['watered_plant'] = False
                            tile['harvest_ready'] = False
                            tile['water_count'] = 0
                            tile['watered_time'] = 0
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
        update_cow_movement()  # Update cow movement
    
    # Draw everything
    if current_state == MENU:
        draw_menu()
    elif current_state == GAME:
        draw_game()
    elif current_state == MAP:
        draw_map()
    
    # Update display and cap FPS
    pygame.display.flip()
    clock.tick(60)

# Cleanup
pygame.quit()
sys.exit()