import random
import pygame
import pygame.freetype
from pygame.locals import *

pygame.init()
SIZE = WIDTH, HEIGHT = 552, 552
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("分屏酷跑")

# 颜色定义
white = (255, 255, 255)
black = (0, 0, 0)
gray = (230, 230, 230)
dark_gray = (40, 40, 40)
dark_green = (0, 155, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 230)
dark_blue =(0,0, 139)
blue_gray = (68, 85, 102)
ice_blue = (176, 224, 230)
dark_green_blue = (47, 79, 79)

BG_COLOR = white #游戏背景颜色

f1 = pygame.freetype.Font("./MSYH.TTC", 36)   # 形成 Font 对象
f2 = pygame.freetype.Font("./MSYH.TTC", 24)   # 形成 Font 对象

class Runway:
    def __init__(self, width: int, height: int, 
                 man_width: int, man_height: int, 
                 pos_x: int, pos_y: int, jump_key, barrier_color, image, bg_image) -> None:
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.jump_key = jump_key
        self.barrier_color = barrier_color
        self.current_speed = 5
        self.miles = 0
        self.game_over = False
        self.barriers = []
        self.barrier_size = 10, 20
        self.clock = pygame.time.Clock()
        self.background = pygame.transform.scale(bg_image, (2 * WIDTH, HEIGHT / 2))
        self.bg_x = 0
        self.man_width = man_width
        self.man_height = man_height
        self.man = pygame.transform.scale(image, (self.man_width, self.man_height))
        self.man_rect = self.man.get_rect()
        self.man_x = random.randint(int(width / 10), int(width / 8)) + self.pos_x
        self.man_y = self.height + self.pos_y - 10
        self.man_rect.bottom = self.man_y
        self.man_rect.left = self.man_x
        self.move_len = 10
        self.man_down_len = 20
        self.man_down_count = 1
        # 初始化生成3个障碍物
        while len(self.barriers) < 3:
            self.generate_barrier()
            
    def generate_barrier(self):
        if not self.barriers:
            x = random.randint(self.man_x + self.man_width * 4, self.man_x + self.man_width * 6)
            l = random.randint(self.barrier_size[1], self.height - 4 * self.man_height)
            y = random.randint(self.pos_y, self.man_y - l)
            self.barriers.append([x, y, l])
        else:
            last_x = self.barriers[-1][0]
            if int(last_x + self.man_width * 2) < self.width:
                x = random.randint(int(last_x + self.man_width * 4), int(last_x + self.man_width * 6))
                if x <= self.pos_x + self.width - self.barrier_size[0]:
                    l = random.randint(self.barrier_size[1], self.height - 4 * self.man_height)
                    y = random.randint(self.pos_y, self.man_y - l)
                    self.barriers.append([x, y, l])
        
    def move(self):
        rm_ids = []
        for idx, barrier in enumerate(self.barriers):
            barrier[0] -= self.move_len
            if barrier[0] <= self.pos_x:
                rm_ids.append(idx)
            else:
                self.barriers[idx][0] = barrier[0]
        if rm_ids:
            for id in rm_ids:
                self.barriers.pop(id)
        if self.pos_y <= self.man_rect.bottom < self.man_y:
            self.man_rect.bottom += self.man_down_len
        else:
            self.man_rect.bottom = self.man_y
        if not self.game_over:
            self.miles += self.current_speed
        self.bg_x -= 2
        self.generate_barrier()
    
    def draw_frame(self):
        pygame.draw.line(screen, black, (self.pos_x, self.man_y + 3), (self.pos_x + self.width, self.man_y + 3), 6)
    
    def draw_background(self):
        screen.blit(self.background, [self.bg_x, self.pos_y])
        if self.bg_x < -WIDTH:
            screen.blit(self.background, [2 * WIDTH + self.bg_x, self.pos_y])
            if 2 * WIDTH + self.bg_x == 0:
                self.bg_x = 0
    
    def draw(self):
        self.draw_background()
        for barrier in self.barriers:
            barrier_rect = pygame.draw.rect(screen, self.barrier_color, (barrier[0], barrier[1], self.barrier_size[0], barrier[2]))
            if self.man_rect.colliderect(barrier_rect):
                self.game_over = True
        screen.blit(self.man, self.man_rect)
        self.draw_frame()
        self.clock.tick(self.current_speed)
    

def main():
    running = True
    try:
        image = pygame.image.load("./little-girl2.jpg")
        bg_image = pygame.image.load('./snowy_mountain_landscape_0.jpg')
    except pygame.error as e:
        print(f"Error loading image: {e}")
        
    up_runway = Runway(WIDTH, HEIGHT / 2, 30, 50, 0, 0, pygame.K_w, ice_blue, image, bg_image)
    down_runway = Runway(WIDTH, HEIGHT / 2, 30, 50, 0, HEIGHT / 2, pygame.K_u, ice_blue, image, bg_image)
    dy = 40
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
                if not up_runway.game_over and not down_runway.game_over and event.key == up_runway.jump_key:
                    if up_runway.man_rect.bottom > up_runway.pos_y + up_runway.man_height:
                        up_runway.man_rect.bottom -= dy
                if not up_runway.game_over and not down_runway.game_over and event.key == down_runway.jump_key:
                    if down_runway.man_rect.bottom > down_runway.pos_y + down_runway.man_height + 20:
                        down_runway.man_rect.bottom -= dy
        
        screen.fill(BG_COLOR)
        if not up_runway.game_over and not down_runway.game_over:
            up_runway.move()
            up_runway.draw()
            down_runway.move()
            down_runway.draw()
        if up_runway.game_over or down_runway.game_over:
            f1surf, f1rect = f1.render("GAME OVER", fgcolor=red, size=50)
            pygame.draw.rect(screen, black, pygame.Rect(0, 0, WIDTH, HEIGHT))
            score = up_runway.miles + down_runway.miles
            f2surf, f2rect = f2.render(f'通关距离: {score}', fgcolor=gray, size=24)
            screen.blit(f1surf, ((WIDTH - f1rect.width) / 2, (HEIGHT - f1rect.height) / 2))
            screen.blit(f2surf, (3, 3))
        pygame.display.flip()
    
    pygame.quit()
    
if __name__=="__main__":
    main()
