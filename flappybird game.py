import pygame
import random
pygame.init()
WIDTH=864
HEIGHT=800
TITLE="flappy bird"
pastpipe=False 
gameover=False
flying=False
pipefreq=2000
score=0
lastpipe=pygame.time.get_ticks()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)


flappy1=pygame.image.load("flappybird1.png")
flappy2=pygame.image.load("flappybird2.png")
flappy3=pygame.image.load("flappy bird3.png")
floor=pygame.image.load("flappyfloor.png")
sky=pygame.image.load("skybackround.png")
pipe=pygame.image.load("pipe.png")



class Flappy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.images=[flappy1,flappy2,flappy3]
        self.index=0
        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.counter=0
        self.velocity=0
    def update(self):
        if flying==True:
            self.counter=self.counter+1
            if self.counter==20:
                self.index=self.index+1
                if self.index==3:
                    self.index=0
                self.image=self.images[self.index]
                self.counter=0
            keypress=pygame.key.get_pressed()

            if keypress[pygame.K_SPACE] and gameover==False: 
                self.velocity=-3    
            self.velocity=self.velocity+0.05
            if self.velocity>=5:
                self.velocity=5 
            self.rect.y=self.rect.y+self.velocity 
           
            
   
bird=Flappy(100,400)
birdsgroup=pygame.sprite.Group()
birdsgroup.add(bird)


class Floor(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=floor
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

floor=Floor(0,700 )
floorgroup=pygame.sprite.Group()
floorgroup.add(floor)


class Pipe(pygame.sprite.Sprite):
    def __init__(self,image,x,y,pos):
        super().__init__()
        self.image=image
        self.rect=self.image.get_rect()
        if pos==1:
            self.image=pygame.transform.flip(self.image,flip_x=False,flip_y=True)
            self.rect.bottomleft=x,y
        else:
            self.rect.topleft=x,y
        
    def update(self):
        self.rect.x=self.rect.x-2
        if self.rect.right<0:
            self.kill()


toppipe=Pipe(pipe,865,250,1)
bottompipe=Pipe(pipe,865,450 ,0)
pipegroup=pygame.sprite.Group()
pipegroup.add(toppipe)
pipegroup.add(bottompipe)

run=True
while run:

    screen.blit(sky,(0,0))

    birdsgroup.draw(screen)
    bird.update()

    if flying==True:
        pipegroup.draw(screen)
        pipegroup.update()
        time_now=pygame.time.get_ticks()
        if time_now-lastpipe>=pipefreq:
            y=random.randint(-100,100)
            toppipe=Pipe(pipe,865,250-y,1)
            bottompipe=Pipe(pipe,865,450-y,0)
            pipegroup.add(toppipe)
            pipegroup.add(bottompipe)
            lastpipe=time_now 
    
    font=pygame.font.SysFont("Arial",50)
    text=font.render("score="+str(score),True,"yellow")
    screen.blit(text,(0,0))

    floorgroup.draw(screen)
    floor.update() 

    if flying==True:
        floor.rect.x=floor.rect.x-1
        if floor.rect.x<=-36:
             floor.rect.x=0

    if bird.rect.y<0:
        run=False
    if bird.rect.y>657:
        run=False  

    if gameover==True:
        font=pygame.font.SysFont("Arial",100)
        text=font.render("GAMEOVER",True,"red")
        screen.blit(text,(0,400))

    if birdsgroup.sprites()[0].rect.left>pipegroup.sprites()[0].rect.left and birdsgroup.sprites()[0].rect.right<pipegroup.sprites()[0].rect.right and pastpipe==False:
        pastpipe=True
    if birdsgroup.sprites()[0].rect.left>pipegroup.sprites()[0].rect.right and pastpipe==True:
        score=score+1
        pastpipe=False

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and gameover==False and flying==False:
                flying=True


    if len(pipegroup)>0:
        if pygame.sprite.groupcollide(birdsgroup,pipegroup,False,False):
            gameover=True



    pygame.display.update()