import pygame as pg
import random
import os
from pygame.math import Vector2 as vec
from constans import *

script_dir = os.path.dirname(os.path.abspath(__file__))

# Calculate the path to the assets folder
assets_path = os.path.normpath(os.path.join(script_dir, '..', 'assets'))

# Construct the full path to the player image
money_image_path = os.path.normpath(os.path.join(assets_path, 'money.png'))
stock_image_path = os.path.normpath(os.path.join(assets_path, 'stock.png'))

# Load images
money_image = pg.image.load(money_image_path)
money_image = pg.transform.scale(money_image, (MOB_SIZE, MOB_SIZE))

stock_image = pg.image.load(stock_image_path)
stock_image = pg.transform.scale(stock_image, (MOB_SIZE, MOB_SIZE))

class Collectible(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Randomly select collectible type and set image
        self.type = random.choice(["Money", "Stocks"])
        self.image = money_image if self.type == "Money" else stock_image
        self.rect = self.image.get_rect()
        self.pos = vec(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.vel = vec(MAX_SPEED, 0).rotate(random.uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.last_update = pg.time.get_ticks()

    def seek(self, target):
        # Calculate the steering force towards the target
        desired = (target - self.pos).normalize() * MAX_SPEED
        steer = desired - self.vel
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def wander_improved(self):
        # Calculate future position for a smoother wandering effect
        future = self.pos + self.vel.normalize() * WANDER_RING_DISTANCE
        target = future + vec(WANDER_RING_RADIUS, 0).rotate(random.uniform(0, 360))
        return self.seek(target)

    def wander(self):
        # Update target periodically to create new random directions
        now = pg.time.get_ticks()
        if now - self.last_update > RAND_TARGET_TIME:
            self.last_update = now
            self.target = vec(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        return self.seek(self.target)

    def update(self):
        # Apply wandering behavior
        self.acc = self.wander_improved()

        # Update velocity and position
        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel

        # Screen wrap-around behavior
        if self.pos.x > WIDTH:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = HEIGHT

        # Update the sprite's position
        self.rect.center = self.pos