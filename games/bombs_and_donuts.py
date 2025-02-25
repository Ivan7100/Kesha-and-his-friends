import pygame
import random
import os

from main_game.player_data import PlayerData
from main_game.interface_elements import load_image


def bombs(screen, data: PlayerData):
    try:
        class RewardsBombs():
            def __init__(self):
                pygame.init()
                self.screen_width = 800
                self.screen_height = 600
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                pygame.display.set_caption("Призы и бомбы")
                self.clock = pygame.time.Clock()
                self.square_image =pygame.transform.scale(load_image('bomb.jpg'), (100, 100))
                self.rectangle_image = pygame.transform.scale(load_image('donut.jpg'), (100, 100))
                self.player_image = pygame.transform.scale(load_image('kesha_image.webp'), (80, 70))

                self.square_pos = [self.screen_width // 2, self.screen_height - 30]
                self.red_positions = []
                self.red_speed = 2
                self.score = 0
                self.font = pygame.font.SysFont("Arial", 24)
                self.run()

            def run(self):
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            raise SyntaxError 

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                if self.square_pos[0] - 20 >= 0:
                                    self.square_pos[0] -= 20
                            elif event.key == pygame.K_RIGHT:
                                if self.square_pos[0] + 20 <= self.screen_width:
                                    self.square_pos[0] += 20
                            elif event.key == pygame.K_UP:
                                if self.square_pos[1] - 20 >= 0:
                                    self.square_pos[1] -= 20
                            elif event.key == pygame.K_DOWN:
                                if self.square_pos[1] + 20 <= self.screen_height:
                                    self.square_pos[1] += 20

                    for i in range(len(self.red_positions)):
                        self.red_positions[i][1] += self.red_speed

                    if random.random() < 0.02:
                        x = random.randint(0, self.screen_width)
                        num = random.randint(1, 10)
                        if num % 2 == 0:
                            self.red_positions.append([x, 0, False])
                        else:
                            self.red_positions.append([x, 0, True])

                    for pos in self.red_positions:
                        if pos[2]:
                            if abs(pos[0] - self.square_pos[0]) <= 20 and abs(pos[1] - self.square_pos[1]) <= 20:
                                self.score += 20
                                data.add_money(20, 'kesha')
                                self.red_positions.remove(pos)
                        else:
                            if (pos[0] - self.square_pos[0]) ** 2 + (pos[1] - self.square_pos[1]) ** 2 < 100:
                                self.game_over()

                    self.red_positions = [pos for pos in self.red_positions if pos[1] < self.screen_height]
                    self.screen.fill((0, 0, 0))

                    for pos in self.red_positions:
                        if pos[2]:
                            self.screen.blit(self.rectangle_image, (pos[0], pos[1]))
                        else:
                            self.screen.blit(self.square_image, (pos[0], pos[1]))

                    self.screen.blit(self.player_image, (self.square_pos[0], self.square_pos[1]))

                    self.draw_score()
                    pygame.display.update()
                    self.clock.tick(60)

            def draw_score(self):
                score_surface = self.font.render(f"Призы: {self.score}", True, (255, 255, 255))
                self.screen.blit(score_surface, (10, 10))

            def game_over(self):
                message_surface = self.font.render(f"Игра закончена! Призы: {self.score}", True, (255, 0, 0))

                self.screen.blit(message_surface, (self.screen_width // 2 - message_surface.get_width() // 2, self.screen_height // 2 - message_surface.get_height() // 2))
                pygame.display.update()
                pygame.time.wait(3000)
                raise SyntaxError

        RewardsBombs()
    except SyntaxError:
        return 2