#! /usr/bin/env python
import pygame
import random as Random
from pygame.locals import *
from sys import exit


pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, 32, 2, 4096) # Thiết lập chất lượng âm thanh (freq/bit size/no. of channels/buffer)
pygame.display.set_caption("Ếch về ao (Frogger)")

font_name = pygame.font.get_default_font()
game_font = pygame.font.SysFont(font_name, 60)
info_font = pygame.font.SysFont(font_name, 24)
menu_font = pygame.font.SysFont(font_name, 32)
screen = pygame.display.set_mode((448,546), 0, 32) # Thiết lập cửa sổ game (resolution, vsync, bit depth)

# Import hình ảnh. Thư mục hình ảnh phải cùng directory với file .py
background_image = "./images/background.png"
frog_image = "./images/sprite_up.png"
finished_image = "./images/frog_static.png"
white_car_image = "./images/white_car.png"
red_car_image = "./images/red_car.png"
blue_car_image = "./images/blue_car.png"
green_car_image = "./images/green_car.png"
yellow_car_image = "./images/yellow_car.png"
platform_image = "./images/tree.png"
bonus_image = "./images/fly.png"

background = pygame.image.load(background_image).convert()
frog_sprite = pygame.image.load(frog_image).convert_alpha()
sprite_finished = pygame.image.load(finished_image).convert_alpha()
sprite_white_car = pygame.image.load(white_car_image).convert_alpha()
sprite_red_car = pygame.image.load(red_car_image).convert_alpha()
sprite_blue_car = pygame.image.load(blue_car_image).convert_alpha()
sprite_green_car = pygame.image.load(green_car_image).convert_alpha()
sprite_yellow_car = pygame.image.load(yellow_car_image).convert_alpha()
sprite_platform = pygame.image.load(platform_image).convert_alpha()
sprite_bonus = pygame.image.load(bonus_image).convert_alpha()

# Import âm thanh. Thư mục âm thanh phải cùng directory với file .py
die_sound = pygame.mixer.Sound("./sounds/364929__jofae__game-die.mp3")
finish_sound = pygame.mixer.Sound("./sounds/514160__edwardszakal__score-beep.mp3")
bgm_sound = pygame.mixer.Sound("./sounds/Chu-Ech-Con-Xuan-Mai.mp3")
bonus_sound = pygame.mixer.Sound("./sounds/smb_1-up.wav")

clock = pygame.time.Clock()


class Frog():
    def __init__(self,position,frog_sprite):
        self.sprite = frog_sprite
        self.position = position
        self.lives = 3
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "UP"
        self.can_move = 1

    def update_sprite(self,key_pressed):
        if self.way != key_pressed:
            self.way = key_pressed
            if self.way == "up":
                frog_image = "./images/sprite_up.png"
                self.sprite = pygame.image.load(frog_image).convert_alpha()
            elif self.way == "down":
                frog_image = "./images/sprite_down.png"
                self.sprite = pygame.image.load(frog_image).convert_alpha()
            elif self.way == "left":
                frog_image = "./images/sprite_left.png"
                self.sprite = pygame.image.load(frog_image).convert_alpha()
            elif self.way == "right":
                frog_image = "./images/sprite_right.png"
                self.sprite = pygame.image.load(frog_image).convert_alpha()


    def move_frog(self,key_pressed, key_up):
        if self.animation_counter == 0 :
            self.update_sprite(key_pressed)
        self.incAnimationCounter()
        if key_up == 1:
            if key_pressed == "up":
                if self.position[1] > 39:
                    self.position[1] = self.position[1]-13
            elif key_pressed == "down":
                if self.position[1] < 473:
                    self.position[1] = self.position[1]+13
            if key_pressed == "left":
                if self.position[0] > 2:
                    if self.animation_counter == 2 :
                        self.position[0] = self.position[0]-13
                    else:
                        self.position[0] = self.position[0]-14
            elif key_pressed == "right":
                if self.position[0] < 401:
                    if self.animation_counter == 2 :
                        self.position[0] = self.position[0]+13
                    else:
                        self.position[0] = self.position[0]+14

    def animate_frog(self,key_pressed,key_up):
        if self.animation_counter != 0 :
            if self.animation_tick <= 0 :
                self.move_frog(key_pressed,key_up)
                self.animation_tick = 1
            else :
                self.animation_tick = self.animation_tick - 1

    def set_position(self,position):
        self.position = position

    def reduce_life(self):
        self.lives = self.lives - 1

    def stop_moving(self):
        self.can_move = 0

    def incAnimationCounter(self):
        self.animation_counter = self.animation_counter + 1
        if self.animation_counter == 3 :
            self.animation_counter = 0
            self.can_move = 1

    def frog_dies(self,game):
        self.starting_position()
        self.reduce_life()
        game.resetTime()
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "UP"
        self.can_move = 1

    def starting_position(self):
        self.position = [207, 475]

    def draw(self):
        current_sprite = self.animation_counter * 30
        screen.blit(self.sprite,(self.position),(0 + current_sprite, 0, 30, 30 + current_sprite))

    def rect(self):
        return Rect(self.position[0],self.position[1],30,30)

