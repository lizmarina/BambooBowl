import pygame

class SettingsState:
    def __init__(self, game):
        self.game = game

        self.panel = self.game.assets["settings_panel"]
        self.back_button = self.game.assets["back_button"]

        self.panel_rect = self.panel.get_rect(center=(self.game.WIDTH // 2, self.game.HEIGHT // 2))
        self.back_rect = self.back_button.get_rect(topleft=(20, 20))

        self.font = pygame.font.Font(None, 40)

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.blit(self.game.assets["menu_background"], (0, 0))
        surface.blit(self.panel, self.panel_rect)
        surface.blit(self.back_button, self.back_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_rect.collidepoint(event.pos):
                self.game.state = "MENU"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.state = "MENU"