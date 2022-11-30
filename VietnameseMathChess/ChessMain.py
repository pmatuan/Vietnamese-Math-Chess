"""
Main driver file.
Handling user input.
Displaying current GameStatus object.
"""

import pygame as p
from VietnameseMathChess import ChessEngine

WIDTH = 576
HEIGHT = 704
C_DIMENSION = 9
R_DIMENSION = 11
SQ_SIZE = HEIGHT // R_DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    pieces = ["b0", "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9",
              "r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("image/" + piece + ".png"), (SQ_SIZE - 10, SQ_SIZE - 10))


def main():
    """
    The main driver for our code.
    This will handle user input and updating the graphics.
    """
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # flag variable for when a move is made
    loadImages()
    running = True
    sqSelected = ()  # no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = []  # keep track of the player clicks
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x,y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):  # the user clicked the same square twice
                    sqSelected = ()  # deselect
                    playerClicks = []  # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # append for both 1st and 2nd clicks
                if len(playerClicks) == 2:  # after 2 click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()  # reset user clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:  # undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    colors = [p.Color("white"), p.Color("bisque3")]
    for r in range(R_DIMENSION):
        for c in range(C_DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for r in range(R_DIMENSION):
        for c in range(C_DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE + 5, r * SQ_SIZE + 5, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
