import random

import pygame
from code.const import UP_HUB_RECT, GAME_AREA_RECT, MONEY_POS, TIP_VALUE, TIP_MAX_ON_SCREEN, \
    TIP_SPAWN_MIN, TIP_SPAWN_MAX, POPUP_LIFETIME, POPUP_SPEED, UP1_BASE_COST, UP_MAX_LEVEL, TIP_AUTO_TIME, \
    UP2_BASE_COST, UP3_BASE_COST, UP4_BASE_COST, TIP_SPAWN_REDUCTION


class PlayingState:
    def __init__(self, game):

        self.game = game
        self.up_hub = pygame.Rect(UP_HUB_RECT)
        self.game_area = pygame.Rect(GAME_AREA_RECT)

        self.font_path = "./assets/Baloo-Regular.ttf"

        self.text_color = (121, 21, 9)
        self.locked_color = (130, 40, 35)

        self.money_font = self.load_font(50)
        self.popup_font = self.load_font(36)
        self.ui_font = self.load_font(28)
        self.cost_font = self.load_font(25)

        self.pressed_button = None
        self.press_timer = 0
        self.press_duration = 0.08
        self.current_cursor = pygame.SYSTEM_CURSOR_ARROW

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
        self.up4_img = self.game.assets["up_button4"]

        self.cabins = [
            self.game.assets["cabin1"],
            self.game.assets["cabin2"],
            self.game.assets["cabin3"],
            self.game.assets["cabin4"],
            self.game.assets["cabin5"],
        ]
        anchor = (self.game_area.centerx, self.game_area.bottom)
        self.cabin_rect = self.cabins[0].get_rect(midbottom=anchor)
        self.cabin_anchor = anchor
        self.click_value = 1

        self.tip_timer = 0.0
        self.tips = []
        self.popups = []
        self.up1_level = 0
        self.up2_level = 0
        self.up3_level = 0
        self.up4_level = 0
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
        self.up3_rect = self.up3_img.get_rect(topleft=(self.up_hub.left + 10, self.up_hub.top + 320))
        self.up4_rect = self.up4_img.get_rect(topleft=(self.up_hub.left + 10, self.up_hub.top + 435))
        self.back_rect = self.back_img.get_rect(topleft=(30, 28))



    def up1_cost(self) -> int:
        return UP1_BASE_COST * (self.up1_level + 1)

    def up2_cost(self) -> int:
        return UP2_BASE_COST * (self.up2_level + 1)

    def up3_cost(self) -> int:
        return UP3_BASE_COST * (self.up3_level + 1)

    def up4_cost(self) -> int:
        return UP4_BASE_COST * (self.up4_level + 1) * 2

    def load_font(self, size):
        try:
            return pygame.font.Font(self.font_path, size)
        except FileNotFoundError:
            return pygame.font.Font(None, size)

    def darken_image(self, image, alpha=75):
        darkened = image.copy()
        overlay = pygame.Surface(darkened.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        darkened.blit(overlay, (0, 0))
        return darkened

    def draw_upgrade(self, surface, image, rect, level, cost_value, button_name):
        draw_rect = self.get_draw_rect(button_name, rect)
        at_max = level >= UP_MAX_LEVEL
        can_afford = self.money >= cost_value

        button_img = image if (at_max or can_afford) else self.darken_image(image)
        surface.blit(button_img, draw_rect)

        indicator_img = self.upgrade_indicators[level]
        indicator_rect = indicator_img.get_rect(center=(draw_rect.centerx + 30, draw_rect.centery))
        surface.blit(indicator_img, indicator_rect)

        if at_max:
            text = "MAX"
            color = self.text_color
        else:
            text = f"Cost: ¥{cost_value}"
            color = self.text_color if can_afford else self.locked_color

        cost_surf = self.cost_font.render(text, True, color)
        cost_rect = cost_surf.get_rect(topleft=(draw_rect.left + 5, draw_rect.bottom - 7))
        surface.blit(cost_surf, cost_rect)

    def get_hovered_button(self, pos):
        if self.up1_rect.collidepoint(pos):
            return "up1"
        if self.up2_rect.collidepoint(pos):
            return "up2"
        if self.up3_rect.collidepoint(pos):
            return "up3"
        if self.up4_rect.collidepoint(pos):
            return "up4"
        if self.back_rect.collidepoint(pos):
            return "back"
        return None

    def get_draw_rect(self, name, rect):
        if self.pressed_button == name and self.press_timer > 0:
            return rect.move(0, 2)
        return rect

    def update_cursor(self):
        hovered = self.get_hovered_button(pygame.mouse.get_pos())
        wanted_cursor = pygame.SYSTEM_CURSOR_HAND if hovered else pygame.SYSTEM_CURSOR_ARROW

        if wanted_cursor != self.current_cursor:
            pygame.mouse.set_cursor(wanted_cursor)
            self.current_cursor = wanted_cursor


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

    def reset_progress(self):
        self.money = 0
        self.click_value = 1

        self.up1_level = 0
        self.up2_level = 0
        self.up3_level = 0
        self.up4_level = 0

        self.tips.clear()
        self.popups.clear()

        self.gain_accum = 0
        self.gain_timer = 0
        self.money_per_sec = 0

        self.tip_timer = 0.0
        self.next_tip_time = self.current_tip_spawn_time()

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

        if self.press_timer > 0:
            self.press_timer -= dt
            if self.press_timer <= 0:
                self.press_timer = 0
                self.pressed_button = None

        self.update_cursor()



    def draw(self, surface):
        surface.blit(self.game.assets["game_background"], (0, 0))
        cabin_img = self.cabins[self.up4_level]
        self.cabin_rect = cabin_img.get_rect(midbottom=self.cabin_anchor)
        surface.blit(cabin_img, self.cabin_rect)


        for t in self.tips:
            surface.blit(self.tip_img, t["rect"])

        self.draw_upgrade(surface, self.up1_img, self.up1_rect, self.up1_level, self.up1_cost(), "up1")
        self.draw_upgrade(surface, self.up2_img, self.up2_rect, self.up2_level, self.up2_cost(), "up2")
        self.draw_upgrade(surface, self.up3_img, self.up3_rect, self.up3_level, self.up3_cost(), "up3")
        self.draw_upgrade(surface, self.up4_img, self.up4_rect, self.up4_level, self.up4_cost(), "up4")

        money_surf = self.money_font.render(f"¥{self.money}", True, self.text_color)
        money_rect = money_surf.get_rect(topleft=self.money_pos)
        surface.blit(money_surf, money_rect)
        mps = self.ui_font.render(f"{self.money_per_sec} ¥/s", True, self.text_color)
        surface.blit(mps, (self.money_pos[0], self.money_pos[1] + 50))

        for p in self.popups:
            ratio = max(0.0, p["life"] / p["max_life"])  # 1 -> 0
            alpha = int(255 * ratio)

            coin_rect = self.coin_img.get_rect(center=(p["x"], p["y"]))
            coin_surf = self.coin_img.copy()
            coin_surf.set_alpha(alpha)
            surface.blit(coin_surf, coin_rect)

            txt_surf = self.popup_font.render(f"+¥{p['value']}", True, self.text_color)
            txt_surf.set_alpha(alpha)
            txt_rect = txt_surf.get_rect(midleft=(coin_rect.right + 6, coin_rect.centery))
            surface.blit(txt_surf, txt_rect)

        back_draw_rect = self.get_draw_rect("back", self.back_rect)
        surface.blit(self.back_img, back_draw_rect)



    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.state = "MENU"
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            clicked_button = self.get_hovered_button(pos)
            if clicked_button:
                self.pressed_button = clicked_button
                self.press_timer = self.press_duration

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

            if self.up4_rect.collidepoint(pos):
                if self.up4_level < UP_MAX_LEVEL:
                    cost = self.up4_cost()
                    if self.money >= cost:
                        self.money -= cost
                        self.up4_level += 1

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