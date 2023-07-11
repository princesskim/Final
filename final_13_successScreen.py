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
        M = T3mat(self.position[0],self.position[1]) @ R3mat(self.direction_angle) @T3mat(0,-10)
        draw(M, self.rect, BLACK)
        pygame.draw.circle(screen, BLACK, self.position, 15)
       
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
        self.trap = False
        self.pop=False
        self.freeze = 5 * FPS #버블에 가두는 시간 5초
        #self.puppy = None

    def update(self):
        if self.trap :
            self.txy += np.array([0.0, 3.0])
            if self.txy[1] + self.radius >= HEIGHT:
                self.txy[1] = HEIGHT-self.radius
                self.pop=True
                self.freeze -=2
                if self.freeze <=0:
                    self.active = False

        else:
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

    def POP(self, pos):
        if np.sqrt((self.txy[0]-pos[0]) ** 2 + (self.txy[1]-pos[1]) ** 2)< self.radius:
            self.active = False
            return True
        else:
            return False
    
    def draw(self, screen):
        if self.active:
            #pygame.draw.circle(screen, (0,0,255), self.txy, 10 )
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
        self.angle1 = 0
        self.angle2 = 0
        self.center1 = [0.0,0.0]
        self.center2 = [0.0,0.0]
        self.ear = getRectangle(self.earA,self.earB,5)
        self.center = [self.x+self.faceLen/2., self.y+self.faceLen/2.]
        self.fly = True
        self.active = True
        self.pop = False
        self.freeze = 5 * FPS #버블에 가두는 시간 5초

    def update(self, timer):
  
        if self.fly:
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
            self.center = [self.x+self.faceLen/2., self.y+self.faceLen/2.]

            if (self.x + self.faceLen + 10 > WIDTH) or (self.x-10 < 0):
                self.x -= self.speed*cos(radians(self.angle)) 
                
            if (self.y + self.faceLen +10 < 0) or self.y -50 > HEIGHT:
                self.reset()
    

        else:
            self.angle1 = -90
            self.angle2 = -90
            self.y += 3
            self.center = [self.x+self.faceLen/2., self.y+self.faceLen/2.]

            if self.center[1]+50  >= HEIGHT:
                self.y = HEIGHT-50. -self.faceLen/2.
                self.pop = True
                self.freeze -=2
                if self.freeze <=0:
                    self.fly = True
                    self.freeze = 5 * FPS 
                    self.pop = False

    def POP(self, pos):
        if np.sqrt((self.center[0]-pos[0]) ** 2 + (self.center[1]-pos[1]) ** 2)< 50:
            self.active = False
            return True
        else:
            return False
            
    def draw(self,screen):

        if self.active:
        
            M1 = T3mat(self.x, self.y) @ T3mat(15,10) @R3mat(self.angle1) @T3mat(-5,-self.earB/2.) 
            self.center1 = M1[0:2,2]
            M2 = T3mat(self.x, self.y) @ T3mat(self.faceLen-15,10) @R3mat(self.angle2) @T3mat(-5,-self.earB/2.) 
            self.center2 = M2[0:2,2]

            draw_rounded_rect(screen, WHITE, [self.x, self.y, 60, 60], 20)
            pygame.draw.circle(screen, BLACK,(self.x+22,self.y+40), 3)
            pygame.draw.circle(screen, BLACK,(self.x+38,self.y+40), 3)
            pygame.draw.ellipse(screen, BLACK, (self.x+30-5,self.y+55, 10, 5))
            #pygame.draw.rect(screen, BLACK, pygame.Rect(self.x, self.y, 60, 60), 3)
            #pygame.draw.circle(screen, BLACK,self.center, 5)

            draw(M1, self.ear, BLACK)
            draw(M2, self.ear, BLACK)
        # if  self.pop:
        #      pygame.draw.circle(screen, (255,0,0),self.center, 50)
     
    def reset(self):
        self.x = random.randrange(50, WIDTH - self.faceLen -50)
        self.y = HEIGHT - 50
        self.angle = 90
        self.speed -= 0.002
        self.proPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]

class tutorial_3_puppy:
    def __init__(self):
        self.faceLen = 60
        self.earA = 40 
        self.earB = 10 
        self.x = WIDTH/2. - self.faceLen/2.
        self.y = HEIGHT/2. - self.faceLen/2.
        self.move = 3
        self.color = WHITE
        self.angle1 = -120
        self.angle2 = -60
        self.center1 = [0.0,0.0]
        self.center2 = [0.0,0.0]
        self.ear = getRectangle(self.earA,self.earB,5)
        self.center = [self.x+self.faceLen/2., self.y+self.faceLen/2.]

    def update(self, timer):

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