class Enemy():
    def __init__(self,position,sprite_enemy,way,factor):
        self.sprite = sprite_enemy
        self.position = position
        self.way = way
        self.factor = factor

    def move(self,speed):
        if self.way == "right":
            self.position[0] = self.position[0] + speed * self.factor
        elif self.way == "left":
            self.position[0] = self.position[0] - speed * self.factor
    
    def draw(self):
        screen.blit(self.sprite,(self.position))

    def rect(self):
        return Rect(self.position[0],self.position[1],self.sprite.get_width(),self.sprite.get_height())
        
class Bonus():
    def __init__(self,position,sprite_bonus,way):
        self.sprite = sprite_bonus
        self.position = position
        self.way = way

    def move(self,speed):
        if self.way == "right":
            self.position[0] = self.position[0] + speed/2
        elif self.way == "left":
            self.position[0] = self.position[0] - speed/2
            
    def draw(self):
        screen.blit(self.sprite,(self.position))

    def rect(self):
        return Rect(self.position[0],self.position[1],self.sprite.get_width(),self.sprite.get_height())


class Platform():
    def __init__(self,position,sprite_platform,way):
        self.sprite = sprite_platform
        self.position = position
        self.way = way

    def move(self,speed):
        if self.way == "right":
            self.position[0] = self.position[0] + speed
        elif self.way == "left":
            self.position[0] = self.position[0] - speed
            
    def draw(self):
        screen.blit(self.sprite,(self.position))

    def rect(self):
        return Rect(self.position[0],self.position[1],self.sprite.get_width(),self.sprite.get_height())

class Finished(): 
    def __init__(self,position,sprite):
        self.sprite = sprite
        self.position = position

    def draw(self):
        screen.blit(self.sprite,(self.position))

    def rect(self):
        return Rect(self.position[0],self.position[1],self.sprite.get_width(),self.sprite.get_height())

class Game(): # Thiết lập game
    def __init__(self,speed,level):
        self.speed = speed
        self.level = level
        self.points = 0
        self.time = 30
        self.gameInit = 0

    def incLevel(self):
        self.level = self.level + 1

    def incSpeed(self):
        self.speed = self.speed + 1

    def incPoints(self,points):
        self.points = self.points + points

    def decTime(self):
        self.time = self.time - 1

    def resetTime(self):
        self.time = 30


# General functions
def draw_list(list):
    for i in list:
        i.draw()

def move_list(list,speed):
    for i in list:
        i.move(speed)

def remove_enemies(list): # Loại bỏ chướng ngại vật đã ra khỏi màn hình chơi
    for i in list:
        if i.position[0] < -80 or i.position[0] > 516:
            list.remove(i)

def remove_bonuses(list): # Loại bỏ ruồi thưởng đã ra khỏi màn hình
    for i in list:
        if i.position[0] < -100 or i.position[0] > 448:
            list.remove(i)
            
def remove_bonuses_eaten(list): # Loại bỏ ruồi thưởng đã bị ăn
    for i in list:
        list.remove(i)

def remove_platforms(list): # Loại bỏ vật tựa đã ra khỏi màn hình
    for i in list:
        if i.position[0] < -100 or i.position[0] > 448:
            list.remove(i)

