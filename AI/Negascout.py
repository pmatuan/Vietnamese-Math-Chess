import random

from AI.AI import AI


class Negascout(AI):

    def findMove(self, gs, valid_moves, depth):
        self.DEPTH = depth
        random.shuffle(valid_moves)
        self.findMoveNegaScout(gs, valid_moves, self.DEPTH, -self.CHECKMATE, self.CHECKMATE,
                               1 if gs.red_to_move else -1)
        return self.next_move

    def findMoveNegaScout(self, gs, valid_moves, depth, alpha, beta, turn):
        if depth == 0:
            return self.quiescenceSearch(gs, alpha, beta, turn)
        b = beta
        for move in valid_moves:
            gs.makeMove(move)
            next_moves = gs.getValidMoves()
            t = -self.findMoveNegaScout(gs, next_moves, depth - 1, -b, -alpha, -turn)
            gs.undoMove()
            if (t > alpha) and (t < beta) and (move != valid_moves[0]):
                t = -self.findMoveNegaScout(gs, next_moves, depth - 1, -beta, -alpha, -turn)
            alpha = max(alpha, t)
            if alpha >= beta:
                return alpha  # cut-off
            b = alpha + 1  # set new null window
        return alpha
