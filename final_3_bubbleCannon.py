import numpy as np
import pygame
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 1200
HEIGHT = 700
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 200, 210)

CannonCenter = [50.0, 350.0]
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
    
    def draw(self, screen):
        rad = np.deg2rad(self.direction_angle)
        self.endposition = self.position + self.mag * np.array([np.cos(rad),np.sin(rad)]) * 3
        pygame.draw.line(screen, BLACK, self.position, self.endposition, 20)
       
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
                elif event.key == pygame.K_UP:
                    cannon.direction_angle -= 3
                elif event.key == pygame.K_DOWN:
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

        screen.fill(WHITE)
        draw_text(screen, "siri!", 64, WIDTH / 2, HEIGHT / 4)
        screen.blit(mouse_s_img, [mouse_x-10, mouse_y-10])  

        for bubble in bubble_list:
            bubble.draw(screen)

        pygame.draw.circle(screen, BLACK, CannonCenter, 10)
        cannon.draw(screen)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
