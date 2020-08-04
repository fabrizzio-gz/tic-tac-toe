# tic-tac-toe

from itertools import cycle


class Board:

    players = cycle('xo')
    
    
    def __init__(self):
        self.board = [['' for _ in range(3)] for __ in range(3)]
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
            if board[i][0] == player and board[i][1] == player and \
               board[i][2] == player:
                print('Horizontal check')
                return True

        # Vertical win
        for j in range(3):
            if board[0][j] == player and board[1][j] == player and \
               board[2][j] == player:
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
                    
    
    def computer_turn(self):
        self.turns += 1
        input('Computer turn... (Press any key to continue)')
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
        self.board = [['' for _ in range(3)] for __ in range(3)]
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
for i in range(3):
    for j in range(3):
        board.set_case(i, j, 'x') #if (i + j) % 2 == 0 else 'o')
        board.check_winner()
        board.reset()
        if board.endgame():
            print('The end!')
        else:
            print('Still going')
