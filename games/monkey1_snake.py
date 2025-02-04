
import pygame
import random
import sys
import os
import time
import math

from main_game.player_data import PlayerData


# Изображение не получится загрузить 
# без предварительной инициализации pygame
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)

def load_image(name, colorkey=None):
    fullname = os.path.join('data/images', name)
    # если файл не существует, то выходим
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


def game1(screen, data: PlayerData):
    # Размеры окна и клеток
    GRID_SIZE = 20
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    GRID_WIDTH = WIDTH // GRID_SIZE
    GRID_HEIGHT = HEIGHT // GRID_SIZE
    pygame.display.set_caption("Змейка")

    # Загрузка изображений
    head_image = load_image("змейка_голова.png", -1)
    body_image = load_image("змейка_туловище.png")
    food_image = load_image("змейка_яблоко.jpg", -1)
    background_image = load_image("змейка_фон.jpg")
    
    # Масштабирование изображений до размера клетки
    head_image = pygame.transform.scale(head_image, (GRID_SIZE, GRID_SIZE))
    body_image = pygame.transform.scale(body_image, (GRID_SIZE, GRID_SIZE))
    food_image = pygame.transform.scale(food_image, (GRID_SIZE, GRID_SIZE))
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    # Начальная позиция змейки
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake_direction = (1, 0)
    previous_direction = snake_direction
    snake_speed = 10

    # Еда
    food = None
    def create_food():
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake:
                return pos

    food = create_food()
    score = 0
    score_per_food = 20
    font = pygame.font.Font(None, 36)
    last_move_time = time.time()
    game_over = False
    running = True

    # Главный цикл игры
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != (0, 1):
                    previous_direction = snake_direction
                    snake_direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                    previous_direction = snake_direction
                    snake_direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                    previous_direction = snake_direction
                    snake_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                    previous_direction = snake_direction
                    snake_direction = (1, 0)
                elif game_over and event.key == pygame.K_SPACE:
                    game_over = False
                    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
                    snake_direction = (1, 0)
                    previous_direction = snake_direction
                    food = create_food()
                    score = 0
                    
        if not game_over:
            current_time = time.time()
            if current_time - last_move_time > 1/snake_speed:
                last_move_time = current_time

                # Расчет новой позиции головы змейки
                head = snake[0]
                new_head = (head[0] + snake_direction[0], head[1] + snake_direction[1])
                
                # Проверка выхода за границы
                if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                    new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
                    game_over = True
                
                # Проверка столкновения с телом
                if new_head in snake:
                    game_over = True
                
                if not game_over:
                    snake.insert(0, new_head)

                    # Проверка столкновения с едой
                    if new_head == food:
                        food = create_food()
                        score += score_per_food  # Даем 20 очков
                        data.add_money(score_per_food, 'monkey')
                        data.save()
                    else:
                        snake.pop()

        # Отрисовка
        screen.blit(background_image, (0, 0))

        # Отрисовка змейки
        for i, part in enumerate(snake):
            rect = pygame.Rect(part[0] * GRID_SIZE, part[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if i == 0:  # голова змейки
                angle = 0
                if snake_direction == (0, -1):  # вверх
                    angle = -90  # Поворот на 90 градусов против часовой стрелки
                elif snake_direction == (0, 1): # вниз
                    angle = 90 # Поворот на 90 градусов по часовой стрелке
                elif snake_direction == (-1, 0): # влево
                    angle = 0
                elif snake_direction == (1, 0):  # вправо
                    angle = 180 # Поворот на 180 градусов

                rotated_head = pygame.transform.rotate(head_image, angle)
                rotated_rect = rotated_head.get_rect(center=rect.center)
                screen.blit(rotated_head, rotated_rect)
            else:  # тело змейки
                screen.blit(body_image, rect)

        # Отрисовка еды
        if food:
            rect = pygame.Rect(food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            screen.blit(food_image, rect)

        # Отображение счета
        text = font.render("Счет: " + str(score), True, WHITE)
        screen.blit(text, (10, 10))

        # Экран Game Over
        if game_over:
            game_over_text = font.render("Game Over! Нажмите SPACE для перезапуска", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(game_over_text, text_rect)


        pygame.display.flip()
        pygame.time.delay(30)

    return 2
