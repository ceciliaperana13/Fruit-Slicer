import pygame
import sys

pygame.init()

# Screen size
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Slayer - Main Menu")

clock = pygame.time.Clock()

# === COLORS ===
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 128, 0)
RED = (255, 0, 0)
BROWN = (88, 41, 0)
PURPLE = (160, 32, 240)

# === FONTS ===
title_font = pygame.font.SysFont("arialblack", 80)
button_font = pygame.font.SysFont("arial", 35, bold=True)

# === BUTTON CLASS ===
class Button:
    def __init__(self, text, x, y, width, height, base_color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.base_color = base_color
        self.hover_color = hover_color

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        
        pygame.draw.rect(surface, color, self.rect, border_radius=20)
        pygame.draw.rect(surface, BROWN, self.rect, 4, border_radius=20)

        text_surf = button_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# === BUTTONS ===
play_button = Button("PLAY", WIDTH//2 - 150, 320, 300, 70, PURPLE, ORANGE)
quit_button = Button("QUIT", WIDTH//2 - 150, 420, 300, 70, RED, ORANGE)
settings_button = Button("settings", 0, HEIGHT//14 - 35, 200, 70, PURPLE, ORANGE)
scores_button = Button("scores", WIDTH - 200, HEIGHT//14 - 35, 200, 70, PURPLE, ORANGE)


# === MAIN MENU ===
def main_menu():
    running = True
    while running:
        screen.fill(BLACK)

        # Title
        title_text = title_font.render("FINAL FANTASY FRUITS", True, ORANGE)
        title_rect = title_text.get_rect(center=(WIDTH//2, 120))
        screen.blit(title_text, title_rect)

        subtitle = button_font.render("MAIN MENU", True, WHITE)
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 230))

        # Draw buttons
        play_button.draw(screen)
        quit_button.draw(screen)
        settings_button.draw(screen)
        scores_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if play_button.is_clicked(event):
                print("Starting game...")

            if quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

            if settings_button.is_clicked(event):
                print("Opening settings...")

            if scores_button.is_clicked(event):
                print("Showing scores...")

        pygame.display.flip()
        clock.tick(60)

main_menu()
