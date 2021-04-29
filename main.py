import pygame
import sys
from pygame.locals import *
import pygame_textinput
import tetrismain
import sqlite3
from sqlite3 import Error

class Main():

    def __init__(self):
        self.screen = pygame.display.set_mode((800, 950), 0, 0, 0,  32)
        self.screen.fill((22, 29, 72))
        self.song = "resources/general.mp3"
        self.icon = "resources/icon.png"
        self.tetris = tetrismain.TetrisGame(self)
        self.player_mode = 0
        self.conn = self.create_connection(r"resources\tetris.db")
        self.names = []

        if self.conn is not None:
            maketable = """CREATE TABLE IF NOT EXISTS players (
                                        score integer NOT NULL,
                                        name text NOT NULL
                                    );"""
            self.create_table(self.conn, maketable)
        else:
            print("error, can't create the database!")

        self.change_music(self.song)
        self.home_screen()

    def home_screen(self):
        pygame.display.set_caption('Tetris')
        while True:

            image = pygame.image.load('resources/TetrisHomeScreen.png')  # get home screen background
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

            self.player_one_button = pygame.image.load('resources/OnePlayerButton.png')  # overlay button imageself.player_one_button = pygame.transform.scale(self.player_one_button, (328, 82))
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
        self.name_screen()  # update screen

    def name_screen(self):
        click = False
        self.textbox = pygame_textinput.TextInput("", "resources/VT323.ttf", 35, True, "white", "white", 400, 35, 10)
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
                    self.pushdb()
                    self.leader_screen()

            pygame.draw.rect(self.screen, (22, 29, 72), self.submit_button)

            self.button = pygame.image.load('resources/SubmitButton.png')  # overlay button image
            self.screen.blit(self.button, (240, 750))

            myfont = pygame.font.Font('resources/VT323.ttf', 60)
            label = myfont.render("Winning player, enter name", True, "white", None)
            self.screen.blit(label,(95, 400))
            label = myfont.render("below!", True, "white", None)
            self.screen.blit(label,(350, 470))
            pygame.draw.rect(self.screen, (4,10,38), pygame.Rect(258, 650, 328, 45))

            self.screen.blit(self.textbox.get_surface(), (263, 650))

            events = pygame.event.get()
            for event in events:
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
            if self.textbox.update(events):
                print(self.textbox.get_text())
            self.playerName = self.textbox.get_text()
            pygame.display.update()  # update screen

    def pushdb(self):
        if self.player_mode == 1:
            try:
                sql = f''' INSERT INTO players(score, name)
                VALUES(?,?)'''
                task = (self.playerName, self.tetris.score)
                cur = self.conn.cursor()
                cur.execute(sql, task)
                self.conn.commit()
            except:
                print("push not successful")
        else:
            #push self.playername, self.tetris.winscore
            try:
                sql = f''' INSERT INTO players(score, name)
                VALUES(?,?)'''
                task = (self.playerName, self.tetris.winscore)
                cur = self.conn.cursor()
                cur.execute(sql, task)
                self.conn.commit()
            except:
                print("push not successful")

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
            return conn
        except Error as e:
            print(e)
        return conn

    def create_table(self, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)
            print("error, database wasn't created")

    def getdata(self, conn):
        cur = conn.cursor()
        cur.execute("SELECT * FROM players")

        rows = cur.fetchall()

        for row in rows:
            self.names.append(row)



    def leader_screen(self):
        click = False
        self.getdata(self.conn)
        if len(self.names) < 6:
            ranks = len(self.names)
        else:
            ranks = 6

        myfont = pygame.font.Font('resources/VT323.ttf', 100)
        myfont2 = pygame.font.Font('resources/VT323.ttf', 70)
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

            namelabel = myfont.render('NAME', True, "white", None)
            self.screen.blit(namelabel,(595,400))

            ranklabel = myfont.render('RANK', True, "white", None)
            self.screen.blit(ranklabel,(50,400))

            scorelabel = myfont.render('SCORE', True, "white", None)
            self.screen.blit(scorelabel,(305,400))


            if ranks > 6:
                start = 480
                for x in range(1,6):
                    numrank = myfont2.render(str(x), True, (143,167,255), None)
                    self.screen.blit(numrank,(110,start))
                    start+=75
            else:
                start = 480
                for x in range(1,ranks):
                    numrank = myfont2.render(str(x), True, (143,167,255), None)
                    self.screen.blit(numrank,(110,start))
                    start+=75
                if ranks < 6:
                    iter = 6 - ranks
                    for x in range (0, iter):
                        dashrank = myfont2.render("-", True, (143,167,255), None)
                        self.screen.blit(dashrank,(110,start))
                        start+=75

            if len(self.names) > 6:
                start = 480
                for x in range(1,6):
                    z = self.names[x][0]
                    y = self.names[x][1]
                    numrank = myfont2.render(str(z), True, (143,167,255), None)
                    self.screen.blit(numrank,(600,start))
                    numrank2 = myfont2.render(str(y), True, (143,167,255), None)
                    self.screen.blit(numrank2,(380,start))
                    start+=75
            else:
                start = 480
                length = len(self.names)
                for x in range(1, length):
                    z = self.names[x][0]
                    y = self.names[x][1]
                    numrank = myfont2.render(str(z), True, (143,167,255), None)
                    self.screen.blit(numrank,(600,start))
                    numrank2 = myfont2.render(str(y), True, (143,167,255), None)
                    self.screen.blit(numrank2,(380,start))
                    start+=75
                if length < 6:
                    iter = 6 - length
                    for x in range (0, iter):
                        dashrank = myfont2.render("---", True, (143,167,255), None)
                        self.screen.blit(dashrank,(620,start))
                        self.screen.blit(dashrank,(360,start))
                        start+=75


            self.button = pygame.image.load('resources/ExitButton.png')  # overlay button image
            self.screen.blit(self.button, (240, 840))

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

            pygame.display.update()

Main()
