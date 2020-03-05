#Pygame template - skeleton for a new pygame project
import pygame
import random
	
#the frame of the game
WIDTH = 480
HEIGHT = 600
FPS = 60
	

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
#(6.)
YELLOW = (255, 255, 0)
	

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
	


#(creating the player)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,40))
        #self.image.set_colorkey(BLACK)
        self.image.fill(GREEN)
       # self.radius = 20
        #(ignore for now)pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect= self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom=HEIGHT - 10
        self.speedx =0


        #(how to move the player)
    def update(self):
        self.speedx=0
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right=WIDTH
        if self.rect.left < 0:
            self.rect.left=0


#(4)
    def shoot(self):
         bullet = Bullet(self.rect.centerx,self.rect.top)
         all_sprites.add(bullet)
         bullets.add(bullet)


#(create the enemy)
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((30,40))
        self.image.fill(RED)
        self.rect=self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y= random.randrange(-150,-100)
        self.speedy=random.randrange(1,9)
        self.speedx= random.randrange(-1,1)
        


    def update(self):
        
        #self.rotate()
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rectx = random.randrange(WIDTH - self.rect.width)
            self.rect.y= random.randrange(-100,-40)
            self.speedy=random.randrange(1,8)



#(2.) the bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((10,10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom =y
        self.rect.centerx=x
        self.speedy = -4

#(3.)
    def update(self):
        self.rect.y += self.speedy
        #kill if it moved off the top of the screen
        if self.rect.bottom <0:
            self.kill()






all_sprites = pygame.sprite.Group()

mobs=pygame.sprite.Group()
#(5.)add bullets
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)



for i in range(10):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    


# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
            
            #(7.)shooting using spacebar
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            
	

    # Update
    all_sprites.update()

    #(8.)check to see if the bullet hit the enemy
    hits = pygame.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hits:
        m=Mob()
        all_sprites.add(m)
        mobs.add(m)
   

    #(1.)#this checks if the enemy has hit the player
    hits = pygame.sprite.spritecollide(player,mobs,False)
    for hit in hits:
        running=False
	

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()
	

pygame.quit()

