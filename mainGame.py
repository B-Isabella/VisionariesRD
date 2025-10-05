import pygame
import sys

# Constants
WIDTH = 1300
HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WATERBLUE = (31, 170, 220)
GREEN = (0, 255, 0)

# Game states
MENU = 0
GAME = 1
current_state = MENU

# Tabla
BORDER = pygame.Rect(40, 50, 170, HEIGHT - 80)
HOUSE = pygame.Rect(1095, 120, 190, 130)

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
standing_surf = pygame.transform.scale(standing_img, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
down_surf = pygame.transform.scale(down_img, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

# Character state
character_x = WIDTH // 2
character_y = HEIGHT // 2
current_character_surf = standing_surf
is_standing = True

def draw_menu():
    # Draw the main menu background and play button.
    screen.blit(menu_bg, (0, 0))
    screen.blit(play_button_img, play_button_rect)

def draw_game():
    # Draw the game background and character.
    pygame.draw.rect(screen, (0, 0, 0), HOUSE)
    screen.blit(game_bg, (0, 0))
    pygame.draw.rect(screen, (196, 160, 146), BORDER)
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
                if is_standing:
                    current_character_surf = down_surf
                    is_standing = False
                else:
                    current_character_surf = standing_surf
                    is_standing = True
    
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