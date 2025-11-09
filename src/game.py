import pygame
pygame.init()


# --- Setup ---
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")

# --- Load images ---
background = pygame.image.load("images/background.png").convert()
background = pygame.transform.scale(background, (800, 600))

player = pygame.image.load("images/player_right.png").convert_alpha()  
player = pygame.transform.scale(player, (96, 96)) 

# --- Player starting position ---
player_x = 100
player_y = 400

# --- Game loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw background
    screen.blit(background, (0, 0))

    # Draw player
    screen.blit(player, (player_x, player_y))

    # Update display
    pygame.display.flip()

pygame.quit()
