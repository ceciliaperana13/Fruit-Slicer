import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION


class Slider:
    """Widget de curseur pour ajuster les valeurs."""
    
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, color, handle_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.color = color
        self.handle_color = handle_color
        self.dragging = False
        
        # Rectangle du curseur
        handle_x = self._value_to_x(initial_val)
        self.handle = pygame.Rect(handle_x - 10, y - 5, 20, height + 10)
    
    def _value_to_x(self, value):
        """Convertit une valeur en position x."""
        ratio = (value - self.min_val) / (self.max_val - self.min_val)
        return self.rect.x + int(ratio * self.rect.width)
    
    def _x_to_value(self, x):
        """Convertit une position x en valeur."""
        x = max(self.rect.x, min(x, self.rect.x + self.rect.width))
        ratio = (x - self.rect.x) / self.rect.width
        return self.min_val + ratio * (self.max_val - self.min_val)
    
    def handle_event(self, event):
        """Gère les événements de la souris."""
        if event.type == MOUSEBUTTONDOWN:
            if self.handle.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == MOUSEMOTION and self.dragging:
            self.value = self._x_to_value(event.pos[0])
            self.handle.x = self._value_to_x(self.value) - 10
            return True
        return False
    
    def draw(self, screen):
        """Dessine le curseur."""
        # Barre de fond
        pygame.draw.rect(screen, self.color, self.rect)
        # Curseur
        pygame.draw.rect(screen, self.handle_color, self.handle)
        pygame.draw.rect(screen, (0, 0, 0), self.handle, 2)


class Button:
    """Bouton cliquable."""
    
    def __init__(self, x, y, width, height, text, font, color, hover_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
    
    def handle_event(self, event):
        """Gère les événements de la souris."""
        if event.type == MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    def draw(self, screen):
        """Dessine le bouton."""
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=10)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class SettingsMenu:
    """Menu des paramètres avec curseurs audio et boutons."""
    
    def __init__(self, settings):
        self.settings = settings
        self.font_title = pygame.font.Font(None, 64)
        self.font_label = pygame.font.Font(None, 36)
        self.font_button = pygame.font.Font(None, 32)
        
        # Position centrale
        center_x = settings.screen_width // 2
        
        # Curseur musique
        self.music_slider = Slider(
            center_x - 150, 200, 300, 10,
            0.0, 1.0, settings.music_volume,
            settings.GRIS_CLAIR, settings.ORANGE
        )
        
        # Curseur effets sonores
        self.sound_slider = Slider(
            center_x - 150, 320, 300, 10,
            0.0, 1.0, settings.sound_volume,
            settings.GRIS_CLAIR, settings.ROUGE
        )
        
        # Bouton plein écran
        self.fullscreen_button = Button(
            center_x - 100, 420, 200, 50,
            "Plein écran: " + ("ON" if settings.fullscreen else "OFF"),
            self.font_button,
            settings.VIOLET, settings.ORANGE, settings.BLANC
        )
        
        # Bouton retour
        self.back_button = Button(
            center_x - 75, 500, 150, 50,
            "Retour",
            self.font_button,
            settings.GRIS, settings.GRIS_CLAIR, settings.BLANC
        )
    
    def handle_event(self, event):
        """Gère les événements du menu."""
        # Curseurs
        if self.music_slider.handle_event(event):
            self.settings.set_music_volume(self.music_slider.value)
        
        if self.sound_slider.handle_event(event):
            self.settings.set_sound_volume(self.sound_slider.value)
        
        # Boutons
        if self.fullscreen_button.handle_event(event):
            self.settings.fullscreen = not self.settings.fullscreen
            self.fullscreen_button.text = "Plein écran: " + ("ON" if self.settings.fullscreen else "OFF")
        
        if self.back_button.handle_event(event):
            return False  # Fermer le menu
        
        return True  # Garder le menu ouvert
    
    def draw(self, screen):
        """Dessine le menu des paramètres."""
        # Fond semi-transparent
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        overlay.set_alpha(230)
        overlay.fill(self.settings.BLANC)
        screen.blit(overlay, (0, 0))
        
        # Titre
        title = self.font_title.render("PARAMÈTRES", True, self.settings.NOIR)
        title_rect = title.get_rect(center=(self.settings.screen_width // 2, 80))
        screen.blit(title, title_rect)
        
        # Label musique
        music_label = self.font_label.render(
            f"Musique: {int(self.music_slider.value * 100)}%",
            True, self.settings.NOIR
        )
        screen.blit(music_label, (self.settings.screen_width // 2 - 150, 160))
        self.music_slider.draw(screen)
        
        # Label effets sonores
        sound_label = self.font_label.render(
            f"Effets sonores: {int(self.sound_slider.value * 100)}%",
            True, self.settings.NOIR
        )
        screen.blit(sound_label, (self.settings.screen_width // 2 - 150, 280))
        self.sound_slider.draw(screen)
        
        # Boutons
        self.fullscreen_button.draw(screen)
        self.back_button.draw(screen)