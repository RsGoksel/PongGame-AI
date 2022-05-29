import gym
from gym import spaces

import pygame
import random
import numpy as np

HEIGHT = 450
WIDTH = 600

screen = pygame.display.set_mode((WIDTH,HEIGHT))

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (50,0,200)


def updatePaddle(action, paddleY):
    
    
    if action == 0:
        paddleY.rect.y -= 4
        
    if action == 1:
        return
       
    if action == 2:
        paddleY.rect.y += 4
    
      
    if paddleY.rect.y < 0:  
        paddleY.rect.y = 0
    
    if paddleY.rect.y > HEIGHT:
        paddleY.rect.y = HEIGHT
    
    return paddleY.rect.y


class PongEnv(gym.Env):
  
    metadata = {'render.modes': ['human']}
      
    
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
            self.Xspeed = 3
            self.Yspeed = 3
    
    
    def __init__(self):
        super(PongEnv, self).__init__()
        
        self.reward = 0
        self.done = False
        self.score = 0
        
        self.action_space = spaces.Discrete(3)
        
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(1,HEIGHT, WIDTH), dtype=np.float32)
    
    
        self.pedal1 = self.paddle(blue)
        self.pedal2 = self.paddle(blue)
        self.BALL = self.ball()
        
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.pedal1, self.pedal2, self.BALL)
        
        #paddle1 and paddle2(bot) location
        self.pedal1.rect.x = WIDTH/50 #25
        self.pedal1.rect.y = random.randint(0,HEIGHT/10)*10 #300
        
        self.pedal2.rect.x = 23*WIDTH/24 #575
        self.pedal2.rect.y =  random.randint(0,HEIGHT/10)*10
        
        
        #ball location. at the beginning of each round, the ball's destination flank changes
        self.BALL.rect.x = WIDTH/2
        self.BALL.rect.y = HEIGHT/4 + random.randint(0, int(3/4*HEIGHT))
        
        self.BALL.Xspeed = random.sample([-self.BALL.Xspeed,self.BALL.Xspeed],1)[0]
        self.BALL.Yspeed = random.sample([-self.BALL.Yspeed,self.BALL.Yspeed],1)[0]
        
        
    def step(self, action):
        
        
        self.BALL.rect.x += self.BALL.Xspeed
        self.BALL.rect.y += self.BALL.Yspeed 
        
        self.pedal2.rect.y = self.BALL.rect.y - (WIDTH/40)
        
        
        if action==0:
            #self.pedal1.rect.y -+= 4
            updatePaddle(0, self.pedal1)
            
        if action==2:
            updatePaddle(2, self.pedal1)
        
       
        #if ball hits pedal1, score for paddle because its is exactly what we want
        if self.pedal1.rect.colliderect(self.BALL.rect):
            self.BALL.Xspeed *= -1
            self.score += 5
            self.reward = self.score
            
            
        #collider with paddle2
        if self.pedal2.rect.colliderect(self.BALL.rect):
            self.BALL.Xspeed *= -1 
       
        #control for ball and boundries
        if self.BALL.rect.y > HEIGHT - (WIDTH/40) or self.BALL.rect.y < WIDTH/200: #435 or self.top.rect.y < 3
             self.BALL.Yspeed *= -1
             
             #its negative score for agent.
        if self.BALL.rect.x <= WIDTH/120:    #self.pedal1.rect.x yazılabilirdi fakat const değişken ile 
             self.score -= 10
             self.reward = self.score
             done = True
    
        self.observation = [self.pedal1.rect.x, self.pedal1.rect.y, self.BALL.rect.x, self.BALL.rect.y] 
        self.observation = np.array(self.observation)
        
        
        info = {}
        return self.observation, self.reward, self.done, info        
        
          
    def reset(self):
        self.done = False
        self.score = 0
        
        
        self.pedal1.rect.x = WIDTH/50 #25
        self.pedal1.rect.y = random.randint(0,HEIGHT/10)*10 #300
        
        
        self.pedal2.rect.x = 23*WIDTH/24 #575
        self.pedal2.rect.y =  random.randint(0,HEIGHT/10)*10
        
        
        self.BALL.rect.x = WIDTH/2
        self.BALL.rect.y = HEIGHT/4 + random.randint(0, int(3/4*HEIGHT))
        
        self.BALL.Xhiz = random.sample([-self.BALL.Xspeed,self.BALL.Xspeed],1)[0]
        self.BALL.Yhiz = random.sample([-self.BALL.Yspeed,self.BALL.Yspeed],1)[0]
        
        self.observation = [self.pedal1.rect.x, self.pedal1.rect.y, self.BALL.rect.x, self.BALL.rect.y] 
        self.observation = np.array(self.observation)
        
        return self.observation  # reward, done, info can't be included
       
            
        
    def render(self, mode='human'):
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.init()
        pygame.display.init()
           
    
        
        while True: 
            
            pygame.time.delay(10)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                
            pygame.display.update()
    
            self.ekran.fill(black)
            self.all_sprites.draw(self.screen)
            #self.step(0)
    
    def close (self):
        if self.screen is not None:
            pygame.display.quit()
            pygame.quit()




