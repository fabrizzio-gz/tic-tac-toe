from itertools import cycle
from random import shuffle
import numpy as np

### TODO:
# - 2 player mode.
# - Choose player/cpu token.


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
        self.players = cycle('xo')
        self.player = '-'
        self.user_score = 0
        self.computer_score = 0
        self.turns = 0

    def check_winner(self, player=None):
        """
        player: The token to check
        Checks if a row, column or diagonal is filled with 'player' token.
        If no 'player' token is given, uses curren self.player token.
        Returns a tuple (True, (i0,j0), (i1,j1)) if winning conditions attained.
        (i0, j0) and (i1, j1) are the border indices of the winning cases.
        (False, 0, 0) otherwise.
        """
        if not player:
            player = self.player

        # Horizontal win
        for i in range(3):
            if np.sum(self.rows[i] == player) == 3:
                print('Horizontal check')
                print(i)
                return (True, (i, 0), (i, 2))

        # Vertical win
        for j in range(3):
            if np.sum(self.columns[j] == player) == 3:
                print('Vertical check')
                print(j)
                return (True, (0, j), (2, j))

        # Diagonal win
        for d in range(2):
            if np.sum(self.diags[d] == player) == 3:
                print('Diagonal check')
                # Main diagonal
                if d == 0:
                    return (True, (0, 0), (2, 2))
                # Second diagnoal
                else:
                    return (True, (0, 2), (2, 0))

        return (False, 0, 0)

    def fill_next(self):
        """
        Fills the next empty case with self.player token.
        Returns th i and j indices played.
        """
        for i in range(3):
            for j in range(3):
                if not self.board[i][j]:
                    self.board[i][j] = self.player
                    return (i, j)

    def fill_corner(self):
        """
        Chooses one corner randomly.
        If it's empty, fills it with self.player token.
        Returns the played indices.
        Raises NoMove exception if not possible for all corners.
        """
        random_corners = list(range(4))
        shuffle(random_corners)
        for i in random_corners:
            if i == 0 and not self.board[0][0]:
                self.board[0][0] = self.player
                return (0, 0)
            elif i == 1 and not self.board[0][2]:
                self.board[0][2] = self.player
                return (0, 2)
            elif i == 2 and not self.board[2][0]:
                self.board[2][0] = self.player
                return (2, 0)
            elif i == 3 and not self.board[2][2]:
                self.board[2][2] = self.player
                return (2, 2)
        else:
            raise NoMove
        
    def diagonal_free(self):
        """
        If center case is free, will attempt to fill the diagonally opposed case
        of a case already filled with self.player token.
        Raises a NoMove exception if conditions aren't met.
        """
        if not self.board[1][1]:
            for d in range(2):
                for filled, empty in [(0, 2), (2, 0)]:
                    if self.diags[d][filled] == self.player and \
                       not self.diags[d][empty]:
                        self.diags[d][empty] = self.player
                        if d == 0:
                            if filled == 0:
                                return (2, 2)
                            else:
                                return (0, 0)
                        else:
                            if filled == 0:
                                return (2, 0)
                            else:
                                return (0, 2)
            else:
                raise NoMove
        else:
            raise NoMove

    def complete_triple(self, target=None):
        """
        target: A player token. If none is given, will use current
        self.player token.
        Scans rows, columns and diagonals for 2 occurrences of target token.
        If 2 cases are filled with 'target', it will fill the remaining case
        with target.
        If no occurrences take place, raises NoMove exception.
        Returns an i, j tuple of the filled case
        """
        def try_fill(array3):
            """
            array3: An array with 3 elements.
            If two elements of the array are filled with 'target' token and
            one is empty, fills the empty case with current self.player token.
            Returns a tuple with the index and True if successful. 
            False and 0 if unsuccessful.
            """
            if np.sum(array3 == target) == 2 and \
               np.sum(array3 == '') == 1:
                for index in range(3):
                    if array3[index] == '':
                        array3[index] = self.player
                        return (True, index)
            return (False, 0)
            
        if not target:
            target = self.player
        
        # Rows
        for i, row in enumerate(self.rows):
            cond, j = try_fill(row)
            if cond:
                return (i, j)

        # Columns
        for j, column in enumerate(self.columns):
            cond, i = try_fill(column)
            if cond:
                return (i, j)

        # Diagonals
        for d, diagonal in enumerate(self.diags):
            cond, empty = try_fill(diagonal)
            if cond:
                # First diagonal
                if d == 0:
                    return (empty, empty)
                # Second diagonal
                else:
                    return (empty, 2 - empty)

        raise NoMove

    def win_move(self):
        """
        Searches for rows, columns and diagonals with 2 occurrences of
        self.symbol and completes it to win.
        If no occurrences take place, complete_triple raises NoMove exception.
        Returns and i,j tuple of the filled case
        """
        return self.complete_triple()

    def avoid_losing(self):
        """
        Searches for rows, columns and diagonals with 2 occurrences of
        the adversary of self.player token.
        Completes the empty case to avoid losing.
        If no occurrences take place, raises NoMove exception.
        Returns an i, j tuple of the filled case.
        """
        if self.player == 'x':
            target = 'o'
        else:
            target = 'x'
        return self.complete_triple(target)

    def count_corners(self, target=None):
        """
        Returns the number of corners occupied by the current
        self.player token. (0 - 4)
        """
        if not target:
            target = self.player

        return np.sum(self.board[[0, 0, -1, -1], [0, -1, 0, -1]] == target)

    def defend_corner(self):
        """
        Checks if the other player has filled one of the corners of the board.
        Returns True or False.
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
        Returns the index of the filled case
        """
        for index in range(3):
            if not array3[index]:
                array3[index] = self.player
                return index

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
                j = self.fill_one(self.rows[i])
                return (i, j)

        for j in range(3):
            if self.scan_one(self.columns[j]):
                i = self.fill_one(self.columns[j])
                return (i, j)

        for d, diagonal in enumerate(self.diags):
            if self.scan_one(diagonal):
                filled = self.fill_one(diagonal)
                # Main diagonal
                if d == 0:
                    return (filled, filled)
                else:
                    return (filled, 2 - filled)

        raise NoMove

    def computer_turn(self):
        """
        Swithches from last player.
        Attempts different moves.
        If any move succeds, it returns None.
        When a move fails, it raises a NoMove exception and
        attempts the next move.
        Returns the indeces i, j of the filled case.
        """
        self.player = next(self.players)
        self.turns +=1
        if self.player == 'x':
            other_player = 'o'
        else:
            other_player = 'x'

        # Starts by filling any of the corners.
        if self.turns <= 2:
            # If the other player started the game and filled
            # any of the corners, fill the center case.
            if self.turns == 2:
                if self.defend_corner():
                    self.board[1][1] = self.player
                    return (1, 1)
            try:
                return self.fill_corner()
            except NoMove:
                pass

        # Attempts to win the game with a single move.
        try:
            return self.win_move()
        except NoMove:
            pass

        # If the opponent is about to complete a triple, avoid it.
        try:
            return self.avoid_losing()
        except NoMove:
            pass

        # Attempts filling the diagonally opposed case if
        # the central case is empty.
        try:
            return self.diagonal_free()
        except NoMove:
            pass

        # During mid game, attempts to continue filling corners.
        # First verifies that some corners are already filled by the player
        # or that the opponent hasn't filled the corners already so that
        # it's a worthy move.
        if (self.turns <= 4 and self.count_corners(other_player) != 2) or \
           self.count_corners() >= 2:
            try:
                return self.fill_corner()
            except NoMove:
                pass

        # If no other option, will complete any row/column/diagonal
        # that has one player token and two empty cases.
        try:
            return self.complete_second()
        except NoMove:
            pass
        
        # If no other possible options, fill any empty case.
        return self.fill_next()


    def user_turn(self, pos):
        """
        pos: A i, j tuple.
        Updates the game stats and switches to next
        player.
        Verifies tuple are valid inputs.
        Verifies the current case is empty
        Fills board and returns True on success.
        Else returns False.
        """
        self.turns += 1
        self.player = next(self.players)
        i = pos[0]
        j = pos[1]
        if i >= 0 and i <= 2:
            if j >= 0 and j <= 2:
                if not self.board[i][j]:
                    self.board[i][j] = self.player
                    return True
        return False

    def play(self):
        """
        Game loop.
        Starts with computer turn.
        Alternates turns between player/computer.
        Verifies if there is a winner.
        Verifies if there is a draw.
        Starts new game alternating from last player.
        """
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
                self.player = next(self.players)
            elif self.endgame():
                self.print_score()
                print("It's a draw!")
                input('Press any key to continue...')
                self.reset()
                print('New game')
                print(self)
                self.player = next(self.players)
            else:
                self.player = next(self.players)

    def endgame(self):
        """
        Checks if 9 turns of the game have elapsed.
        """
        return self.turns == 9

    def reset(self):
        """
        Empties all board cases and sets turns to 0.
        """
        self.board.fill('')
        self.turns = 0


    def __str__(self):
        """
        Game board pretty printing.
        """
        dash = '---'
        counter = 0
        board_str = ''
        for row in self.board:
            board_str += '{: ^5s}|{: ^5s}|{: ^5s}\n'\
                          .format(row[0], row[1], row[2])
            if counter < 2:
                counter += 1
                board_str += '{0: ^5s}+{0: ^5s}+{0: ^5s}\n'.format(dash)

        return board_str