def generate_enemies(list,enemies,game):
    for i, tick in enumerate(list):
        list[i] = list[i] - 1
        if tick <= 0:
            if i == 0:
                list[0] = (40*game.speed)/game.level
                position_init = [-55,436]
                enemy = Enemy(position_init,sprite_white_car,"right",1)
                enemies.append(enemy)
            elif i == 1:
                list[1] = (30*game.speed)/game.level
                position_init = [506, 397]
                enemy = Enemy(position_init,sprite_red_car,"left",2)
                enemies.append(enemy)
            elif i == 2:
                list[2] = (40*game.speed)/game.level
                position_init = [-80, 357]
                enemy = Enemy(position_init,sprite_blue_car,"right",2)
                enemies.append(enemy)
            elif i == 3:
                list[3] = (30*game.speed)/game.level
                position_init = [516, 318]
                enemy = Enemy(position_init,sprite_green_car,"left",1)
                enemies.append(enemy)
            elif i == 4:
                list[4] = (50*game.speed)/game.level
                position_init = [-56, 280]
                enemy = Enemy(position_init,sprite_yellow_car,"right",1)
                enemies.append(enemy)
                
def generate_bonuses(list,bonuses,game):
    for i, tick in enumerate(list):
        list[i] = list[i] - 1
        if tick <= 0:
#           if i == 0:
#               list[0] = (500*game.speed)/game.level
#               position_init = [448, 200]
#               bonus = Bonus(position_init,sprite_bonus,"left")
#               bonuses.append(bonus)
#           elif i == 1:
#               list[1] = (400*game.speed)/game.level
#               position_init = [-100, 161]
#               bonus = Bonus(position_init,sprite_bonus,"right")
#               bonuses.append(bonus)
            if i == 2:
                list[2] = (500*game.speed)/game.level
                position_init = [448, 122]
                bonus = Bonus(position_init,sprite_bonus,"left")
                bonuses.append(bonus)
#           elif i == 3:
#               list[3] = (400*game.speed)/game.level
#               position_init = [-100, 83]
#               bonus = Bonus(position_init,sprite_bonus,"right")
#               bonuses.append(bonus)
#           elif i == 4:
#               list[4] = (500*game.speed)/game.level
#               position_init = [448, 44]
#               bonus = Bonus(position_init,sprite_bonus,"left")
#               bonuses.append(bonus)

def generate_platform(list,platforms,game):
    for i, tick in enumerate(list):
        list[i] = list[i] - 1
        if tick <= 0:
            if i == 0:
                list[0] = (30*game.speed)/game.level
                position_init = [-100,200]
                platform = Platform(position_init,sprite_platform,"right")
                platforms.append(platform)
            elif i == 1:
                list[1] = (30*game.speed)/game.level
                position_init = [448, 161]
                platform = Platform(position_init,sprite_platform,"left")
                platforms.append(platform)
            elif i == 2:
                list[2] = (40*game.speed)/game.level
                position_init = [-100, 122]
                platform = Platform(position_init,sprite_platform,"right")
                platforms.append(platform)
            elif i == 3:
                list[3] = (40*game.speed)/game.level
                position_init = [448, 83]
                platform = Platform(position_init,sprite_platform,"left")
                platforms.append(platform)
            elif i == 4:
                list[4] = (20*game.speed)/game.level
                position_init = [-100, 44]
                platform = Platform(position_init,sprite_platform,"right")
                platforms.append(platform)

def when_on_street(frog,enemies,game):
    for i in enemies:
        enemyRect = i.rect()
        frogRect = frog.rect()
        if frogRect.colliderect(enemyRect):
            die_sound.play()
            frog.frog_dies(game)
            
def frog_eats_fly(frog,bonuses,game):
    for i in bonuses:
        flyRect = i.rect()
        frogRect = frog.rect()
        if frogRect.colliderect(flyRect):
            bonus_sound.play()
            frog.lives += 1
            remove_bonuses_eaten(bonuses)           

def when_at_lake(frog,platforms,game):
    second = 0
    wayPlatform = ""
    for i in platforms:
        platformRect = i.rect()
        frogRect = frog.rect()
        if frogRect.colliderect(platformRect):
            second = 1
            wayPlatform = i.way

    if second == 0:
        die_sound.play()
        frog.frog_dies(game)

    elif second == 1:
        if wayPlatform == "right":
            frog.position[0] = frog.position[0] + game.speed

        elif wayPlatform == "left":
            frog.position[0] = frog.position[0] - game.speed

def frog_finished(frog,arrival,game):
    if frog.position[0] > 33 and frog.position[0] < 53:
        position_init = [43,7]
        create_finished(frog,arrival,game,position_init)

    elif frog.position[0] > 115 and frog.position[0] < 135:
        position_init = [125,7]
        create_finished(frog,arrival,game,position_init)

    elif frog.position[0] > 197 and frog.position[0] < 217:
        position_init = [207,7]
        create_finished(frog,arrival,game,position_init)

    elif frog.position[0] > 279 and frog.position[0] < 299:
        position_init = [289,7]
        create_finished(frog,arrival,game,position_init)

    elif frog.position[0] > 361 and frog.position[0] < 381:
        position_init = [371,7]
        create_finished(frog,arrival,game,position_init)

    else:
        frog.position[1] = 46
        frog.animation_counter = 0
        frog.animation_tick = 1
        frog.can_move = 1