def colli_BP(bubble, puppy):   
    if puppy.fly==True and puppy.active==True and bubble.trap==False :
        d = np.sqrt((bubble.txy[0]-puppy.center[0]) ** 2 + (bubble.txy[1]-puppy.center[1]) ** 2)

        if d < bubble.radius:
            puppy.fly = False
            bubble.trap = True
            bubble.txy = puppy.center.copy()
            return True

    return False

def clik(x1, y1, x2, y2, r): 

    d = np.sqrt((x1-x2)** 2 + (y1-y2) ** 2)
    if d < r:
        return True
    else:
        return False

mouse_img = pygame.image.load(path.join(img_dir, "mouse.png")).convert_alpha()
mouse_s_img = pygame.transform.scale(mouse_img, (30, 30))

tuto1_img = pygame.image.load(path.join(img_dir, "tuto1.png"))
tuto1_s_img = pygame.transform.scale(tuto1_img, (WIDTH, HEIGHT))
tuto1_rect = tuto1_s_img.get_rect()
tuto2_img = pygame.image.load(path.join(img_dir, "tuto2.png"))
tuto2_s_img = pygame.transform.scale(tuto2_img, (WIDTH, HEIGHT))
tuto2_rect = tuto2_s_img.get_rect()
tuto3_img = pygame.image.load(path.join(img_dir, "tuto3.png"))
tuto3_s_img = pygame.transform.scale(tuto3_img, (WIDTH, HEIGHT))
tuto3_rect = tuto3_s_img.get_rect()
tuto4_img = pygame.image.load(path.join(img_dir, "tuto4.png"))
tuto4_s_img = pygame.transform.scale(tuto4_img, (WIDTH, HEIGHT))
tuto4_rect = tuto4_s_img.get_rect()
tuto5_img = pygame.image.load(path.join(img_dir, "tuto5.png"))
tuto5_s_img = pygame.transform.scale(tuto5_img, (WIDTH, HEIGHT))
tuto5_rect = tuto5_s_img.get_rect()
tuto6_img = pygame.image.load(path.join(img_dir, "tuto6.png"))
tuto6_s_img = pygame.transform.scale(tuto6_img, (WIDTH, HEIGHT))
tuto6_rect = tuto6_s_img.get_rect()

suc1_img = pygame.image.load(path.join(img_dir, "suc1.png"))
suc1_s_img = pygame.transform.scale(suc1_img, (WIDTH, HEIGHT))
suc1_rect = suc1_s_img.get_rect()
suc2_img = pygame.image.load(path.join(img_dir, "suc2.png"))
suc2_s_img = pygame.transform.scale(suc2_img, (WIDTH, HEIGHT))
suc2_rect = suc2_s_img.get_rect()
pygame.mouse.set_visible(False)

bubble_sound = pygame.mixer.Sound(path.join(snd_dir, 'bubbles.mp3'))

def tutorial_1_screen(): # title 

    waiting = True
    while waiting:
        pos = pygame.mouse.get_pos()
        mouse_x = pos[0]
        mouse_y = pos[1]
        screen.blit(tuto1_s_img, tuto1_rect) 
        screen.blit(mouse_s_img, [mouse_x-10, mouse_y-10])  
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if clik(WIDTH/2, HEIGHT-150, mouse_x, mouse_y, 60):
                    waiting = False

def tutorial_2_screen(): # 바깥세상이 궁금한 강아지들
    
    puppy = tutorial_3_puppy()
    puppy.y += 20
    puppy.angle1 = -170
    puppy.angle2 = -10
    q_img = pygame.image.load(path.join(img_dir, "Q2.png")).convert_alpha()
    q_s_img = pygame.transform.scale(q_img, (80, 100))

    waiting = True
    while waiting:
        pos = pygame.mouse.get_pos()
        mouse_x = pos[0]
        mouse_y = pos[1]
        screen.blit(tuto2_s_img, tuto2_rect) 
        screen.blit(mouse_s_img, [mouse_x-10, mouse_y-10])  
        screen.blit(q_s_img,[WIDTH/2.-40, HEIGHT/2.-100])
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if clik(WIDTH/2, HEIGHT-150, mouse_x, mouse_y, 60):
                    waiting = False
        puppy.draw(screen)
        pygame.display.flip()

