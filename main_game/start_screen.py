import os

import pygame
from main_game.player_data import PlayerData
from main_game.interface_elements import Button, Gif, load_image



def start_screen(screen:pygame.surface.Surface, data: PlayerData):
    class Window():
        def __init__(self, bg_image_name: str):
            self.bg_image = load_image(bg_image_name)
            self.bg_image = pygame.transform.scale(self.bg_image, (800, 600))
            self.buttons = []
            font_path = os.path.join('data/fonts', 'segoeprint.ttf')
            self.buttons.append(Button('Начать игру', (50, 50), 20, (109, 99, 99), (255, 250, 194), font_path))
        
        def draw(self, screen: pygame.surface.Surface):
            screen.blit(self.bg_image, (0, 0))
            for button in self.buttons:
                button.draw(screen)
        
        def get_click(self, cord: tuple[int, int]):
            for button in self.buttons:
                if button.is_click(cord):
                    if button.message == 'Начать игру':
                        event = pygame.event.Event(pygame.USEREVENT, {'next_screen':2})
                        pygame.event.post(event)

    pygame.init()
    pygame.display.set_caption('Кеша и его друзья')
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    window = Window('main.jpg')
    pygame.time.set_timer(pygame.event.EventType(pygame.USEREVENT + 1), 10)
    gif = Gif(os.path.join('data/images', 'салам-обезьяна.gif'), 450, 350, (288, 288))
    window.draw(screen)
    gif.draw(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            elif event.type == pygame.MOUSEBUTTONUP:
                window.get_click(event.pos)
            elif event.type == pygame.USEREVENT:
                return event.next_screen
            screen.fill((0, 0, 0))
            window.draw(screen)
            gif.draw(screen)
            pygame.display.flip()
    pygame.quit()