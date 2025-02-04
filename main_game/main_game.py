from math import pi
import os

import pygame
import pygame.gfxdraw
from main_game.player_data import PlayerData
from main_game.interface_elements import ImageButton, Button, load_image, hsv2rgb


games_screens = {'Тенис': 11, 'Бомбы и пончики': 12, 'Лабиринт': 13,
                 'Змейка': 21, "Обезьяна и чайник": 22, 'Кубопад': 23,
                 'Тетрис': 31, 'Circle clicker': 32, 'Flappy Elephant': 33}


def main_game(screen:pygame.surface.Surface, data: PlayerData):
    """
    Основная функция игры. Запускает игровой цикл и обрабатывает события.
    """
    class Main:
        def __init__(self, data: PlayerData):
            """
            Инициализирует игру, загружает персонажа и создает кнопки для перехода между комнатами и перексонажами.
            """
            data.update_stats()
            self.data = data
            self.character = data.data['last_character']

            self.load_character(self.character)

            self.icon_room_sprites = pygame.sprite.Group()
            ImageButton(45, 470, 'kitchen_icon.png', lambda: 'kitchen', (110, 110), None, self.icon_room_sprites)
            ImageButton(245, 470, 'playroom_icon.png', lambda: 'playroom', (110, 110), None, self.icon_room_sprites)
            ImageButton(445, 470, 'bathroom_icon.png', lambda: 'bathroom', (110, 110), None, self.icon_room_sprites)
            ImageButton(645, 470, 'bedroom_icon.png', lambda: 'bedroom', (110, 110), None, self.icon_room_sprites)

            self.shop_sprites = pygame.sprite.Group()
            ImageButton(45, 20, 'store_icon.png', lambda: 3, (110, 110), None, self.shop_sprites)

            self.character_sprites = pygame.sprite.Group()
            ImageButton(600, 20, 'left_arrow.png', self.change_character_left, None, -1, self.character_sprites)
            ImageButton(700, 20, 'right_arrow.png', self.change_character_right, None, -1, self.character_sprites)

            self.light_sprites = pygame.sprite.Group()
            ImageButton(45, 330, 'light_icon.png', self.change_light, (110, 110), None, self.light_sprites)

            self.shower_sprites = pygame.sprite.Group()
            ImageButton(45, 330, 'shower_icon.png', self.wash_up, (110, 110), None, self.shower_sprites)

            self.character_buttons = ['kesha', 'monkey', 'elephant']
            self.current_character_index = self.character_buttons.index(self.character)

        def load_character(self, name):
            """
            Загружает персонажа и фоновые изображения для каждой комнаты.
            """
            self.character_image = pygame.transform.scale(load_image(data.data[name]['character_image']), (300, 300))
            self.room = data.data[self.character]['last_room']
            self.backgrounds = {'kitchen':
                        pygame.transform.scale(load_image(self.data.data[self.character]['bg_kitchen']), (800, 600)),
                        'bathroom':
                        pygame.transform.scale(load_image(self.data.data[self.character]['bg_bathroom']), (800, 600)),
                        'playroom':
                        pygame.transform.scale(load_image(self.data.data[self.character]['bg_playroom']), (800, 600)),
                        'bedroom':
                        pygame.transform.scale(load_image(self.data.data[self.character]['bg_bedroom']), (800, 600)),
                        'store': pygame.transform.scale(load_image(self.data.data[self.character]['bg_kitchen']), (800, 600))}
            self.games_buttons = []
            font_path = os.path.join('data/fonts', 'segoeprint.ttf')
            for n, i in enumerate(self.data.data[self.character]['games']):
                self.games_buttons.append(Button(i, (20, 140 + 50 * n), 25, 'black', 'white', font_path))

        def change_character(self, name):
            """
            Меняет персонажа.
            """
            self.data.data[self.character]['last_room'] = self.room
            self.character = name
            self.data.data['last_character'] = name
            self.data.save()
            self.load_character(name)

        def change_character_left(self):
            """
            Переключает персонажа на предыдущего.
            """
            data.update_stats()
            self.current_character_index = (self.current_character_index - 1) % len(self.character_buttons)
            self.change_character(self.character_buttons[self.current_character_index])

        def change_character_right(self):
            """
            Переключает персонажа на следующего.
            """
            data.update_stats()
            self.current_character_index = (self.current_character_index + 1) % len(self.character_buttons)
            self.change_character(self.character_buttons[self.current_character_index])
        
        def change_light(self):
            """
            Меняет состояние света.
            """
            self.data.data[self.character]['is_sleeping'] = not self.data.data[self.character]['is_sleeping']
            self.data.save()
        
        def wash_up(self):
            """
            Меняет состояние чистоты.
            """
            self.data.data[self.character]['purity'] = 100
            self.data.save()
        
        def get_click(self, pos):
            """
            Обрабатывает клики мыши.
            """
            pass
            
            
        def draw(self, screen:pygame.surface.Surface):
            """
            Рисует игру на экране.
            """
            if self.data.data[self.character]['is_sleeping']:
                screen.blit(self.backgrounds[self.room], (0, 0))
                screen.blit(self.character_image, (440, 200))
            self.icon_room_sprites.draw(screen)
            self.character_sprites.draw(screen)
            self.shop_sprites.draw(screen)
            if self.room == 'bedroom':
                self.light_sprites.draw(screen)
            elif self.room == 'bathroom':
                self.shower_sprites.draw(screen)

            satiety = self.data.data[self.character]['satiety']
            mood = self.data.data[self.character]['mood']
            energy = self.data.data[self.character]['energy']
            purity = self.data.data[self.character]['purity']
            pygame.draw.arc(screen, hsv2rgb(satiety / 300, 1, 0.9), (45 - 15, 470 - 15, 110 + 30, 110 + 30), 0, satiety / 50 * pi, 10)
            pygame.draw.arc(screen, hsv2rgb(mood / 300, 1, 0.9), (245 - 15, 470 - 15, 110 + 30, 110 + 30), 0, mood / 50 * pi, 10)
            pygame.draw.arc(screen, hsv2rgb(purity / 300, 1, 0.9), (445 - 15, 470 - 15, 110 + 30, 110 + 30), 0, purity / 50 * pi, 10)
            pygame.draw.arc(screen, hsv2rgb(energy / 300, 1, 0.9), (645 - 15, 470 - 15, 110 + 30, 110 + 30), 0, energy / 50 * pi, 10)
            if self.room == 'playroom':
                for button in self.games_buttons:
                    button.draw(screen)


    pygame.init()
    size = width, height = 800, 600
    window = Main(data)
    window.draw(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.data.data[window.character]['last_room'] = window.room
                window.data.save()
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                for sprite in window.icon_room_sprites:
                    if sprite.update(event):
                        if window.data.data[window.character]['is_sleeping']:
                            window.room = sprite.update(event)
                for sprite in window.character_sprites:
                    if sprite.update(event):
                        sprite.update(event)
                if window.room == 'playroom':
                    for button in window.games_buttons:
                        if button.is_click(event.pos):
                            window.data.data[window.character]['last_room'] = window.room
                            window.data.save()
                            return games_screens[button.message]
                elif window.room == 'bedroom':
                    for sprite in window.light_sprites:
                        if sprite.update(event):
                            sprite.update(event)
                elif window.room == 'bathroom':
                    for sprite in window.shower_sprites:
                        if sprite.update(event):
                            sprite.update(event)
                for sprite in window.shop_sprites:
                    if sprite.update(event):
                        window.data.data[window.character]['last_room'] = window.room
                        window.data.save()
                        return sprite.update(event)
                        
                            
            screen.fill((0, 0, 0))
            window.draw(screen)
            pygame.display.flip()
    return 1



if __name__ == '__name__':
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    data = PlayerData('save1.json')
    main_game(screen, data)