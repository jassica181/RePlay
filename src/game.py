import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")

background = pygame.image.load("images/background.png").convert()
background = pygame.transform.scale(background, (800, 600))

# --- Game loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    pygame.display.flip()

pygame.quit()
