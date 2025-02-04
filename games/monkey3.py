
import pygame
import sys
import os

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


def game3(screen, data: PlayerData):
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    PLAYER_SIZE = 60
    CUBE_SIZE = 50
    PLAYER_SPEED = 5  # Скорость перемещения игрока
    CUBE_SPEED_INITIAL = 3  # Начальная скорость кубов
    CUBE_SPEED_INCREMENT = 1  # Увеличение скорости кубов на 1 пиксель
    FPS = 60
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    PLAYER_COLOR = (0, 0, 255)  # Синий
    LINE_COLOR = (200, 200, 200)  # Светло-серый

    # Настройка экрана
    pygame.display.set_caption("Кубопад")

    # Загрузка изображений
    background_image = pygame.transform.scale(load_image("обезьянка3_фон.webp"), (WIDTH, HEIGHT))
    player_image = pygame.transform.scale(load_image("обезьянка_обезьянка.png", -1), (PLAYER_SIZE, PLAYER_SIZE))
    cube_image = pygame.transform.scale(load_image("обезьянка2_кокос.png", -1), (CUBE_SIZE, CUBE_SIZE))

    # Игрок
    player_x = WIDTH // 2 - PLAYER_SIZE // 2
    player_y = HEIGHT - PLAYER_SIZE - 10
    player_line = 1  # 0 - левая, 1 - средняя, 2 - правая
    player = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

    # Линии
    LINE_X = [WIDTH // 3, WIDTH // 3 * 2]  # X координаты линий
    # Кубы
    cubes = []
    cube_speed = CUBE_SPEED_INITIAL
    last_cube_time = 0

    # Очки
    score = 0
    POINTS_PER_CUBE = 5  # Очков за каждый куб
    cubes_passed = 0
    CUBES_FOR_SPEED_INCREASE = 5  # Кол-во падений для увелечения скорости

    # Шрифты
    font = pygame.font.Font(None, 36)
    font_big = pygame.font.Font(None, 72)  # Для надписи "Game Over"

    # Функция для создания нового куба
    def create_cube():
        cube_x = (WIDTH // 3) * (player_line) + (WIDTH // 6) - CUBE_SIZE // 2
        cube_y = 0 - CUBE_SIZE
        cube = pygame.Rect(cube_x, cube_y, CUBE_SIZE, CUBE_SIZE)
        cubes.append(cube)

    # Функция для отрисовки линий
    def draw_lines():
        for line_x in LINE_X:
            pygame.draw.line(screen, LINE_COLOR, (line_x, 0), (line_x, HEIGHT), 3)

    # Функция для отображения надписи "Game Over"
    def display_game_over():
        text = font_big.render("Game Over", True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    # Функция для отображения счета
    def display_score():
        text = font.render("Score: " + str(score), True, BLACK)
        screen.blit(text, (10, 10))

    # Функция для сброса игры
    def reset_game():
        nonlocal cubes, cube_speed, player_line, player_x, score, last_cube_time, cubes_passed
        cubes = []
        cube_speed = CUBE_SPEED_INITIAL
        player_line = 1
        player_x = (WIDTH // 3) * (player_line) + (WIDTH // 6) - PLAYER_SIZE // 2
        player.x = player_x
        score = 0
        last_cube_time = 0
        cubes_passed = 0

    # Инициализация игры
    reset_game()

    # Основной игровой цикл
    running = True
    game_over = False
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_LEFT:
                    player_line = max(0, player_line - 1)
                    player_x = (WIDTH // 3) * (player_line) + (WIDTH // 6) - PLAYER_SIZE // 2
                    player.x = player_x
                elif event.key == pygame.K_RIGHT:
                    player_line = min(2, player_line + 1)
                    player_x = (WIDTH // 3) * (player_line) + (WIDTH // 6) - PLAYER_SIZE // 2
                    player.x = player_x

        if not game_over:
            # Генерация кубов
            if not cubes:
                create_cube()

            # Движение кубов
            for cube in cubes:
                cube.y += cube_speed

            # Проверка на столкновение и пропуск кубов
            cubes_to_remove = []
            for cube in cubes:
                if cube.colliderect(player):
                    game_over = True
                    break
                elif cube.y > HEIGHT:
                    cubes_to_remove.append(cube)
                    score += POINTS_PER_CUBE
                    data.add_money(POINTS_PER_CUBE, 'monkey')
                    data.save()
                    cubes_passed += 1
                    if cubes_passed % CUBES_FOR_SPEED_INCREASE == 0:
                        cube_speed += CUBE_SPEED_INCREMENT

            # Удаление пропущенных кубов
            for cube in cubes_to_remove:
                cubes.remove(cube)

        # Отрисовка
        screen.blit(background_image, (0, 0))  # Фон
        draw_lines()

        # Отрисовка кубов
        for cube in cubes:
            screen.blit(cube_image, cube)
        screen.blit(player_image, player)  # Отрисовка игрока

        display_score()  # Отображение счета
        if game_over:
            display_game_over()

            # Ждем нажатия клавиши для перезапуска игры
            waiting_for_restart = True
            while waiting_for_restart:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        reset_game()
                        game_over = False
                        waiting_for_restart = False
                        break  # Выходим из цикла, если нажали кнопку
                    if event.type == pygame.QUIT:
                        running = False
                        waiting_for_restart = False
                pygame.display.flip()

        pygame.display.flip()
        clock.tick(FPS)
    return 2