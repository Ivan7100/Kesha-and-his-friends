import pygame
import random
import os

from main_game.player_data import PlayerData


def maze(screen, data: PlayerData):
    pygame.display.set_caption('Лабиринт')
    screen_width = 800
    screen_height = 600

    black = (0, 0, 0)
    red = (255, 0, 0)
    green = ( 52,201,36)

    line_width = 10
    line_gap = 60
    line_offset = 50
    door_width = 50
    door_gap = 40
    max_openings_per_line = 10

    image_path = os.path.join('data/images', 'kesha_image.webp')
    player_image = pygame.transform.scale(pygame.image.load(image_path), (50, 50))
    player_rect = player_image.get_rect(center=(screen_width - 12, screen_height - line_offset))

    lines = []
    for i in range(0, screen_width, line_gap):
        rect = pygame.Rect(i, 0, line_width, screen_height)
        num_openings = random.randint(1, max_openings_per_line)
        if num_openings == 1:
            door_pos = random.randint(line_offset + door_width, screen_height - line_offset - door_width)
            lines.append(pygame.Rect(i, 0, line_width, door_pos - door_width))
            lines.append(pygame.Rect(i, door_pos + door_width, line_width, screen_height - door_pos - door_width))
        else:
            opening_positions = [0] + sorted([random.randint(line_offset + door_width, screen_height - line_offset - door_width) for _ in range(num_openings-1)]) + [screen_height]
            for j in range(num_openings):
                lines.append(pygame.Rect(i, opening_positions[j], line_width, opening_positions[j+1] - opening_positions[j] - door_width))

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 2

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= 5
        elif keys[pygame.K_RIGHT] and player_rect.right < screen_width:
            player_rect.x += 5
        elif keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= 5
        elif keys[pygame.K_DOWN] and player_rect.bottom < screen_height:
            player_rect.y += 5

        for line in lines:
            if line.colliderect(player_rect):
                if player_rect.centery < line.centery:
                    player_rect.bottom = line.top
                else:
                    player_rect.top = line.bottom
                if player_rect.centerx < line.centerx:
                    player_rect.right = line.left
                else:
                    player_rect.left = line.right

        screen.fill(black)
        for line in lines:
            pygame.draw.rect(screen, green, line)

        screen.blit(player_image, player_rect.topleft)

        pygame.display.update()
        clock.tick(60)
