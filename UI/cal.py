import pygame

WIDTH = 832
HEIGHT = 704
WIDTH_CAL = 256
HEIGHT_CAL = 256


class Calculation:
    def __init__(self):
        self.cal_num_1 = 0
        self.cal_num_2 = 0
        self.cal_1 = False
        self.cal_2 = False
        self.board = [
            ["r0", "r1", "r2", "r3", "r4"],
            ["r5", "r6", "r7", "r8", "r9"]]

    def draw_caltable(self, screen, events, IMAGES):
        sub_screen1 = pygame.Surface((WIDTH_CAL, HEIGHT_CAL))
        sub_screen1.fill((166, 230, 151))
        screen.blit(sub_screen1, (WIDTH - WIDTH_CAL, (HEIGHT - HEIGHT_CAL) // 2))
        title = 'Tính nước bắt quân:'
        title_1 = 'Quân đứng trước:'
        title_2 = 'Quân đứng sau:'
        font = pygame.font.Font('UI/font/iCielBCDDCHardwareRough-Compressed.ttf', 30)
        text = font.render(title, True, pygame.Color(144, 8, 8))
        font = pygame.font.Font('UI/font/iCielBCDDCHardwareRough-Compressed.ttf', 18)
        text_1 = font.render(title_1, True, pygame.Color(144, 8, 8))
        text_2 = font.render(title_2, True, pygame.Color(144, 8, 8))
        textRect = text.get_rect()
        textRect_1 = text_1.get_rect()
        textRect_2 = text_2.get_rect()
        textRect.midtop = (WIDTH - WIDTH_CAL // 2, (HEIGHT - HEIGHT_CAL) // 2)
        textRect_1.midtop = (WIDTH - WIDTH_CAL // 4 * 3, (HEIGHT - HEIGHT_CAL) // 2 + 50)
        textRect_2.midtop = (WIDTH - WIDTH_CAL // 4, (HEIGHT - HEIGHT_CAL) // 2 + 50)
        screen.blit(text, textRect)
        screen.blit(text_1, textRect_1)
        screen.blit(text_2, textRect_2)
        b_str_1 = 'r' + str(self.cal_num_1)
        b_str_2 = 'r' + str(self.cal_num_2)
        img1 = IMAGES[b_str_1]
        img2 = IMAGES[b_str_2]
        textimg_1 = img1.get_rect()
        textimg_2 = img2.get_rect()
        textimg_1.midtop = (WIDTH - WIDTH_CAL // 4 * 3, (HEIGHT - HEIGHT_CAL) // 2 + 80)
        textimg_2.midtop = (WIDTH - WIDTH_CAL // 4, (HEIGHT - HEIGHT_CAL) // 2 + 80)
        screen.blit(img1, textimg_1)
        screen.blit(img2, textimg_2)
        rect = pygame.Rect(WIDTH - WIDTH_CAL, (HEIGHT - HEIGHT_CAL) // 2 + 140, WIDTH_CAL, WIDTH_CAL // 5 * 2)

        title_3 = str(self.cal_num_2) + ' + ' + str(self.cal_num_1) + ' = ' + str(
            (self.cal_num_2 + self.cal_num_1) % 10)
        title_4 = str(self.cal_num_2) + ' - ' + str(self.cal_num_1) + ' = ' + str(self.cal_num_2 - self.cal_num_1)
        title_5 = str(self.cal_num_2) + ' * ' + str(self.cal_num_1) + ' = ' + str(
            (self.cal_num_2 * self.cal_num_1) % 10)
        if self.cal_num_1 == 0:
            title_6 = str(self.cal_num_2) + ' / ' + str(self.cal_num_1) + ' = NaN'
            title_7 = str(self.cal_num_2) + ' % ' + str(self.cal_num_1) + ' = NaN'
        else:
            title_6 = str(self.cal_num_2) + ' / ' + str(self.cal_num_1) + ' = ' + str(self.cal_num_2 // self.cal_num_1)
            title_7 = str(self.cal_num_2) + ' % ' + str(self.cal_num_1) + ' = ' + str(self.cal_num_2 % self.cal_num_1)
        font = pygame.font.Font('UI/font/iCielBCDDCHardwareRough-Compressed.ttf', 20)
        font_1 = pygame.font.Font('UI/font/iCielBCDDCHardwareRough-Compressed.ttf', 24)

        if self.cal_2 or self.cal_1:
            if self.cal_1:
                r = self.cal_num_1 % 5
                c = self.cal_num_1 // 5
                sub_screen2 = pygame.Surface((WIDTH_CAL // 5, HEIGHT_CAL // 5))
                sub_screen2.fill((40, 130, 214))
                screen.blit(sub_screen2, (
                WIDTH - WIDTH_CAL + r * WIDTH_CAL // 5, (HEIGHT - HEIGHT_CAL) // 2 + 140 + c * WIDTH_CAL // 5))
            if self.cal_2:
                r = self.cal_num_2 % 5
                c = self.cal_num_2 // 5
                sub_screen2 = pygame.Surface((WIDTH_CAL // 5, HEIGHT_CAL // 5))
                sub_screen2.fill((40, 130, 214))
                screen.blit(sub_screen2, (
                WIDTH - WIDTH_CAL + r * WIDTH_CAL // 5, (HEIGHT - HEIGHT_CAL) // 2 + 140 + c * WIDTH_CAL // 5))
            if rect.collidepoint(pygame.mouse.get_pos()):
                r = (pygame.mouse.get_pos()[0] - WIDTH + WIDTH_CAL) // (WIDTH_CAL // 5)
                c = (pygame.mouse.get_pos()[1] - ((HEIGHT - HEIGHT_CAL) // 2 + 140)) // (WIDTH_CAL // 5)
                sub_screen3 = pygame.Surface((WIDTH_CAL // 5, HEIGHT_CAL // 5))
                sub_screen3.fill((244, 232, 164))
                screen.blit(sub_screen3, (
                WIDTH - WIDTH_CAL + r * WIDTH_CAL // 5, (HEIGHT - HEIGHT_CAL) // 2 + 140 + c * WIDTH_CAL // 5))

            pygame.draw.rect(screen, pygame.Color(120, 8, 8), rect, 2)
            pygame.draw.line(screen, pygame.Color(120, 8, 8),
                             (WIDTH - WIDTH_CAL, (HEIGHT - HEIGHT_CAL) // 2 + 140 + WIDTH_CAL // 5), (
                                 WIDTH,
                                 (HEIGHT - HEIGHT_CAL) // 2 + 140 + WIDTH_CAL // 5), 2)
            for i in range(4):
                pygame.draw.line(screen, pygame.Color(120, 8, 8),
                                 (WIDTH - WIDTH_CAL + WIDTH_CAL // 5 * (i + 1), (HEIGHT - HEIGHT_CAL) // 2 + 140), (
                                 WIDTH - WIDTH_CAL + WIDTH_CAL // 5 * (i + 1),
                                 (HEIGHT - HEIGHT_CAL) // 2 + HEIGHT_CAL // 5 * 2 + 138), 2)
            for r in range(2):
                for c in range(5):
                    piece = self.board[r][c]
                    rect = pygame.Rect(c * HEIGHT_CAL // 5 + 8 + WIDTH - WIDTH_CAL,
                                       r * HEIGHT_CAL // 5 + 8 + (HEIGHT - HEIGHT_CAL) // 2 + 140, HEIGHT_CAL // 5,
                                       HEIGHT_CAL // 5)
                    screen.blit(pygame.transform.scale(IMAGES[piece], (WIDTH_CAL // 7, WIDTH_CAL // 7)), rect)
        else:
            if self.cal_num_1 + self.cal_num_2 > 0 and self.cal_num_1 + self.cal_num_2 == 10:
                text_3 = font_1.render(title_3, True, pygame.Color(212, 88, 88))
            else:
                text_3 = font.render(title_3, True, pygame.Color(144, 8, 8))
            textRect_3 = text_3.get_rect()
            textRect_3.midtop = (WIDTH - WIDTH_CAL // 2, (HEIGHT - HEIGHT_CAL) // 2 + 130)
            screen.blit(text_3, textRect_3)

            if self.cal_num_2 - self.cal_num_1 > 0:
                text_4 = font_1.render(title_4, True, pygame.Color(212, 88, 88))
            else:
                text_4 = font.render(title_4, True, pygame.Color(144, 8, 8))
            textRect_4 = text_4.get_rect()
            textRect_4.midtop = (WIDTH - WIDTH_CAL // 2, (HEIGHT - HEIGHT_CAL) // 2 + 152)
            screen.blit(text_4, textRect_4)

            if self.cal_num_1 * self.cal_num_2 > 0:
                text_5 = font_1.render(title_5, True, pygame.Color(212, 88, 88))
            else:
                text_5 = font.render(title_5, True, pygame.Color(144, 8, 8))
            textRect_5 = text_5.get_rect()
            textRect_5.midtop = (WIDTH - WIDTH_CAL // 2, (HEIGHT - HEIGHT_CAL) // 2 + 174)
            screen.blit(text_5, textRect_5)

            if self.cal_num_1 != 0:
                if self.cal_num_2 / self.cal_num_1 >= 1:
                    text_6 = font_1.render(title_6, True, pygame.Color(212, 88, 88))
                else:
                    text_6 = font.render(title_6, True, pygame.Color(144, 8, 8))
            else:
                text_6 = font.render(title_6, True, pygame.Color(144, 8, 8))
            textRect_6 = text_6.get_rect()
            textRect_6.midtop = (WIDTH - WIDTH_CAL // 2, (HEIGHT - HEIGHT_CAL) // 2 + 196)
            screen.blit(text_6, textRect_6)
            if self.cal_num_1 != 0:
                if self.cal_num_2 % self.cal_num_1 > 0:
                    text_7 = font_1.render(title_7, True, pygame.Color(212, 88, 88))
                else:
                    text_7 = font.render(title_7, True, pygame.Color(144, 8, 8))
            else:
                text_7 = font.render(title_7, True, pygame.Color(144, 8, 8))
            textRect_7 = text_7.get_rect()
            textRect_7.midtop = (WIDTH - WIDTH_CAL // 2, (HEIGHT - HEIGHT_CAL) // 2 + 218)
            screen.blit(text_7, textRect_7)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if textimg_1.collidepoint(event.pos):
                    if self.cal_2:
                        self.cal_2 = False
                    if not self.cal_1:
                        self.cal_1 = True
                    else:
                        self.cal_1 = False
                if textimg_2.collidepoint(event.pos):
                    if self.cal_1:
                        self.cal_1 = False
                    if not self.cal_2:
                        self.cal_2 = True
                    else:
                        self.cal_2 = False
                r = (pygame.mouse.get_pos()[0] - WIDTH + WIDTH_CAL) // (WIDTH_CAL // 5)
                c = (pygame.mouse.get_pos()[1] - ((HEIGHT - HEIGHT_CAL) // 2 + 140)) // (WIDTH_CAL // 5)
                if r >= 0 and r <= 4 and c >= 0 and c <= 1:
                    if self.cal_1:
                        self.cal_num_1 = c * 5 + r
                        self.cal_1 = False
                    if self.cal_2:
                        self.cal_num_2 = c * 5 + r
                        self.cal_2 = False
