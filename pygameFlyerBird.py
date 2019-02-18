#flyer bird
#!/usr/bin/env python
import pygame,time,random,sys
from pygame.locals import *

def print_text(font,x,y,text,color=(255,255,255)):
    imgText=font.render(text,True,color)
    screen.blit(imgText,(x,y))
    
class Wallup(pygame.sprite.Sprite):
    def __init__(self,path):
        pygame.sprite.Sprite.__init__(self)
        self.path=path
        self.x=800
    def update(self,ticks):
        self.x-=10
        rect=Rect(0,0,70,500)
        self.rect=Rect(self.x,self.path-500,70,500)
        self.image=self.master_image.subsurface(rect)

    def load(self,filename=r'wall.png'):
        self.master_image=pygame.image.load(filename).convert_alpha()
        
class Walldown(pygame.sprite.Sprite):
    def __init__(self,path):
        pygame.sprite.Sprite.__init__(self)
        self.path=path
        self.x=800
    def update(self,ticks):
        self.x-=10
        rect=Rect(0,0,70,500)
        self.rect=Rect(self.x,self.path+100,70,500)
        self.image=self.master_image.subsurface(rect)
        
    def load(self,filename=r'wall.png'):
        self.master_image=pygame.image.load(filename).convert_alpha()

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.master_image=pygame.image.load(r'bird.png').convert_alpha()
        self.vel=10
        self.y=150
    def update(self):
        rect=Rect(0,0,50,50)
        self.rect=Rect(100,self.y,50,50)
        self.image=self.master_image.subsurface(rect)


def audio_init():
    global bgm
    pygame.mixer.init()
    bgm=pygame.mixer.Sound(r'bgm.ogg')

def play_sound(sound):
    channel=pygame.mixer.find_channel(True)
    channel.set_volume(0.1)
    channel.play(sound)

def pygame_init():
    global screen,add_vel,font,backbuffer,bird_group,wallup_group,walldown_group,last_time,game_over,\
           score,get_score,backgrn
    pygame.init()
    audio_init()
    play_sound(bgm)
    screen=pygame.display.set_mode((800,600))
    pygame.display.set_caption("Flyer Bird")
    font=pygame.font.SysFont('arial',30)   
    add_vel=-21
    score=0
    get_score=True
    backbuffer=pygame.Surface((800,600))
    

    bird_group=pygame.sprite.Group()
    wallup_group=pygame.sprite.Group()
    walldown_group=pygame.sprite.Group()
    
    last_time=0
    game_over=False
    backgrn=pygame.image.load(r'backgrn.png').convert()

pygame_init()
bird=Bird()
bird_group.add(bird)
while True:
    ticks=pygame.time.get_ticks()
    pygame.time.Clock().tick(30)

    if ticks>last_time+1200:
        path=random.randint(100,400)
        
        wallup=Wallup(path)
        wallup.load()
        wallup_group.add(wallup)

        walldown=Walldown(path)
        walldown.load()
        walldown_group.add(walldown)
        
        last_time=ticks
        
    
    for event in pygame.event.get():
        if event.type==QUIT:
            sys.exit()
    keys=pygame.key.get_pressed()
    if keys[K_ESCAPE]:sys.exit()
    if keys[K_SPACE]:
        bird.vel+=add_vel

    bird.vel+=10
    bird.y=bird.vel+150

    if not game_over:
        bird.update()
        wallup_group.update(ticks)
        walldown_group.update(ticks)

        screen.blit(backgrn,(0,0))
        bird_group.draw(screen)        
        wallup_group.draw(screen)    
        walldown_group.draw(screen)

        print_text(font,50,100,"S C O R E: "+str(score))

        for wallup in wallup_group:
            if wallup.x<100 and get_score:
                get_score=False
                score+=1
            if wallup.x<-100:
                get_score=True
                wallup_group.remove(wallup)

        for walldown in walldown_group:
            if walldown.x<-100:
                walldown_group.remove(walldown)

        coli1=None
        coli2=None
        coli1=pygame.sprite.spritecollideany(bird,wallup_group)
        coli2=pygame.sprite.spritecollideany(bird,walldown_group)
        
        if coli1!=None:
            if pygame.sprite.collide_rect_ratio(0.95)(bird,coli1):
                game_over=True
        if coli2!=None:
            if pygame.sprite.collide_rect_ratio(0.9)(bird,coli2):
                game_over=True        
        if bird.y>600:
            game_over=True
    else:
        print_text(font,300,200,"G  A  M  E  O  V  E  R")
        
    pygame.display.update()
