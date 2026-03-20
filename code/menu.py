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
        self.instructions_button = self.game.assets["instructions_button"]
        self.exit_button = self.game.assets["exit_button"]

        self.start_rect = self.start_button.get_rect(center=(centerx, y_start))

        y = self.start_rect.bottom + gap + (self.settings_button.get_height() // 2)
        self.settings_rect = self.settings_button.get_rect(center=(centerx, y))

        y = self.settings_rect.bottom + gap + (self.instructions_button.get_height() // 2)
        self.instructions_rect = self.instructions_button.get_rect(center=(centerx, y))

        y = self.instructions_rect.bottom + gap + (self.exit_button.get_height() // 2)
        self.exit_rect = self.exit_button.get_rect(center=(centerx, y))

        self.pressed_button = None
        self.current_cursor = pygame.SYSTEM_CURSOR_ARROW

    def get_hovered_button(self, pos):
        if self.start_rect.collidepoint(pos):
            return "start"
        if self.settings_rect.collidepoint(pos):
            return "settings"
        if self.instructions_rect.collidepoint(pos):
            return "instructions"
        if self.exit_rect.collidepoint(pos):
            return "exit"
        return None

    def get_draw_rect(self, name, rect):
        if self.pressed_button == name:
            return rect.move(0, 2)
        return rect

    def update_cursor(self):
        hovered = self.get_hovered_button(pygame.mouse.get_pos())
        wanted_cursor = pygame.SYSTEM_CURSOR_HAND if hovered else pygame.SYSTEM_CURSOR_ARROW

        if wanted_cursor != self.current_cursor:
            pygame.mouse.set_cursor(wanted_cursor)
            self.current_cursor = wanted_cursor

    def update(self, dt):
        self.update_cursor()

    def draw(self, surface):
        surface.blit(self.game.assets["menu_background"], (0, 0))

        start_draw_rect = self.get_draw_rect("start", self.start_rect)
        settings_draw_rect = self.get_draw_rect("settings", self.settings_rect)
        instructions_draw_rect = self.get_draw_rect("instructions", self.instructions_rect)
        exit_draw_rect = self.get_draw_rect("exit", self.exit_rect)

        # Button
        surface.blit(self.start_button, start_draw_rect)
        surface.blit(self.settings_button, settings_draw_rect)
        surface.blit(self.instructions_button, instructions_draw_rect)
        surface.blit(self.exit_button, exit_draw_rect)

    def handle_button_action(self, button_name):
        self.game.sounds["click"].play()

        if button_name == "start":
            self.game.state = "GAME"
            return
        if button_name == "settings":
            self.game.state = "SETTINGS"
            return
        if button_name == "instructions":
            self.game.state = "INSTRUCTIONS"
            return
        if button_name == "exit":
            self.game.running = False
            return

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_button = self.get_hovered_button(event.pos)
            if clicked_button:
                self.pressed_button = clicked_button
                return

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed_button:
                released_over = self.get_hovered_button(event.pos)

                if released_over == self.pressed_button:
                    self.handle_button_action(self.pressed_button)
                self.pressed_button = None


