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

# ----------------------------------- [Sonidos y Música]
# Load sound effects
coin_sound = pygame.mixer.Sound("assets/coin.wav")  # Sonido al recoger dinero
investment_sound = pygame.mixer.Sound("assets/investment.wav")  # Sonido al realizar una inversión
failure_sound = pygame.mixer.Sound("assets/failure.wav")  # Sonido al recibir un golpe de un enemigo
level_up_sound = pygame.mixer.Sound("assets/level_up.flac")  # Sonido al pasar de nivel

# Load background music
pygame.mixer.music.load("assets/background_music.wav")  # Música de fondo para el juego
pygame.mixer.music.set_volume(0.5)  # Volumen de la música
pygame.mixer.music.play(-1)  # Reproduce en bucle

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
    
    # ----------------------------------- [Sonido Final de Nivel]
    level_up_sound.play()  # Reproduce el sonido de cambio de nivel

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
    goal = 5  # Set a goal for the score
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

        # ----------------------------------- [Colisión con Items y Efectos de Sonido]
        # Collision detection between player and collectibles
        collected = pygame.sprite.spritecollide(player, collectibles, dokill=True)
        for item in collected:
            score += 1 if item.type == "Money" else 2
            coin_sound.play()  # Reproduce el sonido al recolectar dinero

        # Collision with enemies
        collected = pygame.sprite.spritecollide(player, enemies, dokill=True)
        for _ in collected:
            score -= 1
            failure_sound.play()  # Sonido al recibir golpe de un enemigo

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
        
        # Collision with collectibles and play sound
        collected = pygame.sprite.spritecollide(player, collectibles, dokill=True)
        for item in collected:
            score += 1 if item.type == "Money" else 2
            investment_sound.play()  # Sonido al realizar inversión

        collected = pygame.sprite.spritecollide(player, enemies, dokill=True)
        for _ in collected:
            score -= 1
            failure_sound.play()

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
