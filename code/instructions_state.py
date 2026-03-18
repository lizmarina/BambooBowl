import pygame


class InstructionsState:
    def __init__(self, game):
        self.game = game

        self.panel = self.game.assets["instructions_panel"]
        self.back_button = self.game.assets["back_button"]

        self.panel_rect = self.panel.get_rect(center=(self.game.WIDTH // 2, self.game.HEIGHT // 2))
        self.back_rect = self.back_button.get_rect(
            midtop=(self.panel_rect.centerx, self.panel_rect.bottom - 110)
        )

        self.pressed_button = None
        self.current_cursor = pygame.SYSTEM_CURSOR_ARROW

    def get_hovered_button(self, pos):
        if self.back_rect.collidepoint(pos):
            return "back"
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
        surface.blit(self.panel, self.panel_rect)

        back_draw_rect = self.get_draw_rect("back", self.back_rect)
        surface.blit(self.back_button, back_draw_rect)

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.state = "MENU"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = self.get_hovered_button(event.pos)
            if clicked:
                self.pressed_button = clicked
                return

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed_button:
                released_over = self.get_hovered_button(event.pos)

                if released_over == self.pressed_button:
                    if self.pressed_button == "back":
                        self.game.state = "MENU"

                self.pressed_button = None
