# player.py
from token import COLON

import pygame
import os


script_dir = os.path.dirname(os.path.abspath(__file__))

# Calculate the path to the assets folder
assets_path = os.path.normpath(os.path.join(script_dir, '..', 'assets'))

# Construct the full path to the player image
player_image_path = os.path.normpath(os.path.join(assets_path, 'player.png'))



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        player_image = pygame.image.load(player_image_path)
        player_image = pygame.transform.scale(player_image, (50, 50))
        self.image = player_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 600:
            self.rect.y += self.speed