def frog_position(frog): # Xác định vị trí ếch để xử lý luật chơi tương ứng
    # Khi ếch sắp băng qua đường
    if frog.position[1] > 240 :
        when_on_street(frog,enemies,game)

    # Khi ếch sắp băng qua sông
    elif frog.position[1] < 240 and frog.position[1] > 40:
        when_at_lake(frog,platforms,game)
        frog_eats_fly(frog,bonuses,game)

    # Khi ếch về đích
    elif frog.position[1] < 40 :
        frog_finished(frog,arrival,game)


def create_finished(frog,arrival,game,position_init):
    frog_checked_in = Finished(position_init,sprite_finished)
    arrival.append(frog_checked_in)
    finish_sound.play()
    frog.starting_position()
    game.incPoints(10 + game.time)
    game.resetTime()
    frog.animation_counter = 0
    frog.animation_tick = 1
    frog.can_move = 1


def next_level(arrival,enemies,platforms,frog,game):
    if len(arrival) == 5:
        arrival[:] = []
        frog.lives += 1
        frog.starting_position()
        game.incLevel()
        game.incSpeed()
        game.incPoints(100)
        game.resetTime()


bgm_sound.play(-1)
text_info = menu_font.render(("Nhan phim bat ki de bat dau"),1,(0,0,0))
gameInit = 0

while gameInit == 0:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            gameInit = 1

    screen.blit(background, (0, 0))
    screen.blit(text_info,(80,150))
    pygame.display.update()

while True:
    gameInit = 1
    game = Game(3,1)
    key_up = 1
    frog_initial_position = [207,475]
    frog = Frog(frog_initial_position,frog_sprite)

    enemies = []
    bonuses = []
    platforms = []
    arrival = []
    ticks_enemies = [30, 0, 30, 0, 60]
    ticks_platforms = [0, 0, 30, 30, 30]
    ticks_bonuses = [0, 0, 30, 30, 30]
    ticks_time = 30
    pressed_keys = 0
    key_pressed = 0

    while frog.lives > 0:

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYUP:
                key_up = 1
            if event.type == KEYDOWN:
                if key_up == 1 and frog.can_move == 1 :
                    key_pressed = pygame.key.name(event.key)
                    frog.move_frog(key_pressed,key_up)
                    frog.stop_moving()
        if not ticks_time:
            ticks_time = 30
            game.decTime()
        else:
            ticks_time -= 1

        if game.time == 0:
            die_sound.play()
            frog.frog_dies(game)

        generate_enemies(ticks_enemies,enemies,game)
        generate_platform(ticks_platforms,platforms,game)
        generate_bonuses(ticks_bonuses,bonuses,game)
        

        move_list(enemies,game.speed)
        move_list(platforms,game.speed)
        move_list(bonuses,game.speed)

        frog_position(frog)

        next_level(arrival,enemies,platforms,frog,game)

        text_info1 = info_font.render(("Cap do: {0}           Diem so: {1}".format(game.level,game.points)),1,(255,255,255))
        text_info2 = info_font.render(("Thoi gian: {0}        Mang: {1}".format(game.time,frog.lives)),1,(255,255,255))
        screen.blit(background, (0, 0))
        screen.blit(text_info1,(10,520))
        screen.blit(text_info2,(250,520))

        draw_list(enemies)
        draw_list(platforms)
        draw_list(bonuses)
        draw_list(arrival)

        frog.animate_frog(key_pressed,key_up)
        frog.draw()

        remove_enemies(enemies)
        remove_platforms(platforms)
        remove_bonuses(bonuses)

        pygame.display.update()
        time_passed = clock.tick(30)

    while gameInit == 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                gameInit = 0

        screen.blit(background, (0, 0))
        text = game_font.render("KET THUC", 1, (255, 0, 0))
        text_points = game_font.render(("Tong diem: {0}".format(game.points)),1,(255,0,0))
        text_restart = info_font.render("Nhan phim bat ki de choi lai",1,(255,0,0))
        screen.blit(text, (120, 120))
        screen.blit(text_points,(85,180))
        screen.blit(text_restart,(115,250))

        pygame.display.update()
