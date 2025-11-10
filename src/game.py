import pygame
from pygame.locals import *  #import everything from pygame

pygame.init()
clock = pygame.time.Clock()

screen_width = 800
screen_height = 800
# --- Setup ---
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("RePlay")

tile_size = 50
mango_count = 0
sting_count = 0

health0 = pygame.image.load("images/Health0.png")
health1 = pygame.image.load("images/Health1.png")
health2 = pygame.image.load("images/Health2.png")
health3 = pygame.image.load("images/Health3.png")

heart3 = pygame.image.load("images/Hearts3.png")
heart2 = pygame.image.load("images/Hearts2.png")
heart1 = pygame.image.load("images/Hearts1.png")
heart0 = pygame.image.load("images/Hearts0.png")

health_images = [health0, health1, health2, health3]

heart_images = [heart3, heart2, heart1, heart0]

# Load up the background image and scale it to the game window size
background = pygame.image.load("images/NewBackground.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

#create a player class
#player = pygame.image.load("images/player_right.png").convert_alpha()  
#player = pygame.transform.scale(player, (96, 96)) 
class Elephant():
    def __init__(self, x, y):
        player_image_right = pygame.image.load("images/ElephantRight.png")
        player_image_left = pygame.image.load("images/ElephantLeft.png")

        self.img_right = pygame.transform.scale(player_image_right, (50, 50)) 
        self.img_left = pygame.transform.scale(player_image_left, (50, 50)) 

        self.img = self.img_right
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.spawn_x = x     
        self.spawn_y = y  
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.elephant_velocity_y = 0
        self.stop_jump = False

    def update(self):
        dx = 0
        dy = 0

        button = pygame.key.get_pressed()
        space = pygame.K_SPACE
        left = pygame.K_LEFT
        right = pygame.K_RIGHT
        if button[pygame.K_SPACE] and self.stop_jump == False:
            self.elephant_velocity_y = -20
            self.stop_jump = True
        if button[pygame.K_SPACE] == False:
            self.stop_jump = False
        if button[pygame.K_LEFT]:
            dx -= 3 #move to the left by 5
            self.img = self.img_left
        if button[pygame.K_RIGHT]:
            dx += 3 #move to the right by 5
            self.img = self.img_right

        self.elephant_velocity_y += 1 #this acts as gravity, helps the elephant come back down after jumping
        if self.elephant_velocity_y > 20:
            self.elephant_velocity_y = 20
        dy += self.elephant_velocity_y

        #check for hitting walls
        for x in grid.world_list:
            if x[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0

            if x[1].colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
                if self.elephant_velocity_y < 0: # means the elephant is jumping up
                    dy = x[1].bottom - self.rect.top
                    self.elephant_velocity_y = 0

                elif self.elephant_velocity_y >= 0:
                    dy = x[1].top - self.rect.bottom
                    self.elephant_velocity_y = 0

        
        #update player position
        self.rect.x += dx
        self.rect.y += dy

        #draw the player on the screen
        screen.blit(self.img, self.rect)
    def respawn(self):
        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y
        self.elephant_velocity_y = 0

class Grid():
    def __init__(self, world_grid):
        self.world_list = []
        
        #load the different tiles
        ground_tile = pygame.image.load("images/GroundTile.png")
        mango = pygame.image.load("images/NewMango.png")
        bee_right = pygame.image.load("images/NewBeeRight.png")
        bee_left = pygame.image.load("images/NewerBeeLeft.png")
        boarder = pygame.image.load("images/NewBoarder.png")
        door1 = pygame.image.load("images/Door1.png")
        door2 = pygame.image.load("images/Door2.png")
        

        row_count = 0
        for row in world_grid:
            col_count = 0
            for col in row:
                if col == 1:
                    img = pygame.transform.scale(ground_tile, (50, 50))
                    img_rect = img.get_rect() #makes a rectangle border around the tile
                    img_rect.x = col_count * 50
                    img_rect.y = row_count * 50
                    tile = (img, img_rect)
                    self.world_list.append(tile)
                if col == 3:
                    img = pygame.transform.scale(door1, (50, 50))
                    img_rect = img.get_rect() #makes a rectangle border around the tile
                    img_rect.x = col_count * 50
                    img_rect.y = row_count * 50
                    tile = (img, img_rect)
                    self.world_list.append(tile)
                if col == 4:
                    exit = Exit(col_count * tile_size, row_count * tile_size)
                    exit_group.add(exit)
                
                if col == 6:
                    mango = Mango(col_count * tile_size, row_count * tile_size)
                    mango_group.add(mango)

                if col == 5:
                    bee = Bee(col_count * tile_size, row_count * tile_size + 15)
                    bee_group.add(bee)

                if col == 8:
                    img = pygame.transform.scale(boarder, (50, 50))
                    img_rect = img.get_rect() #makes a rectangle border around the tile
                    img_rect.x = col_count * 50
                    img_rect.y = row_count * 50
                    tile = (img, img_rect)
                    self.world_list.append(tile)
                col_count += 1
            row_count += 1
        
    def draw(self):
        for x in self.world_list:
            screen.blit(x[0], x[1])
                
class Bee(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_right = pygame.image.load("images/NewBeeRight.png")
        self.image_left = pygame.image.load("images/NewerBeeLeft.png")

        self.image_right = pygame.transform.scale(self.image_right, (50, 50)) 
        self.image_left = pygame.transform.scale(self.image_left, (50, 50)) 

        self.image = self.image_right

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.counter = 0

    def update(self):
        self.rect.x += self.direction
        self.counter += 1

        if self.direction > 0:
            self.image = self.image_right
        else:
            self.image = self.image_left

        if abs(self.counter) > 50:
            self.direction *= -1
            self.counter *= -1

class Mango(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/NewMango.png")
        self.image = pygame.transform.scale(self.image, (50, 50)) 

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Door2.png")
        self.image = pygame.transform.scale(self.image, (50, 50)) 

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


world_grid = [
   # 1  2  3  4  5  6  7  8  9  10  11  12  13 14 15 16
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], #1
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], #2
    [8, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 8], #3
    [8, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 8], #4
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], #5
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], #6
    [8, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 6, 0, 0, 0, 8], #7
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 7, 0, 0, 8], #8
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 8], #9
    [8, 1, 1, 0, 0, 0, 0, 0, 5, 0, 0, 0, 7, 0, 0, 8], #10
    [8, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 8], #11
    [8, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], #12
    [8, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], #13
    [8, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 8], #14
    [8, 3, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 8], #15
    [8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8], #16
]
elephant = Elephant(100, screen_height - 120)
bee_group = pygame.sprite.Group()
mango_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

grid = Grid(world_grid)

running = True
while running:
    # Draw background
    screen.blit(background, (0, 0))

    grid.draw()
    bee_group.update()
    bee_group.draw(screen)
    elephant.update()
    hits = pygame.sprite.spritecollide(elephant, mango_group, True)
    if hits:
        mango_count += len(hits)

    stings = pygame.sprite.spritecollide(elephant, bee_group, False)
    if stings:
        sting_count += len(stings)
        elephant.respawn()
        if sting_count >= 3:
            print("GAME OVER")
            running = False

    screen.blit(health_images[mango_count], (20,20))
    mango_group.draw(screen)
    screen.blit(heart_images[sting_count], (screen_width - 120, 20))
  

    escaped = pygame.sprite.spritecollide(elephant, exit_group, True)
    if escaped:
        print("You win!")
        running = False
    exit_group.draw(screen)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update display
    
    pygame.display.update()
    clock.tick(60) 

pygame.quit()

