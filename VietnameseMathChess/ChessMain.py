import pygame as p

from VietnameseMathChess import ChessEngine

WIDTH = HEIGHT = 576
DIMENSION = 9
SQ_SIZE = HEIGHT // 9
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ["ba", "bb", "bc", "bd", "be", "bf", "bg", "bh", "bi", "bj",
              "ra", "rb", "rc", "rd", "re", "rf", "rg", "rh", "ri", "rj"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("image/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == '__main__':
    main()
