import pygame

def load_image(path):
    return pygame.image.load(path).convert_alpha()

def load_assets():

    assets = {}

    assets["game_background"] = load_image("./assets/Backgrounds/game_background.png")
    assets["menu_background"] = load_image("./assets/Backgrounds/menu_background.png")

    assets["cabin1"] = load_image("./assets/CabinUps/BbBg_bar1.png")
    assets["cabin2"] = load_image("./assets/CabinUps/BbBg_bar2.png")
    assets["cabin3"] = load_image("./assets/CabinUps/BbBg_bar3.png")
    assets["cabin4"] = load_image("./assets/CabinUps/BbBg_bar4.png")
    assets["cabin5"] = load_image("./assets/CabinUps/BbBg_bar5.png")

    assets["coin"] = load_image("./assets/icons/coin_icon.png")
    assets["tip"] = load_image("./assets/icons/tip_icon.png")

    assets["exit_button"] = load_image("./assets/menu/exit_button.png")
    assets["play_button"] = load_image("./assets/menu/play_button.png")
    assets["reset_button"] = load_image("./assets/menu/resetGame_button.png")
    assets["settings_button"] = load_image("./assets/menu/settings_button.png")

    assets["back_button"] = load_image("./assets/ui/back_button.png")
    assets["settings_panel"] = load_image("./assets/ui/settings_panel.png")

    assets["up_button1"] = load_image("./assets/UpButtons/UpButton1.png")
    assets["up_button2"] = load_image("./assets/UpButtons/UpButton2.png")
    assets["up_button3"] = load_image("./assets/UpButtons/UpButton3.png")
    assets["up_button4"] = load_image("./assets/UpButtons/UpButton4.png")

    assets["upgrade0"] = load_image("./assets/Upgrades/Upgrade0.png")
    assets["upgrade1"] = load_image("./assets/Upgrades/Upgrade1.png")
    assets["upgrade2"] = load_image("./assets/Upgrades/Upgrade2.png")
    assets["upgrade3"] = load_image("./assets/Upgrades/Upgrade3.png")
    assets["upgrade4"] = load_image("./assets/Upgrades/Upgrade4.png")

    return assets