import random

import pygame

class PlayingState:
    def __init__(self, game):
        self.game = game

        self.game_area = pygame.Rect(300, 0, 700, 800)
        self.ui_area = pygame.Rect(0, 0, 300, 800) # User interface
        self.UI_PADDING_X = 23
        self.UI_PADDING_TOP = 85
        self.UI_GAP_Y = 18

        self.ui_inner = pygame.Rect(
            self.ui_area.left + self.UI_PADDING_X,
            self.ui_area.top + self.UI_PADDING_TOP,
            self.ui_area.width - self.UI_PADDING_X * 2,
            self.ui_area.height - self.UI_PADDING_TOP * 2)

        self.money_font = pygame.font.Font(None, 50)
        self.popup_font = pygame.font.Font(None, 36)
        self.ui_font = pygame.font.Font(None, 28)

        self.money = 0

        self.tip_img = self.game.assets["tip"]
        self.coin_img = self.game.assets["coin"]
        self.up1_img = self.game.assets["up_button1"]

        self.cabin_img = self.game.assets["cabin1"]
        self.cabin_rect = self.cabin_img.get_rect(center=(self.game_area.centerx, self.game_area.centery))
        self.click_value = 1

        self.tip_timer = 0.0
        self.next_tip_time = random.uniform(2, 5)
        self.tips = []

        self.popups = []
        self.popup_lifetime = 0.8

        self.up1_level = 0
        self.up1_max = 4
        self.up1_base_cost = 10

        self.upgrade_indicators = [
            self.game.assets["upgrade0"],
            self.game.assets["upgrade1"],
            self.game.assets["upgrade2"],
            self.game.assets["upgrade3"],
            self.game.assets["upgrade4"],
        ]

        self.money_pos = (self.ui_inner.left, self.ui_inner.top)
        self.up1_rect = self.up1_img.get_rect(topleft=(self.ui_inner.left, self.ui_inner.top + 70))

    def up1_cost(self) -> int:
        return self.up1_base_cost * (self.up1_level + 1)

    def spawn_tip(self):
        margin = 68
        x = random.randint(self.game_area.left + margin, self.game_area.right - margin)
        y = random.randint(self.game_area.top + margin, self.game_area.bottom - margin)
        tip_rect = self.tip_img.get_rect(center=(x,y))
        self.tips.append(tip_rect)

    def create_popup(self, x, y, value):
        self.popups.append({
            "x": x,
            "y": y,
            "value": value,
            "life": self.popup_lifetime,
            "max_life": self.popup_lifetime,
        })

    def update(self, dt: float):
        self.tip_timer += dt
        if self.tip_timer >= self.next_tip_time:
            self.spawn_tip()
            self.tip_timer = 0.0
            self.next_tip_time = random.uniform(2, 5)
        for p in self.popups:
            p["y"] -= 60 * dt  # makes the popup go upwards
            p["life"] -= dt  # make the tips desapear after a certain time

        self.popups = [p for p in self.popups if p["life"] > 0]

    def draw(self, surface):
        surface.blit(self.game.assets["game_background"], (0, 0))

        surface.blit(self.cabin_img, self.cabin_rect)

        for tip_rect in self.tips:
            surface.blit(self.tip_img, tip_rect)

        surface.blit(self.up1_img, self.up1_rect)

        indicator_img = self.upgrade_indicators[self.up1_level]
        indicator_rect = indicator_img.get_rect(
            midleft=(self.up1_rect.right + 12, self.up1_rect.centery))
        surface.blit(indicator_img, indicator_rect)

        if self.up1_level < self.up1_max:
            cost_surf = self.ui_font.render(f"Cost: ¥{self.up1_cost()}", True, (0, 0, 0))
        else:
            cost_surf = self.ui_font.render("MAX", True, (0, 0, 0))

        cost_rect = cost_surf.get_rect(topleft=(self.up1_rect.left, self.up1_rect.bottom + 8))
        surface.blit(cost_surf, cost_rect)

        money_surf = self.money_font.render(f"¥{self.money}", True, (0, 0, 0))
        money_rect = money_surf.get_rect(topleft=self.money_pos)
        surface.blit(money_surf, money_rect)

        for p in self.popups:
            ratio = max(0.0, p["life"] / p["max_life"])  # 1 -> 0
            alpha = int(255 * ratio)

            coin_rect = self.coin_img.get_rect(center=(p["x"], p["y"]))
            coin_surf = self.coin_img.copy()
            coin_surf.set_alpha(alpha)
            surface.blit(coin_surf, coin_rect)

            txt_surf = self.popup_font.render(f"+¥{p['value']}", True, (0, 0, 0))
            txt_surf.set_alpha(alpha)
            txt_rect = txt_surf.get_rect(midleft=(coin_rect.right + 6, coin_rect.centery))
            surface.blit(txt_surf, txt_rect)

            pygame.draw.rect(surface, (255, 0, 0), self.ui_area, 2)  # contorno UI
            pygame.draw.rect(surface, (0, 0, 255), self.ui_inner, 2)  # contorno UI interna
            pygame.draw.rect(surface, (0, 255, 0), self.up1_rect, 2)  # contorno botão

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.state = "MENU"
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            if self.up1_rect.collidepoint(pos):
                if self.up1_level < self.up1_max:
                    cost = self.up1_cost()
                    if self.money >= cost:
                        self.money -= cost
                        self.up1_level += 1
                        self.click_value += 1
                        # feedback visual opcional:
                        self.create_popup(self.up1_rect.centerx, self.up1_rect.centery, 0)
                return

            for i in range(len(self.tips) - 1, -1, -1):
                if self.tips[i].collidepoint(pos):
                    self.tips.pop(i)
                    tip_value = 5
                    self.money += tip_value
                    self.create_popup(pos[0], pos[1], tip_value)
                    return

            if self.cabin_rect.collidepoint(pos):
                self.money += self.click_value
                self.create_popup(pos[0], pos[1], self.click_value)
                return