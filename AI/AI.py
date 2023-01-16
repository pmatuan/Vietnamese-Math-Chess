import random


class AI:
    def __init__(self):
        self.CHECKMATE = 45
        self.STALEMATE = 0
        self.DEPTH = 3
        self.next_move = None

    def scoreMaterial(self, board):
        score = 0
        for row in board:
            for square in row:
                if square[0] == "r":
                    if int(square[1]) == 0:
                        score += self.CHECKMATE
                    else:
                        score += int(square[1])
                elif square[0] == "b":
                    if int(square[1]) == 0:
                        score -= self.CHECKMATE
                    else:
                        score -= int(square[1])
        score += self.scoreZeroSafety(board)
        return score

    def scoreZeroSafety(self, board):
        red_direction = ((-1, -1), (-1, 1), (-1, 0), (0, -1), (0, 1))
        blue_direction = ((0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        score = 0
        for d in red_direction:
            for i in range(1, 4, 1):
                if board[d[0]*i][d[1]*i][0] == 'b':
                    score -= 1
        for d in blue_direction:
            for i in range(1, 4, 1):
                if board[d[0]*i][d[1]*i][0] == 'r':
                    score += 1
        return score
    
    def findRandomMove(self, valid_moves):
        return random.choice(valid_moves)
