import os

import pygame
from load_image import load_image
from start_screen import start_screen
from v import game1
from player_data import PlayerData

screens = {-1:-1, 1:start_screen, 2:game1}
data = PlayerData('save1.json')

if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    next_screen = start_screen
    while next_screen != -1:
        next_screen = screens[next_screen(screen, data)]

pygame.quit()
