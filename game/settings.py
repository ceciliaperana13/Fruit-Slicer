import pygame
from pygame.locals import FULLSCREEN


class Setting:
    """Classe pour gérer les paramètres du jeu Fruit Slicer."""
    
    # Couleurs
    NOIR = (0, 0, 0)
    BLANC = (255, 255, 255)
    ORANGE = (255, 128, 0)
    ROUGE = (255, 0, 0)
    MARRON = (88, 41, 0)
    VIOLET = (160, 32, 240)
    GRIS = (128, 128, 128)
    GRIS_CLAIR = (200, 200, 200)
    VERT = (0, 200, 0)
    BLEU = (0, 100, 255)
    
    def __init__(self):
        # Paramètres de l'écran
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = self.BLANC

        # Option plein écran
        self.fullscreen = False

        # Musique et sons
        self.music_file = "musique/Zelda_Main_Theme_Song.mp3"
        self.music_volume = 0.5  # Volume entre 0.0 et 1.0
        self.sound_volume = 0.7  # Volume des effets sonores

    def apply_screen(self):
        """Retourne la surface de l'écran selon le mode plein écran."""
        if self.fullscreen:
            screen = pygame.display.set_mode((0, 0), FULLSCREEN)
        else:
            screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        return screen

    def play_music(self):
      if self.music_file:
        try:
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)  # Boucle infinie
        except pygame.error as e:
            print(f"⚠️  Impossible de charger la musique: {e}")
            print(f"   Vérifiez que le fichier existe: {self.music_file}")

    def set_music_volume(self, volume):
        """Ajuste le volume de la musique."""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sound_volume(self, volume):
        """Ajuste le volume des effets sonores."""
        self.sound_volume = max(0.0, min(1.0, volume))