import pygame
import sys
import random
import json


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

score = 0
water_used = 0

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ECOCULTIVO")

try:
    with open("nasa_data.json", "r") as f:
        nasa_data = json.load(f)
    print("NASA data loaded successfully from file.")  # Optional: for debugging
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Warning: Could not load nasa_data.json ({e}). Using default data.")
    # Default data matching your code's expected structure
    nasa_data = {
           "tropical": {
               "temperature": 28.5,
               "soil_moisture": 0.4,
               "rainfall": 120.0,
               "description": "A warm, humid tropical biome with high biodiversity and frequent rains, ideal for crops like bananas and coffee."
           },
           "cold": {
               "temperature": 8.2,
               "soil_moisture": 0.25,
               "rainfall": 60.0,
               "description": "A cooler temperate biome with moderate temperatures, suitable for hardy crops like potatoes and berries, but requiring protection from frost."
           }
       }

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
font_desc = pygame.font.Font(None, 24)  # Smaller font for description panel

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
tropical_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 -25, 200, 70)
cold_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 70)

# Load button images
tropical_button_img = pygame.image.load("assets/tropical_button.png").convert_alpha()
tropical_button_img = pygame.transform.scale(tropical_button_img, (200, 70))
cold_button_img = pygame.image.load("assets/cold_button.png").convert_alpha()
cold_button_img = pygame.transform.scale(cold_button_img, (200, 70))

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

def draw_nasa_data():
    biome = "tropical" if current_bg_index == 0 else "cold"
    data = nasa_data[biome]
    info_text = f"{biome.capitalize()} | Temp: {data['temperature']}°C | Moisture: {data['soil_moisture']*100:.0f}% | Rainfall: {data['rainfall']}mm"
    screen.blit(font.render(info_text, True, (255, 255, 255)), (20, 20))

def draw_score():
    score_text = font.render(f"Sustainability Score: {int(score)}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH - 400, 20))

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

def draw_info_panel():
    biome = "tropical" if current_bg_index == 0 else "cold"
    text = nasa_data[biome]["description"]
    box_width = 380
    box_height = 120
    margin = 20
    box_x = WIDTH - box_width - margin
    box_y = HEIGHT - box_height - margin
    pygame.draw.rect(screen, (0, 0, 0, 150), (box_x, box_y, box_width, box_height))
    lines = []
    words = text.split(' ')
    line = ""
    for word in words:
        if len(line + word) < 50:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)
    text_y_start = box_y + 10
    line_spacing = 28  # Adjusted spacing for smaller font to fit within box
    for i, l in enumerate(lines):
        y_pos = text_y_start + i * line_spacing
        if y_pos + font_desc.get_height() <= box_y + box_height - 5:  # Ensure it fits vertically
            screen.blit(font_desc.render(l.strip(), True, (255, 255, 255)), (box_x + 15, y_pos))

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
            
            # Draw tile directly without opacity/alpha (fully solid)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2) 
    
    draw_nasa_data()
    draw_score()
    draw_info_panel()
    screen.blit(cow_surf, (cow_x, cow_y))
    screen.blit(current_character_surf, (character_x, character_y))

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
                    nearest = get_nearest_tile(character_x, character_y)
                    if nearest:
                        col, row = nearest
                        tile = tiles[row][col]
                        biome = "tropical" if current_bg_index == 0 else "cold"
                        moisture = nasa_data[biome]["soil_moisture"]
                        water_used += 1

                        if tile['planted']:
                            if not tile['harvest_ready']:
                                # Adjust water effectiveness based on NASA soil moisture
                                water_factor = 1 if moisture < 0.5 else 0.5  
                                tile['water_count'] += water_factor
                                tile['watered_plant'] = True
                                tile['watered_time'] = pygame.time.get_ticks()
                                if tile['water_count'] >= 3:
                                    tile['harvest_ready'] = True
                                    tile['watered_plant'] = False
                        elif not tile['watered']:
                            tile['watered'] = True

                elif event.key == pygame.K_h:
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

                            # Add sustainability score (efficient farming = better score)
                            gain = max(5, 15 - water_used * 0.5)
                            score += gain
                            water_used = 0

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
    clock.tick(70)

# Cleanup
pygame.quit()
sys.exit()