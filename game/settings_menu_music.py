import pygame
from pygame.locals import *


class SettingsMenu:
    """Menu de paramètres avec sélection de musique par boutons PNG"""
    
    def __init__(self, width=800, height=580, music_manager=None):
        """Initialise le menu de settings
        
        Args:
            width: Largeur de l'écran
            height: Hauteur de l'écran
            music_manager: Instance du gestionnaire de musique
        """
        self.width = width
        self.height = height
        self.music_manager = music_manager
        
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (200, 200, 200)
        self.BLUE = (59, 130, 246)
        self.PURPLE = (147, 51, 234)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.GOLD = (255, 215, 0)
        
        # Polices
        self.font_large = pygame.font.Font(None, 60)
        self.font_medium = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 30)
        self.font_tiny = pygame.font.Font(None, 24)
    
    def draw_gradient_background(self, surface):
        """Dessine un fond dégradé"""
        for i in range(self.height):
            ratio = i / self.height
            r = int(20 * (1 - ratio) + 40 * ratio)
            g = int(20 * (1 - ratio) + 40 * ratio)
            b = int(60 * (1 - ratio) + 80 * ratio)
            pygame.draw.line(surface, (r, g, b), (0, i), (self.width, i))
    
    def draw(self, surface):
        """Dessine le menu de settings"""
        # Fond dégradé
        self.draw_gradient_background(surface)
        
        # Titre
        title_text = self.font_large.render("MUSIC SETTINGS", True, self.GOLD)
        title_rect = title_text.get_rect(center=(self.width / 2, 60))
        surface.blit(title_text, title_rect)
        
        # Sous-titre
        subtitle_text = self.font_small.render("Select your music:", True, self.WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(self.width / 2, 120))
        surface.blit(subtitle_text, subtitle_rect)
        
        # === Section Boutons de Musique ===
        if self.music_manager:
            music_buttons = self.music_manager.get_music_buttons()
            
            # Dessiner tous les boutons
            for button in music_buttons:
                button.draw(surface, self.font_tiny)
        
        # === Section Volume ===
        y_offset = 480
        
        # Titre de la section
        volume_title = self.font_medium.render("Volume Control", True, self.WHITE)
        volume_rect = volume_title.get_rect(center=(self.width / 2, y_offset))
        surface.blit(volume_title, volume_rect)
        
        if self.music_manager:
            y_offset += 50
            
            # Barre de volume
            volume = self.music_manager.get_volume()
            bar_width = 500
            bar_height = 30
            bar_x = (self.width - bar_width) / 2
            bar_y = y_offset
            
            # Fond de la barre
            pygame.draw.rect(surface, self.GRAY, (bar_x, bar_y, bar_width, bar_height), border_radius=15)
            
            # Barre de volume remplie
            filled_width = int(bar_width * volume)
            if filled_width > 0:
                pygame.draw.rect(surface, self.BLUE, (bar_x, bar_y, filled_width, bar_height), border_radius=15)
            
            # Contour
            pygame.draw.rect(surface, self.WHITE, (bar_x, bar_y, bar_width, bar_height), 2, border_radius=15)
            
            # Pourcentage
            percent_text = self.font_small.render(f"{int(volume * 100)}%", True, self.WHITE)
            percent_rect = percent_text.get_rect(center=(self.width / 2, bar_y - 25))
            surface.blit(percent_text, percent_rect)
            
            # Icônes volume
            if volume == 0:
                icon = "🔇"
            elif volume < 0.3:
                icon = "🔈"
            elif volume < 0.7:
                icon = "🔉"
            else:
                icon = "🔊"
            
            icon_text = self.font_medium.render(icon, True, self.WHITE)
            surface.blit(icon_text, (bar_x - 60, bar_y - 10))
            
            # État de la musique
            status = "♪ Playing" if self.music_manager.is_playing else "⏸ Stopped"
            status_color = self.GREEN if self.music_manager.is_playing else self.RED
            status_text = self.font_small.render(status, True, status_color)
            status_rect = status_text.get_rect(center=(self.width / 2, bar_y + 45))
            surface.blit(status_text, status_rect)
        
        # === Instructions ===
        y_offset = self.height - 35
        
        instructions = "Click on album cover to select  |  ↑↓ : Volume  |  M : Toggle  |  ESC : Back"
        text = self.font_tiny.render(instructions, True, self.LIGHT_GRAY)
        text_rect = text.get_rect(center=(self.width / 2, y_offset))
        surface.blit(text, text_rect)
    
    def handle_event(self, event):
        """Gère les événements du menu
        
        Args:
            event: Événement pygame
            
        Returns:
            str: "BACK" pour retourner au menu, "CONTINUE" sinon
        """
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return "BACK"
            
            if self.music_manager:
                # Contrôle volume
                if event.key == K_UP:
                    self.music_manager.volume_up(0.1)
                elif event.key == K_DOWN:
                    self.music_manager.volume_down(0.1)
                
                # Toggle musique
                elif event.key == K_m:
                    self.music_manager.toggle_music()
                
                # Navigation avec flèches (optionnel)
                elif event.key == K_LEFT:
                    self.music_manager.previous_music()
                elif event.key == K_RIGHT:
                    self.music_manager.next_music()
        
        # Gestion des clics sur les boutons de musique
        if self.music_manager:
            music_buttons = self.music_manager.get_music_buttons()
            for button in music_buttons:
                if button.handle_event(event):
                    # Bouton cliqué
                    self.music_manager.handle_button_click(button.music_index)
        
        return "CONTINUE"