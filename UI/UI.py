import pygame

WIDTH = 640
HEIGHT = 480
HEIGHT_BOX = 50
WIDTH_BOX = 400
NUMBER_DEPTH = 16
WIDTH_PER_BOX = WIDTH_BOX // NUMBER_DEPTH

class SimpleScene:
    def __init__(self, text):
        self.background = pygame.Surface((WIDTH, HEIGHT))
        bg = pygame.transform.scale(pygame.image.load("UI/image/bg.png"), (WIDTH, HEIGHT))
        self.background.blit(bg, (-1, 0))
        self.text = text

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        font = pygame.font.Font('UI/font/iCielBCDDCHardwareRough-Compressed.ttf', 80)
        text = font.render(self.text, True, pygame.Color(144, 8, 8))
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 3)
        screen.blit(text, textRect)
        play = pygame.transform.scale(pygame.image.load("UI/image/start.png"), (
        pygame.image.load("UI/image/start.png").get_width() // 6,
        pygame.image.load("UI/image/start.png").get_height() // 6))
        self.playRect = play.get_rect()
        self.playRect.center = (WIDTH // 2, HEIGHT // 1.5)
        screen.blit(play, self.playRect)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.playRect.collidepoint(event.pos):
                    return ('CHOOSE_MODE')

    def element(self, events):
        pass


class ChooseScene:
    def __init__(self, title, *texts):
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background = pygame.Surface((WIDTH, HEIGHT))
        bg = pygame.transform.scale(pygame.image.load("UI/image/bg.png"), (WIDTH, HEIGHT))
        self.background.blit(bg, (-1, 0))
        self.rects = []
        self.texts = texts
        self.title = title

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        n = 1

        for text in self.texts:
            font = pygame.font.Font('UI/font/iCielBCDDCHardwareRough-Compressed.ttf', 35)
            text = font.render(text, True, pygame.Color(144, 8, 8))
            textRect = text.get_rect()
            textRect.center = (640 // 2, (HEIGHT // 8 + HEIGHT // 5 * n))
            rect = pygame.Rect((WIDTH - WIDTH_BOX) // 2, textRect.top, WIDTH_BOX, HEIGHT_BOX)
            self.rects.append(rect)
            n += 1
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, pygame.Color(120, 200, 112), rect)
            pygame.draw.rect(screen, pygame.Color(120, 8, 8), rect, 5)
            screen.blit(text, textRect)

            font = pygame.font.Font('UI/font/iCielBCDDCHardwareRough-Compressed.ttf', 40)
            text = font.render(self.title, True, pygame.Color(144, 8, 8))
            textRect = text.get_rect()
            textRect.center = (WIDTH // 2, HEIGHT // 6)
            screen.blit(text, textRect)
            play = pygame.transform.scale(pygame.image.load("UI/image/back.png"), (
                pygame.image.load("UI/image/back.png").get_width() // 6,
                pygame.image.load("UI/image/back.png").get_height() // 6))
            self.playRect = play.get_rect()
            self.playRect.center = (WIDTH // 2, HEIGHT // 1.12)
            screen.blit(play, self.playRect)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.playRect.collidepoint(event.pos):
                    return ('TITLE')

    def element(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                n = 1
                for rect in self.rects:
                    if rect.collidepoint(event.pos):
                        if (n == 1):
                            return (True, True)
                        if (n == 2):
                            return (True, False)
                        if (n == 3):
                            return (False, False)
                    n += 1


class ChooseBot:
    def __init__(self, title, *texts):
        self.background = pygame.Surface((WIDTH, HEIGHT))
        bg = pygame.transform.scale(pygame.image.load("UI/image/bg.png"), (WIDTH, HEIGHT))
        self.background.blit(bg, (-1, 0))
        self.rects = []
        self.texts = texts
        self.title = title

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        n = 1

        for text in self.texts:
            font = pygame.font.Font('UI/font/iCielBCDDCHardwareRough-Compressed.ttf', 35)
            text = font.render(text, True, pygame.Color(144, 8, 8))
            textRect = text.get_rect()
            textRect.center = (640 // 2, (HEIGHT // 8 + HEIGHT // 7 * n))
            rect = pygame.Rect((WIDTH - WIDTH_BOX) // 2, textRect.top, WIDTH_BOX, HEIGHT_BOX)
            self.rects.append(rect)
            n += 1
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, pygame.Color(120, 200, 112), rect)
            pygame.draw.rect(screen, pygame.Color(120, 8, 8), rect, 5)
            screen.blit(text, textRect)

        font = pygame.font.Font('UI/font/iCielBCDDCHardwareRough-Compressed.ttf', 40)
        text = font.render(self.title, True, pygame.Color(144, 8, 8))
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 8)
        screen.blit(text, textRect)
        play = pygame.transform.scale(pygame.image.load("UI/image/back.png"), (
            pygame.image.load("UI/image/back.png").get_width() // 6,
            pygame.image.load("UI/image/back.png").get_height() // 6))
        self.playRect = play.get_rect()
        self.playRect.center = (WIDTH // 2, HEIGHT // 1.12)
        screen.blit(play, self.playRect)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.playRect.collidepoint(event.pos):
                    return ('CHOOSE_MODE')

    def element(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                n = 1
                for rect in self.rects:
                    if rect.collidepoint(event.pos):
                        if (n == 1):
                            return 'Negamax'
                        if (n == 2):
                            return 'Negascout'
                        if (n == 3):
                            return 'Minimax'
                        if (n == 4):
                            return 'Greedy'
                    n += 1


class ChooseDepth:
    def __init__(self, title, title_1):
        self.background = pygame.Surface((WIDTH, HEIGHT))
        bg = pygame.transform.scale(pygame.image.load("UI/image/bg.png"), (WIDTH, HEIGHT))
        self.background.blit(bg, (-1, 0))
        self.title = title
        self.mouse_drag = False
        self.title_1 = title_1
        self.offset_x = 0
        self.sau = 0

    def draw(self, screen):
        self.screen = screen
        screen.blit(self.background, (0, 0))

        font = pygame.font.Font('UI/font/iCielBCDDCHardwareRough-Compressed.ttf', 40)
        self.text = font.render(self.title, True, pygame.Color(144, 8, 8))
        self.textRect = self.text.get_rect()
        self.textRect.center = (WIDTH // 2, HEIGHT // 8)
        screen.blit(self.text, self.textRect)

        self.text_1 = font.render(self.title_1, True, pygame.Color(144, 8, 8))
        self.textRect_1 = self.text_1.get_rect()
        self.textRect_1.center = (WIDTH // 2 - 20, HEIGHT // 2.5)
        screen.blit(self.text_1, self.textRect_1)
        self.sau = 0
        self.text_2 = font.render(str(self.sau), True, pygame.Color(144, 8, 8))
        self.textRect_2 = self.text_2.get_rect()
        self.textRect_2.center = (WIDTH // 2 + self.textRect_1.width // 2, HEIGHT // 2.5)
        screen.blit(self.text_2, self.textRect_2)

        self.play = pygame.transform.scale(pygame.image.load("UI/image/back.png"), (
            pygame.image.load("UI/image/back.png").get_width() // 6,
            pygame.image.load("UI/image/back.png").get_height() // 6))
        self.playRect = self.play.get_rect()
        self.playRect.center = (WIDTH // 2 - self.playRect.width -40 , HEIGHT // 1.12)
        screen.blit(self.play, self.playRect)

        self.play_1 = pygame.transform.scale(pygame.image.load("UI/image/next.png"), (
            pygame.image.load("UI/image/next.png").get_width() // 6,
            pygame.image.load("UI/image/next.png").get_height() // 6))
        self.playRect_1 = self.play.get_rect()
        self.playRect_1.center = (WIDTH // 2 + self.playRect_1.width + 30, HEIGHT // 1.12)
        screen.blit(self.play_1, self.playRect_1)

        self.img = pygame.transform.scale(pygame.image.load("UI/image/money.png"), (
            pygame.image.load("UI/image/money.png").get_width() // 6,
            pygame.image.load("UI/image/money.png").get_height() // 6))
        self.rect = pygame.Rect((WIDTH - WIDTH_BOX) // 2, HEIGHT // 1.5 - HEIGHT_BOX // 6, WIDTH_BOX, HEIGHT_BOX // 3)
        pygame.draw.rect(screen, pygame.Color(120, 8, 8), self.rect, 5)
        self.rectimg = self.img.get_rect()
        self.rectimg_min = self.img.get_rect()
        self.rectimg.center = ((WIDTH - WIDTH_BOX) // 2, HEIGHT // 1.5)
        self.rectimg_min.center = ((WIDTH - WIDTH_BOX) // 2, HEIGHT // 1.5)
        screen.blit(self.img, self.rectimg)
        self.rectimg_max = self.img.get_rect()
        self.rectimg_max.center = ((WIDTH + WIDTH_BOX) // 2, HEIGHT // 1.5)
        self.rectimg_min.center = ((WIDTH - WIDTH_BOX) // 2, HEIGHT // 1.5)
        self.rectimg.center = ((WIDTH - WIDTH_BOX) // 2, HEIGHT // 1.5)


        pygame.display.flip()

    def update(self, events):
        self.offset_x = 0
        self.sau = 0
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.rectimg.collidepoint(event.pos):
                            self.mouse_drag = True
                            mouse_x, mouse_y = event.pos
                            self.offset_x = self.rectimg.x - mouse_x
                    if self.playRect.collidepoint(event.pos):
                        return ('CHOOSE_BOT')
                    if self.playRect_1.collidepoint(event.pos):
                        run = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouse_drag = False
                        if (self.rectimg.x < self.rectimg_min.x):
                            self.rectimg.center = ((WIDTH - WIDTH_BOX) // 2, HEIGHT // 1.5)
                        elif (self.rectimg.x > self.rectimg_max.x):
                            self.rectimg.center = ((WIDTH + WIDTH_BOX) // 2, HEIGHT // 1.5)

                elif event.type == pygame.MOUSEMOTION:
                    if self.mouse_drag:
                        mouse_x, mouse_y = event.pos
                        self.rectimg.x = mouse_x + self.offset_x
                        self.screen.blit(self.background, (0, 0))

                        font = pygame.font.Font('UI/font/iCielBCDDCHardwareRough-Compressed.ttf', 40)
                        self.text_1 = font.render(self.title_1, True, pygame.Color(144, 8, 8))
                        self.screen.blit(self.text, self.textRect)
                        self.screen.blit(self.text_1, self.textRect_1)

                        if (self.rectimg.x < self.rectimg_min.x):
                            self.screen.blit(self.img, self.rectimg_min)
                            self.rectbar = pygame.Rect((WIDTH - WIDTH_BOX) // 2, HEIGHT // 1.5 - HEIGHT_BOX // 6,
                                                       self.rectimg_min.x - (WIDTH - WIDTH_BOX) // 2,
                                                       HEIGHT_BOX // 3)
                            pygame.draw.rect(self.screen, pygame.Color(120, 200, 112), self.rectbar)
                            pygame.draw.rect(self.screen, pygame.Color(120, 8, 8), self.rect, 5)
                            self.sau = 0
                            self.screen.blit(self.img, self.rectimg_min)
                        elif (self.rectimg.x > self.rectimg_max.x):
                            self.rectbar = pygame.Rect((WIDTH - WIDTH_BOX) // 2, HEIGHT // 1.5 - HEIGHT_BOX // 6,
                                                       self.rectimg_max.x - (WIDTH - WIDTH_BOX) // 2,
                                                       HEIGHT_BOX // 3)
                            pygame.draw.rect(self.screen, pygame.Color(120, 200, 112), self.rectbar)
                            pygame.draw.rect(self.screen, pygame.Color(120, 8, 8), self.rect, 5)
                            self.sau = NUMBER_DEPTH
                            self.screen.blit(self.img, self.rectimg_max)
                        else:
                            self.rectbar = pygame.Rect((WIDTH - WIDTH_BOX) // 2, HEIGHT // 1.5 - HEIGHT_BOX // 6,
                                                       self.rectimg.x - (WIDTH - WIDTH_BOX) // 2,
                                                       HEIGHT_BOX // 3)
                            pygame.draw.rect(self.screen, pygame.Color(120, 200, 112), self.rectbar)
                            pygame.draw.rect(self.screen, pygame.Color(120, 8, 8), self.rect, 5)
                            self.sau = str(((self.rectimg.x - (WIDTH - WIDTH_BOX) // 2)+self.rectimg.width//2)//WIDTH_PER_BOX)
                            self.screen.blit(self.img, self.rectimg)

                        self.text_2 = font.render(str(self.sau), True, pygame.Color(144, 8, 8))
                        self.textRect_2 = self.text_2.get_rect()
                        self.textRect_2.center = (WIDTH // 2 + self.textRect_1.width // 2, HEIGHT // 2.5)
                        self.screen.blit(self.text_2, self.textRect_2)
                        self.screen.blit(self.play_1, self.playRect_1)
                        self.screen.blit(self.play, self.playRect)
                        pygame.display.flip()
        return True
    def element(self, events):
        return int(self.sau)