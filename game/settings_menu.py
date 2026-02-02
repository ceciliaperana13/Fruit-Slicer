import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION
from slider import Slider
from button_settings import Button
from settings import Setting

class SettingsMenu:
    """Settings menu with audio sliders and buttons."""

    def __init__(self, width, height, settings=None):
        self.width = width
        self.height = height
        
        # Reference to settings to control impact sound volume
        self.settings = settings
        
        # Colors
        self.BLANC = (255, 255, 255)
        self.NOIR = (0, 0, 0)
        self.GRIS = (128, 128, 128)
        self.GRIS_CLAIR = (200, 200, 200)
        self.ORANGE = (255, 128, 0)
        self.ROUGE = (255, 0, 0)
        self.VIOLET = (160, 32, 240)
        
        # Local parameters
        self.music_volume = settings.music_volume if settings else 0.5
        self.sound_volume = settings.sound_volume if settings else 0.7
        self.fullscreen = False
        
        # Fonts
        try:
            self.font_title = pygame.font.Font('./images/comic.ttf', 64)
            self.font_label = pygame.font.Font('./images/comic.ttf', 36)
            self.font_button = pygame.font.Font('./images/comic.ttf', 32)
        except:
            self.font_title = pygame.font.Font(None, 64)
            self.font_label = pygame.font.Font(None, 36)
            self.font_button = pygame.font.Font(None, 32)
        
        # Load background
        try:
            bg_img = pygame.image.load('./images/572603.jpg')
            self.background = pygame.transform.scale(bg_img, (width, height))
        except:
            self.background = pygame.Surface((width, height))
            self.background.fill((50, 50, 50))
        
        # Center position
        center_x = width // 2
        
        # Music slider WITHOUT callback (current version of your Slider)
        self.music_slider = Slider(
            center_x - 150, 220, 300, 10,
            0.0, 1.0, self.music_volume,
            self.GRIS_CLAIR, self.ORANGE
        )
        
        # Sound effects slider (impact sound) WITHOUT callback
        self.sound_slider = Slider(
            center_x - 150, 340, 300, 10,
            0.0, 1.0, self.sound_volume,
            self.GRIS_CLAIR, self.ROUGE
        )
        
        # Fullscreen button
        self.fullscreen_button = Button(
            center_x - 100, 420, 200, 50,
            "Fullscreen: OFF",
            self.font_button,
            self.VIOLET, self.ORANGE, self.BLANC
        )
        
        # Back button
        self.back_button = Button(
            center_x - 75, 500, 150, 50,
            "Back",
            self.font_button,
            self.GRIS, self.GRIS_CLAIR, self.BLANC
        )

    def set_music_volume(self, volume):
        """REAL MUSIC VOLUME - changes IMMEDIATELY"""
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)
        # Also update in settings if available
        if self.settings:
            self.settings.set_music_volume(volume)

    def set_sound_volume(self, volume):
        """REAL SOUND VOLUME - updates impact sound"""
        self.sound_volume = volume
        # Update impact sound volume in settings
        if self.settings:
            self.settings.set_sound_volume(volume)

    def handle_event(self, event):
        """Handles menu events."""
        # Sliders - MANUAL SYNC (no callback)
        if self.music_slider.handle_event(event):
            self.set_music_volume(self.music_slider.value)
            
        if self.sound_slider.handle_event(event):
            self.set_sound_volume(self.sound_slider.value)
            
        # Buttons
        if self.fullscreen_button.handle_event(event):
            self.fullscreen = not self.fullscreen
            self.fullscreen_button.text = "Fullscreen: " + ("ON" if self.fullscreen else "OFF")
            
        if self.back_button.handle_event(event):
            return "BACK"
        
        return None

    def draw(self, screen):
        """Draw the settings menu."""
        # Background
        screen.blit(self.background, (0, 0))
        
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill(self.BLANC)
        screen.blit(overlay, (0, 0))
        
        # Title
        title = self.font_title.render("SETTINGS", True, self.ORANGE)
        title_rect = title.get_rect(center=(self.width // 2, 80))
        screen.blit(title, title_rect)
        
        # Music
        music_label = self.font_label.render(
            f"Music: {int(self.music_slider.value * 100)}%",
            True, self.NOIR
        )
        screen.blit(music_label, (self.width // 2 - 150, 180))
        self.music_slider.draw(screen)
        
        # Sound effects (impact sound)
        sound_label = self.font_label.render(
            f"Impact sound: {int(self.sound_slider.value * 100)}%",
            True, self.NOIR
        )
        screen.blit(sound_label, (self.width // 2 - 150, 300))
        self.sound_slider.draw(screen)
        
        # Buttons
        self.fullscreen_button.draw(screen)
        self.back_button.draw(screen)
