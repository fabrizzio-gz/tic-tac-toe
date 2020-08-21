from importlib import reload
import pygame
import graphics
import logic

reload(graphics)

# TODO:
# - Check winning conditions and draw strike line.

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
CPU_SPEED = FPS // 3


class TicTacToe():
    def __init__(self):
        self.board = graphics.Board(SIZE, TOP, WIDTH)
        self.board_logic = logic.Board()
        self.cells = self.create_cells(CELL)
        self.player_score = graphics.Text('P1 : 0',
                                          (WIDTH * 4 // 5, TOP * 1 // 3))
        self.cpu_score = graphics.Text('CPU : 0',
                                       (WIDTH * 4 // 5, TOP * 2 // 3))
        self.player_play = False
        self.timer = 1

    def add_to_group(self, sprites_group):
        sprites_group.add(self.player_score)
        sprites_group.add(self.cpu_score)
        sprites_group.add(self.board)
        for cell in self.cells:
            sprites_group.add(cell)

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
        if not self.is_player_turn():
            self.timer += 1
            if self.timer % CPU_SPEED == 0:
                self.timer = 1
                self.computer_turn()

    def computer_turn(self):
        i, j = self.board_logic.computer_turn()
        print(self.board_logic)
        self.cells[i][j].computer_fill()
        self.player_play = True
        # computer_turn = False
        # if board_logic.check_winner()[0]:
        #     # CPU win
        #     _, ij_start, ij_end = board_logic.check_winner()
        #     self.set_draw_triple_line((True, ij_start, ij_end, False))
        #     board_logic.reset()
        #     cpu_score.add1()
        #     self.freeze_cells(True)
        #     end_message.write('You lose!')
        #     elif board_logic.endgame():
        #         board_logic.reset()
        #         end_message.write('     Tie!')
        #         self.reset_on_click()
        #         self.freeze_cells(True)
        

    def player_turn(self, ij):
        self.board_logic.user_turn(ij)
        i, j = ij
        self.cells[i][j].player_fill()
        self.player_play = False

    def get_cells(self):
        return self.cells

    def is_player_turn(self):
        return self.player_play


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
        if event.type == pygame.MOUSEBUTTONUP and game.is_player_turn():
            pos = pygame.mouse.get_pos()
            cells = game.get_cells()
            for i in range(3):
                for j in range(3):
                    if cells[i][j].hits(pos):
                        game.player_turn((i, j))
                    # ij = cell.indices()
                    # board_logic.user_turn(ij)
                    # computer_turn = True
                    # if board_logic.check_winner()[0]:
                    #     # Player won
                    #     board.freeze_cells(True)
                    #     _, ij_start, ij_end = board_logic.check_winner()
                    #     board.set_draw_triple_line((True, ij_start,
                    #                                 ij_end, True))
                    #     p1_score.add1()
                    #     board_logic.reset()
                    #     end_message.write('You win!')
                    # elif board_logic.endgame():
                    #     # Tie
                    #     end_message.write('     Tie!')
                    #     board.freeze_cells(True)
                    #     board_logic.reset()
                    #     board.reset_on_click()

    # Update game
    game.update()
    # Update screen
    all_sprites.update()
    
    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # Flip screen after drawing
    pygame.display.flip()

pygame.quit()
