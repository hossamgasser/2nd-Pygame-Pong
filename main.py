import pygame 
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 500

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Second Game: Pong")

#define colors
bg = (50, 25, 50)
white= (255, 255, 255)

#define font
font = pygame.font.SysFont('Constantia', 30)

#game variables
live_ball = False
cpu_score = 0
player_score = 0
ball_speed = 1
fps = 60
margin = 50   #comes into play when wanting to define movement limits, so naming it helps
winner = 0
speed_increase = 0

def draw_board():
    screen.fill(bg)
    pygame.draw.line(screen, white, (0, margin), (screen_width, margin), 3)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

class paddle():
    def __init__(self, x ,y):
        self.x = x
        self.y = y
        self.rect = Rect(self.x, self.y, 20, 100)
        self.speed = 5

    def move(self):
        key = pygame.key.get_pressed() 
        if key[pygame.K_UP] and self.rect.top > margin:   # margin comes into play here, also remember that y increases as you go down not up
            self.rect.move_ip(0, -self.speed) 
        if key[pygame.K_DOWN] and self.rect.bottom < screen_height:
            self.rect.move_ip(0, self.speed) 

    def ai(self):
        if self.rect.centery < game_pong.rect.top and self.rect.bottom < screen_height:
            self.rect.move_ip(0, self.speed)
        
        if self.rect.centery > game_pong.rect.top and self.rect.top > margin:
            self.rect.move_ip(0, -self.speed)

    def draw(self):
        pygame.draw.rect(screen, white, self.rect)

class pong():
    
    def __init__(self, x ,y):
        self.reset(x, y)

    def move(self):
        #add colision detetction
        if self.rect.y < margin or self.rect.y > (screen_height -15):
            self.speed_y *= -1

        
        if self.rect.right < 0:
            self.winner = 1

        if self.rect.left > (screen_width):
            self.winner = -1

        if self.rect.colliderect(player_paddle) or self.rect.colliderect(CPU_paddle):
            self.speed_x *= -1
        # update ball position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
    
        return self.winner
    def draw(self):
        pygame.draw.circle(screen, white, (self.rect.x + self.pong_radius, self.rect.y + self.pong_radius), self.pong_radius)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.pong_radius = 8
        self.rect = Rect(self.x, self.y, self.pong_radius * 2, self.pong_radius * 2)
        self.speed_x = -4      #ball starts in game moving left
        self.speed_y = 4
        self.winner = 0 



        
#create paddles 
player_paddle = paddle(screen_width - 40, screen_height // 2)
CPU_paddle = paddle(0 + 40, screen_height // 2)
game_pong = pong(screen_width // 2, screen_height // 2 + 50)

run = True
while run:

    fpsClock.tick(fps)
    draw_board()
    draw_text("CPU: " + str(cpu_score), font, white, 20, 15)
    draw_text("Player: " + str(player_score), font, white, screen_width - 140, 15)
    draw_text("Ball Speed: " + str(abs(game_pong.speed_x)), font, white, screen_width // 2 -100 , 15)
    
    #draw paddles
    player_paddle.draw()
    CPU_paddle.draw()
    game_pong.draw()

    if live_ball == True:

        speed_increase += 1
        winner = game_pong.move()
        if winner == 0: 
            player_paddle.move()
            CPU_paddle.ai()
            game_pong.draw()
        else:
            live_ball = False
            if winner == 1:
                player_score += 1
            elif winner == -1:
                cpu_score += 1

    if live_ball == False:
        if winner == 0: 
            draw_text("CLICK ANYWHERE TO START", font, white, 100, screen_height // 2 - 100)

        if winner == 1: 
            draw_text("YOU SCORED!", font, white, 220, screen_height // 2 - 100)
            draw_text("CLICK ANYWHERE TO START", font, white, 100, screen_height // 2 - 50)
            
        if winner == -1: 
            draw_text("CPU SCORED!", font, white, 200, screen_height // 2 - 100)
            draw_text("CLICK ANYWHERE TO START", font, white, 100, screen_height // 2 - 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball= True
            game_pong.reset(screen_width // 2, screen_height // 2 + 50)

    if speed_increase > 500:
        speed_increase = 0
        if game_pong.speed_x < 0:
            game_pong.speed_x -=1
        if game_pong.speed_x > 0:
            game_pong.speed_x +=1
        
        if game_pong.speed_y < 0:
            game_pong.speed_y -=1
        if game_pong.speed_y > 0:
            game_pong.speed_y +=1

    pygame.display.update()

pygame.quit()