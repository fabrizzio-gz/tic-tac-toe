from os import path
import pygame

try:
    img_dir = path.join(path.dirname(__file__), 'img')
except NameError:
    img_dir = 'img'

# Defining colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Game settings
WIDTH = 480
TOP = 100
SIZE = 450
CELL = SIZE // 3
BORDER = 5


class Text(pygame.sprite.Sprite):
    """pygame.Sprite object to display game's text.

    Attributes
    ----------
    pos : (int, int)
        Set the (x, y) coordinates of the topleft corner
        of the Sprite object.
    text : str
        String to show on the game.
        Default value is empty string.
    font : pygame.font
        font used for text.
        Default: `freesansbold.ttf`, size 32.

    Methods
    -------
    write(text)
        Change the text to display to `text`
    add1()
        Add one to the text's score.
        Use last part of the `text` string as an int value.
    show()
        Make sprite object render current `self.text` string.
    hide()
        Make sprite object render an empty string.
    """

    def __init__(self,text='', pos=(0,0), font=None):
        pygame.sprite.Sprite.__init__(self)
        if not font:
            font = pygame.font.SysFont('freesansbold.ttf', 32)
        self.font = font
        self.image = self.font.render(text, True, GREEN, BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.text = text

    def write(self, text):
        self.text = text
        self.image = self.font.render(text, True, GREEN, BLACK)

    def add1(self):
        score = int(self.text.split()[-1]) + 1
        player = self.text.split()[0]
        self.text = player + ' : ' + str(score)
        self.write(self.text)

    def show(self):
        self.image = self.font.render(self.text, True, GREEN, BLACK)

    def hide(self):
        self.image = self.font.render('', True, GREEN, BLACK)


class Board(pygame.sprite.Sprite):
    """Tic-tac-toe board. 3x3 grid made of lines.

    Methods
    -------
    new_board()
        Generate a blank `pygame.Surface` of size `SIZE` x `SIZE`.
        Set top border at y=`TOP`.
        Set center at x=`WIDHT` // 2.
        Draw 2 vertical and 2 horizontal lines to create
        a 3x3 grid.
    draw_triple(ij0_ij1)
        `ij0_ij1` : tuple of two (int, int) tuples.
            Each tuple contains (i, j) indices for cell's 
            row and column.
        Draw a line where a player has won, following
        `ij0_ij1` indicative cells.

    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.new_board()

    def new_board(self):
        self.image = pygame.Surface((SIZE, SIZE))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.top = TOP

        # Drawing lines
        cell_size = self.rect.width // 3
        for line in range(1, 3):
            # Vertical lines
            pygame.draw.line(self.image, GREEN,
                             (line * cell_size, 0),
                             (line * cell_size, self.rect.bottom), 2)
            # Horizontal lines
            pygame.draw.line(self.image, GREEN,
                             (self.rect.left, line * cell_size),
                             (self.rect.right, line * cell_size), 2)

    def draw_triple(self, ij0_ij1):
        ij0, ij1 = ij0_ij1
        i0, j0 = ij0
        i1, j1 = ij1
        # Helper ints to extend the line's length
        x0, y0, x1, y1 = [CELL // 4] * 4
        # Extend size depending on line's orientation
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
        # Start line at cell's center
        y_start = CELL // 2
        x_start = CELL // 2
        pygame.draw.line(self.image, GREEN,
                         (x_start + j0 * CELL - x0, y_start + i0 * CELL - y0),
                         (x_start + j1 * CELL + x1, y_start + i1 * CELL + y1), 4)


class Cell(pygame.sprite.Sprite):
    """Sprite to show either 'x' or 'o' at each cell.

    Attributes
    ----------
    cross : pygame.Surface
        To draw a cross using image at `img/cross.png` path.
    circle : pygame.Surface
        To draw a circle using image at `img/circle.png` path.
    free : bool
        Bool to decide when a cell can update sprite to be drawn.
        Default is `True`.

    Methods
    -------
    hits(pos: (int, int)) -> bool
        When `self.free` is true detect collision between
        `pos` coordinates and this object.
        Return `True` for collision. `False` if not.
    fill(token: pygame.Surface)
        Change sprite's image to `token`.
        `token` will always be either `self.cross` or
        `self.circle`.
        Set `self.free` to `False`
    computer_fill():
        Use `self.fill` method to draw a cross.
    player_fill():
        Use `self.fill` method to draw a circle
    reset():
        Generate a blank square pygame.Surface of size
        CELL - BORDER.
        Set `self.free` to `True`.

    """

    def __init__(self, pos):
        """
        pos : (int, int)
            Coordinates for topleft corner.

        """

        pygame.sprite.Sprite.__init__(self)
        dim = (CELL - BORDER, CELL - BORDER)
        cross_path = path.join(img_dir, 'cross.png')
        circle_path = path.join(img_dir, 'circle.png')
        self.image = pygame.Surface(dim)
        self.cross = pygame.image.load(cross_path).convert()
        self.cross = pygame.transform.scale(self.cross, dim)
        self.circle = pygame.image.load(circle_path).convert()
        self.circle = pygame.transform.scale(self.circle, dim)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] + BORDER, pos[1] + BORDER)
        self.free = True

    def hits(self, pos):
        if self.free:
            return self.rect.collidepoint(pos)
        return False

    def fill(self, token):
        self.image = token
        self.free = False

    def computer_fill(self):
        self.fill(self.cross)

    def player_fill(self):
        self.fill(self.circle)

    def reset(self):
        dim = (CELL - BORDER, CELL - BORDER)
        self.image = pygame.Surface(dim)
        self.free = True
