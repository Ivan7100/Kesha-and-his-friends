import pygame
import random
import os
import sys

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


def game2(screen, data: PlayerData):
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Monkey Jumper")

    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    # Загрузка изображений
    background_image = load_image('обезьянка_фон.webp')
    dino_image = load_image('обезьянка_обезьянка.png', -1)  # Используем colorkey для прозрачности
    obstacle_image = load_image('обезьянка_препятствие.png', -1)  # Используем colorkey для прозрачности

    # Масштабирование изображений
    dino_image = pygame.transform.scale(dino_image, (60, 80))  # Уменьшаем размер обезьянки
    obstacle_image = pygame.transform.scale(obstacle_image, (40, 60))  # Уменьшаем размер препятствия
    background_image = pygame.transform.scale(background_image,(WIDTH, HEIGHT))


    # Получаем размеры изображений
    dino_width = dino_image.get_width()
    dino_height = dino_image.get_height()
    obstacle_width = obstacle_image.get_width()
    obstacle_height = obstacle_image.get_height()

    # Настройки игрока
    dino_x = 50
    dino_y = 450 - dino_height  # Учитываем высоту изображения
    dino_y_vel = 0
    dino_gravity = 1.5
    dino_jump_power = -20
    is_jumping = False


    # Настройки препятствий
    obstacle_speed = 8
    obstacles = []
    obstacle_spawn_time = 2000
    last_obstacle_time = pygame.time.get_ticks()


    # Настройки счета
    score = 0
    font = pygame.font.Font(None, 36)

    # Функция для отрисовки игрока
    def draw_dino(x, y):
        screen.blit(dino_image, (x, y))

    # Функция для отрисовки препятствия
    def draw_obstacle(x, y):
        screen.blit(obstacle_image, (x, y))

    # Функция для генерации новых препятствий
    def create_obstacle():
        obstacle_y = 450 - obstacle_height
        obstacle_x = WIDTH
        obstacles.append([obstacle_x, obstacle_y])

    # Функция для обновления позиций препятствий
    def update_obstacles():
        nonlocal score, obstacle_speed
        for obstacle in obstacles:        
            obstacle[0] -= obstacle_speed

            # Проверка на столкновение с игроком
            dino_rect = dino_image.get_rect(topleft=(dino_x, dino_y))
            obstacle_rect = obstacle_image.get_rect(topleft=(obstacle[0], obstacle[1]))

            if dino_rect.colliderect(obstacle_rect):
                return True

            if obstacle[0] < -obstacle_width:
                obstacles.remove(obstacle)
                score += 20
                obstacle_speed += 0.2
                data.add_money(20, 'monkey')
                data.save()
        return False

    # Основной игровой цикл
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping and not game_over:
                    dino_y_vel = dino_jump_power
                    is_jumping = True

        if not game_over:
            # Обновление игрока
            dino_y_vel += dino_gravity
            dino_y += dino_y_vel
            if dino_y >= 450 - dino_height:
                dino_y = 450 - dino_height
                dino_y_vel = 0
                is_jumping = False

            # Генерация препятствий
            current_time = pygame.time.get_ticks()
            if current_time - last_obstacle_time > obstacle_spawn_time:
                create_obstacle()
                last_obstacle_time = current_time

            # Обновление препятствий
            if update_obstacles():
                game_over = True

            # Отрисовка фона
            screen.blit(background_image, (0, 0))

            # Отрисовка игрока
            draw_dino(dino_x, dino_y)

            # Отрисовка препятствий
            for obstacle in obstacles:
                draw_obstacle(obstacle[0], obstacle[1])

            # Отрисовка счета
            score_text = font.render("Score: " + str(score), True, BLACK)
            screen.blit(score_text, (10, 10))

        else:
            # Экран Game Over
            screen.fill(WHITE)
            game_over_text = font.render("Game Over! Score: " + str(score), True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            restart_text = font.render("Press SPACE to restart", True, BLACK)
            screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 10))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                game_over = False
                dino_y = 450 - dino_height
                dino_y_vel = 0
                is_jumping = False
                score = 0
                obstacle_speed = 8
                obstacles.clear()
                last_obstacle_time = pygame.time.get_ticks()

        # Обновление дисплея
        pygame.display.flip()

        # Задержка
        pygame.time.Clock().tick(60)

    return 2