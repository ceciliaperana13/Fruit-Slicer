import pygame
import sys
from button_menu import Button_menu


class MainMenu:
    """Classe pour gérer le menu principal du jeu"""

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # === COULEURS ===
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.ORANGE = (255, 128, 0)
        self.RED = (255, 0, 0)
        self.BROWN = (88, 41, 0)
        self.PURPLE = (160, 32, 240)

        self.BLUE_GRAY = (70, 90, 120)
        self.BLUE_GRAY_LIGHT = (100, 120, 150)
        self.BLUE_GRAY_DARK = (50, 70, 100)

        self.TITLE_BLUE = (70, 130, 180)
        self.TITLE_DARK_BLUE = (25, 60, 100)

        # === IMAGE DE FOND ===
        try:
            bg_img = pygame.image.load('./images/572603.jpg')
            self.background = pygame.transform.scale(bg_img, (width, height))
        except:
            self.background = pygame.Surface((width, height))
            self.background.fill(self.BLACK)
            print("Warning: Background image not found")

        # === ICÔNES ===
        try:
            self.scores_icon = pygame.image.load('./images/scores.png')
            self.scores_icon = pygame.transform.scale(self.scores_icon, (50, 50))
        except:
            self.scores_icon = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.rect(self.scores_icon, (255, 128, 180), (10, 20, 30, 25), border_radius=5)

        try:
            self.settings_icon = pygame.image.load('./images/fruit_settings.png')
            self.settings_icon = pygame.transform.scale(self.settings_icon, (50, 50))
        except:
            self.settings_icon = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(self.settings_icon, (200, 200, 200), (25, 25), 20, 3)
            pygame.draw.circle(self.settings_icon, (200, 200, 200), (25, 25), 10)

        # === FONTS ===
        try:
            self.title_font = pygame.font.Font('./images/comic.ttf', 80)
            self.button_font = pygame.font.Font('./images/comic.ttf', 35)
        except:
            self.title_font = pygame.font.SysFont("arialblack", 80)
            self.button_font = pygame.font.SysFont("arial", 35, bold=True)

        # === BOUTONS ===
        button_y_start = height - 180

        self.play_button = Button_menu(
            "PLAY",
            width // 2 - 150, button_y_start, 300, 70,
            self.BLUE_GRAY, self.BLUE_GRAY_LIGHT,
            self.button_font, self.BLUE_GRAY_DARK
        )

        self.quit_button = Button_menu(
            "QUIT",
            width // 2 - 150, button_y_start + 70, 300, 70,
            self.RED, self.ORANGE,
            self.button_font, self.BROWN
        )

        self.settings_button_rect = pygame.Rect(width - 70, 20, 60, 60)
        self.scores_button_rect = pygame.Rect(10, 20, 60, 60)

        self.settings_hovered = False
        self.scores_hovered = False

        # === SONS ===
        try:
            self.sound_hover = pygame.mixer.Sound("./musique/menu-move.ogg")
            self.sound_click = pygame.mixer.Sound("./musique/game-start.ogg")

            self.sound_hover.set_volume(0.3)
            self.sound_click.set_volume(0.5)
        except:
            print("Warning: sounds not found")
            self.sound_hover = None
            self.sound_click = None

        # === ÉTATS HOVER (anti-spam son) ===
        self.hover_states = {
            "play": False,
            "quit": False,
            "settings": False,
            "scores": False
        }

    # =======================================================

    def draw_fancy_title(self, screen):
        title_line1 = "FINAL FANTASY"
        title_line2 = "FRUITS"

        title_y1 = 180
        title_y2 = 260

        for title_text, title_y in [(title_line1, title_y1), (title_line2, title_y2)]:
            for offset in range(6, 0, -2):
                shadow = self.title_font.render(title_text, True, self.TITLE_DARK_BLUE)
                shadow.set_alpha(40)
                rect = shadow.get_rect(center=(self.width // 2, title_y))
                screen.blit(shadow, (rect.x + offset, rect.y + offset))

            shadow_text = self.title_font.render(title_text, True, self.BLACK)
            shadow_rect = shadow_text.get_rect(center=(self.width // 2 + 3, title_y + 3))
            screen.blit(shadow_text, shadow_rect)

            main_text = self.title_font.render(title_text, True, self.TITLE_BLUE)
            main_rect = main_text.get_rect(center=(self.width // 2, title_y))
            screen.blit(main_text, main_rect)

    # =======================================================

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(150)
        overlay.fill(self.BLACK)
        screen.blit(overlay, (0, 0))

        self.draw_fancy_title(screen)

        self.play_button.draw(screen)
        self.quit_button.draw(screen)

        # Bouton settings
        settings_color = self.BLUE_GRAY_LIGHT if self.settings_hovered else self.BLUE_GRAY
        pygame.draw.rect(screen, settings_color, self.settings_button_rect, border_radius=10)
        pygame.draw.rect(screen, self.WHITE, self.settings_button_rect, 3, border_radius=10)
        screen.blit(self.settings_icon, (self.settings_button_rect.x + 5, self.settings_button_rect.y + 5))

        # Bouton scores
        scores_color = self.BLUE_GRAY_LIGHT if self.scores_hovered else self.BLUE_GRAY
        pygame.draw.rect(screen, scores_color, self.scores_button_rect, border_radius=10)
        pygame.draw.rect(screen, self.WHITE, self.scores_button_rect, 3, border_radius=10)
        screen.blit(self.scores_icon, (self.scores_button_rect.x + 5, self.scores_button_rect.y + 5))

        mouse_pos = pygame.mouse.get_pos()

        self.settings_hovered = self.settings_button_rect.collidepoint(mouse_pos)
        self.scores_hovered = self.scores_button_rect.collidepoint(mouse_pos)

        # === SON AU SURVOL ===
        def handle_hover(name, rect):
            is_hovered = rect.collidepoint(mouse_pos)
            if is_hovered and not self.hover_states[name]:
                if self.sound_hover:
                    self.sound_hover.play()
            self.hover_states[name] = is_hovered

        handle_hover("play", self.play_button.rect)
        handle_hover("quit", self.quit_button.rect)
        handle_hover("settings", self.settings_button_rect)
        handle_hover("scores", self.scores_button_rect)

    # =======================================================

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return "QUIT"

        if self.play_button.is_clicked(event):
            if self.sound_click:
                self.sound_click.play()
            return "START"

        if self.quit_button.is_clicked(event):
            if self.sound_click:
                self.sound_click.play()
            return "QUIT"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.settings_button_rect.collidepoint(event.pos):
                if self.sound_click:
                    self.sound_click.play()
                return "SETTINGS"

            if self.scores_button_rect.collidepoint(event.pos):
                if self.sound_click:
                    self.sound_click.play()
                return "SCORES"

        return None

