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
background_image = pygame.image.load("assets/agua.png").convert()
bg_width, bg_height = background_image.get_size()

# character
char_image = pygame.image.load("assets/farmer.png").convert_alpha()
character = pygame.transform.scale(char_image, (120, 110))
character_x = 650
character_y = 400

# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    # Calculate camera position (follows character, centering it on screen)
    camera_x = character_x - screen_width // 2
    camera_y = character_y - screen_height // 2

    # Draw background (infinite tiling)
    offset_x = camera_x % bg_width
    offset_y = camera_y % bg_height
    x = -offset_x
    while x < screen_width:
        y = -offset_y
        while y < screen_height:
            screen.blit(background_image, (x, y))
            y += bg_height
        x += bg_width

    # Draw character (offset by camera)
    char_screen_x = character_x - camera_x
    char_screen_y = character_y - camera_y
    screen.blit(character, (char_screen_x, char_screen_y))

    pygame.display.update()
    clock.tick(60)

pygame.quit()