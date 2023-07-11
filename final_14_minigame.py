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

CannonCenter = [WIDTH/2, HEIGHT-50]
spawn_interval = 5 * FPS

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("20191235 김시리")
clock = pygame.time.Clock()


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

    pygame.draw.polygon(screen, color, points_transformed) #, width=3)

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
        self.color = BLACK
    
    def draw(self, screen):
        M = T3mat(self.position[0],self.position[1]) @ R3mat(self.direction_angle) @T3mat(0,-10)
        draw(M, self.rect, self.color)
        pygame.draw.circle(screen, self.color, self.position, 15)

def clik(x1, y1, x2, y2, r): 

    d = np.sqrt((x1-x2)** 2 + (y1-y2) ** 2)
    if d < r:
        return True
    else:
        return False



class EYENOSE:
    def __init__(self):

        self.radius = 10.
        self.txy = np.array([self.radius, self.radius])
        self.vxy = np.array([0.0, 0.0])
        self.axy = np.array([0.0, 0.5])
        self.active = True
        self.type_eye = True
        
    def update(self):
        
        self.txy += self.vxy
        self.vxy += self.axy

        if self.txy[0]  < -100:
            self.active = False
        if self.txy[0]  > WIDTH:
            self.active = False
        if self.txy[1] > HEIGHT:
            self.active = False
        if self.txy[1]  < -100:
            self.active = False

    def draw(self, screen):
        if self.active:
            if self.type_eye:
                pygame.draw.circle(screen, BLACK, self.txy, self.radius)
            else:
                pygame.draw.ellipse(screen, BLACK, (self.txy[0]-25,self.txy[1], 50, 25))
                #pygame.draw.circle(screen, (255,0,0), self.txy, self.radius)
 

mouse_img = pygame.image.load(path.join(img_dir, "mouse.png")).convert_alpha()
mouse_s_img = pygame.transform.scale(mouse_img, (30, 30))
pygame.mouse.set_visible(False)

mini_img = pygame.image.load(path.join(img_dir, "minigame.png"))
mini_s_img = pygame.transform.scale(mini_img, (WIDTH, HEIGHT))
mini_rect = mini_s_img.get_rect()

cannon = Cannon()
eye_list = [] 
eye = []
nose_list = []
nose = []

cannon.color = WHITE
cannon.position = np.array([WIDTH/6, HEIGHT/2.+200], dtype='float')

angle1 = -120
angle2 = -60
timer = 0

waiting = True
while waiting:
    timer+=1
    pos = pygame.mouse.get_pos()
    mouse_x = pos[0]
    mouse_y = pos[1]
    
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if clik(WIDTH/2, HEIGHT-150, mouse_x, mouse_y, 60):
                waiting = False
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_q:
                obj = EYENOSE() #eye
                obj.type_eye = True
                obj.txy = cannon.position.copy()
                rad = np.deg2rad(cannon.direction_angle)
                vxy_mag = cannon.mag
                obj.vxy = np.array([np.cos(rad), np.sin(rad)]) * vxy_mag 
                eye_list.append(obj)
            
            if event.key == pygame.K_w:
                obj = EYENOSE()
                obj.type_eye = False #nose
                obj.txy = cannon.position.copy()
                rad = np.deg2rad(cannon.direction_angle)
                vxy_mag = cannon.mag
                obj.vxy = np.array([np.cos(rad), np.sin(rad)]) * vxy_mag 
                nose_list.append(obj)

            if event.key == pygame.K_a:
                for obj in eye_list:
                    if obj.active:
                        txy = obj.txy.copy()
                        obj.active = False
                        eye.append(txy)
            
            if event.key == pygame.K_s:
                for obj in nose_list:
                    if obj.active:
                        txy = obj.txy.copy()
                        obj.active = False
                        nose.append(txy)
    
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_LEFT]:
        cannon.direction_angle -= 3
    if keystate[pygame.K_RIGHT]:
        cannon.direction_angle += 3
    if keystate[pygame.K_SPACE]:
        if timer % 16 ==0 : 
            angle1 = -90
            angle2 = -90
        elif timer % 16==4:
            angle1 = -120
            angle2 = -60
        elif timer % 16==8:
            angle1 = -150
            angle2 = -30
        elif timer %16 ==12:
            angle1 = -180
            angle2 = 0
    
    
    for obj in eye_list:
        obj.update()
    for obj in nose_list:
        obj.update()
    
    screen.blit(mini_s_img, mini_rect) 
    #pygame.draw.circle(screen, (255,0,0), (WIDTH-150, HEIGHT-80),60)
    draw_rounded_rect(screen, WHITE, [3*WIDTH/5.-100,HEIGHT/2.-150,300,300], 100, border_width=0)

    M1 = T3mat(3*WIDTH/5.-100,HEIGHT/2.-150) @ T3mat(15*5,10*5) @R3mat(angle1) @T3mat(-5,-10*5/2.) 
    M2 = T3mat(3*WIDTH/5.-100,HEIGHT/2.-150) @ T3mat(300-15*5,10*5) @R3mat(angle2) @T3mat(-5,-10*5/2.) 
    earRec = getRectangle(40*5,10*5,5*5)
    draw(M1, earRec, BLACK)
    draw(M2, earRec, BLACK)

    cannon.draw(screen)
    
    for p in eye:
        pygame.draw.circle(screen, BLACK, p, 10)
    for p in nose:
        pygame.draw.ellipse(screen, BLACK, (p[0]-25,p[1], 50, 25))
    
    for obj in eye_list:
        obj.draw(screen)
    for obj in nose_list:
        obj.draw(screen)
    
    screen.blit(mouse_s_img, [mouse_x-10, mouse_y-10])  

    pygame.display.flip()