import pygame
class Highlight:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 10)
        self.r = None
        self.c = None
        self.r_text = ""
        self.c_text = ""

    def render(self):
        # Display the prompt
        r_prompt = self.font.render("Enter the value of r: ", True, (255, 255, 255))
        c_prompt = self.font.render("Enter the value of c: ", True, (255, 255, 255))
        self.screen.blit(r_prompt, (600, 650))
        self.screen.blit(c_prompt, (600, 700))

        # Display the input boxes
        r_input = self.font.render(self.r_text, True, (255, 255, 255))
        c_input = self.font.render(self.c_text, True, (255, 255, 255))
        self.screen.blit(r_input, (700, 650))
        self.screen.blit(c_input, (700, 700))

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            # Update the input text
            if event.unicode.isdigit():
                if self.r is None:
                    self.r_text += event.unicode
                else:
                    self.c_text += event.unicode
            elif event.key == pygame.K_RETURN:
                # Update the values of r and c
                if self.r is None:
                    self.r = int(self.r_text)
                    self.r_text = ""
                else:
                    self.c = int(self.c_text)
            elif event.key == pygame.K_BACKSPACE:
                # Delete the last character in the input text
                if self.r is None:
                    self.r_text = self.r_text[:-1]
                else:
                    self.c_text = self.c_text[:-1]

    def update(self):
        if self.r is not None and self.c is not None:
            s = pygame.Surface((56, 56))
            s.set_alpha(100)  # transparency value -> 0 transparent; 255 opaque
            s.fill(pygame.Color('blue'))
            self.screen.blit(s, (self.c * 56, self.r * 56))

