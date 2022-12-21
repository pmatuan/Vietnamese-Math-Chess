import random
import copy
from AI.AI import AI


class Negascout(AI):

    def findMove(self, gs, valid_moves):
        random.shuffle(valid_moves)
        self.findMoveNegaScoutAlphaBeta(gs, valid_moves, self.DEPTH, -self.CHECKMATE, self.CHECKMATE, 1 if gs.red_to_move else -1)
        return self.next_move

    def findMoveNegaScoutAlphaBeta(self, gs, valid_moves, depth, alpha, beta, turn):
        if depth == 0:
            return turn * self.scoreMaterial(gs.board)
        bestValue = -self.CHECKMATE
        for move in valid_moves:
            new_gs = copy.deepcopy(gs)
            next_moves = new_gs.getAllPossibleMoves()
            score = - self.findMoveNegaScoutAlphaBeta(new_gs, next_moves, depth - 1, -beta, -alpha, -turn)
            if score > bestValue:
                bestValue = score
                if depth == self.DEPTH:
                    self.next_move = move
                alpha = max(alpha, bestValue)
                if alpha >= beta:
                    break
        return bestValue
