import numpy as np
import pygame
import random
from os import path
from math import *

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 1200
HEIGHT = 700
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 200, 210)

CannonCenter = [WIDTH/2, HEIGHT-30]
spawn_interval = 5 * 30 

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("20191235 김시리")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def getRectangle(width=40, height=10, d=0, x=0, y=0):
    v=np.array([[x,       y],
                [x+width, y-d],
                [x+width, y+height+d],
                [x,       y+height]],
                dtype = 'float')
    return v

def R3mat(deg): 
    theta = np.deg2rad(deg)
    c = np.cos(theta)
    s = np.sin(theta)
    R = np.array([[ c, -s, 0], 
                  [ s,  c, 0],
                  [ 0,  0, 1] ])
    return R

def T3mat(a,b): 
    t = np.eye(3)
    t[0,2] = a
    t[1,2] = b
    return t

def draw(M, points, color=(0,0,0)):
    R = M[0:2,0:2]
    t = M[0:2,2]
    points_transformed = (R @ points.T).T + t

    pygame.draw.polygon(screen, BLACK, points_transformed) #, width=3)

def draw_rounded_rect(surface, color, rect, radius, border_width=0):
    x, y, width, height = rect
    
    pygame.draw.rect(screen, color, pygame.Rect(x+ radius, y, width- radius*2, height), border_width)
    pygame.draw.rect(screen, color, pygame.Rect(x, y+ radius, width, height- radius*2), border_width)

    pygame.draw.circle(surface, color, (x + radius, y + radius), radius, border_width)
    pygame.draw.circle(surface, color, (x + width - radius, y + radius), radius, border_width)
    pygame.draw.circle(surface, color, (x + radius, y + height - radius), radius, border_width)
    pygame.draw.circle(surface, color, (x + width - radius, y + height - radius), radius, border_width)

class Cannon:
    def __init__(self):
        self.direction_angle = -45.
        self.position = np.array(CannonCenter, dtype='float')
        self.mag = 20 #발사대 길이
        self.rect = getRectangle(self.mag * 5, height=20, d=0, x=0, y=0)
    
    def draw(self, screen):
        M = T3mat(CannonCenter[0],CannonCenter[1]) @ R3mat(self.direction_angle) @T3mat(0,-10)
        draw(M, self.rect, BLACK)
        pygame.draw.circle(screen, BLACK, CannonCenter, 15)
       
class Bubble:
    def __init__(self):

        self.radius = 50.
        self.txy = np.array([self.radius, self.radius])
        self.vxy = np.array([0.0, 0.0])
        self.axy = np.array([0.0, 0.5])
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, (0, 0, 255, 64), self.txy, self.radius)
        self.rect = self.surface.get_rect(center=(self.txy[0],self.txy[1])) 
        self.active = True

    def update(self):
        self.txy += self.vxy
        self.vxy += self.axy


        if self.txy[0] - self.radius < -100:
            self.active = False
        if self.txy[0] + self.radius > WIDTH+100:
            self.active = False
        if self.txy[1] + self.radius > HEIGHT+100:
            self.active = False
        if self.txy[1] - self.radius < -100:
            self.active = False

    def draw(self, screen):
        if self.active:
            #pygame.draw.circle(screen, (0,0,255), self.txy, self.radius )
            pygame.draw.circle(self.surface, (0, 0, 255, 64), self.txy, self.radius)
            self.rect = self.surface.get_rect(center=(self.txy[0],self.txy[1]))
            screen.blit(self.surface, self.rect)
    

