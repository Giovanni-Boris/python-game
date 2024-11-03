import pygame as pg
import random
from constans import *
class Message(pg.sprite.Sprite):
    def __init__(self, text, duration):
        super().__init__()
        self.text = text
        self.duration = duration
        self.start_time = pg.time.get_ticks()  # Track when the message is created

        # Set up the font and create a text surface
        self.font = pg.font.Font(None, 36)  # You can customize the font and size here
        self.color = (255, 255, 255)  # Text color (white)
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()

        # Set initial position and velocity
        self.position = pg.Vector2(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        self.velocity = pg.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 0.5
        self.rect.center = self.position

    def is_active(self):
        # Check if the message duration has passed
        return pg.time.get_ticks() - self.start_time < self.duration

    def update(self):
        if self.is_active():
            # Update position based on velocity
            self.position += self.velocity
            self.rect.center = self.position

            # Bounce off the edges of the screen
            if self.position.x < 0 or self.position.x > WIDTH:
                self.velocity.x *= -1
            if self.position.y < 0 or self.position.y > HEIGHT:
                self.velocity.y *= -1

            # Update the rect position for collision detection
            self.rect.center = self.position
        else:
            self.kill()  # Remove the sprite if it is no longer active
