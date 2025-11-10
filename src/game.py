import pygame
from pygame.locals import * #import everything needed

pygame.init() # starts pygame

screen_width = 1000 # 1000 pixels
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height)) #create game screen #pygame.RESIZABLE as the second param to resize window
pygame.display.set_caption("Game")

#define game variables
tile_size = 50

#sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/background.png')


class Player():
    def __init__(self, x, y):
        img = pygame.image.load('img/player_right.png')
        self.image = pygame.transform.scale(img, (40, 80)) # set the players dimensions
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height =  self.image.get_height()
        self.vel_y = 0 #y velocity
        self.jumped = False # to check if we jumped (helps us not keep flying up after jumping)

    def update(self):

        #change in x and y
        dx = 0
        dy = 0

        #get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -15 # in our implementation, the top of the screen y = 0, bottom y = max so '-' moves up
            self.jumped == True 
        if key[pygame.K_SPACE] == False: # we havent clicked the space bar to jump yet
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
        if key[pygame.K_RIGHT]:
            dx += 5
            
        #add gravity to the fall
        self.vel_y += 2 #helps us get down after we jump
        if self.vel_y > 10:
            self.vel_y = 10 # this just ensures we never get too high

        dy += self.vel_y

        #check for collision
        for tile in world.tile_list:
            #remember that collisions in the x are okay (standing ontop of tiles)
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0

            #we need to check for hitting on the y direction
            #if we check if just self.rect.y hits, we might check too late (it might be already in the wall)
            #we dont update dy right away so we can
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height): # the 1 index is the rectangle info, 0 is the image
                #check if below the ground (jumping)
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                #check if above the ground (falling)    
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0




        #update player position/ coordinates
        self.rect.x += dx
        self.rect.y += dy


        #draw the player on the screen
        screen.blit(self.image, self.rect)




class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1: # if the tile = 1, load the dirt image
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size)) #scale the image by the x and y axis (200x200 tile)
                    img_rect = img.get_rect() #takes the image and gets a rectangle from it
                    img_rect.x = col_count * tile_size 
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) #tuple of the image and the tile rectangle
                    self.tile_list.append(tile) # add the tuple to the list
                if tile == 2: # if the tile = 1, load the dirt image
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size)) #scale the image by the x and y axis (200x200 tile)
                    img_rect = img.get_rect() #takes the image and gets a rectangle from it
                    img_rect.x = col_count * tile_size #
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect) #tuple of the image and the tile rectangle
                    self.tile_list.append(tile) # add the tuple to the list
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15) # +15 so it touches the top of the tile (looks like its resting on the tile)
                    blob_group.add(blob)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/bee_left.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


        

#create list that stores the tilemap grid
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
player = Player(100, screen_height - 130) # x = 100, for the y since the bottom tile is 50 + 80 for the player height = 130. screen_height - 130 puts him ontop of the tile
blob_group = pygame.sprite.Group()

world = World(world_data)


run = True
while run:

    #order of screen.blit statements matter
    screen.blit(bg_img, (0, 0)) # set the sky to take up the entire screen
    screen.blit(sun_img, (100, 100)) # Set the sun to be in the top left

    world.draw() # this adds all the dirt tiles to the tilemap
    blob_group.update()
    blob_group.draw(screen)
    player.update() # add the player to the tilemap
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run =  False
    pygame.display.update() #updates the display window


pygame.quit()