class Puppy:
    ''' Specify properties of balloons in start function '''
    def __init__(self, speed):
        self.faceLen = 60
        self.earA = 40 
        self.earB = 10 
        self.x = random.randrange(50, WIDTH - self.faceLen -50)
        self.y = random.randrange(50, HEIGHT - self.faceLen- 50)
        self.angle = 90
        self.speed = -speed
        self.proPool= [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.color = WHITE
        self.angle1 = -90
        self.angle2 = 0
        self.center1 = [0.0,0.0]
        self.center2 = [0.0,0.0]
        self.ear = getRectangle(self.earA,self.earB,5)
        
    def update(self, timer):
        direct = random.choice(self.proPool)

        if timer % 8 ==0 : 
            self.angle1 = -90
            self.angle2 = -90
        elif timer % 8==2:
            self.angle1 = -120
            self.angle2 = -60
        elif timer % 8==4:
            self.angle1 = -150
            self.angle2 = -30
        elif timer %8 ==6 :
            self.angle1 = -180
            self.angle2 = 0


        if direct == -1:
            self.angle += -10
        elif direct == 0:
            self.angle += 0
        else:
            self.angle += 10

        
        self.y += self.speed*sin(radians(self.angle))
        self.x += self.speed*cos(radians(self.angle))

        if (self.x + self.faceLen + 10 > WIDTH) or (self.x-10 < 0):
            self.x -= self.speed*cos(radians(self.angle)) 
            
        if (self.y + self.faceLen +10 < 0) or self.y -50 > HEIGHT:
            self.reset()
            
    def draw(self,screen):

        
        M1 = T3mat(self.x, self.y) @ T3mat(15,10) @R3mat(self.angle1) @T3mat(-5,-self.earB/2.) 
        self.center1 = M1[0:2,2]
        M2 = T3mat(self.x, self.y) @ T3mat(self.faceLen-15,10) @R3mat(self.angle2) @T3mat(-5,-self.earB/2.) 
        self.center2 = M2[0:2,2]


        draw_rounded_rect(screen, WHITE, [self.x, self.y, 60, 60], 20)
        pygame.draw.circle(screen, BLACK,(self.x+22,self.y+40), 3)
        pygame.draw.circle(screen, BLACK,(self.x+38,self.y+40), 3)
        pygame.draw.ellipse(screen, BLACK, (self.x+30-5,self.y+55, 10, 5))


        draw(M1, self.ear, BLACK)
        draw(M2, self.ear, BLACK)
        #pygame.draw.rect(screen, BLACK, pygame.Rect(self.x, self.y, 60, 60), 3)

    # def trap(self):
    #     global score
    #     pos = pygame.mouse.get_pos()

    #     if isonBalloon(self.x, self.y, self.a, self.b, pos):
    #         score += 1
    #         self.reset()
              
    def reset(self):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(100, WIDTH - self.a -50)
        self.y = HEIGHT - 50
        self.angle = 90
        self.speed -= 0.002
        self.proPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = WHITE



def bubble_pop(x, y, r, pos):
    if np.sqrt((x-pos[0]) ** 2 + (y-pos[1]) ** 2)< r:
        return True
    else:
        return False

def collosion_circle(c, p):  
    d12 = c.txy - p.txy
    d12mag = np.sqrt(d12[0] ** 2 + d12[1] ** 2)
    r12 = c.radius + p.radius
    if d12mag < r12:
        return True
    else:
        return False

def collision_check(c, polygon_list):  
    clist = []
    for p in polygon_list:
        if collosion_circle(c, p):
            clist.append(p)
            
    return clist

mouse_img = pygame.image.load(path.join(img_dir, "mouse.png")).convert_alpha()
mouse_s_img = pygame.transform.scale(mouse_img, (30, 30))
pygame.mouse.set_visible(False)

bubble_sound = pygame.mixer.Sound(path.join(snd_dir, 'bubbles.mp3'))




def main():

    cannon = Cannon()
    bubble_list = []
    dog_list = []
    dogsNum = 3

    for _ in range(dogsNum):
        puppy = Puppy(random.choice([1, 1, 2, 2, 2, 2, 3, 3, 3, 4]))
        dog_list.append(puppy)
    
    timer = 0
    hits = 0

    done = False
    while not done:
        timer += 1 


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_LEFT:
                    cannon.direction_angle -= 3
                elif event.key == pygame.K_RIGHT:
                    cannon.direction_angle += 3
                elif event.key == pygame.K_SPACE:
                    bubble_sound.play()
                    bubble = Bubble()

                    bubble.txy = cannon.position.copy()
                    rad = np.deg2rad(cannon.direction_angle)
                    vxy_mag = cannon.mag
                    bubble.vxy = np.array([np.cos(rad), np.sin(rad)]) * vxy_mag
                    bubble_list.append(bubble)

 
        for bubble in bubble_list:
            bubble.update()

        


        pos = pygame.mouse.get_pos()
        mouse_x = pos[0]
        mouse_y = pos[1]

        screen.fill(PINK)
        draw_text(screen, "siri!", 64, WIDTH / 2, HEIGHT / 4)
        screen.blit(mouse_s_img, [mouse_x-10, mouse_y-10])  

        for bubble in bubble_list:
            bubble.draw(screen)

        for puppy in dog_list:
            puppy.update(timer)
            puppy.draw(screen)

        
        cannon.draw(screen)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
