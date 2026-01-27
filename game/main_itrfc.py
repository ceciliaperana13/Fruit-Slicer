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
        
        # === CHARGER L'IMAGE DE FOND ===
        try:
            bg_img = pygame.image.load('./images/572603.jpg')
            self.background = pygame.transform.scale(bg_img, (width, height))
        except:
            # Fond par défaut si l'image n'existe pas
            self.background = pygame.Surface((width, height))
            self.background.fill(self.BLACK)
            print("Warning: Background image not found, using black background")
        
        # === FONTS ===
        # Essayer de charger la police comic
        try:
            self.title_font = pygame.font.Font('./images/comic.ttf', 80)
            self.button_font = pygame.font.Font('./images/comic.ttf', 35)
        except:
            # Police par défaut si comic.ttf n'existe pas
            self.title_font = pygame.font.SysFont("arialblack", 80)
            self.button_font = pygame.font.SysFont("arial", 35, bold=True)
            print("Warning: comic.ttf not found, using default fonts")
        
        # === BOUTONS ===
        self.play_button = Button_menu(
            "PLAY", 
            width//2 - 150, 320, 300, 70, 
            self.PURPLE, self.ORANGE, 
            self.button_font, self.BROWN
        )
        
        self.quit_button = Button_menu(
            "QUIT", 
            width//2 - 150, 420, 300, 70, 
            self.RED, self.ORANGE, 
            self.button_font, self.BROWN
        )
        
        self.settings_button = Button_menu(
            "SETTINGS", 
            40, height//2 - 35, 200, 70, 
            self.PURPLE, self.ORANGE, 
            self.button_font, self.BROWN
        )
        
        self.scores_button = Button_menu(
            "SCORES", 
            width - 240, height//2 - 35, 200, 70, 
            self.PURPLE, self.ORANGE, 
            self.button_font, self.BROWN
        )
    
    def draw(self, screen):
        """Dessine le menu principal"""
        # Dessiner le fond d'écran du jeu
        screen.blit(self.background, (0, 0))
        
        # Ajouter un overlay semi-transparent pour améliorer la lisibilité
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(150)  # Transparence (0-255)
        overlay.fill(self.BLACK)
        screen.blit(overlay, (0, 0))
        
        # Titre
        title_text = self.title_font.render("FINAL FANTASY FRUITS", True, self.ORANGE)
        title_rect = title_text.get_rect(center=(self.width//2, 150))
        screen.blit(title_text, title_rect)
        
        # Sous-titre
        subtitle = self.button_font.render("MAIN MENU", True, self.WHITE)
        screen.blit(subtitle, (self.width//2 - subtitle.get_width()//2, 230))
        
        # Dessiner les boutons
        self.play_button.draw(screen)
        self.quit_button.draw(screen)
        self.settings_button.draw(screen)
        self.scores_button.draw(screen)
    
    def handle_event(self, event):
        """Gère les événements du menu et retourne l'action correspondante"""
        if event.type == pygame.QUIT:
            return "QUIT"
        
        if self.play_button.is_clicked(event):
            return "START"
        
        if self.quit_button.is_clicked(event):
            return "QUIT"
        
        if self.settings_button.is_clicked(event):
            return "SETTINGS"
        
        if self.scores_button.is_clicked(event):
            return "SCORES"
        
        return None
