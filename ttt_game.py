import pygame
import graphics
import logic

# Setting up window
HEIGHT = 600
WIDTH = 480
FPS = 30
TITLE = "Tic-tac-toe"

# Defining colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Initializing pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Game settings
TOP = 100
SIZE = 450
CELL = SIZE // 3
CPU_SPEED = FPS // 2


class TicTacToe():
    """Main tic-tac-toe game object.

    Attributes
    ----------
    board : graphics.Board
        pygame.Sprite object. Consists mainly of the lines that make
        up the grid.
    board_logic : logic.Board
        Object that defines the game logic and AI.
    cells : 3 x 3 nested list.
        List containing individual graphics.Cell objects.
        Each `Cell` object is a cell sprite.
    player_score : graphics.Text
        Sprite object that shows the player score.
    cpu_score : graphics.Text
        Sprite object that shows the cpu score.
    end_message : graphics.Text
        Sprite object that shows a message when the game ends:
        win/lose/tie.
    player_play : bool
        Determine when it's the player's turn to play.
    check : bool
        Determine when the check the end of the game.
        Set to `True` after each player or cpu move.
    reset : bool
        Determines when to reset the board after the end of game.
    timer : int
        Counter to limit cpu moves speed.
    timer2 : int
        Counter to limit end game reactions speed.

    Methods
    -------
    add_to_group(sprites_group)
        Add all of the sprite objects of the `TicTacToe` object
        to `sprites_group`.
    create_cells(CELL)
        Create 9 `graphics.Cell` objects of size `SIZE` x `SIZE`
        and append them to `self.cells`.
    update()
        Check if the game has ended or a player has won. Calls
        methods accordingly. Verify when to check with `self.check`
        and limit frequency using `self.timer2`.
        Verifies it's the computer's turn to play by checking
        `self.player_turn`. Calls `computer_turn` method when
        corresponds. Limits computer's play speed using
        `self.timer`.
    computer_turn()
        Use `graphics.board_logic.computer_turn()` method to determine
        next case to fill.
        Fill cell accordingly and update to check board end game
        conditions and player's turn.
    reset_game()
        Reset `graphics.Board` to delete extra lines on the board.
        Reset all `graphics.Cell` sprites to a blank surface.
        Reset `self.end_message` to show an empty string.
    update_score()
        Add one point to the corresponding current player score.
        Either `self.cpu_score` or `self.player_score`.
    win_message()
        Modify `self.end_message` to show a win or lose message.
    tie_message()
        Modify `self.end_message` to show a tied game message.
    get_cells():
        Return `self.cells` containing all the `graphics.Cell`
        sprite objects.
    is_player_turn():
        Return `True` when player's turn conditions are met.
        `False` otherwise.
    to_reset():
        Return `self.reset` attribute. Use to determine when
        to reset the game board.

    """

    def __init__(self):
        self.board = graphics.Board()
        self.board_logic = logic.Board()
        self.cells = self.create_cells(CELL)
        self.player_score = graphics.Text('P1 : 0',
                                          (WIDTH * 4 // 5, TOP * 1 // 3))
        self.cpu_score = graphics.Text('CPU : 0',
                                       (WIDTH * 4 // 5, TOP * 2 // 3))
        self.end_message = graphics.Text('',
                                         (WIDTH * 2 // 5, TOP // 2))
        self.player_play = False
        self.check = False
        self.reset = False
        self.timer = 0
        self.timer2 = 0

    def add_to_group(self, sprites_group):
        sprites_group.add(self.player_score)
        sprites_group.add(self.cpu_score)
        sprites_group.add(self.end_message)
        for cell in self.cells:
            sprites_group.add(cell)
        sprites_group.add(self.board)

    def create_cells(self, CELL=CELL):
        cells = []
        for i in range(3):
            row = []
            for j in range(3):
                pos = (self.board.rect.left + j * CELL,
                       self.board.rect.top + i * CELL)
                row.append(graphics.Cell(pos))
            cells.append(row)
        return cells

    def update(self):
        if self.check:
            if self.timer2 > CPU_SPEED // 2:
                self.timer2 = 0
                self.check = False
                if self.board_logic.check_winner():
                    self.board.draw_triple(self.board_logic.win_line_pos())
                    self.win_message()
                    self.update_score()
                    self.reset = True
                elif self.board_logic.endgame():
                    self.tie_message()
                    self.reset = True
            else:
                self.timer2 += 1

        if self.timer < CPU_SPEED:
            self.timer += 1
        else:
            self.timer = 0
            if not self.is_player_turn() and not self.to_reset():
                self.computer_turn()

    def computer_turn(self):
        i, j = self.board_logic.computer_turn()
        # print(self.board_logic)
        self.cells[i][j].computer_fill()
        self.check = True
        self.player_play = True

    def player_turn(self, ij):
        self.timer = 0
        self.board_logic.user_turn(ij)
        i, j = ij
        self.cells[i][j].player_fill()
        self.player_play = False
        self.check = True

    def reset_game(self):
        self.board.new_board()
        self.board_logic.reset()
        self.end_message.write('')
        for i in range(3):
            for j in range(3):
                self.cells[i][j].reset()
        self.reset = False

    def update_score(self):
        if self.board_logic.current_player() == 'o':
            self.player_score.add1()
        else:
            self.cpu_score.add1()

    def win_message(self):
        if self.board_logic.current_player() == 'o':
            self.end_message.write('You win!')
        else:
            self.end_message.write('You lose!')

    def tie_message(self):
        self.end_message.write('     Tie!')

    def get_cells(self):
        return self.cells

    def is_player_turn(self):
        return self.player_play and not self.board_logic.check_winner()

    def to_reset(self):
        return self.reset


all_sprites = pygame.sprite.Group()
game = TicTacToe()
game.add_to_group(all_sprites)

# Game loop
running = True
while running:
    clock.tick(FPS)

    # Process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if game.to_reset():
                game.reset_game()
            elif game.is_player_turn():
                pos = pygame.mouse.get_pos()
                cells = game.get_cells()
                for i in range(3):
                    for j in range(3):
                        if cells[i][j].hits(pos):
                            game.player_turn((i, j))

    game.update()

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
