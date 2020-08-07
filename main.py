# tic-tac-toe
import numpy as np
from itertools import cycle
from random import shuffle

class NoMove(Exception):
    pass

class Board:

    players = cycle('xo')

    def __init__(self):
        self.board = np.array([['', '', ''], ['', '', ''], ['', '', '']])
        self.rows = [self.board[0], self.board[1], self.board[2]]
        self.columns = [self.board[:, 0], self.board[:, 1], self.board[:, 2]]
        # Top to bottom, left to right diagonal
        self.diag0 = np.einsum('ii->i', self.board)
        # To to bottom, right to left diagonal
        self.diag1 = np.einsum('ii->i', np.fliplr(self.board))
        self.diags = [self.diag0, self.diag1]
        self.player = next(Board.players)
        self.user_score = 0
        self.computer_score = 0
        self.turns = 0

    def set_case(self, i, j, player=None):
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

    def check_winner(self, player=None):
        """
        player: The token to check
        Checks if a rouw, column or diagonal is filled with 'player' token.
        If no 'player' token is given, uses curren self.player one.
        Returns True if condition valid. False otherwise.
        """
        if not player:
            player = self.player

        # Horizontal win
        for i in range(3):
            if np.sum(self.rows[i] == player) == 3:
                print('Horizontal check')
                return True

            # for j in range(3):
            #     if not self.rows[i][j] == player:
            #         break
            # else:
            #     print('Horizontal check')
            #     return True

        # Vertical win
        for j in range(3):
            if np.sum(self.columns[j] == player) == 3:
                print('Vertical check')
                return True
            # for i in range(3):
            #     if not self.columns[j][i] == player:
            #         break
            # else:
            #     print('Vertical check')
            #     return True

        # Diagonal win
        for d in range(2):
            if np.sum(self.diags[d] == player) == 3:
                print('Diagonal check')
                return True
        # if (board[0][0], board[1][1], board[2][2]) == (player, player, player) or \
        #    (board[2][0], board[1][1], board[0][2]) == (player, player, player):
        #     print('Diagonal Check')
        #     return True

        return False

    def fill_next(self):
        for i in range(3):
            for j in range(3):
                if not self.board[i][j]:
                    self.board[i][j] = self.player
                    return None

    def fill_corner(self):
        """
        Chooses one corner randomly, if it's empty, fills it 
        with self.player token.
        Raises NoMove exception if not possible for all corner. 
        """
        board = self.board
        random_corners = list(range(4))
        shuffle(random_corners)
        for i in random_corners:
            if i == 0 and not board[0][0]:
                board[0][0] = self.player
                break
            elif i == 1 and not board[0][2]:
                board[0][2] = self.player
                break
            elif i == 2 and not board[2][0]:
                board[2][0] = self.player
                break
            elif i == 3 and not board[2][2]:
                board[2][2] = self.player
                break
        else:
            raise NoMove
        
    def diagonal_free(self):
        """
        Check if center case is free.
        Then checks the top left and right corners and tries
        to fill it's opposed diagonal.
        """
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
        if not target:
            target = self.player
            
        board = self.board

        def try_fill(array3, i):
            if np.sum(array3[i] == target) == 2 and \
               np.sum(array3[i] == '') == 1:
                array3[i][array3[i] == ''] = self.player
                return True
        
        # Rows
        for i in range(3):
            if try_fill(self.rows, i):
                return None
            # if np.sum(self.rows[i] == target) == 2 and \
            #    np.sum(self.rows[i] == '') == 1:
            #     self.rows[i][self.rows[i] == ''] = self.player
            #     return None

        # Columns
        for j in range(3):
            if try_fill(self.columns, j):
                return None
            # if np.sum(self.columns[j] == target) == 2 and \
            #    np.sum(self.columns[j] == '') == 1:
            #     self.columns[j][self.columns[j] == ''] = self.player
            #     return None

        # Diagonals
        for diagonal in self.diags:
            if np.sum(diagonal == target) == 2 and \
               np.sum(diagonal == '') == 1:
                diagonal[diagonal == ''] = self.player
                return None
            
        # diagonal0, diagonal1 = self.get_diagonals()
        # if np.sum(diagonal0 == target) == 2 and \
        #    np.sum(diagonal0 == '') == 1:
        #     diagonal0[diagonal0 == ''] = self.player
        #     self.board[np.diag_indices_from(self.board)] = diagonal0
        #     return None
        # if np.sum(diagonal1 == target) == 2 and \
        #    np.sum(diagonal0 == '') == 1:
        #     diagonal1[diagonal1 == ''] = self.player
        #     # Inverted diagonal indices
        #     dinv = (np.array([0, 1, 2]), np.array([2, 1, 0]))
        #     self.board[dinv] = diagonal1
        #     return None
        
        raise NoMove
    
    def win_move(self):
        """
        Searches for rows, columns and diagonals with 2 occurrences of 
        self.symbol and completes it to win.
        If no occurrences take place, raises NoMove exception.
        """
        print('Trying to win...')
        self.complete_triple()
        print('Won')
    

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
        print('Avoiding losing...')
        self.complete_triple(target)
        print('Achieved')


    def count_corners(self, target = None):
        """
        Returns the number of corners occupied by the current
        self.player token. (0 - 4)
        """
        if not target:
            target = self.player
            
        return np.sum(self.board[[0,0,-1,-1],[0,-1,0,-1]] == target)

    
    def defend_corner(self):
        """
        Checks if the other player has filled one of the corners.
        Fills the center case if True and returns True.
        Else returns False.
        """
        if self.player == 'x':
            other_player = 'o'
        else:
            other_player = 'x'

        return self.count_corners(other_player) >= 1


    def scan_one(self, array3):
        """
        array3: An array with 3 elements.
        Scans if token self.token occupies one and only one token
        in array3. All other cases must be empty.
        Returns True if valid. If not, False.
        """
        return np.sum(array3 == self.player) == 1 and \
               np.sum(array3 == '') == 2


    def fill_one(self, array3):
        """
        array3: An array of 3 elements.
        Fills the first empty case in array3 with self.player token.
        Raise NoMove exception if not possible
        """
        for i in range(3):
            if not array3[i]:
                array3[i] = self.player
                return None
        raise NoMove
    
    def complete_second(self):
        """
        Will scan rows, columns and diagonals (in that order)
        with only one current player case filled and no cases filled
        by the other player. It will then fill one of those cases.
        Returns NoMove exception if no occurrence is possible.
        """
        for i in range(3):
            if self.scan_one(self.rows[i]):
                self.fill_one(self.rows[i])
                return None

        for j in range(3):
            if self.scan_one(self.columns[j]):
                self.fill_one(self.columns[j])
                return None

        for diagonal in self.diags:
            if self.scan_one(diagonal):
                self.fill_one(diagonal)
                return None
                
        raise NoMove
        
        
    def computer_turn(self):
        if self.player == 'x':
            other_player = 'o'
        else:
            other_player = 'x'
        
        self.turns += 1
        input('Computer turn... (Press any key to continue)')
        if self.turns <= 2:
            if self.turns == 2:
                if self.defend_corner():
                    self.board[1][1] = self.player
                    return None
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

        try:
            self.diagonal_free()
            return None
        except NoMove:
            pass

        if (self.turns <= 4 and self.count_corners(other_player) != 2) or \
           self.count_corners() >= 2:
            ### STILL need to check for unimportant cases
            try:
                self.fill_corner()
                return None
            except NoMove:
                pass

        try:
            self.complete_second()
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
        print(self)
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
                print("It's a draw!")
                input('Press any key to continue...')
                self.reset()
                print('New game')
                print(self)
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
board.play()
a = np.ones(shape=(2,2))

def f(array_, index):
    array_[index][0] = 2
    
# for i in range(3):
#     for j in range(3):
#         board.set_case(i, j, 'x') #if (i + j) % 2 == 0 else 'o')
#         board.check_winner()
#         #board.reset()
#         if board.endgame():
#             print('The end!')
#         else:
#             print('Still going')
