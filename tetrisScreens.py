import pygame
import sys
from pygame.locals import *
import tetrismain

song = "resources/general.mp3"
icon = "resources/icon.png"
programIcon = pygame.image.load(icon)
pygame.display.set_icon(programIcon)
screen = pygame.display.set_mode((800, 951), 0, 0, 0,  32)
player_mode = 0

def home_screen():
    pygame.display.set_caption('Tetris')
    while True:

        image = pygame.image.load('resources/TetrisHomeScreen.png')  # get home screen background
        image = pygame.transform.scale(image, (800, 951))  # resize image
        screen.blit(image, (0, 0))  # paste image on screen

        # exit game
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:  # if space pressed, go to game screen
                    player_screen()
                if event.key == K_ESCAPE:  # if escape pressed, exit window
                    pygame.quit()
                    sys.exit()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def change_music(song):
        pygame.init()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(-1)

def player_screen():
    while True:  # stand in
        click = False  # get rid of space, add type == QUIT, copy to all others
        # exit game
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # if escape pressed, exit window
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:  # if mouse clicked, click is true
                if event.button == 1:
                    click = True

        image = pygame.image.load('resources/TetrisPlayerScreen.png')  # get player screen background
        image = pygame.transform.scale(image, (800, 951))  # resize image
        screen.blit(image, (0, 0))  # paste background on screen

        mx, my = pygame.mouse.get_pos()  # get mouse point

        player_button_1 = pygame.Rect((25, 727, 304, 82))
        player_button_2 = pygame.Rect((439, 727, 328, 82))
        leader_button = pygame.Rect((239, 844, 328, 82))
        if player_button_1.collidepoint((mx, my)):  # if button clicked, go to game screen
            if click:
                player_mode = 1  # single player mode
                game_screen()
        if player_button_2.collidepoint((mx, my)):  # if button clicked, go to game screen
            if click:
                player_mode = 2  # two player mode
                game_screen()
        if leader_button.collidepoint((mx, my)):
            if click:
                leader_screen()
        pygame.draw.rect(screen, (22, 29, 72), player_button_1)  # draw player one button
        pygame.draw.rect(screen, (22, 29, 72), player_button_2)  # draw player one button
        pygame.draw.rect(screen, (22, 29, 72), leader_button)  # draw leader button

        player_one_button = pygame.image.load('resources/OnePlayerButton.png')  # overlay button image
        player_one_button = pygame.transform.scale(player_one_button, (328, 82))
        screen.blit(player_one_button, (25, 727))

        player_two_button = pygame.image.load('resources/TwoPlayerButton.png')  # overlay button image
        player_two_button = pygame.transform.scale(player_two_button, (328, 82))
        screen.blit(player_two_button, (439, 727))

        leader_button_image = pygame.image.load('resources/LeaderButton.png')  # overlay button image
        leader_button_image = pygame.transform.scale(leader_button_image, (328, 82))
        screen.blit(leader_button_image, (239, 844))

        pygame.display.update()


def game_screen():
    while True:
        image = pygame.image.load('resources/TetrisGameScreen.png')  # get home screen background
        image = pygame.transform.scale(image, (800, 951))  # resize image
        screen.blit(image, (0, 0))  # paste image on screen

        mx, my = pygame.mouse.get_pos()  # get mouse point

        skip_button = pygame.Rect((620, 730, 171, 65))
        end_button = pygame.Rect((620, 827, 171, 65))

        if skip_button.collidepoint((mx, my)):  # if button clicked, go to game screen
            if click:
                pass  # to be added in double player
        if end_button.collidepoint((mx, my)):  # if button clicked, go to game screen
            if click:
                name_screen()

        pygame.draw.rect(screen, (22, 29, 72), skip_button)  # draw skip button
        pygame.draw.rect(screen, (22, 29, 72), end_button)  # draw end button

        skip_button = pygame.image.load('resources/SkipButton.png')  # overlay button image
        skip_button = pygame.transform.scale(skip_button, (171, 65))
        screen.blit(skip_button, (620, 730))

        end_button = pygame.image.load('resources/EndButton.png')  # overlay button image
        end_button = pygame.transform.scale(end_button, (171, 65))
        screen.blit(end_button, (620, 827))

        click = False
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # if escape pressed, exit window
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:  # if mouse clicked, click is true
                if event.button == 1:
                    click = True

        game_start()
        pygame.display.update()  # update screen

