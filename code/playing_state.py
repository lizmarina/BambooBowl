import random

import pygame

class PlayingState:
    def __init__(self, game):
        self.game = game
        self.test_text_font = pygame.font.Font(None, 50)
        self.game_area = pygame.Rect(300, 0, 700, 800)
        self.ui_area = pygame.Rect(0, 0, 300, 800) # User interface

        self.coin_timer = 0
        self.next_coin_time = random.uniform(2, 5)

    def update(self, dt):
        self.coin_timer += dt

        if self.coin_timer >= self.next_coin_time:
            print("Spawn coin!")

            self.coin_timer = 0
            self.next_coin_time = random.uniform(2, 5)

    def draw(self, surface):
        text = self.test_text_font.render("GAME RUNNING", True, (255, 255, 255))
        rect = text.get_rect(center=(self.game.WIDTH // 2, self.game.HEIGHT // 2))
        surface.blit(text, rect)

        # fundo geral
        surface.fill((30, 30, 30))
        pygame.draw.rect(surface, (170, 180, 120), self.game_area)
        pygame.draw.rect(surface, (230, 215, 185), self.ui_area)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.state = "MENU"