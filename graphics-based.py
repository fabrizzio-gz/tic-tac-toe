from itertools import cycle
import pygame
import logic

# TODO:
# - Clean code.

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
CPU_TIMER = FPS // 5

# Defining colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


# Initializing pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# Ordered sprite group to sort by z attribute
class OrderedGroup(pygame.sprite.Group):
    def by_z(self, spr):
        return spr.z

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sorted(sprites, key=self.by_z):
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []


class Text(pygame.sprite.Sprite):
    """Displays text

    Methods
    -------
    write(text)
        Change the object text to display to `text`
    add1()
        Add the text's last digit (score) by one.
    """

    def __init__(self, font, pos=(0, 0), text=''):
        """
        Parameters
        ----------
        font : pygame.font
            Pygame font to use for text.
        pos : tuple, optional
            tuple of x, y coordinates of the topleft position of the text
            (default is 0, 0).
        text : str, optional
            Object's text (default is the empty string).
        """
        
        pygame.sprite.Sprite.__init__(self)
        #self.font = pygame.font.SysFont('freesansbold.ttf', 32)
        self.font = font
        self.image = self.font.render(text, True, GREEN, BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.text = text
        self.z = 0

    def write(self, text):
        self.text = text
        self.image = self.font.render(text, True, GREEN, BLACK)

    def add1(self):
        score = int(self.text.split()[1]) + 1
        self.text = ': ' + str(score)
        self.write(self.text)


# Board sprite
class Board(pygame.sprite.Sprite):
    """Tic-tac-toe board. 9x9 grid made of lines.

    Attributes
    ----------
    image : pygame.Surface
        A black square pygame.Surface of a specified size.
    rect : pygame.Rect
        Specifies `image` coordinates.
        rect.centerx at `WIDTH // 2`.
        rect.top at `TOP`.
    step : int
        Sets how fast will board be first drawn.
    
    
    """

    def __init__(self, SIZE=450, TOP=100, WIDTH=480):
        """
        Attributes
        ----------
        SIZE : int
            Board is a square of size `SIZE` x `SIZE`
            (default is 450)
        TOP : int
            Board top y coordinate (default is 100).
        WIDTH : int
            Game screen width.
            Board is centered at `WIDHT // 2`
        """
        
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
        self.z = 1
        # Tuple that determinates drawing triple line.
        # ij_start, ij_end are ij indices to draw line
        # Last condition says if player win is True or False
        self.draw_triple_line = (False, (0, 0), (0, 0), False)
        self.reset_cond = False
        self.board_free = True

    def update(self):
        global computer_turn
        # global all_sprites
        global cpu_score
        global end_message
        if self.draw_lines:
            self.draw_board()
        elif not self.created:
            self.create_cell_zones()

        # CPU move
        if computer_turn and cpu_timer % CPU_TIMER == 0 and \
           self.board_free:
            ij = board_logic.computer_turn()
            if ij is not None:
                i, j = ij
                print(board_logic)
                cells_array[i][j].fill(COMPUTER)
                computer_turn = False
                if board_logic.check_winner()[0]:
                    # CPU win
                    _, ij_start, ij_end = board_logic.check_winner()
                    self.set_draw_triple_line((True, ij_start, ij_end, False))
                    board_logic.reset()
                    cpu_score.add1()
                    self.freeze_cells(True)
                    end_message.write('You lose!')
                elif board_logic.endgame():
                    board_logic.reset()
                    end_message.write('     Tie!')
                    self.reset_on_click()
                    self.freeze_cells(True)
        # Drawing strike line
        elif self.draw_triple_line[0] and cpu_timer % CPU_TIMER == 0:
            _, ij_start, ij_end, is_win = self.draw_triple_line
            self.triple_line(ij_start, ij_end, is_win)
            self.reset_on_click()
            self.set_draw_triple_line((False, (0, 0), (0, 0), False))

    def set_draw_triple_line(self, tup):
        self.draw_triple_line = tup

    def triple_line(self, ij_start, ij_end, win):
        """
        ij_start, ij_end: start and end i,j indices of line to be drawn.
        win: User win's conditions.
        Will draw a line that passes along the winning triple cases.
        """
        i0, j0 = ij_start
        i1, j1 = ij_end
        # To draw larger line
        x0, y0, x1, y1 = [CELL // 4] * 4
        # Decide size depending on orientation
        # Horizontal
        if i0 == i1:
            y0, y1 = 0, 0
        # Vertical
        elif j0 == j1:
            x0, x1 = 0, 0
        # 2nd diag:
        elif i0 != j0:
            x0 *= -1
            x1 *= -1
        y_start = CELL // 2
        x_start = CELL // 2
        pygame.draw.line(self.image, GREEN,
                         (x_start + j0 * CELL - x0, y_start + i0 * CELL - y0),
                         (x_start + j1 * CELL + x1, y_start + i1 * CELL + y1), 4)

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

    def new_board(self):
        # Getting a black board
        self.image = pygame.Surface((SIZE, SIZE))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.top = TOP
        # Drawing lines
        for line in range(1, 3):
            # Vertical lines
            pygame.draw.line(self.image, GREEN,
                             (line * SIZE // 3, 0),
                             (line * SIZE // 3, self.rect.bottom),
                             2)
            # Horizontal lines
            pygame.draw.line(self.image, GREEN,
                             (self.rect.left, line * SIZE // 3),
                             (self.rect.right, line * SIZE // 3),
                             2)

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

    def reset_on_click(self):
        self.reset_cond = True

    def to_reset(self):
        return self.reset_cond

    def reset(self):
        self.reset_cond = False
        self.new_board()
        global cells
        for cell in cells:
            cell.reset()

    def freeze_cells(self, freeze_cond):
        global cells
        self.board_free = not freeze_cond
        for cell in cells:
            cell.freeze(freeze_cond)

    def show_text(self):
        return self.created


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
        self.z = 0
        self.free = True

    def update(self):
        pass

    def hits(self, pos):
        return self.rect.collidepoint(pos)

    def freeze(self, freeze_cond):
        self.free = not freeze_cond

    def is_free(self):
        return self.free

    def fill(self, token):
        self.free = False
        global cpu_timer
        if token == COMPUTER:
            self.image = self.cross
        else:
            # Reset timer for computer turn
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
        self.free = True

    def indices(self):
        return self.ij

create_text = True
computer_turn = False
player_turn = False
# all_sprites = pygame.sprite.Group()
all_sprites = OrderedGroup()
cells = pygame.sprite.Group()
cells_array = []
board = Board()
all_sprites.add(board)

# Logic
board_logic = logic.Board()
cpu_timer = 0

# Text
font = pygame.font.SysFont('freesansbold.ttf', 32)
add_text = True
posx, posy = WIDTH * 4 // 5, TOP * 1 // 3
posy2 = TOP * 2 // 3
space = 60
p1 = Text(font, (posx, posy), 'P1')
cpu = Text(font, (posx, posy2), 'CPU')
p1_score = Text(font, (posx + space, posy), ': 0')
cpu_score = Text(font, (posx + space, posy2), ': 0')
end_message = Text(font, (WIDTH * 2 // 5, TOP // 2))
all_sprites.add(end_message)

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
        if event.type == pygame.MOUSEBUTTONUP: # Add not computer_turn here
            # Reset game board
            if board.to_reset():
                end_message.write('')
                board.reset()
                board.freeze_cells(False)
            elif not computer_turn:
                pos = pygame.mouse.get_pos()
                for cell in cells:
                    if cell.hits(pos) and cell.is_free():
                        cell.fill(PLAYER)
                        ij = cell.indices()
                        board_logic.user_turn(ij)
                        computer_turn = True
                        if board_logic.check_winner()[0]:
                            # Player won
                            board.freeze_cells(True)
                            _, ij_start, ij_end = board_logic.check_winner()
                            board.set_draw_triple_line((True, ij_start,
                                                        ij_end, True))
                            p1_score.add1()
                            board_logic.reset()
                            end_message.write('You win!')
                        elif board_logic.endgame():
                            # Tie
                            end_message.write('     Tie!')
                            board.freeze_cells(True)
                            board_logic.reset()
                            board.reset_on_click()
    # Add text after board creation
    if add_text and board.show_text():
        add_text = False
        all_sprites.add(p1)
        all_sprites.add(cpu)
        all_sprites.add(p1_score)
        all_sprites.add(cpu_score)

    # Update screen
    all_sprites.update()

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # Flip screen after drawing
    pygame.display.flip()

pygame.quit()
