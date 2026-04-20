import pygame
from pygame.locals import *
import random
from pygame import mixer

#sound effects
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

#sounds
explosion_fx = pygame.mixer.Sound("explosion.wav")
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound("explosion2.wav")
explosion2_fx.set_volume(1)

laser_fx = pygame.mixer.Sound("laser.wav")
laser_fx.set_volume(0.25)

#FPS
clock=pygame.time.Clock()
fps=60

#game window
screen_width=600
screen_height=800

#game title
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Space Invader")

#fonts
pygame.init()
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)




#define game variables
rows=5
cols=5
alien_cooldown=1000#bullete cooldown in millisecound
last_alien_shot=pygame.time.get_ticks()
countdown=3 #countdown before the start of game
last_count=pygame.time.get_ticks()
game_over=0#0 is game is going on , 1 means player has won ,-1 means player has lost




#define colours
red = (255, 0, 0)#used in health bar
green = (0, 255, 0)
white=(255,255,255)



#BG image
bg=pygame.image.load("bg.png")

def draw_bg():#function for getting bg into the loop
    screen.blit(bg,(0,0))#used for displaying (0,0) are coordinates

#define function for text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    







#create spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("spaceship.png")
        self.rect = self.image.get_rect()#the spaceship is saved in rectangle object
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()


    def update(self):#upadating the spaceship
        #set movement speed
        speed=8
        #set a cooldown for bullets
        cooldown=500#millsecound
        game_over=0

        #get key press
        key=pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left>0:
            self.rect.x-=speed
        if key[pygame.K_RIGHT] and self.rect.right<screen_width: #and and self.rect.right < screen_width used to make it stay within screen
            self.rect.x+=speed


        #record current time
        time_now=pygame.time.get_ticks()

        #shoot
        if key[pygame.K_SPACE]and time_now - self.last_shot > cooldown:
            laser_fx.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now
            
        #update mask
        self.mask=pygame.mask.from_surface(self.image)    


        #draw health bar
        pygame.draw.rect(screen, red, (self.rect.x,(self.rect.bottom + 10),self.rect.width, 15))#creating a health bar 
        if self.health_remaining>0:#reducing the health
            pygame.draw.rect(screen, green,(self.rect.x,(self.rect.bottom + 10),int(self.rect.width *(self.health_remaining/self.health_start)), 15))#self.health_remaining/self.health_start this is because when it gets hit the green bar should reduce     
        elif self.health_remaining <= 0:#killing the spaceship after 0 health
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over=-1
        return game_over


#create bullete class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect() #the spaceship is saved in rectangle object
        self.rect.center = [x, y]


    def update(self):
        self.rect.y-=5
        if self.rect.bottom<0: #to delete the bullets after the end of screen
            self.kill()
        if pygame.sprite.spritecollide(self,alien_group,True):#to check for collisions
            self.kill()
            explosion_fx.play()
            #trigerring the explosion animation
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)
            
        



#create aliens class
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("alien" + str(random.randint(1, 5)) + ".png")
        self.rect = self.image.get_rect() #the spaceship is saved in rectangle object
        self.rect.center = [x, y]
        self.move_counter=0
        self.move_direction=1


        
    def update(self):
        self.rect.x+=self.move_direction
        self.move_counter+=1
        if abs(self.move_counter)>75:
            self.move_direction*=-1
            self.move_counter*=self.move_direction
        
        
#create alien bullete class
class Aline_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("alien_bullet.png")
        self.rect = self.image.get_rect() #the spaceship is saved in rectangle object
        self.rect.center = [x, y]


    def update(self):
        self.rect.y+=2
        if self.rect.top>screen_height: #to delete the bullets after the end of screen
            self.kill()
        if pygame.sprite.spritecollide(self,spaceship_group,False,pygame.sprite.collide_mask):
            self.kill()
            explosion2_fx.play()#playing the sound
            #reduce space ship health
            spaceship.health_remaining-=1
            #trigerring the explosion animation
            explosion=Explosion(self.rect.centerx,self.rect.centery,1)
            explosion_group.add(explosion)

    




#create explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y,size):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]#list of images
        for num in range(1,6):#loading explosion images
            img=pygame.image.load(f"exp{num}.png")
            #if size of the explosions
            if size==1:
                img=pygame.transform.scale(img,(20,20))
            if size==2:
                img=pygame.transform.scale(img,(40,40))
            if size==3:
                img=pygame.transform.scale(img,(160,160))
            #add the image to list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() #the spaceship is saved in rectangle object
        self.rect.center = [x, y]
        self.counter=0#speed of animation of explosion

    def update(self):
        explosion_speed=3
        #update explosion animation
        self.counter+=1
        if self.counter>=explosion_speed and self.index < len(self.images)-1: #starting the animation 
            self.counter=0
            self.index+=1
            self.image=self.images[self.index]

        #if animation is complete delete exp
        if self.index >= len(self.images)-1 and self.counter >= explosion_speed:
            self.kill()
            
            

    






#create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group= pygame.sprite.Group()
alien_group=pygame.sprite.Group()
alien_bullet_group=pygame.sprite.Group()
explosion_group=pygame.sprite.Group()




#create alien npc
def create_aliens():
  #generate aliens
  for row in range(rows):
      for item in range(cols):
          alien=Aliens(100+item*100,100+row*70)#where to start the npc
          alien_group.add(alien)


create_aliens()



#create player
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)#3 is how many times we can get hit
spaceship_group.add(spaceship)



#Game loop
run=True
while run:
    clock.tick(fps)#limiting the frame rate to 60fps


    #draw background
    draw_bg()

    if countdown==0:
     #create random alien bullets
     #record current time
     time_now=pygame.time.get_ticks()


     #shoot
     if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group)<5 and len(alien_group)>0:#for giving some tiime between each shot .alien_bullet_group if for limiting the number of bullets .alien_group to stop if there are no aliens 
        attacking_alien=random.choice(alien_group.sprites())
        alien_bullet=Aline_Bullets(attacking_alien.rect.centerx,attacking_alien.rect.bottom)
        alien_bullet_group.add(alien_bullet)
        last_alien_shot=time_now

     #check if all aliens are killed 
     if len(alien_group)==0:
         game_over=1
     if game_over==0:

      #update spacehip
      game_over=spaceship.update()

      #updating sprite groups
      bullet_group.update()
      alien_group.update()
      alien_bullet_group.update()
     else:
        if game_over==-1:
            draw_text("YOU LOST !",font40,white,int(screen_width/2-100),int(screen_height/2+50))
        if game_over==1:
            draw_text("YOU WON !",font40,white,int(screen_width/2-100),int(screen_height/2+50))
    if countdown>0:
        draw_text("GET READY !",font40,white,int(screen_width/2-110),int(screen_height/2+50))
        draw_text(str(countdown),font40,white,int(screen_width/2-10),int(screen_height/2+100))
        count_timer=pygame.time.get_ticks()
        if count_timer-last_count>1000:
            countdown-=1
            last_count=count_timer


    #update explosion group
    explosion_group.update()


    #draw sprite groups(bringing it to the screen)
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)


    #event Handlers
    for event in pygame.event.get():
        if event.type==pygame.QUIT: #when we click the escape button on top right
            run=False
    pygame.display.update()#updating the screen

pygame.quit()
