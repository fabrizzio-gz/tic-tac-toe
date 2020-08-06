# tic-tac-toe
import numpy as np
from itertools import cycle


class NoMove(Exception):
    pass

class Board:

    players = cycle('xo')
    
    
    def __init__(self):
        self.board = np.array([['','',''], ['','',''], ['','','']])
        self.rows = [self.board[0], self.board[1], self.board[2]]
        self.columns = [self.board[:,0], self.board[:,1], self.board[:,2]]
        self.player = next(Board.players)
        self.user_score = 0
        self.computer_score = 0
        self.turns = 0
        
        

    def set_case(self, i, j, player = None):
        """
        i, j: The i and j indexes of the case. Starting from top left
              corner.
        symbol: Either 'x' or 'o'
        """
        self.turns += 1
        if not player:
            player = self.player
        
        # Error checking
        assert i <= 2, "Invalid i case"
        assert j <= 2, "Invalid j case"
        assert player in ('x', 'o'), "Usage: symbol 'x' or 'o'"
        assert not self.board[i][j], "Case already set"
        
        self.board[i][j] = player
        print(self)
        #return 0


    def check_winner(self, player = None):
        if not player:
            player = self.player
        board = self.board

        # Horizontal win
        for i in range(3):
            for j in range(3):
                if not self.rows[i][j] == player:
                    break
            else:
                print('Horizontal check')
                return True
            
        # Vertical win
        for j in range(3):
            for i in range(3):
                if not self.columns[j][i] == player:
                    break
            else:
                print('Vertical check')
                return True

        # Diagonal win
        if (board[0][0], board[1][1], board[2][2]) == (player, player, player) or \
           (board[2][0], board[1][1], board[0][2]) == (player, player, player):
            print('Diagonal Check')
            return True

        #print('No winner')
        return False

    def fill_next(self):
        for i in range(3):
            for j in range(3):
                if not self.board[i][j]:
                    self.board[i][j] = self.player
                    return None
                    

    def fill_corner(self):
        board = self.board
        if not board[0][0]:
            board[0][0] = self.player
        elif not board[0][2]:
            board[0][2] = self.player
        elif not board[2][0]:
            board[2][0] = self.player
        elif not board[2][2]:
            board[2][2] = self.player
        else:
            raise NoMove
        
    def diagonal_free(self):
        board = self.board
        if not board[1][1]:
            if board[0][0] == self.player and not board[2][2]:
                board[2][2] = self.player
            elif board[0][2] == self.player and not board[2][0]:
                board[2][0] = self.player
            else:
                raise NoMove
        else:
            raise NoMove


    def get_diagonals(self):
        return self.board.diagonal().copy(), np.diagonal(np.fliplr(self.board)).copy()
    
    
    def complete_triple(self, target = None):
        """
        Will scan rows, columns and diagonals for 2 occurrences of
        'target'. If 2 cases are filled with 'target', it will
        fill the remaining case with self.player symbol.
        If no 'target' is specified, it will use current player.symbol one.
        If no occurrences take place, raises NoMove exception.
        """
        print('Completing triples')
        if not target:
            target = self.player
            
        board = self.board

        # Rows
        for i in range(3):
            if np.sum(self.rows[i] == target) == 2:
                self.rows[i][self.rows[i] == ''] = self.player
                return None

        # Columns
        for j in range(3):
            if np.sum(self.columns[j] == target) == 2:
                self.columns[j][self.rows[j] == ''] = self.player
                return None

        # Diagonals
        diagonal0, diagonal1 = self.get_diagonals()
        if np.sum(diagonal0 == target) == 2:
            diagonal0[diagonal0 == ''] = self.player
            self.board[np.diag_indices_from(self.board)] = diagonal0
            return None
        if np.sum(diagonal1 == target) == 2:
            diagonal1[diagonal1 == ''] = self.player
            # Inverted diagonal indices
            dinv = (np.array([0, 1, 2]), np.array([2, 1, 0]))
            self.board[dinv] = diagonal1
            return None

        raise NoMove
    
    def win_move(self):
        """
        Searches for rows, columns and diagonals with 2 occurrences of 
        self.symbol and completes it to win.
        If no occurrences take place, raises NoMove exception.
        """
        print('Trying to win...', end='')
        self.complete_triple()
        print('Could not')
    

    def avoid_losing(self):
        """
        Searches for rows, columns and diagonals with 2 occurrences of 
        the opposed of self.symbol. Completes it to avoid losing.
        If no occurrences take place, raises NoMove exception.
        """
        if self.player == 'x':
            target = 'o'
        else:
            target = 'x'
        print('Avoiding loosing...', end='')
        self.complete_triple(target)
        print('No need')

        
    def computer_turn(self):
        self.turns += 1
        input('Computer turn... (Press any key to continue)')
        if self.turns <= 2:
            try:
                self.fill_corner()
                return None
            except NoMove:
                pass

        try:
            self.win_move()
            return None
        except NoMove:
            pass

        try:
            self.avoid_losing()
            return None
        except NoMove:
            pass

        if self.turns <= 4:
            try:
                self.diagonal_free()
                return None
            except NoMove:
                pass

            try:
                self.fill_corner()
                return None
            except NoMove:
                pass      
        
        # If no other possible options
        self.fill_next()
        return None
       

    def get_index(self, text):
        index = 0
        while True:
            index = input("Choose a {}\n".format(text))
            try:
                index = int(index)
            except ValueError:
                print('Please enter a number')
                continue
            if index > 2:
                print('Invalid input. Possible values: 0 - 2')
            else:
                break
        return index


    def try_case(self, i, j):
        if not self.board[i][j]:
            self.board[i][j] = self.player
            return True
        else:
            return False
    
    def user_turn(self):
        self.turns += 1
        print('Your turn')
        while True:
            i = self.get_index('row')
            j = self.get_index('column')
            if self.try_case(i, j):
                break
            else:
                print('Case is filled. Choose another one!')
        return None

    
    def play(self):
        current_player = self.player
        print('Welcome!')
        self.print_score()
        input('New game?\n(Press any key to continue)')
        print(board)
        while True:
            current_player = self.player
            if current_player == 'x':
                self.computer_turn()
                print(self)
            else:
                self.user_turn()
                print(self)
            if self.check_winner():
                if current_player == 'x':
                    self.computer_win()
                else:
                    self.player_win()
                self.print_score()
                self.reset()
                print('New game')
                print(self)
                # Loser starts next game
                self.player = next(Board.players)
            elif self.endgame():
                self.print_score()
                self.print("It's a draw!")
                self.reset()
                self.print('New game')
                self.print(self)
                self.player = next(Board.players)
            else:
                self.player = next(Board.players)

                
    def endgame(self):
        return self.turns == 9


    def reset(self):
        self.board.fill('')
        self.turns = 0

        
    def computer_win(self):
        print('Computer won!')
        input('Press enter to continue...')
        self.computer_score += 1

        
    def player_win(self):
        print('You win!')
        input('Press enter to continue...')
        self.user_score += 1

        
    def print_score(self):
        print('Current score is:\n Player\t: {}\n CPU\t: {}'.format(self.user_score,
               self.computer_score))
    
    def __str__(self):
        dash = '---'
        counter = 0
        board_str = ''
        for row in self.board:
            board_str += '{: ^5s}|{: ^5s}|{: ^5s}\n'.format(row[0], row[1], row[2])
            if counter < 2:
                counter += 1
                board_str += '{: ^5s}+{: ^5s}+{: ^5s}\n'.format(dash, dash, dash)
        return board_str

board = Board()
def f():
    raise NoMove

def call_f():
    return f()

call_f()
#board.play()
# for i in range(3):
#     for j in range(3):
#         board.set_case(i, j, 'x') #if (i + j) % 2 == 0 else 'o')
#         board.check_winner()
#         #board.reset()
#         if board.endgame():
#             print('The end!')
#         else:
#             print('Still going')
