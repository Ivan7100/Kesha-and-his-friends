import pygame
import random
import sys
import os

from main_game.player_data import PlayerData

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)

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

def game5(screen, data: PlayerData):
    WIDTH = 800
    HEIGHT = 600
    FPS = 60
    GRAVITY = 0.5
    JUMP_HEIGHT = -10
    PIPE_GAP = 150
    PIPE_WIDTH = 70
    PIPE_SPEED = 3
    SCORE_INCREMENT = 100
    PIPE_COLOR = (0, 128, 0)
    TEXT_COLOR = (255, 255, 255)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Elephant")

    # Загрузка изображений
    BACKGROUND_IMAGE = load_image("слон_фон.webp")
    BIRD_IMAGE = load_image("слон_слон.png")
    BIRD_IMAGE = pygame.transform.scale(BIRD_IMAGE, (152, 124))
    BIRD_IMAGE = pygame.transform.scale(BIRD_IMAGE, (BIRD_IMAGE.get_width() // 3, BIRD_IMAGE.get_height() // 3))
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

    class Bird:
        def __init__(self):
            self.x = WIDTH // 4
            self.y = HEIGHT // 2
            self.velocity = 0
            self.rect = BIRD_IMAGE.get_rect(topleft=(self.x - BIRD_IMAGE.get_width() / 2, self.y - BIRD_IMAGE.get_height() / 2))

        def update(self):
            self.velocity += GRAVITY
            self.y += self.velocity
            self.rect.topleft = (self.x - BIRD_IMAGE.get_width() / 2, self.y - BIRD_IMAGE.get_height() / 2)

        def jump(self):
            self.velocity = JUMP_HEIGHT

        def draw(self, screen):
            screen.blit(BIRD_IMAGE, self.rect.topleft)


    class Pipe:
        def __init__(self, x):
            self.x = x
            self.height = random.randint(100, HEIGHT - PIPE_GAP - 100)
            self.passed = False

        def update(self):
            self.x -= PIPE_SPEED

        def draw(self, screen):
            pygame.draw.rect(screen, PIPE_COLOR, (self.x, 0, PIPE_WIDTH, self.height))
            pygame.draw.rect(screen, PIPE_COLOR, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP))

        def collides(self, bird):
            if bird.rect.colliderect(pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)):
                return True
            if bird.rect.colliderect(pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP)): return True
            return False

    def create_pipe():
        return Pipe(WIDTH)

    def draw_text(screen, text, size, x, y, color=TEXT_COLOR):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        screen.blit(text_surface, text_rect)

    # Инициализация объектов
    bird = Bird()
    pipes = [create_pipe()]
    score = 0
    game_over = False
    clock = pygame.time.Clock()
    running = True

    # Основной цикл игры
    while running:
        clock.tick(FPS)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.jump()
                if event.key == pygame.K_r and game_over:
                    # Перезапуск игры
                    bird = Bird()
                    pipes = [create_pipe()]
                    score = 0
                    game_over = False

        # Обновление игровых объектов (если игра не окончена)
        if not game_over:
            bird.update()
            for pipe in pipes:
                pipe.update()
            if pipes[-1].x < WIDTH - 200:
                pipes.append(create_pipe())
            if pipes[0].x < -PIPE_WIDTH:
                pipes.pop(0)

            for pipe in pipes:
                if pipe.collides(bird):
                    game_over = True
                    break  # Важно! Прекращаем проверку, чтобы избежать двойных столкновений
            if bird.y > HEIGHT or bird.y < 0:
                game_over = True

            # Подсчет очков
            for pipe in pipes:
                if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x - bird.rect.width / 2:
                    score += SCORE_INCREMENT
                    data.add_money(SCORE_INCREMENT, 'elephant')
                    data.save()
                    pipe.passed = True

        # Отрисовка
        screen.blit(BACKGROUND_IMAGE, (0, 0))
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)
        draw_text(screen, f"Score: {score}", 30, WIDTH // 2, 50)

        # Отрисовка Game Over экрана
        if game_over:
            screen.fill((0, 0, 0))
            draw_text(screen, "Game Over", 50, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text(screen, f"Final Score: {score}", 30, WIDTH // 2, HEIGHT // 2)
            draw_text(screen, "Press R to Restart", 30, WIDTH // 2, HEIGHT // 2 + 50)

        pygame.display.flip()

    return 2