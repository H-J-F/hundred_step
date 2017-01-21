#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pygame, random, sqlite3
from pygame.locals import *
from sys import exit

pygame.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((400, 600), DOUBLEBUF, 32)
pygame.display.set_caption(u"垃圾游戏")
pygame.mixer.music.set_volume(10)

soundwav = pygame.mixer.Sound("src/musics/guan.wav")
icon = pygame.image.load("src/Icon/laji.ico").convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load("src/background/bg.png").convert_alpha()
shit = pygame.image.load("src/background/shit.png").convert_alpha()
tip = pygame.image.load("src/widgets/tips.png").convert_alpha()
delete_data = pygame.image.load("src/widgets/delete_data.png").convert_alpha()
gameover = pygame.image.load("src/widgets/gameover.png").convert_alpha()
pause_box = pygame.image.load("src/widgets/pause.png").convert_alpha()
bubble = pygame.image.load("src/widgets/bubble.png").convert_alpha()
bubble_down = pygame.image.load("src/widgets/bubble_down.png").convert_alpha()
start_btn = pygame.image.load("src/widgets/start.png").convert_alpha()
instruction_btn = pygame.image.load("src/widgets/Instructions.png").convert_alpha()
back = pygame.image.load("src/widgets/back.png").convert_alpha()
restart = pygame.image.load("src/widgets/restart.png").convert_alpha()
pedal = pygame.image.load("src/pedal/pedal.png").convert_alpha()
pedal_shit = pygame.image.load("src/pedal/pedal_shit.png").convert_alpha()
choice_image = pygame.image.load("src/widgets/choice.png").convert_alpha()
select_image = pygame.image.load("src/widgets/select.png").convert_alpha()
next_image = pygame.image.load("src/widgets/next.png").convert_alpha()
previous_image = pygame.image.load("src/widgets/previous.png").convert_alpha()
door_left = pygame.image.load("src/widgets/door_left.png").convert_alpha()
door_right = pygame.image.load("src/widgets/door_right.png").convert_alpha()

pausebtn_on = pygame.image.load("src/widgets/pause_on.png").convert_alpha()
pausebtn_off = pygame.image.load("src/widgets/pause_off.png").convert_alpha()
pause = pausebtn_on

sound_on = pygame.image.load("src/widgets/sound_on.png").convert_alpha()
sound_off = pygame.image.load("src/widgets/sound_off.png").convert_alpha()
sound = sound_on

heroes = [0 for h in range(6)]
player = [0 for p in range(6)]
player[0] = pygame.image.load("src/heroes/guangmingshili.png").convert_alpha()
player[1] = pygame.image.load("src/heroes/jiaoyubu.png").convert_alpha()
player[2] = pygame.image.load("src/heroes/meitishili.png").convert_alpha()
player[3] = pygame.image.load("src/heroes/shanghui.png").convert_alpha()
player[4] = pygame.image.load("src/heroes/suoyoushili.png").convert_alpha()
player[5] = pygame.image.load("src/heroes/zhifashili.png").convert_alpha()

player_right = [0 for i in range(6)]
player_right[0] = pygame.image.load("src/heroes/image_right/guangmingshili_right.png").convert_alpha()
player_right[1] = pygame.image.load("src/heroes/image_right/jiaoyubu_right.png").convert_alpha()
player_right[2] = pygame.image.load("src/heroes/image_right/meitishili_right.png").convert_alpha()
player_right[3] = pygame.image.load("src/heroes/image_right/shanghui_right.png").convert_alpha()
player_right[4] = pygame.image.load("src/heroes/image_right/suoyoushili_right.png").convert_alpha()
player_right[5] = pygame.image.load("src/heroes/image_right/zhifashili_right.png").convert_alpha()

drop_shits = []
drop_shit = pygame.image.load("src/widgets/drop_shit.png").convert_alpha()

saying = [0 for s in range(6)]
saying[0] = ('坚决不踩大便，否则', '就是打脸')
saying[1] = ('有事秘书干，没事干', '秘书')
saying[2] = ('看什么看，没见过制', '服诱惑吗')
saying[3] = ('人家要做领导的小公', '举')
saying[4] = ('那个去开房的领导，', '已经被我举报了')
saying[5] = ('就算我能打手枪，那', '又有什么卵用')

over_word = [0 for s in range(6)]
over_word[0] = ('你没踩大便，但你吃', '大便了')
over_word[1] = ('你跟秘书去开房被隔', '壁那个法官举报了')
over_word[2] = ('这次扫黄打非又抓到', '你')
over_word[3] = ('你的领导已经被抓，', '你就从了我吧')
over_word[4] = ('落马之前来一发，法', '官大人你行啊')
over_word[5] = ('新闻报导：今天一城', '管当众吃屎')

hero_name = ('天屎', '领导', '婊砸', '公举', '法官', '城管')
edge_left = (27, 9, 14, 0, 0, 7)
left_edge = (40, 17, 25, 14, 14, 20)
right_edge = (42, 8, 12, 13, 8, 7)
score = 0
raw_meter = 0
select = 0
my_hero = 0
max_word = 0
pedals = [0]
accelerate = 1
max_score = '0.0'
drop_flag = False

conn = sqlite3.connect(r'src/data/maxscore.db')
cuso = conn.cursor()
cuso.execute('''CREATE TABLE IF NOT EXISTS maxscore (score TEXT)''')

pygame.key.set_repeat(3)


