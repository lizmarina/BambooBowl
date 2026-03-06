import pygame

from code import const


class SettingsState:
    def __init__(self, game):
        self.game = game

        self.panel = self.game.assets["settings_panel"]
        self.back_button = self.game.assets["back_button"]

        self.panel_rect = self.panel.get_rect(center=(self.game.WIDTH // 2, self.game.HEIGHT // 2))

        self.font = pygame.font.Font(None, 40)
        self.title_font = pygame.font.Font(None, 54)

        self.volume_rect = pygame.Rect(
            self.panel_rect.left + 70,
            self.panel_rect.top + 160,
            self.panel_rect.width - 140,
            48,
        )
        self.fps_rect = pygame.Rect(
            self.panel_rect.left + 70,
            self.panel_rect.top + 230,
            self.panel_rect.width - 140,
            48,
        )

        self.reset_rect = pygame.Rect(
            self.panel_rect.left + 70,
            self.panel_rect.top + 300,
            self.panel_rect.width - 140,
            48,
        )
        self.reset_confirm = False

        back_x = self.reset_rect.left + 55
        back_y = self.reset_rect.bottom + 25
        self.back_rect = self.back_button.get_rect(topleft=(back_x, back_y))

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.blit(self.game.assets["menu_background"], (0, 0))
        surface.blit(self.panel, self.panel_rect)
        surface.blit(self.back_button, self.back_rect)


        volume_text = self.font.render(f"Master Volume: {int(const.MASTER_VOLUME * 100)}%", True, (0, 0, 0))
        fps_text = self.font.render(f"Show FPS: {'ON' if const.SHOW_FPS else 'OFF'}", True, (0, 0, 0))
        surface.blit(volume_text, volume_text.get_rect(midleft=(self.volume_rect.left, self.volume_rect.centery)))
        surface.blit(fps_text, fps_text.get_rect(midleft=(self.fps_rect.left, self.fps_rect.centery)))

        if not self.reset_confirm:
            reset_text = self.font.render("Reset Progress", True, (0, 0, 0))
        else:
            reset_text = self.font.render("Click again to confirm", True, (0, 0, 0))
        surface.blit(reset_text, reset_text.get_rect(midleft=(self.reset_rect.left, self.reset_rect.centery)))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.reset_confirm = False
            self.game.state = "MENU"
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            if self.volume_rect.collidepoint(pos):
                self.reset_confirm = False
                levels = [0.0, 0.25, 0.5, 0.75, 1.0]
                current_index = min(range(len(levels)), key=lambda i: abs(levels[i] - const.MASTER_VOLUME))
                const.MASTER_VOLUME = levels[(current_index + 1) % len(levels)]
                if pygame.mixer.get_init():
                    pygame.mixer.music.set_volume(const.MASTER_VOLUME)
                return

            if self.fps_rect.collidepoint(pos):
                self.reset_confirm = False
                const.SHOW_FPS = not const.SHOW_FPS
                print("SHOW_FPS =", const.SHOW_FPS)
                return

            if self.reset_rect.collidepoint(pos):
                if not self.reset_confirm:
                    self.reset_confirm = True
                else:
                    self.game.playing_state.reset_progress()
                    self.reset_confirm = False
                return

            if self.back_rect.collidepoint(pos):
                self.reset_confirm = False
                self.game.state = "MENU"
                return