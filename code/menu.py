
import pygame

class Menu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 60)
        self.button_rect = pygame.Rect(400, 350, 200, 80)


    def update(self, dt):
        pass

    def draw(self, surface):
        text = self.font.render("Bamboo Bowl", True, (255,255,255))
        surface.blit(text, (300,200))

        # Button
        pygame.draw.rect(surface, (200, 200, 200), self.button_rect)
        font = pygame.font.Font(None, 60)
        text = self.font.render("START", True, (0,0,0))
        text_rect = text.get_rect(center=self.button_rect.center)
        surface.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.button_rect.collidepoint(event.pos):
                    print("Start clicked!")
                    self.game.state = "GAME"
