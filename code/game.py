import pygame

from code.assets import load_assets
from code.menu import Menu
from code.playing_state import PlayingState
from code.instructions_state import InstructionsState
from code.settings import WIDTH, HEIGHT, FPS
from code.settings_state import SettingsState
from code import const


class Game:
    def __init__(self):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        pygame.display.set_caption("Bamboo Bowl")
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.clock = pygame.time.Clock()
        self.running = True

        self.assets = load_assets()
        self.state = "MENU"
        self.menu = Menu(self)
        self.playing_state = PlayingState(self)
        self.settings_state = SettingsState(self)
        self.instructions_state = InstructionsState(self)
        self.fps_font = pygame.font.Font(None, 28)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000 # delta time

            self.events()
            self.update(dt)
            self.draw()

        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == "MENU":
                self.menu.handle_event(event)
            elif self.state == "GAME":
                self.playing_state.handle_event(event)
            elif self.state == "SETTINGS":
                self.settings_state.handle_event(event)
            elif self.state == "INSTRUCTIONS":
                self.instructions_state.handle_event(event)

    def update(self, dt):
        if self.state == "MENU":
            self.menu.update(dt)
        elif self.state == "GAME":
            self.playing_state.update(dt)
        elif self.state == "SETTINGS":
            self.settings_state.update(dt)
        elif self.state == "INSTRUCTIONS":
            self.instructions_state.update(dt)

    def draw(self):
        self.window.fill((30, 30, 30))

        if self.state == "MENU":
            self.menu.draw(self.window)
        elif self.state == "GAME":
            self.playing_state.draw(self.window)
        elif self.state == "SETTINGS":
            self.settings_state.draw(self.window)
        elif self.state == "INSTRUCTIONS":
            self.instructions_state.draw(self.window)

        if const.SHOW_FPS:
            fps = int(self.clock.get_fps())
            fps_surf = self.fps_font.render(f"FPS: {fps}", True, (255, 255, 255))
            self.window.blit(fps_surf, (10, 10))

        pygame.display.flip()

