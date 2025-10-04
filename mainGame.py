import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1300, 800))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("ECOCULTIVO")

# character
char_image = pygame.image.load("assets/farmer.png", ).convert_alpha()
character = pygame.transform.scale(char_image, (100, 110))
character_x = 600
character_y = 400

def draw_character():
    screen.blit(character, (character_x, character_y))

# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    draw_character()
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
    pygame.display.update()

    clock.tick(60)

pygame.quit()