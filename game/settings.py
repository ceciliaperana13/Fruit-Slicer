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
        self.fullscreen = False # dois changer et mettr epleine ecran si besoin#####################################################

        # Musique et sons
        self.music_file = "./musique/Swing De Chocobo (Final Fantasy Series).mp3"
        self.music_volume = 0.5  # Volume entre 0.0 et 1.0
        self.sound_volume = 0.7  # Volume des effets sonores
        
        # Son d'impact (clic/slice)
        self.impact_sound_file = "./musique/impact (1).mp3"  
        self.impact_sound = None
        self.load_impact_sound()

    def apply_screen(self):
        """Retourne la surface de l'écran selon le mode plein écran."""
        if self.fullscreen:
            screen = pygame.display.set_mode((0, 0), FULLSCREEN)
        else:
            screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        return screen

    def play_music(self):
        """Lance la lecture de la musique de fond."""
        if self.music_file:
            try:
                pygame.mixer.music.load(self.music_file)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # Boucle infinie
            except pygame.error as e:
                print(f"Impossible de charger la musique: {e}")
                print(f"Vérifiez que le fichier existe: {self.music_file}")

    def set_music_volume(self, volume):
        """Ajuste le volume de la musique."""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sound_volume(self, volume):
        """Ajuste le volume des effets sonores (y compris le son d'impact)."""
        self.sound_volume = max(0.0, min(1.0, volume))
        if self.impact_sound:
            self.impact_sound.set_volume(self.sound_volume)
    
    def load_impact_sound(self):
        """Charge le son d'impact."""
        try:
            self.impact_sound = pygame.mixer.Sound(self.impact_sound_file)
            self.impact_sound.set_volume(self.sound_volume)
            print(f"Son d'impact chargé: {self.impact_sound_file}")
        except pygame.error as e:
            print(f"Impossible de charger le son d'impact: {e}")
            print(f"Vérifiez que le fichier existe: {self.impact_sound_file}")
            self.impact_sound = None
    
    def play_impact_sound(self):
        """Joue le son d'impact (appelé lors d'un clic sur un fruit/lettre)."""
        if self.impact_sound:
            self.impact_sound.play()
    
    def set_impact_sound_file(self, filepath):
        """Change le fichier du son d'impact."""
        self.impact_sound_file = filepath
        self.load_impact_sound()