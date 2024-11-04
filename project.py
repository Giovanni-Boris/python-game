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

# Function to show the end game menu
def show_end_game_menu(score):
    screen.fill((255, 255, 255))
    draw_text(f"Game Over! Your score: {score}", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text("Press SPACE to go to Level 2", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
    return True

def main(level):
    # Scoring variables
    score = 0
    goal = 10  # Set a goal for the score
    # Game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        # Draw the background
        screen.blit(background_image, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update player and collectibles
        all_sprites.update()  # Update all collectibles

        # Collision detection between player and collectibles
        collected = pygame.sprite.spritecollide(player, collectibles, dokill=True)
        for item in collected:
            score +=  1 if item.type == "Money" else 2

        collected = pygame.sprite.spritecollide(player, enemies, dokill=True)
        for _ in collected:
            score -= 1

        # Check if all collectibles are collected
        if len(collectibles) == 0:
            if show_end_game_menu(score):
                level_two()
            running = False

        # Draw all sprites
        all_sprites.draw(screen)
        # Draw the score on the screen
        draw_text(f"Score: {score}", font, (0, 0, 0), screen, 70, 30)

        # Update the display
        pygame.display.flip()
        clock.tick(30)  # Maintain 30 frames per second

    # Quit pygame
    pygame.quit()

def level_two():
    # Level 2 setup is similar to level 1, you can add additional complexities or differences if desired.
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Financial Game - Level 2: Investing")
    
    player = Player(WIDTH // 2, HEIGHT // 2)
    all_sprites = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    all_sprites.add(player)
    
    for _ in range(7):  # Increased number of collectibles
        collectible = Collectible()
        all_sprites.add(collectible)
        collectibles.add(collectible)
    for _ in range(7):  # Increased number of enemies
        enemy = Enemy(player)
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    score = 0
    goal = 15  # New goal for level 2
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        screen.blit(background_image, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()
        collected = pygame.sprite.spritecollide(player, collectibles, dokill=True)
        for item in collected:
            score += 1 if item.type == "Money" else 2

        collected = pygame.sprite.spritecollide(player, enemies, dokill=True)
        for _ in collected:
            score -= 1

        if len(collectibles) == 0:
            draw_text("Congratulations! You completed Level 2!", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        all_sprites.draw(screen)
        draw_text(f"Score: {score}", font, (0, 0, 0), screen, 70, 30)
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()

main(1)

