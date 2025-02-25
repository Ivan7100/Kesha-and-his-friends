import pygame
import random
import sys
import os

from main_game.player_data import PlayerData

def tenis(screen, data: PlayerData):
    try:
        screen_width = 800
        screen_height = 600
        pygame.display.set_caption("Аркада")

        image_path = os.path.join('data/images', 'kesha_image.webp')
        ball_image = pygame.transform.scale(pygame.image.load(image_path), (100, 100))
        ball_rect = ball_image.get_rect(center=(250, 200))

        platform_color = (0, 255, 0)
        platform_rect = pygame.Rect(230, 300, 100, 10)

        ball_speed = [random.choice([-3, -2, -1, 1, 2, 3]), -1]
        touch_bottom = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SyntaxError

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and platform_rect.left > 0:
                platform_rect.x -= 2
            if keys[pygame.K_RIGHT] and platform_rect.right < screen_width:
                platform_rect.x += 2

            ball_rect.move_ip(ball_speed)

            if ball_rect.top <= 0:
                ball_speed[1] = 3

            if ball_rect.colliderect(platform_rect):
                ball_speed[1] = -3

            if ball_rect.bottom >= screen_height:
                touch_bottom = True

            if ball_rect.left <= 0 or ball_rect.right >= screen_width:
                ball_speed[0] = -ball_speed[0]

            screen.fill((0, 0, 0))

            screen.blit(ball_image, ball_rect)
            pygame.draw.rect(screen, platform_color, platform_rect)

            pygame.display.flip()

            if touch_bottom:
                return 2

            pygame.time.delay(10)
    except SyntaxError:
        return 2
