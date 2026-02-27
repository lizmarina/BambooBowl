import random
from typing import Self

import pygame
from code.const import WIDTH, HEIGHT, UP_HUB_RECT, GAME_AREA_RECT, MONEY_POS, TIP_VALUE, TIP_MAX_ON_SCREEN, \
    TIP_SPAWN_MIN, TIP_SPAWN_MAX, POPUP_LIFETIME, POPUP_SPEED, UP1_BASE_COST, UP_MAX_LEVEL, TIP_AUTO_TIME, \
    UP2_BASE_COST, UP3_BASE_COST, TIP_SPAWN_REDUCTION


class PlayingState:
    def __init__(self, game):

        self.game = game
        self.up_hub = pygame.Rect(UP_HUB_RECT)
        self.game_area = pygame.Rect(GAME_AREA_RECT)

        self.money_font = pygame.font.Font(None, 50)
        self.popup_font = pygame.font.Font(None, 36)
        self.ui_font = pygame.font.Font(None, 28)

        self.money = 0
        self.gain_accum = 0
        self.gain_timer = 0
        self.money_per_sec = 0

        self.tip_img = self.game.assets["tip"]
        self.coin_img = self.game.assets["coin"]
        self.back_img = self.game.assets["back_button"]
        self.up1_img = self.game.assets["up_button1"]
        self.up2_img = self.game.assets["up_button2"]
        self.up3_img = self.game.assets["up_button3"]

        self.cabin_img = self.game.assets["cabin1"]
        self.cabin_rect = self.cabin_img.get_rect(topleft =(self.game_area.left, self.game_area.top))
        self.click_value = 1

        self.tip_timer = 0.0
        self.tips = []
        self.popups = []
        self.up1_level = 0
        self.up2_level = 0
        self.up3_level = 0
        self.next_tip_time = self.current_tip_spawn_time()

        self.upgrade_indicators = [
            self.game.assets["upgrade0"],
            self.game.assets["upgrade1"],
            self.game.assets["upgrade2"],
            self.game.assets["upgrade3"],
            self.game.assets["upgrade4"],
        ]

        self.money_pos = MONEY_POS
        self.up1_rect = self.up1_img.get_rect(topleft=(self.up_hub.left + 10, self.up_hub.top + 90))
        self.up2_rect = self.up2_img.get_rect(topleft=(self.up_hub.left + 10, self.up_hub.top + 205))
        self.up3_rect = self.up3_img.get_rect(topleft=(self.up_hub.left + 10, self.up_hub.top + 315))
        self.back_rect = self.back_img.get_rect(topleft=(30, 28))



    def up1_cost(self) -> int:
        return UP1_BASE_COST * (self.up1_level + 1)

    def up2_cost(self) -> int:
        return UP2_BASE_COST * (self.up2_level + 1)

    def up3_cost(self) -> int:
        return UP3_BASE_COST * (self.up3_level + 1)



    def spawn_tip(self):
        if len(self.tips) >= TIP_MAX_ON_SCREEN:
            return
        margin = 17
        x = random.randint(self.cabin_rect.left + margin, self.cabin_rect.right - margin)
        y = random.randint(self.cabin_rect.top + margin, self.cabin_rect.bottom - margin)
        tip_rect = self.tip_img.get_rect(center=(x,y))
        self.tips.append({"rect": tip_rect,
                          "tat": TIP_AUTO_TIME})

    def create_popup(self, x, y, value):
        self.popups.append({
            "x": x,
            "y": y,
            "value": value,
            "life": POPUP_LIFETIME,
            "max_life": POPUP_LIFETIME,
        })

    def tip_value(self):
        return TIP_VALUE + (self.up2_level * 2)


    def current_tip_spawn_time(self):
        min_time = TIP_SPAWN_MIN - (self.up3_level * TIP_SPAWN_REDUCTION)
        max_time = TIP_SPAWN_MAX - (self.up3_level * TIP_SPAWN_REDUCTION)
        return random.uniform(min_time, max_time)


    def update(self, dt: float):
        self.tip_timer += dt
        if self.tip_timer >= self.next_tip_time:
            self.spawn_tip()
            self.tip_timer = 0.0
            self.next_tip_time = self.current_tip_spawn_time()


        for p in self.popups:
            p["y"] -= POPUP_SPEED * dt  # makes the popup go upwards
            p["life"] -= dt  # make the tips desapear after a certain time
        self.popups = [p for p in self.popups if p["life"] > 0]

        for t in self.tips:
            t["tat"] -= dt

        for i in range(len(self.tips)-1, -1, -1):
            if self.tips[i]["tat"] <= 0:
                value = self.tip_value()
                self.money += value
                self.gain_accum += value
                r = self.tips[i]["rect"]
                self.create_popup(r.centerx, r.centery, value)
                self.tips.pop(i)

        self.gain_timer += dt
        if self.gain_timer >= 1.0:
            self.money_per_sec = self.gain_accum
            self.gain_accum = 0
            self.gain_timer = 0



    def draw(self, surface):
        surface.blit(self.game.assets["game_background"], (0, 0))
        surface.blit(self.cabin_img, self.cabin_rect)


        for t in self.tips:
            surface.blit(self.tip_img, t["rect"])


        surface.blit(self.up1_img, self.up1_rect)

        indicator_img = self.upgrade_indicators[self.up1_level]
        indicator_rect = indicator_img.get_rect(topleft= (self.up1_rect.left + 80, self.up1_rect.top + 30))
        surface.blit(indicator_img, indicator_rect)

        if self.up1_level < UP_MAX_LEVEL:
            cost_surf = self.ui_font.render(f"Cost: ¥{self.up1_cost()}", True, (0, 0, 0))
        else:
            cost_surf = self.ui_font.render("MAX", True, (0, 0, 0))

        cost_rect = cost_surf.get_rect(topleft=(self.up1_rect.left, self.up1_rect.bottom + 8))
        surface.blit(cost_surf, cost_rect)


        surface.blit(self.up2_img, self.up2_rect)

        indicator2_img = self.upgrade_indicators[self.up2_level]
        indicator2_rect = indicator2_img.get_rect(topleft= (self.up2_rect.left + 80, self.up2_rect.top + 30))
        surface.blit(indicator2_img, indicator2_rect)

        if self.up2_level < UP_MAX_LEVEL:
            cost2_surf = self.ui_font.render(f"Cost: ¥{self.up2_cost()}", True, (0, 0, 0))
        else:
            cost2_surf = self.ui_font.render("MAX", True, (0, 0, 0))

        cost2_rect = cost2_surf.get_rect(topleft=(self.up2_rect.left, self.up2_rect.bottom + 8))
        surface.blit(cost2_surf, cost2_rect)


        surface.blit(self.up3_img, self.up3_rect)

        indicator3_img = self.upgrade_indicators[self.up3_level]
        indicator3_rect = indicator3_img.get_rect(topleft= (self.up3_rect.left + 80, self.up3_rect.top + 30))
        surface.blit(indicator3_img, indicator3_rect)

        if self.up3_level < UP_MAX_LEVEL:
            cost3_surf = self.ui_font.render(f"Cost: ¥{self.up3_cost()}", True, (0, 0, 0))
        else:
            cost3_surf = self.ui_font.render("MAX", True, (0, 0, 0))

        cost3_rect = cost3_surf.get_rect(topleft=(self.up3_rect.left, self.up3_rect.bottom + 8))
        surface.blit(cost3_surf, cost3_rect)


        money_surf = self.money_font.render(f"¥{self.money}", True, (0, 0, 0))
        money_rect = money_surf.get_rect(topleft=self.money_pos)
        surface.blit(money_surf, money_rect)
        mps = self.ui_font.render(f"{self.money_per_sec} ¥/s", True, (0, 0, 0))
        surface.blit(mps, (self.money_pos[0], self.money_pos[1] + 40))


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

        surface.blit(self.back_img, self.back_rect)



    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.state = "MENU"
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            if self.up1_rect.collidepoint(pos):
                if self.up1_level < UP_MAX_LEVEL:
                    cost = self.up1_cost()
                    if self.money >= cost:
                        self.money -= cost
                        self.up1_level += 1
                        self.click_value += 1

                return

            if self.up2_rect.collidepoint(pos):
                if self.up2_level < UP_MAX_LEVEL:
                    cost = self.up2_cost()
                    if self.money >= cost:
                        self.money -= cost
                        self.up2_level += 1

                return

            if self.up3_rect.collidepoint(pos):
                if self.up3_level < UP_MAX_LEVEL:
                    cost = self.up3_cost()
                    if self.money >= cost:
                        self.money -= cost
                        self.up3_level += 1
                        self.tip_timer = 0.0
                        self.next_tip_time = self.current_tip_spawn_time()

                return


            for i in range(len(self.tips) - 1, -1, -1):
                if self.tips[i]["rect"].collidepoint(pos):
                    self.tips.pop(i)
                    tip_value = self.tip_value()
                    self.money += tip_value
                    self.gain_accum += tip_value
                    self.create_popup(pos[0], pos[1], tip_value)
                    return


            if self.cabin_rect.collidepoint(pos):
                self.money += self.click_value
                self.create_popup(pos[0], pos[1], self.click_value)
                return


            if self.back_rect.collidepoint(pos):
                self.game.state = "MENU"