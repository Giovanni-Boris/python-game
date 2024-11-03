import random
import pygame

from levels import *
from things import Player, Collectible, Enemy, Message
from constans import *

# Initialize pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Financial Game - Level 1: Saving Coins")


# Load background image
background_image = pygame.image.load("assets/background.png")  # Replace with actual city image path
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Initialize player and sprite groups
player = Player(WIDTH // 2, HEIGHT // 2)  # Start the player in the center of the screen
all_sprites = pygame.sprite.Group()
collectibles = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Add player to the sprite group
all_sprites.add(player)

# Create collectibles with wandering behavior
for _ in range(5):
    collectible = Collectible()
    all_sprites.add(collectible)
    collectibles.add(collectible)
for _ in range(5):
    enemy = Enemy(player)
    all_sprites.add(enemy)
    enemies.add(enemy)




# Font for displaying text
font = pygame.font.Font(None, 36)

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

font_small = pygame.font.Font(None, 48)
menu = Menu(screen, background_image, "Financial Adventure", font, font_small)
messages = pygame.sprite.Group()
def main():
    # Scoring variables
    score = 0
    goal = 10  # Set a goal for the score
    # Game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        if not menu.nextScreen:
            menu.show_intro_screen()
        # Draw the background
        screen.blit(background_image, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update player and collectibles
        all_sprites.update()  # Update all collectibles
        messages.update()

        # Collision detection between player and collectibles
        collected = pygame.sprite.spritecollide(player, collectibles, dokill=True)
        for item in collected:
            score +=  1 if item.type == "Money" else 2
            messages.add(Message(random.choice(POSITIVE_MESSAGES), 4000))  # Show for 2 seconds

        collected = pygame.sprite.spritecollide(player, enemies, dokill=True)
        for _ in collected:
            score -= 1
            messages.add(Message(random.choice(NEGATIVE_MESSAGES), 4000))  # Show for 2 seconds
        # Cgit

    # Quit pygame
    pygame.quit()

main()