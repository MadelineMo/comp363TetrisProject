import pygame
import sys
from pygame.locals import *
import tetrismain

class Main():

    def __init__(self):
        self.screen = pygame.display.set_mode((800, 950), 0, 0, 0,  32)
        self.screen.fill((22, 29, 72))
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
            self.screen.blit(image, (0, 0))  # paste image on screen

           # programIcon = pygame.image.load(self.icon)
           # pygame.display.set_icon(programIcon)

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
            click = False
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

            self.screen.fill((22, 29, 72))  # reset background
            image = pygame.image.load('resources/TetrisBanner.png')  # get tetris banner
            self.screen.blit(image, (0, 18))  # paste banner on screen
            image = pygame.image.load('resources/PlayersText.png')  # 'how many players?'
            self.screen.blit(image, (75, 215))
            image = pygame.image.load('resources/PlayerOneIcon.png')  # one player image
            self.screen.blit(image, (50, 360))
            image = pygame.image.load('resources/PlayerTwoIcon.png')  # Two player image
            self.screen.blit(image, (470, 360))

            mx, my = pygame.mouse.get_pos()  # get mouse point

            self.player_button_1 = pygame.Rect((25, 727, 328, 82))
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
            self.screen.blit(self.player_one_button, (30, 730))

            self.player_two_button = pygame.image.load('resources/TwoPlayerButton.png')  # overlay button image
            self.screen.blit(self.player_two_button, (450, 730))

            leader_button_image = pygame.image.load('resources/LeaderButton.png')  # overlay button image
            self.screen.blit(leader_button_image, (240, 840))

            pygame.display.update()

    def game_screen(self):
        if self.player_mode == 1:
            self.tetris = tetrismain.TetrisGame(self)
        elif self.player_mode == 2:
            self.tetris = tetrismain.TetrisGame2Player(self)
        self.tetris.run()
        pygame.display.update()

    def name_screen(self):
        click = False
        while True:
            self.screen.fill((22, 29, 72))  # reset background
            image = pygame.image.load('resources/TetrisBanner.png')  # get tetris banner
            self.screen.blit(image, (0, 18))  # paste banner on screen
            image = pygame.image.load('resources/RainbowBoarder.png')  # get rainbow boarder
            self.screen.blit(image, (30, 170))
            image = pygame.image.load('resources/SubTitleText.png')  # 'Thanks for playing'
            self.screen.blit(image, (142.5, 200))

            mx, my = pygame.mouse.get_pos()  # get mouse point

            self.submit_button = pygame.Rect((258, 735, 328, 82))
            if self.submit_button.collidepoint((mx, my)):  # if button clicked, go to leader screen
                if click:
                    self.leader_screen()

            pygame.draw.rect(self.screen, (22, 29, 72), self.submit_button)

            self.button = pygame.image.load('resources/SubmitButton.png')  # overlay button image
            self.screen.blit(self.button, (240, 750))

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
        click = False
        while True:
            self.screen.fill((22, 29, 72))  # reset background
            image = pygame.image.load('resources/LeaderboardBanner.png')  # get leader screen
            self.screen.blit(image, (0, 48))  # paste image on screen

            mx, my = pygame.mouse.get_pos()  # get mouse point

            self.exit_button = pygame.Rect((240, 824, 328, 82))

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
            self.screen.blit(self.button, (240, 824))

            pygame.display.update()  # update screen

    def credit_screen(self):
        click = False
        while True:
            self.screen.fill((22, 29, 72))  # reset background
            image = pygame.image.load('resources/TetrisBanner.png')  # get tetris banner
            self.screen.blit(image, (0, 18))  # paste banner on screen
            image = pygame.image.load('resources/RainbowBoarder.png')  # get rainbow boarder
            self.screen.blit(image, (30, 170))
            image = pygame.image.load('resources/CreditsText.png')  # credits
            self.screen.blit(image, (150, 190))

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
            self.screen.blit(rematch_button_image, (240, 652))

            home_button_image = pygame.image.load('resources/HomeButton.png')  # overlay button image
            self.screen.blit(home_button_image, (240, 766))


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
