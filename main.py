import pygame
from load_image import load_image


class Window():
    def __init__(self, bg_image_name: str):
        self.bg_image = load_image(bg_image_name)
        self.bg_image = pygame.transform.scale(self.bg_image, (800, 600))
        self.buttons = []
        self.buttons.append(Button('Начать игру', (50, 50), 30, (109, 99, 99), (255, 250, 194)))
        self.buttons.append(Button('Продолжить игру', (50, 100), 30, (109, 99, 99), (255, 250, 194)))
        self.buttons.append(Button('Настройки', (50, 150), 30, (109, 99, 99), (255, 250, 194)))
    
    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.bg_image, (0, 0))
        for button in self.buttons:
            button.draw(screen)
    
    def get_click(self, cord: tuple[int, int]):
        for button in self.buttons:
            if button.is_click(cord):
                print(button.message)
                break


class Button():
    def __init__(self, text: str, pos: tuple[int, int], size: tuple[int, int],
                 color: tuple[int, int]|pygame.color.Color,
                 bg_color: tuple[int, int]|pygame.color.Color|None):
        font = pygame.font.Font(None, size)
        self.color = color
        self.bg_color = bg_color
        self.pos0 = pos
        self.message = text
        self.text = font.render(text, True, self.color, bg_color)
        self.pos = (self.text.get_width(), self.text.get_height())
    
    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.text, (self.pos0[0], self.pos0[1]))
        x, y, x1, y1 = *self.pos0, *self.pos
        pygame.draw.rect(screen, self.color, (x - 2, y - 2, x1 + 4, y1 + 4), 1)
    
    def is_click(self, cord: tuple[int, int]) -> bool:
        if self.pos0[0] <= cord[0] <= self.pos[0] + self.pos0[0] and \
            self.pos0[1] <= cord[1] <= self.pos[1] + self.pos0[1]:
            return True
        return False

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Кеша и его друзья')
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    window = Window('main.jpg')
    window.draw(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                window.get_click(event.pos)
            screen.fill((0, 0, 0))
            window.draw(screen)
            pygame.display.flip()
    pygame.quit()