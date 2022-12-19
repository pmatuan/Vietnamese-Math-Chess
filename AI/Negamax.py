import random

from AI.AI import AI


class Negamax(AI):

    def findMove(self, gs, valid_moves):
        random.shuffle(valid_moves)
        self.findMoveNegaMaxAlphaBeta(gs, valid_moves, self.DEPTH, -self.CHECKMATE, self.CHECKMATE, 1 if gs.red_to_move else -1)
        return self.next_move

    def findMoveNegaMaxAlphaBeta(self, gs, valid_moves, depth, alpha, beta, turn):
        if depth == 0:
            return turn * self.scoreMaterial(gs.board)
        bestValue = -self.CHECKMATE
        for move in valid_moves:
            gs.makeMove(move)
            next_moves = gs.getAllPossibleMoves()
            score = - self.findMoveNegaMaxAlphaBeta(gs, next_moves, depth - 1, -beta, -alpha, -turn)
            if score > bestValue:
                bestValue = score
                if depth == self.DEPTH:
                    self.next_move = move
            gs.undoMove()
            if bestValue > alpha:
                alpha = bestValue
            if alpha >= beta:
                break
        return bestValue
