import pygame


class Menu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 60)

        centerx = self.game.WIDTH // 2
        y_start = 410
        gap = 10

        self.start_button = self.game.assets["start_button"]
        self.settings_button = self.game.assets["settings_button"]
        self.instructions_button = self.game.assets.get(
            "instructions_button",
            self.game.assets.get("reset_button", self.settings_button),
        )
        self.exit_button = self.game.assets["exit_button"]

        self.start_rect = self.start_button.get_rect(center=(centerx, y_start))

        y = self.start_rect.bottom + gap + (self.settings_button.get_height() // 2)
        self.settings_rect = self.settings_button.get_rect(center=(centerx, y))

        y = self.settings_rect.bottom + gap + (self.instructions_button.get_height() // 2)
        self.instructions_rect = self.instructions_button.get_rect(center=(centerx, y))

        y = self.instructions_rect.bottom + gap + (self.exit_button.get_height() // 2)
        self.exit_rect = self.exit_button.get_rect(center=(centerx, y))

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.blit(self.game.assets["menu_background"], (0, 0))

        # Button
        surface.blit(self.start_button, self.start_rect)
        surface.blit(self.settings_button, self.settings_rect)
        surface.blit(self.instructions_button, self.instructions_rect)
        surface.blit(self.exit_button, self.exit_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_rect.collidepoint(event.pos):
                self.game.state = "GAME"
                return
            if self.settings_rect.collidepoint(event.pos):
                self.game.state = "SETTINGS"
                return
            if self.instructions_rect.collidepoint(event.pos):
                self.game.state = "INSTRUCTIONS"
                return
            if self.exit_rect.collidepoint(event.pos):
                self.game.running = False
                return



