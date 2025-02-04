import os

import pygame
from main_game.player_data import PlayerData
from main_game.interface_elements import Button, load_image


def shop(screen: pygame.surface.Surface, data: PlayerData):
    class Window():
        def __init__(self):
            self.bg_image = load_image('bg_shop.jpg')
            self.bg_image = pygame.transform.scale(self.bg_image, (800, 600))
            self.data = data
            self.character = data.data['last_character']
            self.character_image = pygame.transform.scale(load_image(data.data[self.character]['character_image']), (300, 300))
            font_path = os.path.join('data/fonts', 'segoeprint.ttf')
            self.buttons = {'кошелёк': Button(f'кошелёк: {data.data[self.character]['money']}', (50, 50), 20, (109, 99, 99), (255, 250, 194), font_path),
                            'classic_skin': Button(f'обычная одежда: 0', (50, 100), 20, (109, 99, 99), (255, 250, 194), font_path),
                            'other_skin': Button(f'улучшенная одежда: {self.data.data[self.character]['shop']['other_skin'][1]}', (50, 150), 20, (109, 99, 99), (255, 250, 194), font_path),
                            'classic_bg_skin': Button(f'обычные комнаты: 0', (50, 200), 20, (109, 99, 99), (255, 250, 194), font_path),
                            'other_bg_skin': Button(f'улучшенные комнаты: {self.data.data[self.character]['shop']['other_bg_skin'][1]}', (50, 250), 20, (109, 99, 99), (255, 250, 194), font_path),
                            'cola': Button(f'кола: {data.data[self.character]['shop']['cola'][0]}', (50, 300), 20, (109, 99, 99), (255, 250, 194), font_path),
                            'porridge': Button(f'каша: {data.data[self.character]['shop']['porridge'][0]}', (50, 350), 20, (109, 99, 99), (255, 250, 194), font_path),
                            'cutlet': Button(f'котлета: {data.data[self.character]['shop']['cutlet'][0]}', (50, 400), 20, (109, 99, 99), (255, 250, 194), font_path),
                            'chocolate': Button(f'шоколад: {data.data[self.character]['shop']['chocolate'][0]}', (50, 450), 20, (109, 99, 99), (255, 250, 194), font_path),
                            }

        
        def draw(self, screen: pygame.surface.Surface):
            screen.blit(self.bg_image, (0, 0))
            screen.blit(self.character_image, (340, 300))
            for button in self.buttons:
                self.buttons[button].draw(screen)
        
        def get_click(self, cord: tuple[int, int]):
            for button in self.buttons:
                if self.buttons[button].is_click(cord):
                    if button in ['classic_skin', 'other_skin']:
                        self.buy_skin(button)
                    elif button in ['classic_bg_skin', 'other_bg_skin']:
                        self.buy_room_skin(button)
                    elif button in ['cola', 'porridge', 'cutlet', 'chocolate']:
                        self.buy_food(button)

        
        def change_money(self, money):
            self.data.data[self.character]['money'] += money
            self.buttons['кошелёк'].change_text(f'кошелёк: {self.data.data[self.character]["money"]}')
            self.data.save()
        
        def buy_food(self, food_name: str):
            if self.data.data[self.character]['money'] >= self.data.data[self.character]['shop'][food_name][0] and \
            self.data.data[self.character]['satiety'] < 100:
                self.data.data[self.character]['satiety'] += self.data.data[self.character]['shop'][food_name][1]
                self.data.data[self.character]['satiety'] = min(self.data.data[self.character]['satiety'], 100)
                self.change_money(-self.data.data[self.character]['shop'][food_name][0])
                self.data.save()
        
        def buy_skin(self, skin_name: str):
            if self.data.data[self.character]['money'] >= self.data.data[self.character]['shop'][skin_name][1]:
                self.data.data[self.character]['character_image'] = self.data.data[self.character]['shop'][skin_name][0]
                self.change_money(-self.data.data[self.character]['shop'][skin_name][1])
                self.data.data[self.character]['shop'][skin_name][1] = 0
                self.character_image = pygame.transform.scale(load_image(data.data[self.character]['character_image']), (300, 300))
                self.data.save()
        
        def buy_room_skin(self, skin_name: str):
            if self.data.data[self.character]['money'] >= self.data.data[self.character]['shop'][skin_name][1]:
                self.data.data[self.character]['bg_kitchen'] = self.data.data[self.character]['shop'][skin_name][0][0]
                self.data.data[self.character]['bg_bathroom'] = self.data.data[self.character]['shop'][skin_name][0][1]
                self.data.data[self.character]['bg_playroom'] = self.data.data[self.character]['shop'][skin_name][0][2]
                self.data.data[self.character]['bg_bedroom'] = self.data.data[self.character]['shop'][skin_name][0][3]
                self.change_money(-self.data.data[self.character]['shop'][skin_name][1])
                self.data.data[self.character]['shop'][skin_name][1] = 0
                self.data.save()
            


    window = Window()
    running = True
    window.draw(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 2
            elif event.type == pygame.MOUSEBUTTONUP:
                window.get_click(event.pos)
            screen.fill((0, 0, 0))
            window.draw(screen)
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.time.set_timer(pygame.USEREVENT, 10)
    shop(screen, PlayerData("save1.json"))
