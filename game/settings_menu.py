import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION
from slider import Slider
from button_settings import Button
from settings import Setting
from music_manager import MusicManager
from button_manager import ButtonManager



class SettingsMenu:
    """Menu des paramètres avec curseurs audio et boutons."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Couleurs
        self.BLANC = (255, 255, 255)
        self.NOIR = (0, 0, 0)
        self.GRIS = (128, 128, 128)
        self.GRIS_CLAIR = (200, 200, 200)
        self.ORANGE = (255, 128, 0)
        self.ROUGE = (255, 0, 0)
        self.VIOLET = (160, 32, 240)
        
        # Paramètres locaux
        self.music_volume = 0.5
        self.sound_volume = 0.7
        self.fullscreen = False
        
        # Polices
        try:
            self.font_title = pygame.font.Font('./images/comic.ttf', 64)
            self.font_label = pygame.font.Font('./images/comic.ttf', 36)
            self.font_button = pygame.font.Font('./images/comic.ttf', 32)
        except:
            self.font_title = pygame.font.Font(None, 64)
            self.font_label = pygame.font.Font(None, 36)
            self.font_button = pygame.font.Font(None, 32)
        
        # Charger le fond
        try:
            bg_img = pygame.image.load('./images/572603.jpg')
            self.background = pygame.transform.scale(bg_img, (width, height))
        except:
            self.background = pygame.Surface((width, height))
            self.background.fill((50, 50, 50))
        
        # Position centrale
        center_x = width // 2
        
        # Curseur musique  SANS callback (version actuelle de ton Slider)
        self.music_slider = Slider(
            center_x - 150, 220, 300, 10,
            0.0, 1.0, self.music_volume,
            self.GRIS_CLAIR, self.ORANGE
        )
        
        # Curseur effets sonores ✅ SANS callback
        self.sound_slider = Slider(
            center_x - 150, 340, 300, 10,
            0.0, 1.0, self.sound_volume,
            self.GRIS_CLAIR, self.ROUGE
        )
        
        # Bouton plein écran
        self.fullscreen_button = Button(
            center_x - 100, 420, 200, 50,
            "Plein écran: OFF",
            self.font_button,
            self.VIOLET, self.ORANGE, self.BLANC
        )
        
        # Bouton retour
        self.back_button = Button(
            center_x - 75, 500, 150, 50,
            "Retour",
            self.font_button,
            self.GRIS, self.GRIS_CLAIR, self.BLANC
        )

    def set_music_volume(self, volume):
        """ VOLUME MUSIQUE RÉEL - change IMMÉDIATEMENT"""
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)

    def set_sound_volume(self, volume):
        """VOLUME SONS RÉEL"""
        self.sound_volume = volume

    def handle_event(self, event):
        """Gère les événements du menu."""
        # Curseurs ✅ SYNCHRO MANUELLE (pas de callback)
        if self.music_slider.handle_event(event):
            self.set_music_volume(self.music_slider.value)
            
        if self.sound_slider.handle_event(event):
            self.set_sound_volume(self.sound_slider.value)
            
        # Boutons
        if self.fullscreen_button.handle_event(event):
            self.fullscreen = not self.fullscreen
            self.fullscreen_button.text = "Plein écran: " + ("ON" if self.fullscreen else "OFF")
            
        if self.back_button.handle_event(event):
            return "BACK"
        
        return None

    def draw(self, screen):
        """Dessine le menu des paramètres."""
        # Fond
        screen.blit(self.background, (0, 0))
        
        # Overlay semi-transparent
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill(self.BLANC)
        screen.blit(overlay, (0, 0))
        
        # Titre
        title = self.font_title.render("PARAMÈTRES", True, self.ORANGE)
        title_rect = title.get_rect(center=(self.width // 2, 80))
        screen.blit(title, title_rect)
        
        # Musique
        music_label = self.font_label.render(
            f"Musique: {int(self.music_slider.value * 100)}%",
            True, self.NOIR
        )
        screen.blit(music_label, (self.width // 2 - 150, 180))
        self.music_slider.draw(screen)
        
        # Effets sonores
        sound_label = self.font_label.render(
            f"Effets sonores: {int(self.sound_slider.value * 100)}%",
            True, self.NOIR
        )
        screen.blit(sound_label, (self.width // 2 - 150, 300))
        self.sound_slider.draw(screen)
        
        # Boutons
        self.fullscreen_button.draw(screen)
        self.back_button.draw(screen)