def tutorial_3_screen(): # 스페이스바 누르면 귀 펄럭
    timer=0
    puppy = tutorial_3_puppy()
    waiting = True
    while waiting:
        timer+=1
        pos = pygame.mouse.get_pos()
        mouse_x = pos[0]
        mouse_y = pos[1]
        screen.blit(tuto3_s_img, tuto3_rect) 
        screen.blit(mouse_s_img, [mouse_x-10, mouse_y-10])  
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if clik(WIDTH/2, HEIGHT-150, mouse_x, mouse_y, 60):
                    waiting = False

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            puppy.update(timer)
        puppy.draw(screen)
        pygame.display.flip()

def tutorial_4_screen():

    waiting = True
    while waiting:
        pos = pygame.mouse.get_pos()
        mouse_x = pos[0]
        mouse_y = pos[1]
        screen.blit(tuto4_s_img, tuto4_rect) 
        screen.blit(mouse_s_img, [mouse_x-10, mouse_y-10])  
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if clik(WIDTH/2, HEIGHT-150, mouse_x, mouse_y, 60):
                    waiting = False

def tutorial_5_screen(): # 버블 발사 체험 
    cannon = Cannon()
    bubble_list = []
    cannon.position = np.array([WIDTH/2, HEIGHT-280], dtype='float')
    waiting = True
    while waiting:
        pos = pygame.mouse.get_pos()
        mouse_x = pos[0]
        mouse_y = pos[1]
        screen.blit(tuto5_s_img, tuto5_rect) 
        screen.blit(mouse_s_img, [mouse_x-10, mouse_y-10])  
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if clik(WIDTH/2, HEIGHT-150, mouse_x, mouse_y, 60):
                    waiting = False
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    bubble_sound.play()
                    bubble = Bubble()
                    bubble.txy = cannon.position.copy()
                    rad = np.deg2rad(cannon.direction_angle)
                    vxy_mag = cannon.mag
                    bubble.vxy = np.array([np.cos(rad), np.sin(rad)]) * vxy_mag 
                    bubble_list.append(bubble)
        
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            cannon.direction_angle -= 3
        if keystate[pygame.K_RIGHT]:
            cannon.direction_angle += 3
        
        for bubble in bubble_list:
            bubble.update()
        
        for bubble in bubble_list:
            bubble.draw(screen)


        cannon.draw(screen)
        pygame.display.flip()

def tutorial_6_screen():

    waiting = True
    while waiting:
        pos = pygame.mouse.get_pos()
        mouse_x = pos[0]
        mouse_y = pos[1]
        screen.blit(tuto6_s_img, tuto6_rect) 
        screen.blit(mouse_s_img, [mouse_x-10, mouse_y-10])  
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if clik(WIDTH/2, HEIGHT-150, mouse_x, mouse_y, 60):
                    waiting = False

def success1_screen():

    waiting = True
    while waiting:
        pos = pygame.mouse.get_pos()
        mouse_x = pos[0]
        mouse_y = pos[1]
        screen.blit(suc1_s_img, suc1_rect) 
        screen.blit(mouse_s_img, [mouse_x-10, mouse_y-10])  
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if clik(WIDTH/2, HEIGHT-150, mouse_x, mouse_y, 60):
                    waiting = False

def success2_screen():

    waiting = True
    while waiting:
        pos = pygame.mouse.get_pos()
        mouse_x = pos[0]
        mouse_y = pos[1]
        screen.blit(suc2_s_img, suc2_rect) 
        screen.blit(mouse_s_img, [mouse_x-10, mouse_y-10])  
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if clik(WIDTH/2, HEIGHT-150, mouse_x, mouse_y, 60):
                    waiting = False

