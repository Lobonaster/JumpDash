import pygame
import sys
from level import Level
from game_data import level1

pygame.init()
screen = pygame.display.set_mode((1420, 960))
clock = pygame.time.Clock()

layouts = {
    0: level1
}
levels = {
    0: Level(layouts[0], 1, screen)
}

def main_menu(state, progress):
    x = 0
    shift = 0.2
    s = pygame.Surface((400, 960), pygame.SRCALPHA)
    s.fill((255, 255, 255, 128))
    sky_main_screen = pygame.image.load('assets/sky/sky_main_screen.png').convert_alpha()
    logo = pygame.image.load('assets/misc_art/logo.png').convert_alpha()
    play = pygame.image.load('assets/misc_art/play.png').convert_alpha()
    lvl1 = pygame.image.load('assets/misc_art/1.png').convert_alpha()

    click = False
    counter1 = 0
    counter2 = 0

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

            if event.type == pygame.MOUSEBUTTONUP:
                click = False

        screen.fill('black')

        x -= shift
        if x < -1420:
            shift *= -1
        screen.blit(sky_main_screen, (x, 0))

        screen.blit(s, (0, 0))
        screen.blit(logo, (20, 100))

        if state == 0:
            screen.blit(play, (30, 480))
            button = play.get_rect(topleft=(30, 480))
            if button.collidepoint((mx, my)):
                if click:
                    state = 0.5

        elif state == 0.5:
            screen.blit(play, (30 - counter2, 480))
            button = play.get_rect(topleft=(30 - counter2, 480))
            counter1 += 1
            counter2 += counter1
            if button.right < 0:
                state = 1

        elif state == 1:

            if progress >= 0:
                screen.blit(lvl1, (-120 + counter2, 400))
                button1 = lvl1.get_rect(topleft=(-120 + counter2, 400))
                counter1 += 1
                counter2 += counter1
                if button1.left > 50:
                    state = 2


        elif state >= 2:

            screen.blit(lvl1, (50, 400))
            button1 = lvl1.get_rect(topleft=(50, 400))
            if button1.collidepoint((mx, my)):
                if click:
                    level_func(0, progress)



        pygame.display.update()
        clock.tick(60)


def level_func(level_num, progress):
    s = pygame.Surface((1500, 960), pygame.SRCALPHA)
    s.fill((30, 30, 30, 150))
    level = levels[level_num]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit

        screen.fill('black')
        level.run()

        if not level.check_living_status():
            levels[level_num] = Level(layouts[level_num], level_num + 1, screen)
            screen.blit(s, (0, 0))
            exit_level(False)
            screen.blit(s, (0, 0))
            main_menu(2, progress)

        elif level.check_void_death():
            levels[level_num] = Level(layouts[level_num], level_num + 1, screen)
            screen.blit(s, (0, 0))
            exit_level(False)
            screen.blit(s, (0, 0))
            main_menu(2, progress)

        if level.check_end():
            levels[level_num] = Level(layouts[level_num], level_num + 1, screen)
            screen.blit(s, (0, 0))
            exit_level(True)
            if level_num != 3:
                main_menu(0, level_num + 1)
            else:
                main_menu(0, 2)

        pygame.display.update()
        clock.tick(60)


def exit_level(iscomplete):
    font = pygame.font.Font('assets/ui/ARCADEPI.TTF', 90)

    text1 = font.render('Level Failed', True, (255, 255, 255), None)
    text1_shadow = font.render('Level Failed', True, (0, 40, 40), None)
    text2 = font.render('Level Complete', True, (255, 255, 255), None)
    text2_shadow = font.render('Level Complete', True, (0, 40, 40), None)

    if not iscomplete:
        text = text1
        text_shadow = text1_shadow
    else:
        text = text2
        text_shadow = text2_shadow

    text_rect = text.get_rect(center=(710, 480))
    text_shadow_rect = text_shadow.get_rect(center=(720, 490))

    while True:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            return -1

        screen.blit(text_shadow, text_shadow_rect)
        screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


main_menu(0, 0)