class Drop_thing(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (random.randint(0, 370), -30)
        self.acc = 1


class Player(pygame.sprite.Sprite):
    def __init__(self, image, position, speed):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = speed


class Pedal(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (random.randint(0, 251), random.randint(0, 100))


def check(my_hero, check_pedal):
    global right_edge, left_edge, select, player, player_right, pedal, pedal_shit, bubble, over_word, sound, sound_on, \
        drop_shits, drop_shit

    head = (38, 30, 40, 30, 27, 35)
    width = (99, 50, 58, 51, 48, 44)
    height = (90, 80, 90, 80, 80, 80)
    result = True

    if check_pedal.image == drop_shit:
        if (my_hero.rect.top < check_pedal.rect.top < (my_hero.rect.top + height[select])):
            if my_hero.image == player[select]:
                if (((my_hero.rect.left + left_edge[select] - 30) < check_pedal.rect.left < (my_hero.rect.left + width[select] - right_edge[select]))):
                    situation = 3
                    game_over(situation)
            elif my_hero.image == player_right[select]:
                if ((my_hero.rect.left + right_edge[select] - 30) < check_pedal.rect.left < (my_hero.rect.left + width[select] - left_edge[select])):
                    situation = 3
                    game_over(situation)
    else:
        if (my_hero.rect.top > 620):
            situation = 1
            game_over(situation)

        if (my_hero.rect.top < 25 - head[select]):
            situation = 2
            game_over(situation)

        if check_pedal.rect.top - height[select] + 17 >= my_hero.rect.top >= check_pedal.rect.top - height[select] + 7:
            if my_hero.image == player[select]:
                if ((my_hero.rect.left + width[select] - right_edge[select]) > check_pedal.rect.left) and ((my_hero.rect.left + left_edge[select]) < (check_pedal.rect.left + 150)):
                    if check_pedal.image == pedal:
                        result = False
                    elif check_pedal.image == pedal_shit:
                        situation = 3
                        game_over(situation)
            elif my_hero.image == player_right[select]:
                if ((my_hero.rect.left + width[select] - left_edge[select]) > check_pedal.rect.left) and ((my_hero.rect.left + right_edge[select]) < (check_pedal.rect.left + 150)):
                    if check_pedal.image == pedal:
                        result = False
                    elif check_pedal.image == pedal_shit:
                        situation = 3
                        game_over(situation)

    return result


def game_over(situation):
    global screen, gameover, score, raw_meter, max_score, cuso, conn, max_word, sound, sound_on, sound_off, soundwav

    font = pygame.font.Font('src/font/STXINWEI.ttf', 25)
    score_font = pygame.font.Font('src/font/BAUHS93.ttf', 30)
    meter = score_font.render(raw_meter, True, (60, 60, 60))
    word_up = font.render(over_word[select][0], True, (255, 255, 255))
    word_width = word_up.get_rect().width
    word_height = word_up.get_rect().height
    word_down = font.render(over_word[select][1], True, (255, 255, 255))
    screen_shot = screen.subsurface((0, 0, 400, 600)).copy()
    buble = bubble.subsurface((0, 0, 336, 176)).copy()
    buble_down = bubble_down.subsurface((0, 0, 336, 176)).copy()
    clock = pygame.time.Clock()

    max_int = round((score / 50), 1)
    if max_score == '0.0':
        max_score = str(round((score / 50), 1))
        cuso.execute('''INSERT INTO maxscore (score) VALUES (\'%s\')''' % max_score)
        conn.commit()

    elif max_int > float(max_score):
        max = str(round((score / 50), 1))
        cuso.execute('''DELETE FROM maxscore WHERE (score = \'%s\')''' % max_score)
        max_score = max
        cuso.execute('''INSERT INTO maxscore (score) VALUES (\'%s\')''' % max)
        conn.commit()

    max_font = pygame.font.Font('src/font/STXINGKA.ttf', 25)
    raw_max = '历史最长高度：' + max_score + 'm'
    max_word = max_font.render(raw_max, True, (255, 255, 255))

    if sound == sound_on:
        if pygame.mixer.music.get_busy() == 1:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("src/musics/gameover.wav")
            pygame.mixer.music.play()

    if situation == 1:
        t = 0
        while t <= 60:
            for event in pygame.event.get():
                if event.type == QUIT:
                    conn.close()
                    pygame.quit()
                    exit()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()

                        if (372 <= mouse_pos[0] <= 397) and (3 <= mouse_pos[1] <= 28):
                            if sound == sound_on:
                                soundwav.play()
                                if pygame.mixer.music.get_busy() == 1:
                                    pygame.mixer.music.stop()
                                sound = sound_off
                            elif sound == sound_off:
                                sound = sound_on
                            screen.blit(sound, (372, 3))
                            pygame.display.flip()

                if event.type == KEYUP:
                    if event.key == K_m:
                        if sound == sound_on:
                            soundwav.play()
                            if pygame.mixer.music.get_busy() == 1:
                                pygame.mixer.music.stop()
                            sound = sound_off
                        elif sound == sound_off:
                            sound = sound_on

            buble.blit(word_up, (168 - word_width // 2, 88 - 2 * word_height))
            buble.blit(word_down, (168 - word_width // 2, 98 - word_height))
            screen.blit(buble, (32, 420))
            screen.blit(sound, (372, 3))
            pygame.display.flip()
            pygame.time.delay(50)
            t += 1
        screen.blit(screen_shot, (0, 0))
        screen.blit(sound, (372, 3))
        pygame.display.flip()

    elif situation == 2:
        t = 0
        while t <= 60:
            for event in pygame.event.get():
                if event.type == QUIT:
                    conn.close()
                    pygame.quit()
                    exit()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()

                        if (372 <= mouse_pos[0] <= 397) and (3 <= mouse_pos[1] <= 28):
                            if sound == sound_on:
                                soundwav.play()
                                if pygame.mixer.music.get_busy() == 1:
                                    pygame.mixer.music.stop()
                                sound = sound_off
                            elif sound == sound_off:
                                sound = sound_on
                            screen.blit(sound, (372, 3))
                            pygame.display.flip()

                if event.type == KEYUP:
                    if event.key == K_m:
                        if sound == sound_on:
                            soundwav.play()
                            if pygame.mixer.music.get_busy() == 1:
                                pygame.mixer.music.stop()
                            sound = sound_off
                        elif sound == sound_off:
                            sound = sound_on

            buble_down.blit(word_up, (168 - word_width // 2, 128 - 2 * word_height))
            buble_down.blit(word_down, (168 - word_width // 2, 138 - word_height))
            screen.blit(buble_down, (32, 100))
            screen.blit(sound, (372, 3))
            pygame.display.flip()
            pygame.time.delay(50)
            t += 1
        screen.blit(screen_shot, (0, 0))
        screen.blit(sound, (372, 3))
        pygame.display.flip()

    elif situation == 3:
        t = 0
        while t <= 60:
            for event in pygame.event.get():
                if event.type == QUIT:
                    conn.close()
                    pygame.quit()
                    exit()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()

                        if (372 <= mouse_pos[0] <= 397) and (3 <= mouse_pos[1] <= 28):
                            if sound == sound_on:
                                soundwav.play()
                                if pygame.mixer.music.get_busy() == 1:
                                    pygame.mixer.music.stop()
                                sound = sound_off
                            elif sound == sound_off:
                                sound = sound_on
                            screen.blit(sound, (372, 3))
                            pygame.display.flip()

                if event.type == KEYUP:
                    if event.key == K_m:
                        if sound == sound_on:
                            soundwav.play()
                            if pygame.mixer.music.get_busy() == 1:
                                pygame.mixer.music.stop()
                            sound = sound_off
                        elif sound == sound_off:
                            sound = sound_on

            if my_hero.rect.top >= 203:
                buble.blit(word_up, (168 - word_width // 2, 88 - 2 * word_height))
                buble.blit(word_down, (168 - word_width // 2, 98 - word_height))
                screen.blit(buble, (32, my_hero.rect.top - 185))
                screen.blit(sound, (372, 3))
                pygame.display.flip()
                pygame.time.delay(50)
                t += 1

            else:
                buble_down.blit(word_up, (168 - word_width // 2, 128 - 2 * word_height))
                buble_down.blit(word_down, (168 - word_width // 2, 138 - word_height))
                screen.blit(buble_down, (32, my_hero.rect.top + 90))
                screen.blit(sound, (372, 3))
                pygame.display.flip()
                pygame.time.delay(50)
                t += 1

        screen.blit(screen_shot, (0, 0))
        screen.blit(sound, (372, 3))
        pygame.display.flip()

    meter_width = meter.get_rect().width // 2
    gameover_copy = gameover.subsurface(0, 0, 300, 350).copy()
    gameover_copy.blit(meter, (150 - meter_width, 290))
    for i in range(-352, 126, 3):
        for event in pygame.event.get():
            if event.type == QUIT:
                conn.close()
                pygame.quit()
                exit()

            if event.type == KEYUP:
                if event.key == K_m:
                    if sound == sound_on:
                        soundwav.play()
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.stop()
                        sound = sound_off
                    elif sound == sound_off:
                        sound = sound_on

        screen.blit(screen_shot, (0, 0))
        screen.blit(sound, (372, 3))
        screen.blit(gameover_copy, (50, i))

        pygame.display.flip()
        clock.tick(400)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                conn.close()
                pygame.quit()
                exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if (31 <= mouse_pos[0] <= 56) and (3 <= mouse_pos[1] <= 28):
                        if sound == sound_on:
                            soundwav.play()
                        close_door()
                        if sound == sound_on:
                            soundwav.play()
                            if pygame.mixer.music.get_busy() != 1:
                                pygame.mixer.music.load("src/musics/playing.wav")
                                pygame.mixer.music.play(loops=-1)
                        show_game()

                    elif (372 <= mouse_pos[0] <= 397) and (3 <= mouse_pos[1] <= 28):
                        if sound == sound_on:
                            soundwav.play()
                            if pygame.mixer.music.get_busy() == 1:
                                pygame.mixer.music.stop()
                            sound = sound_off
                        elif sound == sound_off:
                            sound = sound_on
                        screen.blit(sound, (372, 3))
                        pygame.display.flip()

                    else:
                        if sound == sound_on:
                            soundwav.play()
                        close_door()
                        door_to_begin()

            if event.type == KEYUP:
                if event.key == K_m:
                    if sound == sound_on:
                        soundwav.play()
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.stop()
                        sound = sound_off
                    elif sound == sound_off:
                        sound = sound_on
                    screen.blit(sound, (372, 3))
                    pygame.display.flip()

                if event.key == K_r:
                    if sound == sound_on:
                        soundwav.play()
                    close_door()
                    if sound == sound_on:
                        if pygame.mixer.music.get_busy() != 1:
                            pygame.mixer.music.load("src/musics/playing.wav")
                            pygame.mixer.music.play(loops=-1)
                    show_game()
                if (event.key == K_KP_ENTER) or (event.key == K_RETURN) or (event.key == K_SPACE) or (event.key == K_ESCAPE):
                    if sound == sound_on:
                        soundwav.play()
                    close_door()
                    door_to_begin()


def door_to_begin():
    global screen, player, sound, bg, door_left, door_right, start_btn, instruction_btn, max_word, delete_data

    clock = pygame.time.Clock()

    screen.blit(bg, (0, 0))
    for i in range(6):
        screen.blit(player[i], (65 * i + 15, 100 * i + 10))
    screen.blit(start_btn, (24, 420))
    screen.blit(instruction_btn, (180, 130))
    screen.blit(delete_data, (3, 574))
    screen.blit(max_word, (30, 515))
    screen.blit(sound, (372, 3))

    screen_shot = screen.subsurface(0, 0, 400, 600).copy()

    for j in range(201):
        screen.blit(screen_shot, (0, 0))
        screen.blit(door_left, (-j, 0))
        screen.blit(door_right, (j + 200, 0))
        pygame.display.flip()
        clock.tick(500)

    begin()


def close_door():
    global screen, player, sound, soundwav, sound_off, sound_on, back, bg, choice_image, select_image, next_image, previous_image, \
        door_left, door_right


    clock = pygame.time.Clock()

    for i in range(-200, 1):
        for event in pygame.event.get():
            if event.type == QUIT:
                conn.close()
                pygame.quit()
                exit()

            if event.type == KEYUP:
                if event.key == K_m:
                    if sound == sound_on:
                        soundwav.play()
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.stop()
                        sound = sound_off
                    elif sound == sound_off:
                        if pygame.mixer.music.get_busy() != 1:
                            pygame.mixer.music.load("src/musics/playing.wav")
                            pygame.mixer.music.play(loops=-1)
                        sound = sound_on

        screen.blit(door_left, (i, 0))
        screen.blit(door_right, (-i + 200, 0))
        pygame.display.flip()
        clock.tick(500)

    pygame.time.delay(1300)


def pause_game():
    global screen, pause_box, pause, pausebtn_on, conn, sound, sound_off, sound_on, soundwav

    break_flag = False
    screen_shot = screen.subsurface((0, 0, 400, 600)).copy()
    clock = pygame.time.Clock()

    for i in range(-136, 234, 3):
        screen.blit(screen_shot, (0, 0))
        screen.blit(pause_box, (50, i))

        pygame.display.flip()
        clock.tick(500)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                conn.close()
                pygame.quit()
                exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if (3 <= mouse_pos[0] <= 28) and (3 <= mouse_pos[1] <= 28):
                        if sound == sound_on:
                            soundwav.play()
                        close_door()
                        if sound == sound_on:
                            if pygame.mixer.music.get_busy() == 1:
                                pygame.mixer.music.load("src/musics/Pisky.wav")
                                pygame.mixer.music.play(loops=-1)
                        door_to_begin()

                    elif (31 <= mouse_pos[0] <= 56) and (3 <= mouse_pos[1] <= 28):
                        if sound == sound_on:
                            soundwav.play()
                        close_door()
                        show_game()

                    elif (372 <= mouse_pos[0] <= 397) and (3 <= mouse_pos[1] <= 28):
                        if sound == sound_on:
                            soundwav.play()
                            if pygame.mixer.music.get_busy() == 1:
                                pygame.mixer.music.stop()
                            sound = sound_off
                        elif sound == sound_off:
                            if pygame.mixer.music.get_busy() != 1:
                                pygame.mixer.music.load("src/musics/playing.wav")
                                pygame.mixer.music.play(loops=-1)
                            sound = sound_on
                        screen.blit(sound, (372, 3))
                        pygame.display.flip()

                    else:
                        if sound == sound_on:
                            soundwav.play()
                        pause = pausebtn_on
                        screen.blit(pause, (345, 3))
                        pygame.display.flip()

                        for i in range(233, 603, 3):
                            screen.blit(screen_shot, (0, 0))
                            screen.blit(pause, (345, 3))
                            screen.blit(pause_box, (50, i))

                            pygame.display.flip()
                            clock.tick(500)
                        break_flag = True

            if event.type == KEYUP:
                if event.key == K_m:
                    if sound == sound_on:
                        soundwav.play()
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.stop()
                        sound = sound_off
                    elif sound == sound_off:
                        if pygame.mixer.music.get_busy() != 1:
                            pygame.mixer.music.load("src/musics/playing.wav")
                            pygame.mixer.music.play(loops=-1)
                        sound = sound_on
                    screen.blit(sound, (372, 3))
                    pygame.display.flip()

            if event.type == KEYDOWN:
                if (event.key == K_p) or (event.key == K_RETURN) or (event.key == K_SPACE) or (event.key == K_KP_ENTER):
                    if sound == sound_on:
                        soundwav.play()
                    pause = pausebtn_on
                    screen.blit(pause, (345, 3))
                    pygame.display.flip()

                    for i in range(233, 603, 3):
                        screen.blit(screen_shot, (0, 0))
                        screen.blit(pause, (345, 3))
                        screen.blit(pause_box, (50, i))

                        pygame.display.flip()
                        clock.tick(500)
                    break_flag = True

                elif event.key == K_ESCAPE:
                    if sound == sound_on:
                        soundwav.play()
                    close_door()
                    if sound == sound_on:
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.load("src/musics/Pisky.wav")
                            pygame.mixer.music.play(loops=-1)
                    door_to_begin()

        if break_flag:
            break


def show_game():
    global my_hero, bg, shit, screen, bubble, back, restart, sound, sound_on, sound_off, pause, pausebtn_on, pausebtn_off,\
        pause_box, edge_right, door_left, door_right, pedal, pedal_shit, player, player_right, saying, pedals, drop_flag, \
        accelerate, left_edge, select, edge_left, score, raw_meter, conn, drop_shit, drop_shits, soundwav

    score = 0
    drop_pro = 10
    shit_speed = 0.13
    tic = 120
    width = (50, 25, 29, 25, 24, 22)
    height = (45, 40, 45, 40, 40, 40)
    clock = pygame.time.Clock()
    font = pygame.font.Font('src/font/STXINWEI.ttf', 45)
    score_font = pygame.font.Font('src/font/MAIAN.ttf', 20)
    xiafan = font.render(u'黑恶势力下凡', True, (255, 255, 255))
    raw_meter = 'Meters: ' + str(round((score / 50), 1)) + 'm'
    meter = score_font.render(raw_meter, True, (60, 60, 60))
    buble = bubble.subsurface((0, 0, 336, 176)).copy()

    pedals = [0]
    my_hero = Player(player[select], (200 - width[select], 0), [0, 1])
    pedals[0] = Pedal(pedal)
    drop_shits = []

    screen.blit(bg, (0, 0))
    screen.blit(back, (3, 3))
    screen.blit(restart, (31, 3))
    screen.blit(sound, (372, 3))
    screen.blit(pause, (345, 3))
    screen.blit(meter, (5, 576))
    screen_shot = screen.subsurface((0, 0, 400, 600)).copy()

    for j in range(201):
        for event in pygame.event.get():
            if event.type == QUIT:
                conn.close()
                pygame.quit()
                exit()

            if event.type == KEYUP:
                if event.key == K_m:
                    if sound == sound_on:
                        soundwav.play()
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.stop()
                        sound = sound_off
                    elif sound == sound_off:
                        if pygame.mixer.music.get_busy() != 1:
                            pygame.mixer.music.load("src/musics/playing.wav")
                            pygame.mixer.music.play(loops=-1)
                        sound = sound_on

                if event.key == K_ESCAPE:
                    if sound == sound_on:
                        soundwav.play()
                    close_door()
                    if sound == sound_on:
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.load("src/musics/Pisky.wav")
                            pygame.mixer.music.play(loops=-1)
                    door_to_begin()

        screen.blit(screen_shot, (0, 0))
        screen.blit(sound, (372, 3))
        screen.blit(door_left, (-j, 0))
        screen.blit(door_right, (j + 200, 0))
        pygame.display.flip()
        clock.tick(500)

    screen_shot = screen.subsurface((0, 0, 400, 600)).copy()

    for i in range(-2 * height[select] - 50, 351 - height[select], 2):
        for event in pygame.event.get():
            if event.type == QUIT:
                conn.close()
                pygame.quit()
                exit()

            if event.type == KEYUP:
                if event.key == K_m:
                    if sound == sound_on:
                        soundwav.play()
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.stop()
                        sound = sound_off
                    elif sound == sound_off:
                        if pygame.mixer.music.get_busy() != 1:
                            pygame.mixer.music.load("src/musics/playing.wav")
                            pygame.mixer.music.play(loops=-1)
                        sound = sound_on
                    screen.blit(sound, (372, 3))
                    pygame.display.flip()

                if event.key == K_ESCAPE:
                    if sound == sound_on:
                        soundwav.play()
                    close_door()
                    if sound == sound_on:
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.load("src/musics/Pisky.wav")
                            pygame.mixer.music.play(loops=-1)
                    door_to_begin()

                if event.key == K_r:
                    if sound == sound_on:
                        soundwav.play()
                    close_door()
                    show_game()

            if event.type == KEYDOWN:
                if event.key == K_p:
                    if sound == sound_on:
                        soundwav.play()
                    pause = pausebtn_off
                    screen.blit(pause, (345, 3))
                    pygame.display.flip()
                    pause_game()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if (3<=mouse_pos[0]<=28) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                        close_door()
                        if sound == sound_on:
                            if pygame.mixer.music.get_busy() == 1:
                                pygame.mixer.music.load("src/musics/Pisky.wav")
                                pygame.mixer.music.play(loops=-1)
                        door_to_begin()

                    elif (31<=mouse_pos[0]<=56) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                        close_door()
                        show_game()

                    elif (345<=mouse_pos[0]<=370) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                        pause = pausebtn_off
                        screen.blit(pause, (345, 3))
                        pygame.display.flip()
                        pause_game()

                    elif (372<=mouse_pos[0]<=397) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                            if pygame.mixer.music.get_busy() == 1:
                                pygame.mixer.music.stop()
                            sound = sound_off
                        elif sound == sound_off:
                            if pygame.mixer.music.get_busy() != 1:
                                pygame.mixer.music.load("src/musics/playing.wav")
                                pygame.mixer.music.play(loops=-1)
                            sound = sound_on

        my_hero.rect.top = i
        pedals[0].rect.top = i + 2 * height[select] - 8

        screen.blit(screen_shot, (0, 0))
        screen.blit(sound, (372, 3))
        screen.blit(my_hero.image, (200 - width[select], i))
        screen.blit(pedals[0].image, (125, pedals[0].rect.top))
        pygame.display.flip()
        clock.tick(220)

    pedals[0].rect.left = 125
    pygame.time.delay(200)
    screen_shot = screen.subsurface((0, 0, 400, 600)).copy()

    t = 0
    while t <= 50:
        for event in pygame.event.get():
            if event.type == QUIT:
                conn.close()
                pygame.quit()
                exit()

            if event.type == KEYUP:
                if event.key == K_m:
                    if sound == sound_on:
                        soundwav.play()
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.stop()
                        sound = sound_off
                    elif sound == sound_off:
                        if pygame.mixer.music.get_busy() != 1:
                            pygame.mixer.music.load("src/musics/playing.wav")
                            pygame.mixer.music.play(loops=-1)
                        sound = sound_on
                    screen.blit(sound, (372, 3))
                    pygame.display.flip()

                if event.key == K_ESCAPE:
                    if sound == sound_on:
                        soundwav.play()
                    close_door()
                    if sound == sound_on:
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.load("src/musics/Pisky.wav")
                            pygame.mixer.music.play(loops=-1)
                    door_to_begin()

                if event.key == K_r:
                    if sound == sound_on:
                        soundwav.play()
                    close_door()
                    show_game()

            if event.type == KEYDOWN:
                if event.key == K_p:
                    if sound == sound_on:
                        soundwav.play()
                    pause = pausebtn_off
                    screen.blit(pause, (345, 3))
                    pygame.display.flip()
                    pause_game()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if (3<=mouse_pos[0]<=28) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                        close_door()
                        if sound == sound_on:
                            if pygame.mixer.music.get_busy() == 1:
                                pygame.mixer.music.load("src/musics/Pisky.wav")
                                pygame.mixer.music.play(loops=-1)
                        door_to_begin()

                    elif (31<=mouse_pos[0]<=56) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                        close_door()
                        show_game()

                    elif (345<=mouse_pos[0]<=370) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                        pause = pausebtn_off
                        screen.blit(pause, (345, 3))
                        pygame.display.flip()
                        pause_game()

                    elif (372<=mouse_pos[0]<=397) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                            if pygame.mixer.music.get_busy() == 1:
                                pygame.mixer.music.stop()
                            sound = sound_off
                        elif sound == sound_off:
                            if pygame.mixer.music.get_busy() != 1:
                                pygame.mixer.music.load("src/musics/playing.wav")
                                pygame.mixer.music.play(loops=-1)
                            sound = sound_on
                        screen.blit(sound, (372, 3))
                        pygame.display.flip()

        buble.blit(xiafan, (30, 40))
        screen.blit(buble, (32, 174 - height[select]))
        pygame.display.flip()
        pygame.time.delay(50)
        t += 1

    t = 0
    buble = bubble.subsurface((0, 0, 336, 176)).copy()
    font = pygame.font.Font('src/font/STXINWEI.ttf', 25)
    word_up = font.render(saying[select][0], True, (255, 255, 255))
    word_width = word_up.get_rect().width
    word_height = word_up.get_rect().height
    word_down = font.render(saying[select][1], True, (255, 255, 255))
    while t < 60:
        for event in pygame.event.get():
            if event.type == QUIT:
                conn.close()
                pygame.quit()
                exit()

            if event.type == KEYUP:
                if event.key == K_m:
                    if sound == sound_on:
                        soundwav.play()
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.stop()
                        sound = sound_off
                    elif sound == sound_off:
                        if pygame.mixer.music.get_busy() != 1:
                            pygame.mixer.music.load("src/musics/playing.wav")
                            pygame.mixer.music.play(loops=-1)
                        sound = sound_on
                screen.blit(sound, (372, 3))
                pygame.display.flip()

                if event.key == K_ESCAPE:
                    if sound == sound_on:
                        soundwav.play()
                    close_door()
                    if sound == sound_on:
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.load("src/musics/Pisky.wav")
                            pygame.mixer.music.play(loops=-1)
                    door_to_begin()

                if event.key == K_r:
                    if sound == sound_on:
                        soundwav.play()
                    close_door()
                    show_game()

            if event.type == KEYDOWN:
                if event.key == K_p:
                    if sound == sound_on:
                        soundwav.play()
                    pause = pausebtn_off
                    screen.blit(pause, (345, 3))
                    pygame.display.flip()
                    pause_game()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if (3<=mouse_pos[0]<=28) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                        close_door()
                        if sound == sound_on:
                            if pygame.mixer.music.get_busy() == 1:
                                pygame.mixer.music.load("src/musics/Pisky.wav")
                                pygame.mixer.music.play(loops=-1)
                        door_to_begin()

                    elif (31<=mouse_pos[0]<=56) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                        close_door()
                        show_game()

                    elif (345<=mouse_pos[0]<=370) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                        pause = pausebtn_off
                        screen.blit(pause, (345, 3))
                        pygame.display.flip()
                        pause_game()

                    elif (372<=mouse_pos[0]<=397) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                            if pygame.mixer.music.get_busy() == 1:
                                pygame.mixer.music.stop()
                            sound = sound_off
                        elif sound == sound_off:
                            if pygame.mixer.music.get_busy() != 1:
                                pygame.mixer.music.load("src/musics/playing.wav")
                                pygame.mixer.music.play(loops=-1)
                            sound = sound_on

        screen.blit(screen_shot, (0, 0))
        screen.blit(sound, (372, 3))
        buble.blit(word_up, (168 - word_width // 2, 88 - 2 * word_height))
        buble.blit(word_down, (168 - word_width // 2, 98 - word_height))
        screen.blit(buble, (32, 174 - height[select]))
        pygame.display.flip()
        pygame.time.delay(50)
        t += 1

    new_pedal = Pedal(pedal)
    new_pedal.rect.top = 600
    pedals.append(new_pedal)
    new_time = 0
    new_pix = random.randint(50, 180)

    for i in range(-26, 1):
        screen.blit(bg, (0, 0))
        screen.blit(shit, (0, i))
        screen.blit(back, (3, 3))
        screen.blit(restart, (31, 3))
        screen.blit(sound, (372, 3))
        screen.blit(pause, (345, 3))
        second_shot = screen.subsurface((0, 0, 400, 600)).copy()
        screen.blit(meter, (5, 576))
        screen.blit(my_hero.image, (200 - width[select], my_hero.rect.top))
        screen.blit(pedals[0].image, (125, pedals[0].rect.top))
        pygame.display.flip()
        clock.tick(60)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                conn.close()
                pygame.quit()
                exit()

            if event.type == KEYUP:
                if event.key == K_m:
                    if sound == sound_on:
                        soundwav.play()
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.stop()
                        sound = sound_off
                    elif sound == sound_off:
                        if pygame.mixer.music.get_busy() != 1:
                            pygame.mixer.music.load("src/musics/playing.wav")
                            pygame.mixer.music.play(loops=-1)
                        sound = sound_on

                if event.key == K_ESCAPE:
                    if sound == sound_on:
                        soundwav.play()
                    close_door()
                    if sound == sound_on:
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.load("src/musics/Pisky.wav")
                            pygame.mixer.music.play(loops=-1)
                    door_to_begin()

                if event.key == K_r:
                    if sound == sound_on:
                        soundwav.play()
                    close_door()
                    show_game()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if (3<=mouse_pos[0]<=28) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                        close_door()
                        if sound == sound_on:
                            if pygame.mixer.music.get_busy() == 1:
                                pygame.mixer.music.load("src/musics/Pisky.wav")
                                pygame.mixer.music.play(loops=-1)
                        door_to_begin()

                    elif (31<=mouse_pos[0]<=56) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                        close_door()
                        show_game()

                    elif (345<=mouse_pos[0]<=370) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                        pause = pausebtn_off
                        screen.blit(pause, (345, 3))
                        pygame.display.flip()
                        pause_game()

                    elif (372<=mouse_pos[0]<=397) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                            if pygame.mixer.music.get_busy() == 1:
                                pygame.mixer.music.stop()
                            sound = sound_off
                        elif sound == sound_off:
                            if pygame.mixer.music.get_busy() != 1:
                                pygame.mixer.music.load("src/musics/playing.wav")
                                pygame.mixer.music.play(loops=-1)
                            sound = sound_on

        keys = pygame.key.get_pressed()
        if keys[K_a] or keys[K_LEFT]:
            my_hero.image = player[select]
            if my_hero.rect.left >= -edge_left[select]:
                my_hero.rect.left -= 3
        if keys[K_d] or keys[K_RIGHT]:
            my_hero.image = player_right[select]
            if my_hero.rect.left <= 400 - 2 * width[select] + edge_left[select]:
                my_hero.rect.left += 3
        if keys[K_p]:
            if sound == sound_on:
                soundwav.play()
            pause = pausebtn_off
            screen.blit(pause, (345, 3))
            pygame.display.flip()
            pause_game()

        if pause == pausebtn_on:
            new_time += 1

            if new_time > new_pix:
                shit_num = 0
                for each in pedals:
                    if each.image == pedal_shit:
                        shit_num += 1

                probability = random.randint(0, 10)
                if probability == 0:
                    new_pedal = Pedal(pedal_shit)
                elif (0 < probability < 3) and (shit_num < 2):
                    new_pedal = Pedal(pedal_shit)
                elif drop_pro <= probability < 11:
                    new_pedal = Pedal(pedal)
                    if (score // 50) > 80:
                        drop = Drop_thing(drop_shit)
                        drop_shits.append(drop)
                else:
                    new_pedal = Pedal(pedal)

                new_pedal.rect.top = pedals[len(pedals) - 1].rect.top + 50 + new_pix
                pedals.append(new_pedal)
                new_time = 0
                new_pix = random.randint(50, 180)

            if drop_shits != []:
                for shi in drop_shits:
                    shi.rect.top += shi.acc
                    shi.acc += shit_speed
                    check(my_hero, shi)

            for each in pedals:
                each .rect.top -= 1

            for e in pedals:
                result = check(my_hero, e)
                if not result:
                    drop_flag = result

            if drop_flag:
                my_hero.rect.top = my_hero.rect.top + accelerate
                score += accelerate
                accelerate += 0.1
            else:
                accelerate = 1
                my_hero.rect.top -= 1

            raw_meter = 'Meters: ' + str(round((score / 50), 1)) + 'm'
            meter = score_font.render(raw_meter, True, (60, 60, 60))

            screen.blit(second_shot, (0, 0))
            screen.blit(my_hero.image, (my_hero.rect.left, my_hero.rect.top))
            for each in pedals:
                screen.blit(each.image, (each.rect.left, each.rect.top))
            if drop_shits != []:
                for shi in drop_shits:
                    screen.blit(shi.image, (shi.rect.left, shi.rect.top))
            screen.blit(shit, (0, 0))
            screen.blit(back, (3, 3))
            screen.blit(restart, (31, 3))
            screen.blit(sound, (372, 3))
            screen.blit(pause, (345, 3))
            screen.blit(meter, (5, 576))
            pygame.display.flip()
            clock.tick(tic)

            if pedals[0].rect.top < -51:
                del(pedals[0])
            if drop_shits != []:
                if drop_shits[0].rect.top > 600:
                    del(drop_shits[0])
            drop_flag = True
            if (tic < 240):
                tic = 120 + score // 200
            if score > 10000:
                drop_pro = 9
                shit_speed = 0.2
            elif score > 15000:
                drop_pro = 8


def choose_hero():
    global screen, player, hero_name, sound, sound_on, sound_off, back, bg, choice_image, select_image, next_image, \
        previous_image, select, conn, soundwav

    font = pygame.font.Font('src/font/STXINGKA.ttf', 32)
    clock = pygame.time.Clock()
    hero = [0 for i in range(6)]
    interval = (50, 25, 29, 25, 24, 22)
    pos_y = (-10, 0, -10, 0, 0, 0)
    speed = [2, 0]
    select = 0
    name = font.render(hero_name[select], True, (128, 30, 0))
    name_width = name.get_rect().width

    for i in range(6):
        hero[i] = Player(player[i], (0, 0), speed)

    for i in range(450, 201, -5):
        screen.blit(bg, (0, 0))
        for j in range(3):
            screen.blit(hero[j].image, (i - interval[j] + j * 100, 260 + pos_y[j]))
        screen.blit(sound, (372, 3))
        pygame.display.flip()
        clock.tick(160)

    for j in range(6):
        hero[j].rect.left, hero[j].rect.top = (200 - interval[j] + j * 100, 260 + pos_y[j])

    screen_shot = screen.subsurface((0, 0, 400, 600)).copy()
    for i in range(-135, 226, 5):
        screen.blit(screen_shot, (0, 0))
        screen.blit(choice_image, (145, i))
        screen.blit(select_image, (145, -i + 585))
        screen.blit(next_image, (275, -i + 615))
        screen.blit(previous_image, (65, -i + 615))
        screen.blit(back, (345, i // 5 - 42))

        pygame.display.flip()
        clock.tick(200)

    screen.blit(name, (200 - name_width // 2, 485))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                conn.close()
                pygame.quit()
                exit()

            if event.type == KEYUP:
                if event.key == K_m:
                    if sound == sound_on:
                        soundwav.play()
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.stop()
                        sound = sound_off
                    elif sound == sound_off:
                        if pygame.mixer.music.get_busy() != 1:
                            pygame.mixer.music.load("src/musics/Pisky.wav")
                            pygame.mixer.music.play(loops=-1)
                        sound = sound_on
                    screen.blit(sound, (372, 3))
                    pygame.display.flip()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if sound == sound_on:
                        soundwav.play()
                    close_door()
                    door_to_begin()
                if (event.key == K_d)  or (event.key == K_RIGHT):
                    if select != 5:
                        if sound == sound_on:
                            soundwav.play()
                        name = font.render(hero_name[select + 1], True, (128, 30, 0))
                        for j in range(200 - interval[select + 1], hero[select + 1].rect.left, 4):
                            screen.blit(bg, (0, 0))
                            for i in range(6):
                                hero[i].rect.left -= 4
                                screen.blit(hero[i].image, (hero[i].rect.left, hero[i].rect.top))
                            screen.blit(choice_image, (145, 225))
                            screen.blit(select_image, (145, 360))
                            screen.blit(next_image, (275, 390))
                            screen.blit(previous_image, (65, 390))
                            screen.blit(back, (345, 3))
                            screen.blit(sound, (372, 3))
                            screen.blit(name, (200 - name_width // 2, 485))
                            pygame.display.flip()
                            clock.tick(160)
                        select += 1

                if (event.key == K_a) or (event.key == K_LEFT):
                    if select != 0:
                        if sound == sound_on:
                            soundwav.play()
                        name = font.render(hero_name[select - 1], True, (128, 30, 0))
                        for j in range(hero[select - 1].rect.left, 200 - interval[select - 1], 4):
                            screen.blit(bg, (0, 0))
                            for i in range(6):
                                hero[i].rect.left += 4
                                screen.blit(hero[i].image, (hero[i].rect.left, hero[i].rect.top))
                            screen.blit(choice_image, (145, 225))
                            screen.blit(select_image, (145, 360))
                            screen.blit(next_image, (275, 390))
                            screen.blit(previous_image, (65, 390))
                            screen.blit(back, (345, 3))
                            screen.blit(sound, (372, 3))
                            screen.blit(name, (200 - name_width // 2, 485))
                            pygame.display.flip()
                            clock.tick(160)
                        select -= 1

                if (event.key == K_RETURN) or (event.key == K_SPACE) or (event.key == K_KP_ENTER):
                    if sound == sound_on:
                        soundwav.play()
                    close_door()
                    if sound == sound_on:
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.load("src/musics/playing.wav")
                            pygame.mixer.music.play(loops=-1)
                    show_game()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if (372<=mouse_pos[0]<=397) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                            if pygame.mixer.music.get_busy() == 1:
                                pygame.mixer.music.stop()
                            sound = sound_off
                        elif sound == sound_off:
                            if pygame.mixer.music.get_busy() != 1:
                                pygame.mixer.music.load("src/musics/Pisky.wav")
                                pygame.mixer.music.play(loops=-1)
                            sound = sound_on
                        screen.blit(sound, (372, 3))
                        pygame.display.flip()

                    elif (345<=mouse_pos[0]<=370) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                        close_door()
                        door_to_begin()

                    elif (65<=mouse_pos[0]<=125) and (390<=mouse_pos[1]<=450):
                        if select != 0:
                            if sound == sound_on:
                                soundwav.play()
                            name = font.render(hero_name[select - 1], True, (128, 30, 0))
                            for j in range(hero[select - 1].rect.left, 200 - interval[select - 1], 4):
                                screen.blit(bg, (0, 0))
                                for i in range(6):
                                    hero[i].rect.left += 4
                                    screen.blit(hero[i].image, (hero[i].rect.left, hero[i].rect.top))
                                screen.blit(choice_image, (145, 225))
                                screen.blit(select_image, (145, 360))
                                screen.blit(next_image, (275, 390))
                                screen.blit(previous_image, (65, 390))
                                screen.blit(back, (345, 3))
                                screen.blit(sound, (372, 3))
                                screen.blit(name, (200 - name_width // 2, 485))
                                pygame.display.flip()
                                clock.tick(160)
                            select -= 1

                    elif (275<=mouse_pos[0]<=335) and (390<=mouse_pos[1]<=450):
                        if select != 5:
                            if sound == sound_on:
                                soundwav.play()
                            name = font.render(hero_name[select + 1], True, (128, 30, 0))
                            for j in range(200 - interval[select + 1], hero[select + 1].rect.left, 4):
                                screen.blit(bg, (0, 0))
                                for i in range(6):
                                    hero[i].rect.left -= 4
                                    screen.blit(hero[i].image, (hero[i].rect.left, hero[i].rect.top))
                                screen.blit(choice_image, (145, 225))
                                screen.blit(select_image, (145, 360))
                                screen.blit(next_image, (275, 390))
                                screen.blit(previous_image, (65, 390))
                                screen.blit(back, (345, 3))
                                screen.blit(sound, (372, 3))
                                screen.blit(name, (200 - name_width // 2, 485))
                                pygame.display.flip()
                                clock.tick(160)
                            select += 1

                    elif (145<=mouse_pos[0]<=225) and (360<=mouse_pos[1]<=482):
                        if sound == sound_on:
                            soundwav.play()
                        close_door()
                        if sound == sound_on:
                            if pygame.mixer.music.get_busy() == 1:
                                pygame.mixer.music.load("src/musics/playing.wav")
                                pygame.mixer.music.play(loops=-1)
                        show_game()


def all_widgets_leave():
    global screen, player, sound, start_btn, instruction_btn, tip, bg, max_word, delete_data

    clock = pygame.time.Clock()

    for i in range(210, 501, 5):
        screen.blit(bg, (0, 0))
        for j in range(3):
            screen.blit(player[j], (415 - i - (-j + 3) * 65, 100 * j + 10))
        for k in range(3, 6):
            screen.blit(player[k], (i + (k - 3) * 65, 100 * k + 10))
        screen.blit(start_btn, (24, 210 + i))
        screen.blit(instruction_btn, (180, -i + 340))
        screen.blit(max_word, (30, 305 + i))
        screen.blit(delete_data, (3, 469 + i // 2))
        screen.blit(sound, (372, 3))

        pygame.display.flip()
        clock.tick(200)

    choose_hero()


def show_instruction():
    global screen,tip,conn,sound,sound_off,sound_on

    break_flag = False
    screen_shot = screen.subsurface((0, 0, 400, 600)).copy()
    clock = pygame.time.Clock()

    for i in range(-360, 121, 3):
        screen.blit(screen_shot, (0, 0))
        screen.blit(tip, (20, i))

        pygame.display.flip()
        clock.tick(500)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                conn.close()
                pygame.quit()
                exit()

            if event.type == KEYUP:
                if event.key == K_m:
                    if sound == sound_on:
                        soundwav.play()
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.stop()
                        sound = sound_off
                    elif sound == sound_off:
                        if pygame.mixer.music.get_busy() != 1:
                            pygame.mixer.music.load("src/musics/Pisky.wav")
                            pygame.mixer.music.play(loops=-1)
                        sound = sound_on
                    screen.blit(sound, (372, 3))
                    pygame.display.flip()

                if event.key == K_ESCAPE:
                    for i in range(120, 601, 3):
                        screen.blit(screen_shot, (0, 0))
                        screen.blit(tip, (20, i))

                        pygame.display.flip()
                        clock.tick(500)
                    break_flag = True

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if sound == sound_on:
                        soundwav.play()
                    for i in range(120, 601, 3):
                        screen.blit(screen_shot, (0, 0))
                        screen.blit(tip, (20, i))

                        pygame.display.flip()
                        clock.tick(500)
                    break_flag = True
        if break_flag:
            break


def begin():
    global screen,player,start_btn,instruction_btn,sound,sound_on,sound_off,bg,max_score,max_word,cuso,conn,delete_data,\
        soundwav

    cuso.execute('''SELECT * FROM maxscore''')
    value = cuso.fetchall()
    if value == []:
        max_score = '0.0'
    else:
        max_score = value[0][0]

    max_font = pygame.font.Font('src/font/STXINGKA.ttf', 25)
    raw_max = '历史最长高度：' + max_score + 'm'
    max_word = max_font.render(raw_max, True, (255, 255, 255))

    screen.blit(bg, (0, 0))

    for i in range(6):
        screen.blit(player[i], (65 * i + 15, 100 * i + 10))

    screen.blit(start_btn, (24, 420))
    screen.blit(instruction_btn, (180, 130))
    screen.blit(delete_data, (3, 574))
    screen.blit(sound, (372, 3))
    screen_shot = screen.subsurface(0, 0, 400, 600).copy()
    screen.blit(max_word, (30, 515))

    if sound == sound_on:
        if pygame.mixer.music.get_busy() != 1:
            pygame.mixer.music.load("src/musics/Pisky.wav")
            pygame.mixer.music.play(loops=-1)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                conn.close()
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    conn.close()
                    pygame.quit()
                    exit()
                if (event.key == K_SPACE) or (event.key == K_KP_ENTER) or (event.key == K_RETURN):
                    if sound == sound_on:
                        soundwav.play()
                    all_widgets_leave()

            if event.type == KEYUP:
                if event.key == K_m:
                    if sound == sound_on:
                        soundwav.play()
                        if pygame.mixer.music.get_busy() == 1:
                            pygame.mixer.music.stop()
                        sound = sound_off
                    elif sound == sound_off:
                        if pygame.mixer.music.get_busy() != 1:
                            pygame.mixer.music.load("src/musics/Pisky.wav")
                            pygame.mixer.music.play(loops=-1)
                        sound = sound_on
                    screen.blit(sound, (372, 3))
                    pygame.display.flip()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if (372<=mouse_pos[0]<=397) and (3<=mouse_pos[1]<=28):
                        if sound == sound_on:
                            soundwav.play()
                            if pygame.mixer.music.get_busy() == 1:
                                pygame.mixer.music.stop()
                            sound = sound_off
                        elif sound == sound_off:
                            if pygame.mixer.music.get_busy() != 1:
                                pygame.mixer.music.load("src/musics/Pisky.wav")
                                pygame.mixer.music.play(loops=-1)
                            sound = sound_on
                        screen.blit(sound, (372, 3))
                        pygame.display.flip()
                    elif (180<=mouse_pos[0]<=376) and (130<=mouse_pos[1]<=180):
                        if sound == sound_on:
                            soundwav.play()
                        show_instruction()
                    elif (24<=mouse_pos[0]<=220) and (420<=mouse_pos[1]<=470):
                        if sound == sound_on:
                            soundwav.play()
                        all_widgets_leave()
                    elif (mouse_pos[0]<=150) and (574<=mouse_pos[1]):
                        if sound == sound_on:
                            soundwav.play()
                        cuso.execute('''DELETE FROM maxscore WHERE (score = \'%s\')''' % max_score)
                        max_score = '0.0'
                        conn.commit()
                        raw_max = '历史最长高度：' + max_score + 'm'
                        max_word = max_font.render(raw_max, True, (255, 255, 255))
                        screen.blit(screen_shot, (0, 0))
                        screen.blit(max_word, (30, 515))
                        pygame.display.flip()



if __name__ =='__main__':
    begin()