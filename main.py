import os

import pygame
from main_game.start_screen import start_screen
from main_game.player_data import PlayerData
from main_game.main_game import main_game
from main_game.shop import shop

# импорт игр
from games.maze import maze
from games.tetris import tetris
from games.tenis import tenis
from games.bombs_and_donuts import bombs
from games.monkey1_snake import game1
from games.monkey2 import game2
from games.monkey3 import game3
from games.elephant2 import game4
from games.elephant3 import game5

# Словарь, связывающий номер экрана с функцией, которая его отображает
screens = {-1: -1, 1: start_screen, 2: main_game, 3: shop,
           11: tenis, 12: bombs, 13: maze,
           21: game1, 22: game2, 23: game3,
           31: tetris, 32: game4, 33: game5}

# Создание экземпляра класса PlayerData для сохранения данных игрока
data = PlayerData('save1.json')

if __name__ == '__main__':
   # Инициализация pygame
   pygame.init()
   # Установка размера окна
   size = width, height = 800, 600
   screen = pygame.display.set_mode(size)
   # Начальный экран
   next_screen = start_screen
   # Цикл, пока не будет выбран экран с номером -1
   while next_screen != -1:
       pygame.display.set_caption('Кеша и его друзья')
       # Переход к следующему экрану
       next_screen = screens[next_screen(screen, data)]

# Завершение работы pygame
pygame.quit()
