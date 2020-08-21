from importlib import reload
import pygame
import graphics
import logic

reload(graphics)

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


class TicTacToe():
    def __init__(self):
        self.board = graphics.Board(SIZE, TOP, WIDTH)
        #self.board_logic = logic.Board()
        self.cells = self.create_cells(CELL)
        self.player_score = graphics.Text('P1 : 0',
                                          (WIDTH * 4 // 5, TOP * 1 // 3))
        self.cpu_score = graphics.Text('CPU : 0',
                                       (WIDTH * 4 // 5, TOP * 2 // 3))

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
                pos = (self.board.rect.left + i * CELL,
                       self.board.rect.top + j * CELL)
                row.append(graphics.Cell(pos))
            cells.append(row)
        return cells

    def get_cells(self):
        return self.cells


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
            pos = pygame.mouse.get_pos()
            cells = game.get_cells()
            for i in range(3):
                for j in range(3):
                    if cells[i][j].hits(pos):
                        cells[i][j].fill()
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

    # Update screen
    all_sprites.update()
    
    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # Flip screen after drawing
    pygame.display.flip()

pygame.quit()
