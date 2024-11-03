import pygame as pg
from random import randint, uniform, random
from constans import *
from pygame.math import Vector2 as vec
import os

# Mob properties
MOB_SIZE = 32
MAX_SPEED = 5
MAX_FORCE = 0.1
APPROACH_RADIUS = 120

script_dir = os.path.dirname(os.path.abspath(__file__))

# Calculate the path to the assets folder
assets_path = os.path.normpath(os.path.join(script_dir, '..', 'assets'))

# Construct the full path to the player image
enemy_image_path = os.path.normpath(os.path.join(assets_path, 'enemy.png'))

class Enemy(pg.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        enemy_image = pg.image.load(enemy_image_path)
        enemy_image = pg.transform.scale(enemy_image, (25, 25))
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.pos = vec(randint(0, WIDTH), randint(0, HEIGHT))
        self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))*random()
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.player = player  # Reference to the player object

    def seek(self, target):
        self.desired = (target - self.pos).normalize() * MAX_SPEED

        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def seek_with_approach(self, target):
        self.desired = (target - self.pos)
        dist = self.desired.length()
        self.desired.normalize_ip()
        if dist < APPROACH_RADIUS:
            self.desired *= dist / APPROACH_RADIUS * MAX_SPEED
        else:
            self.desired *= MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def update(self):
        # self.follow_mouse()
        self.acc = self.seek_with_approach([self.player.rect.x, self.player.rect.y])
        # equations of motion
        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
        self.rect.center = self.pos