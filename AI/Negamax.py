import random

class Negamax:
    def __init__(self):
        self.CHECKMATE = 45
        self.STALEMATE = 0
        self.DEPTH = 2
        self.next_move = None

    def scoreMaterial(self, board):
        score = 0
        for row in board:
            for square in row:
                if square[0] == "r":
                    if int(square[1]) == 0:
                        score += 1000
                    else:
                        score += int(square[1])
                elif square[0] == "b":
                    if int(square[1]) == 0:
                        score -= 1000
                    else:
                        score -= int(square[1])
        return score
    def findMove(self, gs, valid_moves):
        self.findBestMove(gs, valid_moves, self.DEPTH, 1 if gs.red_to_move else -1)
        return self.next_move
    def findBestMove(self, gs, valid_moves, depth, turn):
        if depth == 0:
            return turn * self.scoreMaterial(gs.board)
        bestValue = -self.CHECKMATE
        for move in valid_moves:
            gs.makeMove(move)
            next_moves = gs.getAllPossibleMoves()
            score = - self.findBestMove(gs, next_moves, depth - 1, -turn)
            if score > bestValue:
                bestValue = score
                if depth == self.DEPTH:
                    self.next_move = move
            gs.undoMove()
        return bestValue
