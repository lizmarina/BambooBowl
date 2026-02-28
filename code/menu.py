
import pygame


class Menu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 60)

        self.start_button = self.game.assets["start_button"]
        self.start_rect = self.start_button.get_rect(center=(500, 500))

        self.settings_button = self.game.assets["settings_button"]
        self.settings_rect = self.settings_button.get_rect(center=(500, 610))


    def update(self, dt):
        pass

    def draw(self, surface):
        surface.blit(self.game.assets["menu_background"], (0, 0))
        title = self.font.render("Bamboo Bowl", True, (255,255,255))
        title_rect = title.get_rect(center=(500, 180))
        surface.blit(title, title_rect)


        # Button
        surface.blit(self.start_button, self.start_rect)
        surface.blit(self.settings_button, self.settings_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_rect.collidepoint(event.pos):
                    self.game.state = "GAME"
            if self.settings_rect.collidepoint(event.pos):
                self.game.state = "SETTINGS"
