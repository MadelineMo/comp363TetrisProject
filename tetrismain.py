import pygame
import sys
from random import randrange as rand

#Board configuration and block size (which can be changed to create different board dimensions: default is a square board 25x25)
blocksize = 30
columnnum = 20
rownum = 25
maxfps = 60

#create a list of the colors (using the RBG color system)
colors = [
(0, 0, 0), #black
(255, 85, 85), #red
(255, 140, 50 ), #orange
(239, 212, 89 ), #yellow
(100, 200, 115), #light green
(50,  120, 52 ), #dark green
(44, 177, 238 ), #blue
(120, 108, 245), #purple
(1, 5, 28) #dark grey (used for the background)
]

# Define the shapes of the single pieces using "0" for blank spaces in the pieces (T, S, Z, J, L, I, O)
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]], #T shape

    [[0, 2, 2],
     [2, 2, 0]], #S shape

    [[3, 3, 0],
     [0, 3, 3]], #Z shape

    [[4, 0, 0],
     [4, 4, 4]], #J shape

    [[0, 0, 5],
     [5, 5, 5]], #L Shape

    [[6, 6, 6, 6]], #I shape

    [[7, 7],
     [7, 7]] #O Shape
]

#create a definition to create a new board
def new_board():
    board = [
        [ 0 for x in range(columnnum) ]
        for y in range(rownum)
    ]
    board += [[ 1 for x in range(columnnum)]]
    return board

#create a definition to remove a row from the board
def remove_row(board, row):
    del board[row]
    return [[0 for i in range(columnnum)]] + board

#create a function to join the matrices
def join_matrices(mat1, mat2, mat2_offset):
    offsetx, offsety = mat2_offset
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+offsety-1 ][cx+offsetx] += val
    return mat1

#create a definition to check and see if collisions occurred
def check_collision(board, shape, offsetval):
    offsetx, offsety = offsetval
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[ cy + offsety ][ cx + offsetx ]:
                    return True
            except IndexError:
                return True
    return False

#create a definition to rotate the pieces
def rotate_clockwise(piece):
    return [
        [ piece[y][x] for y in range(len(piece)) ]
        for x in range(len(piece[0]) - 1, -1, -1)
    ]


