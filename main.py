import random
import pygame

from levels import *
from things import Player, Collectible, Enemy, Message
from constans import *

def init_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Financial Game")
    return screen

def load_assets():
    assets = {
        "background": pygame.transform.scale(
            pygame.image.load("assets/background.png"), (WIDTH, HEIGHT)
        ),
        "sounds": {
            "coin": pygame.mixer.Sound("assets/coin.wav"),
            "investment": pygame.mixer.Sound("assets/investment.wav"),
            "failure": pygame.mixer.Sound("assets/failure.wav"),
            "level_up": pygame.mixer.Sound("assets/level_up.flac"),
        },
        "music": "assets/background_music.wav",
    }
    pygame.mixer.music.load(assets["music"])
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    return assets

def draw_text(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def show_end_game_menu(screen, font, score, level_up_sound):
    screen.fill((255, 255, 255))
    draw_text(f"Game Over! Your score: {score}", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text("Press SPACE to go to Level 2", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()

    level_up_sound.play()

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

def run_level(screen, assets, level_data, next_level_callback):
    player = Player(WIDTH // 2, HEIGHT // 2)
    all_sprites = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    all_sprites.add(player)

    for _ in range(level_data["collectibles"]):
        collectible = Collectible()
        all_sprites.add(collectible)
        collectibles.add(collectible)

    for _ in range(level_data["enemies"]):
        enemy = Enemy(player)
        all_sprites.add(enemy)
        enemies.add(enemy)

    font = pygame.font.Font(None, 36)
    score = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.blit(assets["background"], (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        collected = pygame.sprite.spritecollide(player, collectibles, dokill=True)
        for item in collected:
            score += 1 if item.type == "Money" else 2
            assets["sounds"]["coin"].play()

        collected = pygame.sprite.spritecollide(player, enemies, dokill=True)
        for _ in collected:
            score -= 1
            assets["sounds"]["failure"].play()

        if len(collectibles) == 0:
            if level_data["next"]:
                if show_end_game_menu(screen, font, score, assets["sounds"]["level_up"]):
                    next_level_callback()
            running = False

        all_sprites.draw(screen)
        draw_text(f"Score: {score}", font, (0, 0, 0), screen, 70, 30)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

def main():
    screen = init_game()
    assets = load_assets()

    # Show the intro screen
    font = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)
    menu = Menu(screen, assets["background"], "Welcome to Financial Game", font, font_small)
    if not menu.show_intro_screen():
        return

    level_1_data = {
        "collectibles": 5,
        "enemies": 5,
        "next": True,
    }

    level_2_data = {
        "collectibles": 7,
        "enemies": 7,
        "next": False,
    }

    def level_two():
        run_level(screen, assets, level_2_data, lambda: None)

    run_level(screen, assets, level_1_data, level_two)

if __name__ == "__main__":
    main()
