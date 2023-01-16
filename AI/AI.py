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
        return score
    
    def findRandomMove(self, valid_moves):
        return random.choice(valid_moves)
