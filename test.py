import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1300, 800))
screen_width = screen.get_width()
screen_height = screen.get_height()
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("ECOCULTIVO")

# background (load without scaling for tiling)
background_image = pygame.image.load("assets/background.png").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Load character images
standing_image = pygame.image.load("assets/farmer.png").convert_alpha()
down_image = pygame.image.load("assets/farmer_down.png").convert_alpha()
standing_surf = pygame.transform.scale(standing_image, (100, 90))
down_surf = pygame.transform.scale(down_image, (100, 90))

# Character dimensions (for boundary checking)
character_width = 100
character_height = 90

# Initial state
current_surf = standing_surf
is_standing = True
character_x = 650
character_y = 400

# Floor setup
floor_height = 50
floor_picture = pygame.image.load("assets/grass.png").convert_alpha()
floor_surf = pygame.transform.scale(floor_picture, (80, 80))

# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                if is_standing:
                    current_surf = down_surf
                    is_standing = False
                else:
                    current_surf = standing_surf
                    is_standing = True

    # Handle input first (movement)
    speed = 5
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        character_y -= speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        character_y += speed
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        character_x -= speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        character_x += speed

    # Boundary checking to prevent character from going outside the screen
    character_x = max(0, min(character_x, screen_width - character_width))
    character_y = max(0, min(character_y, screen_height - character_height))

    # Draw everything
    screen.fill((0, 0, 0))  # Clear the screen with black
    screen.blit(background_image, (0, 0))  # Draw the scaled background
    screen.blit(current_surf, (character_x, character_y))  # Draw character
    pygame.display.update()

    clock.tick(60)

pygame.quit()