#use this class to run the Tetris game
class TetrisGame(object):
    #start by initializing the game as well as the width, height, background
    #grid, font size, and screen
    def __init__(self, mainscreens):
        pygame.init()
        pygame.key.set_repeat(250,25)
        self.width = 800
        self.height = 951
        self.mainscreens = mainscreens
        self.rowlim = blocksize*columnnum
        self.bground_grid = [[ 8 if x%2==y%2 else 0
                               for x in range(columnnum)] for y in range(rownum)]

        self.default_font =  pygame.font.Font(
            pygame.font.get_default_font(), 25)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        #when choosing the piece, make it a random choice
        self.next_piece = tetris_shapes[rand(len(tetris_shapes))]
        self.init_game()

    #create a definition to setup a new piece
    def new_piece(self):
        self.piece = self.next_piece[:]
        self.next_piece = tetris_shapes[rand(len(tetris_shapes))]
        self.piece_x = int(columnnum / 2 - len(self.piece[0])/2)
        self.piece_y = 0

        if check_collision(self.board,
                           self.piece,
                           (self.piece_x, self.piece_y)):
            self.gameover = True

    #create a definition to initialize the game (board, pieces, levels, scores, etc)
    def init_game(self):
        self.board = new_board()
        self.new_piece()
        self.level = 1
        self.score = 0
        self.lines = 0
        pygame.time.set_timer(pygame.USEREVENT+1, 1000)

    #create a function to display messages on the screen
    def disp_msg(self, message, toparea):
        x,y = toparea
        for line in message.splitlines():
            self.screen.blit(
                self.default_font.render(
                    line,
                    False,
                    (255,255,255),
                    (0,0,0)),
                (x,y))
            y+=14

    #create a function to display the message in the center of the screen
    def center_msg(self, message):
        for i, line in enumerate(message.splitlines()):
            messageimage =  self.default_font.render(line, False,
                (255,255,255), (0,0,0))

            messagecenter_x, messagecenter_y = messageimage.get_size()
            messagecenter_x //= 2
            messagecenter_y //= 2

            self.screen.blit(messageimage, (
              self.width // 2-messagecenter_x,
              self.height // 2-messagecenter_y+i*22))

    #create a function to draw the matrix (including the offset values)
    def draw_matrix(self, matrix, offsetval):
        offsetx, offsety  = offsetval
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (offsetx+x) *
                              blocksize,
                            (offsety+y) *
                              blocksize,
                            blocksize,
                            blocksize),0)


    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level
        if self.lines >= self.level*6:
            self.level += 1
            newdelay = 1000-50*(self.level-1)
            newdelay = 100 if newdelay < 100 else newdelay
            pygame.time.set_timer(pygame.USEREVENT+1, newdelay)

    #create a function to move the piece
    def move(self, xchange):
        if not self.gameover and not self.paused:
            new_x = self.piece_x + xchange
            if new_x < 0:
                new_x = 0
            if new_x > columnnum - len(self.piece[0]):
                new_x = columnnum - len(self.piece[0])
            if not check_collision(self.board,
                                   self.piece,
                                   (new_x, self.piece_y)):
                self.piece_x = new_x

    #create a function to drop the piece, check for collisions
    def drop(self, auto):
        if not self.gameover and not self.paused:
            self.score += 1 if auto else 0
            self.piece_y += 1
            if check_collision(self.board,
                               self.piece,
                               (self.piece_x, self.piece_y)):
                self.board = join_matrices(self.board, self.piece,
                  (self.piece_x, self.piece_y))
                self.new_piece()
                cleared_rows = 0
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = remove_row(self.board, i)
                            cleared_rows += 1
                            break
                    else:
                        break
                self.add_cl_lines(cleared_rows)
                return True
        return False

    #create a function to instantly drop the piece
    def insta_drop(self):
        if not self.gameover and not self.paused:
            while(not self.drop(True)):
                pass

    #create a function to rotate a piece if up arrow is pushed
    def rotate_piece(self):
        if not self.gameover and not self.paused:
            new_piece = rotate_clockwise(self.piece)
            if not check_collision(self.board,new_piece,(self.piece_x, self.piece_y)):
                self.piece = new_piece

    #create a function to pause the game (use it when the "p" key is pressed)
    def toggle_pause(self):
        self.paused = not self.paused

    #create function to quit the game
    def quit(self):
        self.center_msg("Ending the game!")
        pygame.display.update()
        sys.exit()

    #create a function to start the game (gameover = False)
    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    #create a function to run the game (include the clock, what the different keys
    #represent, and how to pause game and display things)
    def run(self):
        #create a dictionary for the possible moves: up, down, left, right,
        #p, escape, return, and space (and their coordinate code calls)
        keyslist = {
            'SPACE':    self.start_game,
            'LEFT':     lambda:self.move(-1), #moving left is negative
            'RIGHT':    lambda:self.move(+1),
            'UP':       self.rotate_piece,
            'DOWN':     lambda:self.drop(True),
            'a': lambda: self.move(-1),  # moving left is negative
            'd': lambda: self.move(+1),
            'w': self.rotate_piece,
            's': lambda: self.drop(True),
            'p':        self.toggle_pause,
            'ESCAPE':   self.quit,
            'RETURN':   self.insta_drop
        }

        #start the game with gameover as false (until they lose) and pause as false
        self.gameover = False
        self.paused = False

        clocktime = pygame.time.Clock()
        while 1:
            self.screen.fill((22, 29, 72))
            image = pygame.image.load('resources/TetrisBanner.png')  # get tetris banner
            self.screen.blit(image, (-96, 799))  # paste banner on screen

            mx, my = pygame.mouse.get_pos()  # get mouse points

            self.skip_button = pygame.Rect((620, 730, 171, 65))
            self.end_button = pygame.Rect((620, 827, 171, 65))
            if self.skip_button.collidepoint((mx, my)):  # if button clicked, go to game screen
                if self.click:
                    pass  # to be added in double player
            if self.end_button.collidepoint((mx, my)):  # if button clicked, go to game screen
                if self.click:
                    self.mainscreens.name_screen()
                    pass

            pygame.draw.rect(self.screen, (22, 29, 72), self.skip_button)  # draw skip button
            pygame.draw.rect(self.screen, (22, 29, 72), self.end_button)  # draw end button

            self.skip_button = pygame.image.load('resources/SkipButton.png')  # overlay button image
            self.screen.blit(self.skip_button, (615, 730))

            self.end_button = pygame.image.load('resources/EndButton.png')  # overlay button image
            self.screen.blit(self.end_button, (615, 827))

            #GAMEOVER
            if self.gameover:
                self.center_msg("""Game Over. You Lost! \n\n Score: %d \n\n To start a new game, press SPACE"""
                                % self.score)
            else:
                #PAUSE
                if self.paused:
                    self.center_msg("Game has been paused.")
                else:
                    #IF NOT GAMEOVER/PAUSE
                    pygame.draw.line(self.screen,
                        (255,255,255),
                        (self.rowlim+1, 0),
                        (self.rowlim+1, self.height-1))
                    self.disp_msg("Next:", (
                        self.rowlim+blocksize,
                        3))
                    self.disp_msg("\n Score: %d"
                        % (self.score),
                        (self.rowlim+blocksize, blocksize*5))

                    self.draw_matrix(self.bground_grid, (0,0))
                    self.draw_matrix(self.board, (0,0))
                    self.draw_matrix(self.piece,
                        (self.piece_x, self.piece_y))
                    self.draw_matrix(self.next_piece,
                        (columnnum+1,2))
            pygame.display.update()

            #create movements for the various key events (pause, up, down, quit, etc)
            self.click = False
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:
                    self.drop(False)
                elif event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in keyslist:
                        if event.key == eval("pygame.K_"
                        +key):
                            keyslist[key]()
                if event.type == pygame.MOUSEBUTTONDOWN:  # if mouse clicked, click is true
                    if event.button == 1:
                        self.click = True

            #set the clock to tick with the maxfps given in the beginning
            clocktime.tick(maxfps)


