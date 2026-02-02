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
        # Nouvelles couleurs gris-bleu
        self.BLUE_GRAY = (70, 90, 120)
        self.BLUE_GRAY_LIGHT = (100, 120, 150)
        self.BLUE_GRAY_DARK = (50, 70, 100)
        # Couleurs pour titre Final Fantasy
        self.TITLE_BLUE = (70, 130, 180)    # Bleu acier sobre
        self.TITLE_DARK_BLUE = (25, 60, 100)  # Bleu foncé pour l'ombre
        
        # === CHARGER L'IMAGE DE FOND ===
        try:
            bg_img = pygame.image.load('./images/572603.jpg')
            self.background = pygame.transform.scale(bg_img, (width, height))
        except:
            # Fond par défaut si l'image n'existe pas
            self.background = pygame.Surface((width, height))
            self.background.fill(self.BLACK)
            print("Warning: Background image not found, using black background")
        
        # === CHARGER LES ICÔNES ===
        try:
            self.scores_icon = pygame.image.load('./images/scores.png')
            self.scores_icon = pygame.transform.scale(self.scores_icon, (50, 50))
        except:
            # Créer une icône par défaut si l'image n'existe pas
            self.scores_icon = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.rect(self.scores_icon, (255, 128, 180), (10, 20, 30, 25), border_radius=5)
            print("Warning: scores_icon.png not found, using default icon")
        
        try:
            self.settings_icon = pygame.image.load('./images/fruit_settings.png')
            self.settings_icon = pygame.transform.scale(self.settings_icon, (50, 50))
        except:
            # Créer une icône d'engrenage par défaut
            self.settings_icon = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(self.settings_icon, (200, 200, 200), (25, 25), 20, 3)
            pygame.draw.circle(self.settings_icon, (200, 200, 200), (25, 25), 10)
            print("Warning: settings_icon.png not found, using default icon")
        
        # === FONTS ===
        try:
            self.title_font = pygame.font.Font('./images/comic.ttf', 80)
            self.button_font = pygame.font.Font('./images/comic.ttf', 35)
        except:
            self.title_font = pygame.font.SysFont("arialblack", 80)
            self.button_font = pygame.font.SysFont("arial", 35, bold=True)
            print("Warning: comic.ttf not found, using default fonts")
        
        # === BOUTONS PRINCIPAUX (GRIS-BLEU) - Position plus basse sans gap ===
        button_y_start = height - 180  # Encore plus bas dans la fenêtre
        button_gap = 0  # Pas de gap entre les boutons
        
        self.play_button = Button_menu(
            "PLAY", 
            width//2 - 150, button_y_start, 300, 70, 
            self.BLUE_GRAY, self.BLUE_GRAY_LIGHT, 
            self.button_font, self.BLUE_GRAY_DARK
        )
        
        self.quit_button = Button_menu(
            "QUIT", 
            width//2 - 150, button_y_start + 70 + button_gap, 300, 70, 
            self.RED, self.ORANGE, 
            self.button_font, self.BROWN
        )

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
        
        
        # Settings en haut à droite
        self.settings_button_rect = pygame.Rect(width - 70, 20, 60, 60)
        
        # Scores en haut à gauche
        self.scores_button_rect = pygame.Rect(10, 20, 60, 60)
        
        # États de hover
        self.settings_hovered = False
        self.scores_hovered = False
    
    def draw_fancy_title(self, screen):
        """Dessine un titre fantaisiste style Final Fantasy avec effet de lueur"""
        title_line1 = "FINAL FANTASY"
        title_line2 = "FRUITS"
        
        # Position du titre (plus bas)
        title_y1 = 180
        title_y2 = 260
        
        # Dessiner les deux lignes du titre
        for title_text, title_y in [(title_line1, title_y1), (title_line2, title_y2)]:
            # Effet de lueur bleu sobre
            for offset in range(6, 0, -2):
                shadow_surface = self.title_font.render(title_text, True, self.TITLE_DARK_BLUE)
                shadow_surface.set_alpha(40)
                shadow_rect = shadow_surface.get_rect(center=(self.width//2, title_y))
                screen.blit(shadow_surface, (shadow_rect.x + offset, shadow_rect.y + offset))
            
            # Ombre noire pour la profondeur
            shadow_text = self.title_font.render(title_text, True, self.BLACK)
            shadow_rect = shadow_text.get_rect(center=(self.width//2 + 3, title_y + 3))
            screen.blit(shadow_text, shadow_rect)
            
            # Texte principal bleu sobre
            main_text = self.title_font.render(title_text, True, self.TITLE_BLUE)
            main_rect = main_text.get_rect(center=(self.width//2, title_y))
            screen.blit(main_text, main_rect)
            
            # Contour blanc léger
            white_text = self.title_font.render(title_text, True, self.WHITE)
            white_text.set_alpha(80)
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                white_rect = white_text.get_rect(center=(self.width//2 + dx, title_y + dy))
                screen.blit(white_text, white_rect)
    
    def draw(self, screen):
        """Dessine le menu principal"""
        # Dessiner le fond d'écran du jeu
        screen.blit(self.background, (0, 0))
        
        # Ajouter un overlay semi-transparent pour améliorer la lisibilité
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(150)  # Transparence 
        overlay.fill(self.BLACK)
        screen.blit(overlay, (0, 0))
        
        # Titre fantaisiste style Final Fantasy
        self.draw_fancy_title(screen)
        
        # Dessiner les boutons principaux
        self.play_button.draw(screen)
        self.quit_button.draw(screen)
        
        # === DESSINER BOUTON SETTINGS (en haut à droite) ===
        # Fond du bouton avec effet hover
        settings_color = self.BLUE_GRAY_LIGHT if self.settings_hovered else self.BLUE_GRAY
        pygame.draw.rect(screen, settings_color, self.settings_button_rect, border_radius=10)
        pygame.draw.rect(screen, self.WHITE, self.settings_button_rect, 3, border_radius=10)
        
        # Centrer l'icône dans le bouton
        icon_x = self.settings_button_rect.x + (self.settings_button_rect.width - 50) // 2
        icon_y = self.settings_button_rect.y + (self.settings_button_rect.height - 50) // 2
        screen.blit(self.settings_icon, (icon_x, icon_y))
        
        # === DESSINER BOUTON SCORES (en haut à gauche) ===
        # Fond du bouton avec effet hover
        scores_color = self.BLUE_GRAY_LIGHT if self.scores_hovered else self.BLUE_GRAY
        pygame.draw.rect(screen, scores_color, self.scores_button_rect, border_radius=10)
        pygame.draw.rect(screen, self.WHITE, self.scores_button_rect, 3, border_radius=10)
        
        # Centrer l'icône dans le bouton
        icon_x = self.scores_button_rect.x + (self.scores_button_rect.width - 50) // 2
        icon_y = self.scores_button_rect.y + (self.scores_button_rect.height - 50) // 2
        screen.blit(self.scores_icon, (icon_x, icon_y))
        
        # Mettre à jour les états hover
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

    
    def handle_event(self, event):
        """Gère les événements du menu et retourne l'action correspondante"""
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
        
        # Gestion des clics sur les boutons icônes
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