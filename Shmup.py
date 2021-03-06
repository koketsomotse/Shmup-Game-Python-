#shump game

import pygame
import random
from os import path


#image directory to find the graphic images
img_dir = path.join(path.dirname(__file__),'img')

WIDTH=480
HEIGHT=600
FPS=60

#define colours

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)

#initialize pygame abd creating window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Invaders 2.0")
clock=pygame.time.Clock()




def draw_shield_bar(surf,x,y,pct):
    if pct <0:
        pct=0
    BAR_LENGTH =100
    BAR_HEIGHT =10
    fill = (pct/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect=pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)

    
def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


score=0
font_name = pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,WHITE)
    text_rect= text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)
    


#player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,38))
        self.image.set_colorkey(BLACK)
        #self.image.fill(GREEN)
        self.radius = 20
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect= self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom=HEIGHT - 10
        self.speedx =0
        self.shield = 100
        self.shoot_delay =250
        self.last_shot = pygame.time.get_ticks()

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


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx,self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
#enemy
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig=random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect=self.image.get_rect()
        self.radius = int(self.rect.width * .85/2)
        #this part is to test the radius of the collisions using circular collion calculations
        # pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        #self.image.fill(RED)
        
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y= random.randrange(-150,-100)
        self.speedy=random.randrange(1,9)
        self.speedx= random.randrange(-1,1)
        #rotations of the meteor
        self.rot=0
        self.rot_speed=random.randrange(-9,9)
        self.last_update=pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig,self.rot)
            old_center=self.rect.center
            self.image=new_image
            self.rect=self.image.get_rect()
            self.rect.center=old_center
            
        

        
    def update(self):
        self.rotate()
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            
            self.rectx = random.randrange(WIDTH - self.rect.width)
            self.rect.y= random.randrange(-100,-40)
            self.speedy=random.randrange(1,12)

            
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=bullet_img
        self.image.set_colorkey(BLACK)
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom =y
        self.rect.centerx=x
        self.speedy = -4


    def update(self):
        self.rect.y += self.speedy
        #kill if it moved off the top of the screen
        if self.rect.bottom <0:
            self.kill()
        
        

#load all the game graphics

background = pygame.image.load(path.join(img_dir,"bHiPMju.png")).convert()
background_rect=background.get_rect()
player_img=pygame.image.load(path.join(img_dir,"playerShip1_red.png")).convert()
bullet_img=pygame.image.load(path.join(img_dir,"laserRed16.png")).convert()
meteor_images= []
meteor_list=['meteorGrey_big4.png','ufoYellow.png','meteorBrown_big3.png','meteorBrown_tiny1.png','meteorGrey_med1.png','meteorGrey_tiny2.png']

for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir,img)).convert())
    

            
all_sprites=pygame.sprite.Group()
mobs=pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(10):
    #m = Mob()
    #all_sprites.add(m)
    #mobs.add(m)
    newmob()

#game loop

running=True
while running:
    #keeping loop running at the right speed
    clock.tick(FPS)
    #events inputs
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
       # elif event.type==pygame.KEYDOWN:
       #     if event.key==pygame.K_SPACE:
       #         player.shoot()

    #update
    all_sprites.update()
    #this is to check if the bullet has hit the player
    hits = pygame.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hits:
        score += 50 - hit.radius
       # m=Mob()
       # all_sprites.add(m)
       # mobs.add(m)
        newmob()
    
    #this checks if the enemy has hit the player
    hits = pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        newmob()
        if player.shield <=0:
            running=False
        


    #draw/render
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,WIDTH/2,10)
    draw_shield_bar(screen,5,5,player.shield)
    pygame.display.flip()

pygame.quit()    
