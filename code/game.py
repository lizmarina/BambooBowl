
import pygame
from code.menu import Menu
from code.playing_state import PlayingState

class Game:
    def __init__(self):
        self.WIDTH = 1000
        self.HEIGHT = 800
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Bamboo Bowl")

        self.clock = pygame.time.Clock()
        self.running = True

        self.state = "MENU"
        self.menu = Menu(self)
        self.playing_state = PlayingState(self)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000 # delta time

            self.events()
            self.update(dt)
            self.draw()

        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "GAME"

            if self.state == "MENU":
                self.menu.handle_event(event)
            elif self.state == "GAME":
                self.playing_state.handle_event(event)

    def update(self, dt):
        if self.state == "MENU":
            self.menu.update(dt)
        elif self.state == "GAME":
            self.playing_state.update(dt)

    def draw(self):
        self.window.fill((30, 30, 30))

        if self.state == "MENU":
            self.menu.draw(self.window)
        elif self.state == "GAME":
            self.playing_state.draw(self.window)

        pygame.display.flip()