class TetrisGame2Player(object):
    #start by initializing the game as well as the width, height, background
    #grid, font size, and screen
    def __init__(self, mainscreens):
        pygame.init()
        pygame.key.set_repeat(250,25)
        self.width = 800
        self.height = 951
        self.mainscreens = mainscreens
        self.rowlim = blocksize*columnnum
        self.bground_grid = [[ 8 if x%2==y%2 else 0
                               for x in range(columnnum)] for y in range(rownum)]

        self.default_font =  pygame.font.Font(
            pygame.font.get_default_font(), 25)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        #when choosing the piece, make it a random choice
        self.next_piece = tetris_shapes[rand(len(tetris_shapes))]
        self.gametwo = False
        self.init_game()

    #create a definition to setup a new piece
    def new_piece(self):
        self.piece = self.next_piece[:]
        self.next_piece = tetris_shapes[rand(len(tetris_shapes))]
        self.piece_x = int(columnnum / 2 - len(self.piece[0])/2)
        self.piece_y = 0

        if check_collision(self.board,
                           self.piece,
                           (self.piece_x, self.piece_y)):
            self.gameover = True

    #create a definition to initialize the game (board, pieces, levels, scores, etc)
    def init_game(self):
        self.board = new_board()
        self.new_piece()
        self.level = 1
        self.score = 0
        self.lines = 0
        pygame.time.set_timer(pygame.USEREVENT+1, 1000)

    #create a function to display messages on the screen
    def disp_msg(self, message, toparea):
        x,y = toparea
        for line in message.splitlines():
            self.screen.blit(
                self.default_font.render(
                    line,
                    False,
                    (255,255,255),
                    (0,0,0)),
                (x,y))
            y+=14

    #create a function to display the message in the center of the screen
    def center_msg(self, message):
        for i, line in enumerate(message.splitlines()):
            messageimage =  self.default_font.render(line, False,
                (255,255,255), (0,0,0))

            messagecenter_x, messagecenter_y = messageimage.get_size()
            messagecenter_x //= 2
            messagecenter_y //= 2

            self.screen.blit(messageimage, (
              self.width // 2-messagecenter_x,
              self.height // 2-messagecenter_y+i*22))

    #create a function to draw the matrix (including the offset values)
    def draw_matrix(self, matrix, offsetval):
        offsetx, offsety  = offsetval
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (offsetx+x) *
                              blocksize,
                            (offsety+y) *
                              blocksize,
                            blocksize,
                            blocksize),0)


    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level
        if self.lines >= self.level*6:
            self.level += 1
            newdelay = 1000-50*(self.level-1)
            newdelay = 100 if newdelay < 100 else newdelay
            pygame.time.set_timer(pygame.USEREVENT+1, newdelay)

    #create a function to move the piece
    def move(self, xchange):
        if not self.gameover and not self.paused:
            new_x = self.piece_x + xchange
            if new_x < 0:
                new_x = 0
            if new_x > columnnum - len(self.piece[0]):
                new_x = columnnum - len(self.piece[0])
            if not check_collision(self.board,
                                   self.piece,
                                   (new_x, self.piece_y)):
                self.piece_x = new_x

    #create a function to drop the piece, check for collisions
    def drop(self, auto):
        if not self.gameover and not self.paused:
            self.score += 1 if auto else 0
            self.piece_y += 1
            if check_collision(self.board,
                               self.piece,
                               (self.piece_x, self.piece_y)):
                self.board = join_matrices(self.board, self.piece,
                  (self.piece_x, self.piece_y))
                self.new_piece()
                cleared_rows = 0
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = remove_row(self.board, i)
                            cleared_rows += 1
                            break
                    else:
                        break
                self.add_cl_lines(cleared_rows)
                return True
        return False

    #create a function to instantly drop the piece
    def insta_drop(self):
        if not self.gameover and not self.paused:
            while(not self.drop(True)):
                pass

    #create a function to rotate a piece if up arrow is pushed
    def rotate_piece(self):
        if not self.gameover and not self.paused:
            new_piece = rotate_clockwise(self.piece)
            if not check_collision(self.board,new_piece,(self.piece_x, self.piece_y)):
                self.piece = new_piece

    #create a function to pause the game (use it when the "p" key is pressed)
    def toggle_pause(self):
        self.paused = not self.paused

    #create function to quit the game
    def quit(self):
        self.center_msg("Ending the game!")
        pygame.display.update()
        sys.exit()

    #create a function to start the game (gameover = False)
    def start_game(self):
        if self.gameover:
            if self.gametwo == False:
                self.gametwo = True
            elif self.gametwo == True:
                self.gametwo = False
            self.init_game()
            self.gameover = False

    #create a function to run the game (include the clock, what the different keys
    #represent, and how to pause game and display things)
    def run(self):
        #create a dictionary for the possible moves: up, down, left, right,
        #p, escape, return, and space (and their coordinate code calls)
        keyslist = {
            'SPACE':    self.start_game,
            'LEFT':     lambda:self.move(-1), #moving left is negative
            'RIGHT':    lambda:self.move(+1),
            'UP':       self.rotate_piece,
            'DOWN':     lambda:self.drop(True),
            'a': lambda: self.move(-1),  # moving left is negative
            'd': lambda: self.move(+1),
            'w': self.rotate_piece,
            's': lambda: self.drop(True),
            'p':        self.toggle_pause,
            'ESCAPE':   self.quit,
            'RETURN':   self.insta_drop
        }

        #start the game with gameover as false (until they lose) and pause as false
        self.gameover = False
        self.paused = False

        p1score = 0
        p2score = 0

        clocktime = pygame.time.Clock()
        while 1:
            self.screen.fill((22, 29, 72))
            image = pygame.image.load('resources/TetrisBanner.png')  # get tetris banner
            self.screen.blit(image, (-96, 799))  # paste banner on screen

            mx, my = pygame.mouse.get_pos()  # get mouse points

            self.skip_button = pygame.Rect((620, 730, 171, 65))
            self.end_button = pygame.Rect((620, 827, 171, 65))
            if self.skip_button.collidepoint((mx, my)):  # if button clicked, go to game screen
                if self.click:
                    pass  # to be added in double player
            if self.end_button.collidepoint((mx, my)):  # if button clicked, go to game screen
                if self.click:
                    self.mainscreens.name_screen()
                    pass

            pygame.draw.rect(self.screen, (22, 29, 72), self.skip_button)  # draw skip button
            pygame.draw.rect(self.screen, (22, 29, 72), self.end_button)  # draw end button

            self.skip_button = pygame.image.load('resources/SkipButton.png')  # overlay button image
            self.screen.blit(self.skip_button, (615, 730))

            self.end_button = pygame.image.load('resources/EndButton.png')  # overlay button image
            self.screen.blit(self.end_button, (615, 827))

            #GAMEOVER
            if self.gameover:
                if self.gametwo == False:
                    self.center_msg("""Player 1: Game Over \n\n Score: %d \n\n When Player 2 is ready, press SPACE"""
                                % self.score)
                    p1score = self.score
                elif self.gametwo == True:
                    p2score = self.score
                    if p1score > p2score:
                        self.center_msg("""Player 2: Game Over. Player 1 Wins! \n\nP1 Score: %d \nP2 Score: %d\n\n To start a new 2 player game, press SPACE""" % (p1score, p2score))
                        self.winscore = p1score
                    elif p2score > p1score:
                        self.center_msg("""Player 2: Game Over. Player 2 Wins! \n\nP1 Score: %d \nP2 Score: %d\n\n To start a brand new 2 player game, press SPACE""" % (p1score, p2score))
                        self.winscore = p2score
            else:
                #PAUSE
                if self.paused:
                    self.center_msg("Game has been paused.")
                else:
                    #IF NOT GAMEOVER/PAUSE
                    pygame.draw.line(self.screen,
                        (255,255,255),
                        (self.rowlim+1, 0),
                        (self.rowlim+1, self.height-1))
                    self.disp_msg("Next:", (
                        self.rowlim+blocksize,
                        3))
                    self.disp_msg("\n Score: %d"
                        % (self.score),
                        (self.rowlim+blocksize, blocksize*5))

                    self.draw_matrix(self.bground_grid, (0,0))
                    self.draw_matrix(self.board, (0,0))
                    self.draw_matrix(self.piece,
                        (self.piece_x, self.piece_y))
                    self.draw_matrix(self.next_piece,
                        (columnnum+1,2))
            pygame.display.update()

            #create movements for the various key events (pause, up, down, quit, etc)
            self.click = False
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:
                    self.drop(False)
                elif event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in keyslist:
                        if event.key == eval("pygame.K_"
                        +key):
                            keyslist[key]()
                if event.type == pygame.MOUSEBUTTONDOWN:  # if mouse clicked, click is true
                    if event.button == 1:
                        self.click = True

            #set the clock to tick with the maxfps given in the beginning
            clocktime.tick(maxfps)

#then run the Tetris App in the main screen
if __name__ == '__main__':
    tetris = TetrisGame()
    tetris.run()
