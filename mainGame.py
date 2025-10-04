import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1300, 800))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("NAME OF GAME")

# character
char_image = pygame.image.load("assets/farmer.png", ).convert_alpha()
character = pygame.transform.scale(char_image, (100, 110))
character_x = 600
character_y = 400

def draw_character():
    screen.blit(character, (character_x, character_y))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    draw_character()
    pygame.display.update()

    clock.tick(60)

pygame.quit()