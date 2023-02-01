import time

from Engine.GameState import GameState
from Engine.Move import Move
from AI.Negamax import Negamax
from AI.Negascout import Negascout
from AI.Minimax import Minimax
from AI.Greedy import Greedy
from UI.UI import *
from UI.cal import *

WIDTH = 832
HEIGHT = 832
C_DIMENSION = 9
R_DIMENSION = 11
SQ_SIZE = 64
MAX_FPS = 10
IMAGES = {}

scenes = {
    'TITLE': SimpleScene('Cờ toán Việt Nam'),
    'CHOOSE_MODE': ChooseScene('Chọn chế độ chơi', 'Người Vs Người', 'Người Vs Máy', 'Máy Vs Máy'),
    'CHOOSE_BOT': ChooseBot('Chọn Bot', 'Negamax', 'Negascout', 'Minimax', 'Greedy'),
    'CHOOSE_DEPTH': ChooseDepth('Chọn độ sâu', 'Độ sâu: ')
}
bot_ai = {
    'Negamax': Negamax(),
    'Negascout': Negascout(),
    'Minimax': Minimax(),
    'Greedy': Greedy()
}


def main():
    """
    The main driver for our code.
    This will handle user input and updating the graphics.
    """
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    gs = GameState()
    valid_moves = gs.getValidMoves()
    move_made = False  # flag variable for when a move is made
    loadImages()
    running = True
    sq_selected = ()  # no square is selected, keep track of the last click of the user (tuple: (row, col))
    player_clicks = []  # keep track of the player clicks
    game_over = False
    AI_BLUE = None
    DEPTH_AI_BLUE = None
    DEPTH_AI_RED = None
    AI_RED = None
    end_UI = True
    scene = scenes['TITLE']
    cal = Calculation()
    while running:
        if end_UI:
            screen = pygame.display.set_mode((640, 480))
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    return
            result = scene.update(events)
            ele = scene.element(events)
            if result or ele:
                if ele or ele == 0:
                    if ele == (True, True):
                        player_one = True  # if a human playing red, then this will be True. If an AI is playing, then false
                        player_two = True  # same as above but for blue
                        end_UI = False
                        result = 'CHOOSE_MODE'
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    if ele == (True, False):
                        player_one = True
                        player_two = False
                        result = 'CHOOSE_BOT'
                    if ele == (False, False):
                        player_one = False
                        player_two = False
                        result = 'CHOOSE_BOT'
                    if ele == 'Negamax' and AI_BLUE:
                        AI_RED = bot_ai['Negamax']
                        result = 'CHOOSE_DEPTH'
                    if ele == 'Negamax' and not AI_BLUE:
                        AI_BLUE = bot_ai['Negamax']
                        result = 'CHOOSE_DEPTH'
                    if ele == 'Negascout' and AI_BLUE:
                        AI_RED = bot_ai['Negamax']
                        result = 'CHOOSE_DEPTH'
                    if ele == 'Negascout' and not AI_BLUE:
                        AI_BLUE = bot_ai['Negascout']
                        result = 'CHOOSE_DEPTH'
                    if ele == 'Minimax' and AI_BLUE:
                        AI_RED = bot_ai['Negamax']
                        result = 'CHOOSE_DEPTH'
                    if ele == 'Minimax' and not AI_BLUE:
                        AI_BLUE = bot_ai['Minimax']
                        result = 'CHOOSE_DEPTH'
                    if ele == 'Greedy' and AI_BLUE:
                        AI_RED = bot_ai['Greedy']
                        DEPTH_AI_RED = True
                    if ele == 'Greedy' and not AI_BLUE:
                        AI_BLUE = bot_ai['Greedy']
                        DEPTH_AI_BLUE = True

                    if isinstance(ele, int) and DEPTH_AI_BLUE:
                        if ele >= 0:
                            DEPTH_AI_RED = ele
                        else:
                            AI_RED = None
                    if isinstance(ele, int) and not DEPTH_AI_BLUE:
                        if ele >= 0:
                            DEPTH_AI_BLUE = ele
                        else:
                            AI_BLUE = None

                    if not player_one and not AI_RED and (DEPTH_AI_BLUE or DEPTH_AI_BLUE == 0):
                        result = 'CHOOSE_BOT'

                    if (player_one and not player_two and AI_BLUE and (DEPTH_AI_BLUE or DEPTH_AI_BLUE == 0)) or (
                            not player_one and not player_two and AI_BLUE and AI_RED and (
                            DEPTH_AI_BLUE or DEPTH_AI_BLUE == 0) and (DEPTH_AI_RED or DEPTH_AI_RED == 0)):
                        result = 'CHOOSE_MODE'
                        end_UI = False
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))

                scene = scenes[result]
            scene.draw(screen)
            pygame.display.flip()
        else:
            drawGameState(screen, gs, valid_moves, sq_selected)
            human_turn = (gs.red_to_move and player_one) or (not gs.red_to_move and player_two)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    if not game_over and human_turn and location[0] <= WIDTH - WIDTH_CAL:
                        # (x,y) location of mouse
                        col = location[0] // SQ_SIZE
                        row = location[1] // SQ_SIZE
                        if sq_selected == (row, col):  # the user clicked the same square twice
                            sq_selected = ()  # deselect
                            player_clicks = []  # clear player clicks
                        else:
                            sq_selected = (row, col)
                            player_clicks.append(sq_selected)  # append for both 1st and 2nd clicks
                        if len(player_clicks) == 2:  # after 2 click
                            move = Move(player_clicks[0], player_clicks[1], gs.board)
                            if move in valid_moves:
                                gs.makeMove(move)
                                move_made = True
                                sq_selected = ()  # reset user clicks
                                player_clicks = []
                            else:
                                player_clicks = [sq_selected]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:  # undo when 'z' is pressed
                        gs.undoMove()
                        gs.undoMove()
                        move_made = True

            # calculate red score
            red_score = score(gs)[0]
            blue_score = score(gs)[1]
            red_lost = score(gs)[2]
            blue_lost = score(gs)[3]
            if red_score >= 15 or blue_score >= 15:
                game_over = True
            game_over = game_over or gs.check()
            if game_over:
                if gs.red_to_move:
                    loser("Blue win", screen)
                    running = False
                else:
                    loser("Red win", screen)
                    running = False
            # AI move finder
            if not game_over and not human_turn and not gs.red_to_move:
                ################################
                if AI_BLUE == bot_ai['Greedy']:
                    AIMove = AI_BLUE.findMove(gs, valid_moves)
                else:
                    AIMove = AI_BLUE.findMove(gs, valid_moves, DEPTH_AI_BLUE)
                gs.makeMove(AIMove)
                move_made = True
                ################################

            elif not game_over and not human_turn and AI_RED and gs.red_to_move:
                ################################
                if AI_RED == bot_ai['Greedy']:
                    AIMove = AI_RED.findMove(gs, valid_moves)
                else:
                    AIMove = AI_RED.findMove(gs, valid_moves, DEPTH_AI_BLUE)
                gs.makeMove(AIMove)
                move_made = True
                ################################
            if move_made:
                valid_moves = gs.getValidMoves()
                move_made = False
            drawGameState(screen, gs, valid_moves, sq_selected)
            clock.tick(MAX_FPS)
            subScreen(screen, "Blue score: " + str(blue_score), 30, (256, 112), (576, 0), (0, 0, 255))
            subScreen(screen, "Blue lost: " + str(blue_lost), 30, (256, 112), (576, 112), (0, 0, 255))
            cal.draw_caltable(screen, events, IMAGES)
            subScreen(screen, "Red score: " + str(red_score), 30, (256, 112), (576, 480), (255, 0, 0))
            subScreen(screen, "Red lost: " + str(red_lost), 30, (256, 112), (576, 592), (255, 0, 0))
            valid_attacks = ""
            move_previous = None
            for move in gs.getAllPossibleAttacks():
                if move_previous == move:
                    continue
                valid_attacks += move.piece_captured
                valid_attacks += " "
                move_previous = move
            subScreen(screen, "Available attack: " + valid_attacks, 30, (834, 128), (0, 704), (0, 0, 0))
            pygame.display.flip()


