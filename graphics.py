from itertools import cycle
from time import sleep
import pygame
import logic

# TODO:
# - Lag computer input.
# - Add triple lines upon winning/losing.
# - Add score.
# - Add win/lose/draw message.

# Setting up window
HEIGHT = 600
WIDTH = 480
FPS = 30
TITLE = "Tic-tac-toe"

# Game variables
SIZE = 450
TOP = 100
CELL = SIZE // 3
BORDER = 5
FILL_CELLS = False
CROSS = "img/cross.png"
CIRCLE = "img/circle.png"
COMPUTER = 'x'
PLAYER = 'o'
CPU_TIMER = FPS // 2

# Defining colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initializing pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()




# Board sprite
class Board(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((SIZE, SIZE))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.top = TOP
        self.posy = 0
        self.posx = SIZE
        self.step = 50
        self.line_y = 1
        self.line_x = 2
        self.lines = 0
        self.draw_lines = True
        self.created = False


    def update(self):
        global computer_turn
        if self.draw_lines:
            self.draw_board()
        elif not self.created:
            self.create_cell_zones()
        # CPU move
        if computer_turn and cpu_timer % CPU_TIMER == 0:
            ij = board_logic.computer_turn()
            if ij is not None:
                i, j = ij
                print(board_logic)
                cells_array[i][j].fill(COMPUTER)
                computer_turn = False
                if board_logic.check_winner()[0]:
                    _, ij_start, ij_end = board_logic.check_winner()
                    self.triple_line(ij_start, ij_end, win=False)
                    board_logic.reset()
                    #self.reset()
                elif board_logic.endgame():
                    board_logic.reset()
                    self.reset()

    def triple_line(self, ij_start, ij_end, win):
        """
        ij_start, ij_end: start and end i,j indices of line to be drawn.
        win: User win's conditions.
        Will draw a line that passes along the winning triple cases.
        """
        i0, j0 = ij_start
        i1, j1 = ij_end
        y_start = CELL // 2
        x_start = CELL // 2
        pygame.draw.line(self.image, GREEN,
                         (x_start + j0 * CELL, y_start + i0 * CELL),
                         (x_start + j1 * CELL, y_start + j1 * CELL), 3)
        sleep(1)

    def draw_board(self):
        # Vertical line
        if self.posy >= 0:
            # Vertical lines
            pygame.draw.line(self.image, GREEN,
                             (self.line_y * SIZE // 3, self.posy),
                             (self.line_y * SIZE // 3, self.posy + self.step),
                             2)
            self.posy += self.step
            # Horizontal lines
            pygame.draw.line(self.image, GREEN,
                             (self.posx, self.line_x * SIZE // 3),
                             (self.posx - self.step, self.line_x *
                              SIZE // 3),
                             2)
            self.posx -= self.step
            if self.posy > SIZE + 20:
                # Invert to draw second line
                self.posy = SIZE
                self.posx = 0
                self.step *= -1
                self.line_x = 1
                self.line_y = 2
                self.lines += 1
            if self.posy < 0:
                self.draw_lines = False

    def create_cell_zones(self):
        global computer_turn
        self.created = True
        for i in range(3):
            row = []
            for j in range(3):
                # Creating topleft coordinates for each cell
                x = j * CELL + BORDER
                y = i * CELL + BORDER
                pos = (x + self.rect.left, y + self.rect.top)
                ij = (i, j)
                cell = Cell(pos, ij)
                all_sprites.add(cell)
                cells.add(cell)
                row.append(cell)
            cells_array.append(row)
        # Allow computer to play after cells have been created
        computer_turn = True

    def reset(self):
        global cells
        for cell in cells:
            cell.reset()


# Board cell class:
class Cell(pygame.sprite.Sprite):
    def __init__(self, pos, ij):
        """
        pos: position tuple to create cell.
        ij: i, j tuple of cell.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((CELL - BORDER,
                                     CELL - BORDER))
        self.cross = pygame.transform.scale(pygame.image.load(CROSS).convert(),
                                            (CELL - BORDER, CELL - BORDER))
        self.circle = pygame.transform.scale(pygame.image.load(CIRCLE).convert(),
                                             (CELL - BORDER, CELL - BORDER))
        self.image.set_colorkey(BLACK)
        self.token = cycle([self.cross, self.circle])
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.i = 0
        self.ij = ij
        self.make_empty = False

    def update(self):
        pass

    def hits(self, pos):
        return self.rect.collidepoint(pos)

    def fill(self, token):
        global cpu_timer
        if token == COMPUTER:
            self.image = self.cross
        else:
            cpu_timer = 1
            self.image = self.circle

    def is_clicked(self):
        events = pygame.event.get()
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONUP:
                return self.rect.collidepoint(
                    pygame.mouse.get_pos())

    def reset(self):
        self.image = pygame.Surface((CELL - BORDER,
                                     CELL - BORDER))
        self.make_empty = False

    def indices(self):
        return self.ij


computer_turn = False
player_turn = False
all_sprites = pygame.sprite.Group()
cells = pygame.sprite.Group()
cells_array = []
board = Board()
all_sprites.add(board)

# Logic
board_logic = logic.Board()
cpu_timer = 0
print(board_logic)


# Game loop
running = True
while running:
    cpu_timer += 1
    # Process input
    clock.tick(FPS)
    # Process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Player's move
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for cell in cells:
                if cell.hits(pos):
                    cell.fill(PLAYER)
                    ij = cell.indices()
                    board_logic.user_turn(ij)
                    computer_turn = True
                    if board_logic.check_winner()[0]:
                        _, ij_start, ij_end = board_logic.check_winner()
                        board.triple_line(ij_start, ij_end, win=True)
                        board_logic.reset()
                        #board.reset()
                    elif board_logic.endgame():
                        board_logic.reset()
                        board.reset()
    # Update screen
    all_sprites.update()

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # Flip screen after drawing
    pygame.display.flip()

pygame.quit()
