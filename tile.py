import pygame
from support2 import import_folder


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()

        self.image = pygame.Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, x_shift):
        self.rect.x += x_shift


class Spike(Tile):
    def __init__(self, size, x, y, value):
        super().__init__(size, x, y)

        if value == '0':
            self.image = pygame.image.load('assets/level_art/spikes_left.png')
            self.rect = self.image.get_rect(topleft=(x - 5, y))
        elif value == '1':
            self.image = pygame.image.load('assets/level_art/spikes_right.png')
            self.rect = self.image.get_rect(topleft=(x + 41, y))
        elif value == '2':
            self.image = pygame.image.load('assets/level_art/spikes_bottom.png')
            self.rect = self.image.get_rect(topleft=(x, y + 37))
        elif value == '3':
            self.image = pygame.image.load('assets/level_art/spikes_top.png')
            self.rect = self.image.get_rect(topleft=(x, y - 10))

    def update(self, x_shift):
        self.rect.x += x_shift

class Bridge(pygame.sprite.Sprite):
    def __init__(self, x, y, surface):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, x_shift):
        self.rect.x += x_shift


class Terrain(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface


class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift

class Goal(Terrain):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y, surface)

        self.rect = self.image.get_rect(bottomleft=(x, y + 48))

class Sky(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()

        self.image = surface
        self.rect = self.image.get_rect(topleft=(-100, 0))

    def update(self, x_shift):
        self.rect.x += x_shift