def game_start():
    tetris = tetrismain.TetrisGame()
    tetris.run()


def name_screen():
    while True:
        image = pygame.image.load('resources/TetrisNameScreen.png')  # get home screen background
        image = pygame.transform.scale(image, (800, 951))  # resize image
        screen.blit(image, (0, 0))  # paste image on screen

        mx, my = pygame.mouse.get_pos()  # get mouse point

        submit_button = pygame.Rect((258, 735, 328, 82))
        if submit_button.collidepoint((mx, my)):  # if button clicked, go to leader screen
            if click:
                leader_screen()

        pygame.draw.rect(screen, (22, 29, 72), submit_button)

        button = pygame.image.load('resources/SubmitButton.png')  # overlay button image
        button = pygame.transform.scale(button, (328, 82))
        screen.blit(button, (258, 735))

        click = False
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # if escape pressed, exit window
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:  # if mouse clicked, click is true
                if event.button == 1:
                    click = True
        pygame.display.update()  # update screen


def leader_screen():
    while True:
        image = pygame.image.load('resources/TetrisLeaderboardScreen.png')  # get home screen background
        image = pygame.transform.scale(image, (800, 951))  # resize image
        screen.blit(image, (0, 0))  # paste image on screen

        mx, my = pygame.mouse.get_pos()  # get mouse point

        exit_button = pygame.Rect((300, 867, 196, 59))

        # for some reason, this one decided to need to be different
        click = False
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # if escape pressed, exit window
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:  # if mouse clicked, click is true
                if event.button == 1:
                    click = True

        if exit_button.collidepoint((mx, my)):  # if button clicked, go to game screen
            if click:
                credit_screen()

        pygame.draw.rect(screen, (22, 29, 72), exit_button)  # draw exit button

        button = pygame.image.load('resources/ExitButton.png')  # overlay button image
        button = pygame.transform.scale(button, (196, 59))
        screen.blit(button, (300, 867))


        pygame.display.update()  # update screen


def credit_screen():
    while True:
        image = pygame.image.load('resources/TetrisCreditsScreen.png')  # get home screen background
        image = pygame.transform.scale(image, (800, 951))  # resize image
        screen.blit(image, (0, 0))  # paste image on screen

        mx, my = pygame.mouse.get_pos()  # get mouse point

        rematch_button = pygame.Rect((233, 665, 328, 82))
        home_button = pygame.Rect((236, 777, 328, 82))

        if rematch_button.collidepoint((mx, my)):  # if button clicked, go to game screen
            if click:
                game_screen()
        if home_button.collidepoint((mx, my)):  # if button clicked, go to home screen
            if click:
                home_screen()

        pygame.draw.rect(screen, (22, 29, 72), rematch_button)  # draw rematch button
        pygame.draw.rect(screen, (22, 29, 72), home_button)  # draw player one button

        rematch_button_image = pygame.image.load('resources/RematchButton.png')  # overlay button image
        rematch_button_image = pygame.transform.scale(rematch_button_image, (328, 82))
        screen.blit(rematch_button_image, (233, 665))

        home_button_image = pygame.image.load('resources/HomeButton.png')  # overlay button image
        home_button_image = pygame.transform.scale(home_button_image, (328, 82))
        screen.blit(home_button_image, (236, 777))

        click = False
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # if escape pressed, exit window
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:  # if mouse clicked, click is true
                if event.button == 1:
                    click = True

        pygame.display.update()  # update screen


screen.fill((0, 0, 0))
change_music(song)
home_screen()
