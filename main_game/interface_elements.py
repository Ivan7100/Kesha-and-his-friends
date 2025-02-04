import os
from colorsys import hsv_to_rgb
import sys

import pygame
import types
from PIL import Image, ImageSequence


def load_image(name, colorkey=None):
    fullname = os.path.join('data\\images', name)
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


class Button:
    def __init__(self, text: str, pos: tuple[int, int], size: int,
                 color: tuple[int, int]|pygame.color.Color,
                 bg_color: tuple[int, int]|pygame.color.Color|None, font_path):
        self.font = pygame.font.Font(font_path, size)
        self.color = color
        self.bg_color = bg_color
        self.pos0 = pos
        self.message = text
        self.text = self.font.render(text, True, self.color, bg_color)
        self.pos = (self.text.get_width(), self.text.get_height())
    
    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.text, (self.pos0[0], self.pos0[1]))
        x, y, x1, y1 = *self.pos0, *self.pos
        pygame.draw.rect(screen, self.color, (x - 1, y - 1, x1 + 2, y1 + 2), 1)
    
    def is_click(self, cord: tuple[int, int]) -> bool:
        if self.pos0[0] <= cord[0] <= self.pos[0] + self.pos0[0] and \
            self.pos0[1] <= cord[1] <= self.pos[1] + self.pos0[1]:
            return True
        return False

    def change_text(self, text):
        self.text = self.font.render(text, True, self.color, self.bg_color)
        self.pos = (self.text.get_width(), self.text.get_height())
        

class ImageButton(pygame.sprite.Sprite):
    def __init__(self,x, y, image_name, func: types.FunctionType, scale: tuple[int, int]|None = None, colorkey = None, *group):
        super().__init__(*group)
        self.func = func
        self.image = load_image(image_name, colorkey)
        if scale:
            self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        try:
            if args and args[0].type == pygame.MOUSEBUTTONUP and \
                    self.mask.get_at((args[0].pos[0] - self.rect.x, args[0].pos[1] - self.rect.y)):
                return self.func()
        except IndexError:
            pass

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in hsv_to_rgb(h,s,v))

def print_image():
    print('image')

import pygame
from PIL import Image, ImageSequence

class Gif:
    def __init__(self, filename, x, y, scale=None):
        self.filename = filename
        self.x = x
        self.y = y
        self.image = Image.open(filename)
        self.frames = []
        self.current_frame = 0
        self.last_frame_time = 0
        self.frame_duration = 2 * 1000 / self.image.info['duration']  # Время между кадрами в миллисекундах

        for frame in ImageSequence.Iterator(self.image):
            image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            if scale:
                image = pygame.transform.scale(image, scale)
            self.frames.append(image)
        self.frames.pop(0)

    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time > self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_frame_time = current_time
        screen.blit(self.frames[self.current_frame], (self.x, self.y))


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.time.set_timer(pygame.USEREVENT, 10)
    font_path = os.path.join('data/fonts', 'segoeprint.ttf')
    button = Button('Обычная кнопка', (10, 10), 40, 'blue', 'white', font_path)
    all_sprites = pygame.sprite.Group()
    image = ImageButton(10, 100, 'main.jpg', print_image, (300, 300), None,  all_sprites)
    gif = Gif(os.path.join('data/images', 'салам-обезьяна.gif'), 10, 100)
    gif.draw(screen)
    button.draw(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if button.is_click(event.pos): print('button')
                all_sprites.update(event)
            screen.fill((0, 0, 0))
            all_sprites.draw(screen)
            button.draw(screen)
            gif.draw(screen)
            pygame.display.flip()
    pygame.quit()