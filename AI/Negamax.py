import random

class Negamax:
    def __init__(self, valid_moves):
        self.valid_moves = valid_moves
    def findMove(self):
        return self.valid_moves[random.randint(0, len(self.valid_moves) - 1)]