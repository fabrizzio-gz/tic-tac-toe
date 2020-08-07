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

        # Vertical win
        for j in range(3):
            if np.sum(self.columns[j] == player) == 3:
                print('Vertical check')
                return True

        # Diagonal win
        for d in range(2):
            if np.sum(self.diags[d] == player) == 3:
                print('Diagonal check')
                return True

        return False

    def fill_next(self):
        """
        Scans all cases of the board from left to right, top to bottom.
        Fills first empty case found with self.player token.
        """
        for i in range(3):
            for j in range(3):
                if not self.board[i][j]:
                    self.board[i][j] = self.player
                    return None

    def fill_corner(self):
        """
        Chooses one corner randomly.
        If it's empty, fills it with self.player token.
        Raises NoMove exception if not possible for all corners.
        """
        random_corners = list(range(4))
        shuffle(random_corners)
        for i in random_corners:
            if i == 0 and not self.board[0][0]:
                self.board[0][0] = self.player
                break
            elif i == 1 and not self.board[0][2]:
                self.board[0][2] = self.player
                break
            elif i == 2 and not self.board[2][0]:
                self.board[2][0] = self.player
                break
            elif i == 3 and not self.board[2][2]:
                self.board[2][2] = self.player
                break
        else:
            raise NoMove
        
    def diagonal_free(self):
        """
        Check if center case is free.
        Then checks every corner in the board and fills its diagonally
        opposed case if it's empty.
        Raises NoMove exception if not possible for all corners.
        """
        if not self.board[1][1]:
            for d in range(2):
                for filled, empty in [(0, 2), (2, 0)]:
                    if self.diags[d][filled] == self.player and \
                       not self.diags[d][empty]:
                        self.diags[d][empty] = self.player
                        return None
            else:
                raise NoMove
        else:
            raise NoMove

    def complete_triple(self, target=None):###
        """
        target: A player token. If none is given, will use current
        self.player token.
        Scans rows, columns and diagonals for 2 occurrences of target token.
        If 2 cases are filled with 'target', it will fill the remaining case
        with target.
        If no occurrences take place, raises NoMove exception.
        """
        def try_fill(array3):
            """
            array3: An array with 3 elements.
            If two elements of the array are filled with 'target' token and
            one is empty, fills the empty case with current self.player token.
            Returns True if successful. False if not.
            """
            if np.sum(array3 == target) == 2 and \
               np.sum(array3 == '') == 1:
                array3[array3 == ''] = self.player
                return True
            return False
            
        if not target:
            target = self.player
        
        # Rows
        for row in self.rows:
            if try_fill(row):
                return None

        # Columns
        for column in self.columns:
            if try_fill(column):
                return None

        # Diagonals
        for diagonal in self.diags:
            if try_fill(diagonal):
                return None

        raise NoMove

    def win_move(self):
        """
        Searches for rows, columns and diagonals with 2 occurrences of
        self.symbol and completes it to win.
        If no occurrences take place, complete_triple raises NoMove exception.
        """
        self.complete_triple()
        return None

    def avoid_losing(self):
        """
        Searches for rows, columns and diagonals with 2 occurrences of
        the adversary of self.player token. 
        Completes the empty case to avoid losing.
        If no occurrences take place, raises NoMove exception.
        """
        if self.player == 'x':
            target = 'o'
        else:
            target = 'x'
        self.complete_triple(target)
        return None

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
        """
        Attempts different moves.
        If any move succeds, it returns None.
        When a move fails, it raises a NoMove exception and
        attempts the next move.
        """
        self.turns +=1
        if self.player == 'x':
            other_player = 'o'
        else:
            other_player = 'x'

        input('Computer turn... (Press any key to continue)')

        # Starts by filling any of the corners.
        if self.turns <= 2:
            # If the other player started the game and filled
            # any of the corners, fill the center case.
            if self.turns == 2:
                if self.defend_corner():
                    self.board[1][1] = self.player
                    return None
            try:
                self.fill_corner()
                return None
            except NoMove:
                pass

        # Attempts to win the game with a single move.
        try:
            self.win_move()
            return None
        except NoMove:
            pass

        # If the opponent is about to complete a triple, avoid it.
        try:
            self.avoid_losing()
            return None
        except NoMove:
            pass

        # Attempts filling the diagonally opposed case if
        # the central case is empty.
        try:
            self.diagonal_free()
            return None
        except NoMove:
            pass

        # During mid game, attempts to continue filling corners.
        # First verifies that some corners are already filled by the current
        # token or that the opponent hasn't filled the corners already so that
        # it's a worthy move.
        if (self.turns <= 4 and self.count_corners(other_player) != 2) or \
           self.count_corners() >= 2:
            try:
                self.fill_corner()
                return None
            except NoMove:
                pass

        # If no other option, will complete any row/column/diagonal
        # that has one player token and two empty cases.
        try:
            self.complete_second()
            return None
        except NoMove:
            pass
        
        # If no other possible options, fill any empty case.
        self.fill_next()
        return None

    def get_index(self, text):
        """
        Will prompt the player for a row or coluumn index.
        Returns an integer index between 0 - 2.
        """
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
        """
        Will atempt filling the case[i][j].
        Returns True on success. False otherwise.
        """
        if not self.board[i][j]:
            self.board[i][j] = self.player
            return True
        return False

    def user_turn(self):
        """
        Prompts the user for a row and a column index.
        Verifies case isn't filled.
        """
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

    def computer_win(self):
        """
        Prints computer winning message.
        Increments computer score by one.
        """
        print('Computer won!')
        input('Press enter to continue...')
        self.computer_score += 1

    def player_win(self):
        """
        Prints player winning message.
        Increases player score.
        """
        print('You win!')
        input('Press enter to continue...')
        self.user_score += 1

    def print_score(self):
        """
        Prints score
        """
        print('Current score is:\n Player\t: {}\n CPU\t: {}'
              .format(self.user_score,self.computer_score))

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


board = Board()
board.play()
