import pygame
import sys
from pygame.locals import *


screen = pygame.display.set_mode((800, 951), 0, 0, 0,  32)
player_mode = 0


def home_screen():
    while True:
        image = pygame.image.load('TetrisHomeScreen.png')  # get home screen background
        image = pygame.transform.scale(image, (800, 951))  # resize image
        screen.blit(image, (0, 0))  # paste image on screen

        # exit game
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:  # if space pressed, go to game screen
                    game_screen()
                if event.key == K_ESCAPE:  # if escape pressed, exit window
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:  # if mouse clicked, click is true
                if event.button == 1:
                    click = True

        pygame.display.update()


def player_screen():
    while True:  # stand in
        image = pygame.image.load('TetrisPlayerScreen.png')  # get player screen background
        image = pygame.transform.scale(image, (800, 951))  # resize image
        screen.blit(image, (0, 0))  # paste image on screen

        mx, my = pygame.mouse.get_pos()  # get mouse point

        player_button_1 = pygame.Rect((25, 727, 304, 82))
        player_button_2 = pygame.Rect((439, 727, 328, 82))
        if player_button_1.collidepoint((mx, my)):  # if button clicked, go to game screen
            if click:
                player_mode = 1  # single player mode
                game_screen()
        if player_button_2.collidepoint((mx, my)):  # if button clicked, go to game screen
            if click:
                player_mode = 2  # two player mode
                game_screen()

        pygame.draw.rect(screen, (153, 73, 255), player_button_1)  # draw player one button
        pygame.draw.rect(screen, (153, 73, 255), player_button_2)  # draw player one button

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

        pygame.display.update()


def game_screen():
    while True:
        image = pygame.image.load('TetrisGameScreen.png')  # get home screen background
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

        pygame.draw.rect(screen, (153, 73, 255), skip_button)  # draw skip button
        pygame.draw.rect(screen, (37, 45, 246), end_button)  # draw end button


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


def name_screen():
    while True:
        image = pygame.image.load('TetrisNameScreen.png')  # get home screen background
        image = pygame.transform.scale(image, (800, 951))  # resize image
        screen.blit(image, (0, 0))  # paste image on screen

        mx, my = pygame.mouse.get_pos()  # get mouse point

        submit_button = pygame.Rect((258, 735, 328, 82))
        if submit_button.collidepoint((mx, my)):  # if button clicked, go to leader screen
            if click:
                leader_screen()

        pygame.draw.rect(screen, (37, 45, 246), submit_button)

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
        image = pygame.image.load('TetrisLeaderboardScreen.png')  # get home screen background
        image = pygame.transform.scale(image, (800, 951))  # resize image
        screen.blit(image, (0, 0))  # paste image on screen

        mx, my = pygame.mouse.get_pos()  # get mouse point

        exit_button = pygame.Rect((300, 867, 196, 59))

        if exit_button.collidepoint((mx, my)):  # if button clicked, go to game screen
            if click:
                credit_screen()

        pygame.draw.rect(screen, (37, 45, 246), exit_button)  # draw exit button

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


def credit_screen():
    while True:
        image = pygame.image.load('TetrisCreditsScreen.png')  # get home screen background
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

        pygame.draw.rect(screen, (153, 73, 255), rematch_button)  # draw rematch button
        pygame.draw.rect(screen, (37, 45, 246), home_button)  # draw player one button

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
home_screen()
