import pygame

from code.assets import load_assets
from code.menu import Menu
from code.playing_state import PlayingState
from code.instructions_state import InstructionsState
from code.settings import WIDTH, HEIGHT, FPS
from code.settings_state import SettingsState
from code import const
pygame.mixer.init()

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
        self.sounds = {
            "click": pygame.mixer.Sound("./assets/sounds/click_sound.wav"),
            "coin": pygame.mixer.Sound("./assets/sounds/coin_sound.wav"),
            "upgrade": pygame.mixer.Sound("./assets/sounds/shine_sound.wav"),
        }
        self.sounds["click"].set_volume(0.4)
        self.sounds["coin"].set_volume(0.4)
        self.sounds["upgrade"].set_volume(0.3)

        pygame.mixer.music.load("./assets/music/bg_music.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        self.transition_active = False
        self.transition_alpha = 0
        self.transition_speed = 1000
        self.transition_direction = 1
        self.next_state = None

        self.transition_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.transition_color = (60, 30, 10)

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

        if self.transition_active:
            self.transition_alpha += self.transition_speed * dt * self.transition_direction

            if self.transition_direction == 1 and self.transition_alpha >= 255:
                self.transition_alpha = 255

                # troca o state aqui (no escuro)
                self.state = self.next_state

                # começa a clarear
                self.transition_direction = -1

            elif self.transition_direction == -1 and self.transition_alpha <= 0:
                self.transition_alpha = 0
                self.transition_active = False

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

        if self.transition_active:
            self.transition_surface.fill(self.transition_color)
            self.transition_surface.set_alpha(int(self.transition_alpha))
            self.window.blit(self.transition_surface, (0, 0))

        pygame.display.flip()

    def change_state(self, new_state):
        if self.transition_active:
            return

        self.transition_active = True
        self.transition_direction = 1
        self.transition_alpha = 0
        self.next_state = new_state
