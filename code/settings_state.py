import pygame

from code import const


class SettingsState:
    def __init__(self, game):
        self.game = game

        self.panel = self.game.assets["settings_panel"]
        self.back_button = self.game.assets["back_button"]

        self.panel_rect = self.panel.get_rect(center=(self.game.WIDTH // 2, self.game.HEIGHT // 2))

        self.font_path = "./assets/Baloo-Regular.ttf"
        self.text_color = (121, 21, 9)
        self.button_color = (220, 205, 175)
        self.button_border_color = (227, 178, 83)
        self.bar_bg_color = (210, 190, 160)
        self.bar_fill_color = (121, 21, 9)

        self.font = self.load_font(30)
        self.small_font = self.load_font(24)
        self.title_font = self.load_font(54)

        self.volume_rect = pygame.Rect(
            self.panel_rect.left + 70,
            self.panel_rect.top + 145,
            self.panel_rect.width - 140,
            78,
        )
        self.fps_rect = pygame.Rect(
            self.panel_rect.left + 70,
            self.panel_rect.top + 240,
            self.panel_rect.width - 140,
            62,
        )
        self.reset_rect = pygame.Rect(
            self.panel_rect.left + 50,
            self.panel_rect.top + 320,
            self.panel_rect.width - 100,
            62,
        )

        self.reset_confirm = False

        back_x = self.reset_rect.left + 75
        back_y = self.reset_rect.bottom + 25
        self.back_rect = self.back_button.get_rect(topleft=(back_x, back_y))

        self.pressed_button = None
        self.current_cursor = pygame.SYSTEM_CURSOR_ARROW

    def load_font(self, size):
        try:
            return pygame.font.Font(self.font_path, size)
        except FileNotFoundError:
            return pygame.font.Font(None, size)

    def get_hovered_button(self, pos):
        if self.volume_rect.collidepoint(pos):
            return "volume"
        if self.fps_rect.collidepoint(pos):
            return "fps"
        if self.reset_rect.collidepoint(pos):
            return "reset"
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

    def draw_volume_button(self, surface, rect, pressed=False):
        draw_rect = rect.move(0, 2) if pressed else rect

        pygame.draw.rect(surface, self.button_color, draw_rect, border_radius=14)
        pygame.draw.rect(surface, self.button_border_color, draw_rect, width=5, border_radius=14)

        label_surf = self.font.render("Master Volume", True, self.text_color)
        label_rect = label_surf.get_rect(center=(draw_rect.centerx, draw_rect.top + 25))
        surface.blit(label_surf, label_rect)

        bar_width = 130
        bar_height = 16
        percent_text = f"{int(const.MASTER_VOLUME * 100)}%"

        percent_surf = self.small_font.render(percent_text, True, self.text_color)
        percent_rect = percent_surf.get_rect(midright=(draw_rect.right - 14, draw_rect.top + 52))
        surface.blit(percent_surf, percent_rect)

        bar_x = draw_rect.left + 18
        bar_y = draw_rect.top + 44
        bar_right_limit = percent_rect.left - 10
        actual_bar_width = bar_right_limit - bar_x

        bar_bg_rect = pygame.Rect(bar_x, bar_y, actual_bar_width, bar_height)
        pygame.draw.rect(surface, self.bar_bg_color, bar_bg_rect, border_radius=8)
        pygame.draw.rect(surface, self.button_border_color, bar_bg_rect, width=2, border_radius=8)

        fill_width = int(actual_bar_width * const.MASTER_VOLUME)
        if fill_width > 0:
            fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
            pygame.draw.rect(surface, self.bar_fill_color, fill_rect, border_radius=8)

    def draw_text_button(self, surface, rect, text, pressed=False):
        draw_rect = rect.move(0, 2) if pressed else rect

        pygame.draw.rect(surface, self.button_color, draw_rect, border_radius=14)
        pygame.draw.rect(surface, self.button_border_color, draw_rect, width=5, border_radius=14)

        text_surf = self.font.render(text, True, self.text_color)
        text_rect = text_surf.get_rect(center=draw_rect.center)
        surface.blit(text_surf, text_rect)

    def draw(self, surface):
        surface.blit(self.game.assets["menu_background"], (0, 0))
        surface.blit(self.panel, self.panel_rect)

        self.draw_volume_button(
            surface,
            self.volume_rect,
            pressed=self.pressed_button == "volume"
        )

        self.draw_text_button(
            surface,
            self.fps_rect,
            f"Show FPS: {'ON' if const.SHOW_FPS else 'OFF'}",
            pressed=self.pressed_button == "fps"
        )

        reset_label = "Reset Progress" if not self.reset_confirm else "Click again to confirm"
        self.draw_text_button(
            surface,
            self.reset_rect,
            reset_label,
            pressed=self.pressed_button == "reset"
        )

        back_draw_rect = self.get_draw_rect("back", self.back_rect)
        surface.blit(self.back_button, back_draw_rect)

    def handle_button_action(self, button_name):
        if button_name == "volume":
            self.reset_confirm = False
            levels = [0.0, 0.25, 0.5, 0.75, 1.0]
            current_index = min(range(len(levels)), key=lambda i: abs(levels[i] - const.MASTER_VOLUME))
            const.MASTER_VOLUME = levels[(current_index + 1) % len(levels)]
            if pygame.mixer.get_init():
                pygame.mixer.music.set_volume(const.MASTER_VOLUME)
            return

        if button_name == "fps":
            self.reset_confirm = False
            const.SHOW_FPS = not const.SHOW_FPS
            print("SHOW_FPS =", const.SHOW_FPS)
            return

        if button_name == "reset":
            if not self.reset_confirm:
                self.reset_confirm = True
            else:
                self.game.playing_state.reset_progress()
                self.reset_confirm = False
            return

        if button_name == "back":
            self.reset_confirm = False
            self.game.state = "MENU"
            return

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.reset_confirm = False
            self.game.state = "MENU"
            return

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