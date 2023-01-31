import random

from AI.AI import AI


class Negascout(AI):

    def findMove(self, gs, valid_moves):
        random.shuffle(valid_moves)
        self.findMoveNegascout(gs, valid_moves, self.DEPTH, -self.CHECKMATE, self.CHECKMATE,
                                      1 if gs.red_to_move else -1)
        return self.next_move

    def findMoveNegascout(self, gs, valid_moves, depth, alpha, beta, turn):
        best_move = None
        if depth == 0:
            return self.quiescenceSearch(gs, alpha, beta, turn)
        for i, move in enumerate(valid_moves):
            if i == 0:
                gs.makeMove(move)
                next_moves = gs.getValidMoves()
                score = -self.findMoveNegascout(gs, next_moves, depth - 1, -beta, -alpha, -turn)
                gs.undoMove()
            else:
                gs.makeMove(move)
                next_moves = gs.getValidMoves()
                score = -self.findMoveNegascout(gs, next_moves, depth - 1, -alpha - 1, -alpha, -turn) # search with a null window
                gs.undoMove()
                if alpha < score < beta:
                    gs.makeMove(move)
                    next_moves = gs.getValidMoves()
                    score = -self.findMoveNegascout(gs, next_moves, depth - 1, -beta, -score, -turn) # if it failed high, do a full re-search
                    gs.undoMove()
            if alpha < score:
                best_move = move
                alpha = score
            if alpha >= beta:
                break # cut-off
        if depth == self.DEPTH:
            self.next_move = best_move
        return alpha

    def quiescenceSearch(self, gs, alpha, beta, turn):
        score = turn * self.scoreMaterial(gs)
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
        capture_moves = gs.getAllPossibleAttacks()
        for move in capture_moves:
            if beta <= alpha:
                break
            gs.makeMove(move)
            score = -self.quiescenceSearch(gs, -beta, -alpha, -turn)
            gs.undoMove()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        return alpha


