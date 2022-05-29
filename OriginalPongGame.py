
import pygame
import random

#paddle2, which is at the right, its a bot. It is synchron with ball's y location. I will use it train my agent 

HEIGHT = 450
WIDTH = 600

#pygame screen for game
screen = pygame.display.set_mode((WIDTH,HEIGHT))

#colors for sprite
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (50,0,200)


#change paddle's location for y axis
def updatePaddle(action, paddleY):
    
    #up
    if action == 0:
        paddleY.rect.y -= 4
      
    #just stop    
    if action == 1:
        return
       
    #down    
    if action == 2:
        paddleY.rect.y += 4
    
    
    #for the control of paddle's fitting in screen
    if paddleY.rect.y < 0:  
        paddleY.rect.y = 0
    
    if paddleY.rect.y > HEIGHT:
        paddleY.rect.y = HEIGHT
    
    return paddleY.rect.y


class GAME:
    
    class paddle(pygame.sprite.Sprite):
        def __init__(self,color):
           pygame.sprite.Sprite.__init__(self)
           self.image = pygame.Surface([WIDTH/40,HEIGHT/4.5])
           self.image.fill(color)
           self.rect = self.image.get_rect()
           

    class ball(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([WIDTH/40,WIDTH/40])
            self.image.fill(red)
            self.rect = self.image.get_rect()
            
            #initial axis speeds
            self.Xspeed = 3
            self.Yspeed = 3
    
    
    def __init__(self):
        
        #creating classes
        self.pedal1 = self.paddle(blue)
        self.pedal2 = self.paddle(blue)
        self.BALL = self.ball()
        
        
        #pedal1 location. 
        self.pedal1.rect.x = WIDTH/50 #25
        self.pedal1.rect.y = random.randint(0,HEIGHT/10)*10 #300
        
        #pedal2 location
        self.pedal2.rect.x = 23*WIDTH/24 #575
        self.pedal2.rect.y =  random.randint(0,HEIGHT/10)*10
        
        #ball location
        self.BALL.rect.x = WIDTH/2
        self.BALL.rect.y = HEIGHT/4 + random.randint(0, int(3/4*HEIGHT))
        
        #for process of drawing screen objects
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.pedal1, self.pedal2, self.BALL)
        
                

    def InitialDisplay(self):
       
        run = True
        while run:
            
            #refrehsiing screen, and putting objects again every per unit time.
            screen.fill(black)
            
            #drawing objects to screen
            self.all_sprites.draw(screen)
            
            #game speed
            pygame.time.delay(10)
            
            #for exit buttons working properly
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        
           
            pygame.display.update()
                
            
            #balls movement 
            self.BALL.rect.x += self.BALL.Xspeed
            self.BALL.rect.y += self.BALL.Yspeed 
    
        
            # synchronous movement of the ball and the paddle 
            self.pedal2.rect.y = self.BALL.rect.y - (WIDTH/40) #40, top yuksekligi
            
            
            ###Skor control
            if self.BALL.rect.x <= WIDTH/120:    
                    #reset settings
                 self.BALL.rect.x = WIDTH/2 
                 self.BALL.rect.y = HEIGHT/4 + random.randint(0, int(3/4*HEIGHT))
                
                    #when its reset, ball has to do move different sides for every after score
                 self.BALL.Xspeed = random.sample([-self.BALL.Xspeed,self.BALL.Xspeed],1)[0]
                 self.BALL.Yspeed = random.sample([-self.BALL.Yspeed,self.BALL.Yspeed],1)[0]
                
            
            
            #same score control for other side
            if self.BALL.rect.x >= WIDTH*39/40:
                self.BALL.rect.x = WIDTH/2 
                self.BALL.rect.y = HEIGHT/4 + random.randint(0, int(3/4*HEIGHT))
        
                self.BALL.Xspeed = random.sample([-self.BALL.Xspeed,self.BALL.Xspeed],1)[0]
                self.BALL.Yspeed = random.sample([-self.top.Yspeed,self.BALL.Yspeed],1)[0]
                #skor sol
                
                
            key = pygame.key.get_pressed()
            #control paddle
            if key[pygame.K_w]:
                #self.pedal1.rect.y -+= 4
                updatePaddle(0, self.pedal1)
                
            if key[pygame.K_s]:
                updatePaddle(2, self.pedal1)
            
            
            
            #after collide peddals
            if self.pedal1.rect.colliderect(self.BALL.rect):
                self.BALL.Xspeed *= -1
                
            if self.pedal2.rect.colliderect(self.BALL.rect):
                self.BALL.Xspeed *= -1
                
            
            #if ball is at bound sections, turn back it to game 
            if self.BALL.rect.y > HEIGHT - (WIDTH/40) or self.BALL.rect.y < WIDTH/200: #435 or self.top.rect.y < 3
                 self.BALL.Yspeed *= -1    
    
    
    
    
     
    
pg = GAME()
pg.InitialDisplay()
pygame.quit()
    