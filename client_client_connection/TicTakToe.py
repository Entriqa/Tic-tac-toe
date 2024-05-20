from modules import PlayerType


class Game:
    def __init__(self):
        self.board = [[(i + j * 3, -1) for i in range(1, 4)] for j in range(3)]
        self.winner = None
        self.draw = False

    def player_move(self, player_type, cage_number):
        if player_type == 0:
            player = PlayerType.noughts
        else:
            player = PlayerType.crosses
        point = tuple()
        for i in range(3):
            for j in range(3):
                if self.board[i][j][0] == cage_number:
                    point = (i, j)
        if point and player:
            self.move_checker(player, point)

    def move_checker(self, player: PlayerType, point):
        if self.board[point[0]][point[1]][1] != -1:
            return False
        self.board[point[0]][point[1]] = self.board[point[0]][point[1]][0], player.value
        win_flag = True
        for i in range(3):
            if self.board[point[0]][i][1] != player.value:
                win_flag = False
        if win_flag:
            self.winner = player
        win_flag = True
        for i in range(3):
            if self.board[i][point[0]][1] != player.value:
                win_flag = False
        if win_flag:
            self.winner = player
        if self.board[0][0][1] == self.board[1][1][1] == self.board[2][2][1] == player.value:
            self.winner = player
        if self.board[0][2][1] == self.board[1][1][1] == self.board[2][0][1] == player.value:
            self.winner = player

        self.draw = True
        for i in range(3):
            for j in range(3):
                if self.board[i][j][1] == -1:
                    self.draw = False
        return True

    def get_board(self):
        board_view = [['' for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                if self.board[i][j][1] == 0:
                    board_view[i][j] = 'O'
                elif self.board[i][j][1] == 1:
                    board_view[i][j] = 'X'
                else:
                    board_view[i][j] = str(self.board[i][j][0])
        return '\n'.join([' | '.join(i) for i in board_view])
