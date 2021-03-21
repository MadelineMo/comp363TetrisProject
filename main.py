import pygame
import sys
from pygame.locals import *
import tetrismain

class Main():

    def __init__(self):
        self.screen = pygame.display.set_mode((800, 951), 0, 0, 0,  32)
        self.screen.fill((0, 0, 0))
        self.song = "resources/general.mp3"
        self.icon = "resources/icon.png"
        self.tetris = tetrismain.TetrisGame(self)
        self.player_mode = 0

        self.change_music(self.song)
        self.home_screen()

    def home_screen(self):
        pygame.display.set_caption('Tetris')
        while True:

            image = pygame.image.load('resources/TetrisHomeScreen.png')  # get home screen background
            image = pygame.transform.scale(image, (800, 951))  # resize image
            self.screen.blit(image, (0, 0))  # paste image on screen

            programIcon = pygame.image.load(self.icon)
            pygame.display.set_icon(programIcon)

            # exit game
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:  # if space pressed, go to game screen
                        self.player_screen()
                    if event.key == K_ESCAPE:  # if escape pressed, exit window
                        pygame.quit()
                        sys.exit()
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def change_music(self, song):
            pygame.init()
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(-1)

    def player_screen(self):
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
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            image = pygame.image.load('resources/TetrisPlayerScreen.png')  # get player screen background
            image = pygame.transform.scale(image, (800, 951))  # resize image
            self.screen.blit(image, (0, 0))  # paste background on screen

            mx, my = pygame.mouse.get_pos()  # get mouse point

            self.player_button_1 = pygame.Rect((25, 727, 304, 82))
            self.player_button_2 = pygame.Rect((439, 727, 328, 82))
            self.leader_button = pygame.Rect((239, 844, 328, 82))
            if self.player_button_1.collidepoint((mx, my)):  # if button clicked, go to game screen
                if click:
                    self.player_mode = 1  # single player mode
                    self.game_screen()
            if self.player_button_2.collidepoint((mx, my)):  # if button clicked, go to game screen
                if click:
                    self.player_mode = 2  # two player mode
                    self.game_screen()
            if self.leader_button.collidepoint((mx, my)):
                if click:
                    self.leader_screen()
            pygame.draw.rect(self.screen, (22, 29, 72), self.player_button_1)  # draw player one button
            pygame.draw.rect(self.screen, (22, 29, 72), self.player_button_2)  # draw player one button
            pygame.draw.rect(self.screen, (22, 29, 72), self.leader_button)  # draw leader button

            self.player_one_button = pygame.image.load('resources/OnePlayerButton.png')  # overlay button image
            self.player_one_button = pygame.transform.scale(self.player_one_button, (328, 82))
            self.screen.blit(self.player_one_button, (25, 727))

            self.player_two_button = pygame.image.load('resources/TwoPlayerButton.png')  # overlay button image
            self.player_two_button = pygame.transform.scale(self.player_two_button, (328, 82))
            self.screen.blit(self.player_two_button, (439, 727))

            leader_button_image = pygame.image.load('resources/LeaderButton.png')  # overlay button image
            leader_button_image = pygame.transform.scale(leader_button_image, (328, 82))
            self.screen.blit(leader_button_image, (239, 844))

            out_of_order_image = pygame.image.load('resources/PlayersOutOfOrder.png')  # overlay out of order image
            out_of_order_image = pygame.transform.scale(out_of_order_image, (344, 484))
            self.screen.blit(out_of_order_image, (430, 338))

            pygame.display.update()


    def game_screen(self):
        self.tetris = tetrismain.TetrisGame(self)
        self.tetris.run()
        pygame.display.update()
        self.name_screen()  # update screen

    def name_screen(self):
        click = False
        while True:
            image = pygame.image.load('resources/NamesOutOfOrder.png')  # name screen (out of order version)
            image = pygame.transform.scale(image, (800, 951))  # resize image
            self.screen.blit(image, (0, 0))  # paste image on screen

            mx, my = pygame.mouse.get_pos()  # get mouse point

            self.submit_button = pygame.Rect((258, 735, 328, 82))
            if self.submit_button.collidepoint((mx, my)):  # if button clicked, go to leader screen
                if click:
                    self.leader_screen()

            pygame.draw.rect(self.screen, (22, 29, 72), self.submit_button)

            self.button = pygame.image.load('resources/SubmitButton.png')  # overlay button image
            self.button = pygame.transform.scale(self.button, (328, 82))
            self.screen.blit(self.button, (258, 735))

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  # if escape pressed, exit window
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:  # if mouse clicked, click is true
                    if event.button == 1:
                        click = True
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()  # update screen


    def leader_screen(self):
        while True:
            image = pygame.image.load('resources/LeaderboardOutOfOrder.png')  # get leader screen (out of order version)
            image = pygame.transform.scale(image, (800, 951))  # resize image
            self.screen.blit(image, (0, 0))  # paste image on screen

            mx, my = pygame.mouse.get_pos()  # get mouse point

            self.exit_button = pygame.Rect((300, 867, 196, 59))

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
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            if self.exit_button.collidepoint((mx, my)):  # if button clicked, go to game screen
                if click:
                    self.credit_screen()

            pygame.draw.rect(self.screen, (22, 29, 72), self.exit_button)  # draw exit button

            self.button = pygame.image.load('resources/ExitButton.png')  # overlay button image
            self.button = pygame.transform.scale(self.button, (196, 59))
            self.screen.blit(self.button, (300, 867))


            pygame.display.update()  # update screen


    def credit_screen(self):
        while True:
            image = pygame.image.load('resources/TetrisCreditsScreen.png')  # get home screen background
            image = pygame.transform.scale(image, (800, 951))  # resize image
            self.screen.blit(image, (0, 0))  # paste image on screen

            mx, my = pygame.mouse.get_pos()  # get mouse point

            self.rematch_button = pygame.Rect((233, 665, 328, 82))
            self.home_button = pygame.Rect((236, 777, 328, 82))

            if self.rematch_button.collidepoint((mx, my)):  # if button clicked, go to game screen
                if click:
                    self.game_screen()
            if self.home_button.collidepoint((mx, my)):  # if button clicked, go to home screen
                if click:
                    self.home_screen()

            pygame.draw.rect(self.screen, (22, 29, 72), self.rematch_button)  # draw rematch button
            pygame.draw.rect(self.screen, (22, 29, 72), self.home_button)  # draw player one button

            rematch_button_image = pygame.image.load('resources/RematchButton.png')  # overlay button image
            rematch_button_image = pygame.transform.scale(rematch_button_image, (328, 82))
            self.screen.blit(rematch_button_image, (233, 665))

            home_button_image = pygame.image.load('resources/HomeButton.png')  # overlay button image
            home_button_image = pygame.transform.scale(home_button_image, (328, 82))
            self.screen.blit(home_button_image, (236, 777))

            click = False
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  # if escape pressed, exit window
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:  # if mouse clicked, click is true
                    if event.button == 1:
                        click = True
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()  # update screen

Main()
