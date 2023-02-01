import random

from AI.AI import AI


class Negascout(AI):

    def findMove(self, gs, valid_moves, depth):
        self.DEPTH = depth
        random.shuffle(valid_moves)
        self.browsed_nodes = 0
        self.total_nodes = 0
        self.counter = 0
        self.findMoveMinimax(gs, valid_moves, self.DEPTH, gs.red_to_move)
        self.findMoveNegascout(gs, valid_moves, self.DEPTH, -self.CHECKMATE, self.CHECKMATE,
                                      1 if gs.red_to_move else -1)
        return self.next_move, self.browsed_nodes, self.total_nodes, self.counter

    def findMoveNegascout(self, gs, valid_moves, depth, alpha, beta, turn):
        best_move = None
        self.browsed_nodes += 1
        if depth == 0:
            return self.quiescenceSearch(gs, alpha, beta, turn)
        for i, move in enumerate(valid_moves):
            gs.makeMove(move)
            self.counter += 1
            next_moves = gs.getValidMoves()
            if i == 0:
                score = -self.findMoveNegascout(gs, next_moves, depth - 1, -beta, -alpha, -turn)
            else:
                score = -self.findMoveNegascout(gs, next_moves, depth - 1, -alpha - 1, -alpha, -turn) # search with a null window
                if alpha < score < beta:
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

    def findMoveMinimax(self, gs, valid_moves, depth, red_to_move):
        self.total_nodes += 1
        if depth == 0:
            return self.scoreMaterial(gs)
        if red_to_move:
            max_score = -self.CHECKMATE
            for move in valid_moves:
                gs.makeMove(move)
                next_moves = gs.getValidMoves()
                score = self.findMoveMinimax(gs, next_moves, depth - 1, False)
                gs.undoMove()
                if score > max_score:
                    max_score = score
                    if depth == self.DEPTH:
                        self.next_move1 = move
            return max_score
        else:
            min_score = self.CHECKMATE
            for move in valid_moves:
                gs.makeMove(move)
                next_moves = gs.getValidMoves()
                score = self.findMoveMinimax(gs, next_moves, depth - 1, True)
                gs.undoMove()
                if score < min_score:
                    min_score = score
                    if depth == self.DEPTH:
                        self.next_move1 = move
            return min_score
