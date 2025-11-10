import pygame

from dataRead import readData, readEmg

pygame.init()
screen = pygame.display.set_mode((800, 600))

ser = readData()  # connect ONCE here

player_x = 100
player_y = 400
vel_y = 0
gravity = 1
threshold = 40  # pick a starting threshold then later we do calibration

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    val = readEmg(ser)
    if val is not None:
        if val > threshold:
            vel_y = -15  # jump impulse

    # physics step
    vel_y += gravity
    player_y += vel_y

    # floor clamp
    if player_y > 400:
        player_y = 400
        vel_y = 0

    screen.fill((0, 0, 0))
    # draw background / player
    # screen.blit(background,(0,0))
    # screen.blit(player,(player_x,player_y))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
