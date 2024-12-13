import pygame as pg
from constans import *  # Assuming you have constants defined in a separate file

class Menu:
    start_button_color = (0, 128, 0)
    quit_button_color = (128, 0, 0)

    def __init__(self, screen, background_image, title, font, font_small):
        self.screen = screen
        self.background_image = background_image
        self.title = title
        self.font = font
        self.font_small = font_small
        self.nextScreen = False

    def draw_text(self, text, font, color, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))
        self.screen.blit(textobj, textrect)

    def draw_button(self, text, color, x, y, width, height):
        # Draw button rectangle
        button_rect = pg.Rect(x - width // 2, y - height // 2, width, height)
        pg.draw.rect(self.screen, color, button_rect)

        # Draw button text
        self.draw_text(text, self.font_small, (255, 255, 255), x, y)  # White text on button

        return button_rect

    def show_intro_screen(self):
        if self.nextScreen: return True

        while True:
            self.screen.blit(self.background_image, (0, 0))  # Draw background

            # Define button dimensions and positions
            start_button_rect = self.draw_button("Start Game", self.start_button_color, WIDTH // 2, HEIGHT // 2 + 50, 200, 50)
            quit_button_rect = self.draw_button("Quit", self.quit_button_color, WIDTH // 2, HEIGHT // 2 + 100, 200, 50)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return False  # Return false to indicate quitting
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:  # Start the game when Enter is pressed
                        self.nextScreen = True
                        return True  # Return true to start the game
                    elif event.key == pg.K_ESCAPE:  # Quit the game when Escape is pressed
                        pg.quit()
                        return False  # Return false to indicate quitting

                # Check mouse position for button hover
                mouse_pos = pg.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    # Change button color on hover
                    self.start_button_color = (0, 255, 0)
                    start_button_rect = self.draw_button("Start Game", self.start_button_color, WIDTH // 2, HEIGHT // 2 + 50, 200, 50)
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                        self.nextScreen = True
                        return True  # Return true to start the game
                else:
                    # Draw the button with the default color
                    self.start_button_color = (0, 128, 0)
                    start_button_rect = self.draw_button("Start Game", self.start_button_color, WIDTH // 2, HEIGHT // 2 + 50, 200, 50)

                if quit_button_rect.collidepoint(mouse_pos):
                    # Change button color on hover
                    self.quit_button_color = (255, 0, 0)
                    quit_button_rect = self.draw_button("Quit", self.quit_button_color, WIDTH // 2, HEIGHT // 2 + 100, 200, 50)
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                        pg.quit()
                        return False  # Return false to indicate quitting
                else:
                    # Draw the button with the default color
                    self.quit_button_color = (128, 0, 0)
                    quit_button_rect = self.draw_button("Quit", self.quit_button_color, WIDTH // 2, HEIGHT // 2 + 100, 200, 50)

            # Draw the title
            self.draw_text(self.title, self.font, (0, 0, 0), WIDTH // 2, HEIGHT // 2 - 50)

            pg.display.flip()  # Update the display