def loadImages():
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    pieces = ["b0", "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9",
              "r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("image/" + piece + ".png"),
                                               (SQ_SIZE - 10, SQ_SIZE - 10))


def score(gs):
    score_red = 0
    score_blue = 0
    remaining_red = []
    remaining_blue = []
    for row in gs.board:
        for square in row:
            if square[0] == "r":
                score_red += int(square[1])
                remaining_red.append(int(square[1]))
            elif square[0] == "b":
                score_blue += int(square[1])
                remaining_blue.append(int(square[1]))
    lost_red = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}.difference(set(remaining_red))
    lost_blue = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}.difference(set(remaining_blue))
    if lost_red == set():
        lost_red = None
    if lost_blue == set():
        lost_blue = None
    return 45 - score_blue, 45 - score_red, lost_red, lost_blue


def subScreen(screen, message, font_size, area, location, color):
    sub_screen = pygame.Surface(area)
    sub_screen.fill(color)
    font = pygame.font.Font(None, font_size)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.centerx = sub_screen.get_rect().centerx
    text_rect.centery = sub_screen.get_rect().centery
    sub_screen.blit(text, text_rect)
    screen.blit(sub_screen, location)


def highlightSquares(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        r, c = sq_selected
        if gs.board[r][c][0] == ('r' if gs.red_to_move else 'b'):  # sq_selected is a piece that can be moved
            # highlight selected square
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value -> 0 transparent; 255 opaque
            s.fill(pygame.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(pygame.Color('yellow'))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))


def drawGameState(screen, gs, valid_moves, sq_selected):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)
    highlightSquares(screen, gs, valid_moves, sq_selected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    colors = [pygame.Color("white"), pygame.Color("bisque3")]
    for r in range(R_DIMENSION):
        for c in range(C_DIMENSION):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for r in range(R_DIMENSION):
        for c in range(C_DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c * SQ_SIZE + 5, r * SQ_SIZE + 5, SQ_SIZE, SQ_SIZE))


def loser(message, screen):
    time.sleep(0.5)
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(message, True, pygame.Color('green'))
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2)
    screen.fill(pygame.Color('white'))
    screen.blit(text, textRect)
    pygame.display.update()
    time.sleep(5)


if __name__ == "__main__":
    main()