def minigame_screen(): # not yet
    cannon = Cannon()
    bubble_list = []
    cannon.position = np.array([WIDTH/2, HEIGHT-280], dtype='float')
    waiting = True
    while waiting:
        pos = pygame.mouse.get_pos()
        mouse_x = pos[0]
        mouse_y = pos[1]
        screen.blit(tuto5_s_img, tuto5_rect) 
        screen.blit(mouse_s_img, [mouse_x-10, mouse_y-10])  
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if clik(WIDTH/2, HEIGHT-150, mouse_x, mouse_y, 60):
                    waiting = False
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    bubble_sound.play()
                    bubble = Bubble()
                    bubble.txy = cannon.position.copy()
                    rad = np.deg2rad(cannon.direction_angle)
                    vxy_mag = cannon.mag
                    bubble.vxy = np.array([np.cos(rad), np.sin(rad)]) * vxy_mag 
                    bubble_list.append(bubble)
        
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            cannon.direction_angle -= 3
        if keystate[pygame.K_RIGHT]:
            cannon.direction_angle += 3
        
        for bubble in bubble_list:
            bubble.update()
        
        for bubble in bubble_list:
            bubble.draw(screen)


        cannon.draw(screen)
        pygame.display.flip()


def main():

    tuto1_run = True
    tuto2_run = False
    tuto3_run = False
    tuto4_run = False
    tuto5_run = False
    tuto6_run = False
    success1_run = False
    success2_run = False
    minigame_run = False




    cannon = Cannon()
    bubble_list = []
    dog_list = []
    dogsNum = 10

    for _ in range(dogsNum):
        puppy = Puppy(random.choice([1, 1, 2, 2, 2, 2, 3, 3, 3, 4]))
        dog_list.append(puppy)
    
    timer = 0 #귀 펄럭용
    timer2 = 0
    #dogs=0


    done = False
    while not done:
        timer += 1 

        # if timer % spawn_interval == 3:
        #     if dogs<100:
        #         for _ in range(5):
        #             dogs+=5
        #             puppy = Puppy(random.choice([1, 1, 2, 2, 2, 2, 3, 3, 3, 4]))
        #             dog_list.append(puppy)

        pos = pygame.mouse.get_pos()


        if tuto1_run:
            tutorial_1_screen()
            tuto1_run = False
            tuto2_run = True
            continue
    
        elif tuto2_run:
            tutorial_2_screen()
            tuto2_run = False
            tuto3_run = True
            continue

        elif tuto3_run:
            tutorial_3_screen()
            tuto3_run = False
            tuto4_run = True
            continue

        elif tuto4_run:
            tutorial_4_screen()
            tuto4_run = False
            tuto5_run = True
            continue

        elif tuto5_run:
            tutorial_5_screen()
            tuto5_run = False
            tuto6_run = True
            continue

        elif tuto6_run:
            tutorial_6_screen()
            tuto6_run = False

        elif success1_run :
            success1_screen()
            success1_run = False
            success2_run = True
            continue

        elif success2_run :
            success2_screen()
            success2_run = False
            minigame_run = True
            continue

        elif minigame_run :
            minigame_screen()
            done = True #게임 끝


            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for bubble in bubble_list:
                    if bubble.pop:
                        bubble.POP(pos)
                for puppy in dog_list:       
                    if puppy.pop:
                        puppy.POP(pos)
                            

        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_SPACE:
                    bubble_sound.play()
                    bubble = Bubble()
                    bubble.txy = cannon.position.copy()
                    # bubble.txy[0] += cannon.mag * np.cos(cannon.direction_angle)
                    # bubble.txy[1] += cannon.mag * np.sin(cannon.direction_angle)
                    rad = np.deg2rad(cannon.direction_angle)
                    vxy_mag = cannon.mag
                    bubble.vxy = np.array([np.cos(rad), np.sin(rad)]) * vxy_mag 
                    bubble_list.append(bubble)
        
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            cannon.direction_angle -= 3
        if keystate[pygame.K_RIGHT]:
            cannon.direction_angle += 3
        
        for bubble in bubble_list:
            for puppy in dog_list:
                if colli_BP(bubble, puppy): #,dog_list):
                    break #버블 하나당 퍼피 한마리


        # bubble_list = [b for b in bubble_list if b.active ]
        # dog_list = [d for d in dog_list if d.active]

        for bubble in bubble_list:
            bubble.update()

        for puppy in dog_list:
            puppy.update(timer)

        count=0
        for puppy in dog_list:
            if puppy.active == False:
                count+=1
        if count==dogsNum:
            timer2+=1

        if timer2>= 2*FPS: 
            success1_run=True
    
        mouse_x = pos[0]
        mouse_y = pos[1]

        screen.fill(PINK)

        for puppy in dog_list:
            puppy.draw(screen)

        for bubble in bubble_list:
            bubble.draw(screen)

        
 
        screen.blit(mouse_s_img, [mouse_x-10, mouse_y-10])  
        cannon.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()