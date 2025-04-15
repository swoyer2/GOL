import pygame

WIDTH = 32
HEIGHT = 32

# Define colors
BLACK = (0, 0, 0)
GREEN = (153, 255, 153)
PINK = (255, 204, 255)

class Square(pygame.sprite.Sprite):
    def __init__(self, state):
        super().__init__()
        self.image = None
        self.rect = None

        self.set_image(state)
    
    def get_color(self, state):
        if state == 0:
            return BLACK
        elif state == 1:
            return GREEN
        elif state == 2:
            return PINK
        else:
            raise ValueError(f"ERROR: Invalid state: {state}")
    
    def set_image(self, state):
        color = self.get_color(state)
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill(color)

    def set_pos(self, x, y):
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
