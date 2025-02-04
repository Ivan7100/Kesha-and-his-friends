import random
import sys
import os

import pygame
from main_game.interface_elements import load_image
from main_game.player_data import PlayerData

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.init()

def load_image(name, colorkey=None):
    fullname = os.path.join('data/images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def game4(screen, data: PlayerData):
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Circle Clicker")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    elephant_image = load_image("слон_слон.png")
    background_image = load_image("слон_фон.webp")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    class Circle:
        def __init__(self):
            self.radius = random.randint(20, 50)
            self.x = random.randint(self.radius, WIDTH - self.radius)
            self.y = random.randint(self.radius, HEIGHT - self.radius)
            self.image = pygame.transform.scale(elephant_image, (self.radius * 2, self.radius * 2))
            self.rect = self.image.get_rect(center=(self.x, self.y))
            self.visible = True

        def draw(self):
            if self.visible:
                screen.blit(self.image, self.rect)

        def is_clicked(self, mouse_x, mouse_y):
            if not self.visible:
                return False
            return self.rect.collidepoint(mouse_x, mouse_y)

    def init_game(game_over_var): # game_over теперь передается как параметр
        game_over_var.game_over = False # изменяем game_over снаружи
        game_over_var.circles = [Circle() for _ in range(5)]
        game_over_var.score = 0


    # Создаем объект для хранения переменных состояния игры
    class GameState:
      pass
    game_state = GameState()
    init_game(game_state) # Передаем game_state в init_game


    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_state.game_over:
                mouse_x, mouse_y = event.pos
                clicked_circle = False
                for i, circle in enumerate(game_state.circles):
                    if circle.is_clicked(mouse_x, mouse_y):
                        game_state.circles[i] = Circle()
                        game_state.score += 5
                        data.add_money(5, 'elephant')
                        data.save()
                        clicked_circle = True
                        break
                if not clicked_circle:
                    game_state.game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state.game_over:
                    init_game(game_state) # Передаем game_state в init_game

        screen.blit(background_image, (0, 0))

        if not game_state.game_over:
            for circle in game_state.circles:
                circle.draw()
            text = font.render(f"Score: {game_state.score}", True, WHITE)
            screen.blit(text, (10, 10))
        else:
            game_over_text = font.render("Game Over! Press Space to Restart", True, RED)
            score_text = font.render(f"Final Score: {game_state.score}", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 240, HEIGHT // 2 - 20))
            screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 20))

        pygame.display.flip()
    return 2