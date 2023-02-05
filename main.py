import time

from Engine.GameState import GameState
from Engine.Move import Move
from AI.Negamax import Negamax
from AI.Negascout import Negascout
from AI.Minimax import Minimax
from AI.Greedy import Greedy
from UI.UI import *
from UI.cal import *

from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import random

def draw_list(data, title, filename):
    plt.plot(data)
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.title(title)
    plt.savefig(filename)
def list_to_pdf(data, filename):
    c = canvas.Canvas(filename)
    for item in data:
        c.drawString(100, 800, str(item))
        c.showPage()
    c.save()

WIDTH = 1000
HEIGHT = 760
C_DIMENSION = 9
R_DIMENSION = 11
SQ_SIZE = 56
MAX_FPS = 10
IMAGES = {}
Red_Browse = 'None'
Blue_Browse = 'None'
Red_Counter = 'None'
Blue_Counter = 'None'
Red_AI_Time = 'None'
Blue_AI_Time = 'None'
ai_red = 'Human'
ai_blue = 'Human'

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
    global Red_Browse
    global Blue_Browse
    global Red_Counter
    global Blue_Counter
    global Red_AI_Time
    global Blue_AI_Time
    global ai_red
    global ai_blue
    red_browse = []
    blue_browse = []
    red_counter = []
    blue_counter = []
    red_ai_time = []
    blue_ai_time = []
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
                        AI_RED = bot_ai['Negascout']
                        result = 'CHOOSE_DEPTH'
                    if ele == 'Negascout' and not AI_BLUE:
                        AI_BLUE = bot_ai['Negascout']
                        result = 'CHOOSE_DEPTH'
                    if ele == 'Minimax' and AI_BLUE:
                        AI_RED = bot_ai['Minimax']
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
            if AI_RED == bot_ai['Minimax']:
                ai_red = 'Minimax'
            if AI_RED == bot_ai['Negamax']:
                ai_red = 'Negamax'
            if AI_RED == bot_ai['Negascout']:
                ai_red = 'Negascout'
            if AI_RED == bot_ai['Greedy']:
                ai_red = 'Greedy'
            if AI_BLUE == bot_ai['Minimax']:
                ai_blue = 'Minimax'
            if AI_BLUE == bot_ai['Negamax']:
                ai_blue = 'Negamax'
            if AI_BLUE == bot_ai['Negascout']:
                ai_blue = 'Negascout'
            if AI_BLUE == bot_ai['Greedy']:
                ai_blue = 'Greedy'

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
                    AIMove = AI_BLUE.findMove(gs, valid_moves, DEPTH_AI_BLUE)[0]
                    Blue_Browse = AI_BLUE.findMove(gs, valid_moves, DEPTH_AI_BLUE)[1]
                    Blue_Counter = AI_BLUE.findMove(gs, valid_moves, DEPTH_AI_BLUE)[2]
                    Blue_AI_Time = AI_BLUE.findMove(gs, valid_moves, DEPTH_AI_BLUE)[3]
                    blue_browse.append(Blue_Browse)
                    blue_counter.append(Blue_Counter)
                    blue_ai_time.append(Blue_AI_Time)
                gs.makeMove(AIMove)
                move_made = True


                ################################

            elif not game_over and not human_turn and AI_RED and gs.red_to_move:
                ################################
                if AI_RED == bot_ai['Greedy']:
                    AIMove = AI_RED.findMove(gs, valid_moves)
                else:
                    AIMove = AI_RED.findMove(gs, valid_moves, DEPTH_AI_RED)[0]
                    Red_Browse = AI_RED.findMove(gs, valid_moves, DEPTH_AI_RED)[1]
                    Red_Counter = AI_RED.findMove(gs, valid_moves, DEPTH_AI_RED)[2]
                    Red_AI_Time = AI_RED.findMove(gs, valid_moves, DEPTH_AI_RED)[3]
                    red_browse.append(Red_Browse)
                    red_counter.append(Red_Counter)
                    red_ai_time.append(Red_AI_Time)
                gs.makeMove(AIMove)
                move_made = True
                ################################
            if move_made:
                valid_moves = gs.getValidMoves()
                move_made = False
            drawGameState(screen, gs, valid_moves, sq_selected)
            clock.tick(MAX_FPS)
            subScreen(screen, "Blue score: " + str(blue_score), 24, (224, 90), (504, 0), (0, 0, 255))
            subScreen(screen, "Blue lost: " + str(blue_lost), 24, (224, 90), (504, 90), (0, 0, 255))
            cal.draw_caltable(screen, events, IMAGES)
            subScreen(screen, "Red score: " + str(red_score), 24, (224, 90), (504, 436), (255, 0, 0))
            subScreen(screen, "Red lost: " + str(red_lost), 24, (224, 90), (504, 526), (255, 0, 0))
            valid_attacks = ""
            move_previous = None
            for move in gs.getAllPossibleAttacks():
                if move_previous == move:
                    continue
                valid_attacks += move.piece_captured
                valid_attacks += " "
                move_previous = move
            if not game_over and gs.red_to_move:
                subScreen(screen, 'Red turn', 25, (272, 144), (728, 616), (255, 0, 0))
            if not game_over and not gs.red_to_move:
                subScreen(screen, 'Blue turn', 25, (272, 144), (728, 616), (0, 0, 255))
            subScreen(screen, 'Available Attack: ' + str(valid_attacks), 25, (728, 144), (0, 616), (0, 0, 0))
            subScreen(screen, "Blue player: " + ai_blue, 21, (272, 77), (728, 0), (128, 0, 128))
            subScreen(screen, "Red player: " + ai_red, 21, (272, 77), (728, 539), (240, 0, 255))
            subScreen(screen, "Blue AI calculating: " + str(Blue_AI_Time), 21, (272, 77), (728, 231), (128, 0, 128))
            subScreen(screen, "Blue counter: " + str(Blue_Counter), 21, (272, 77), (728, 77), (128, 0, 128))
            subScreen(screen, "Blue browser nodes: " + str(Blue_Browse), 21, (272, 77), (728, 154), (128, 0, 128))
            subScreen(screen, "Red browser nodes: " + str(Red_Browse), 21, (272, 77), (728, 385), (240, 0, 255))
            subScreen(screen, "Red counter: " + str(Red_Counter), 21, (272, 77), (728, 462), (240, 0, 255))
            subScreen(screen, "Red AI calculating: " + str(Red_AI_Time), 21, (272, 77), (728, 308),
                      (240, 0, 255))
            pygame.display.flip()
            if event.type == pygame.QUIT or running == False:
                a = random.randint(0, 100)
                if len(red_browse) > 0:
                    title = str(ai_red) + ' Visited Node'
                    filename1 = str(ai_red) + str(a) + 'redbrowse.png'
                    draw_list(red_browse, title, filename1)
                if len(red_counter) > 0:
                    title = str(ai_red) + ' Counter'
                    filename1 = str(ai_red) + str(a) + 'redcounter.png'
                    draw_list(red_counter, title, filename1)
                if len(red_ai_time) > 0:
                    title = str(ai_red) + ' Calculation Time'
                    filename1 = str(ai_red) + str(a) + 'redaitime.png'
                    draw_list(red_ai_time, title, filename1)
                if len(blue_browse) > 0:
                    title = str(ai_blue) + ' Visited Node'
                    filename1 = str(ai_blue) + str(a) + 'bluebrowse.png'
                    draw_list(blue_browse, title, filename1)
                if len(blue_counter) > 0:
                    title = str(ai_blue) + ' Counter'
                    filename1 = str(ai_blue) + str(a) + 'bluecounter.png'
                    draw_list(blue_counter, title, filename1)
                if len(red_ai_time) > 0:
                    title = str(ai_blue) + ' Calculation Time'
                    filename1 = str(ai_blue) + str(a) + 'blueaitime.png'
                    draw_list(blue_ai_time, title, filename1)
    print(ai_red, red_browse, red_counter, red_ai_time, ai_blue, blue_browse, blue_counter, blue_ai_time)




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
