import pygame
from pygame.locals import FULLSCREEN


class Setting:
    """Class to manage Fruit Slicer game settings."""
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    ORANGE = (255, 128, 0)
    RED = (255, 0, 0)
    BROWN = (88, 41, 0)
    PURPLE = (160, 32, 240)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    GREEN = (0, 200, 0)
    BLUE = (0, 100, 255)
    
    def __init__(self):
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = self.WHITE

        # Fullscreen option
        self.fullscreen = False

        # Music and sounds
        self.music_file = "./musique/Swing De Chocobo (Final Fantasy Series).mp3"
        self.music_volume = 0.5  # Volume between 0.0 and 1.0
        self.sound_volume = 0.7  # Sound effects volume
        
        # Single impact sound for all elements
        self.impact_sound_file = "./musique/impact.mp3"
        self.impact_sound = None
        self.load_impact_sound()

    def apply_screen(self):
        """Return the screen surface according to fullscreen mode."""
        if self.fullscreen:
            screen = pygame.display.set_mode((0, 0), FULLSCREEN)
        else:
            screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        return screen

    def play_music(self):
        """Start playing background music."""
        if self.music_file:
            try:
                pygame.mixer.music.load(self.music_file)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # Infinite loop
            except pygame.error as e:
                print(f"Unable to load music: {e}")
                print(f"Check that the file exists: {self.music_file}")

    def set_music_volume(self, volume):
        """Adjust the music volume."""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sound_volume(self, volume):
        """Adjust the sound effects volume."""
        self.sound_volume = max(0.0, min(1.0, volume))
        if self.impact_sound:
            self.impact_sound.set_volume(self.sound_volume)
    
    def load_impact_sound(self):
        """Load the impact sound effect."""
        try:
            self.impact_sound = pygame.mixer.Sound(self.impact_sound_file)
            self.impact_sound.set_volume(self.sound_volume)
            print(f"✓ Impact sound loaded: {self.impact_sound_file}")
        except pygame.error as e:
            print(f"⚠ Unable to load impact sound: {e}")
            print(f"Check that the file exists: {self.impact_sound_file}")
            self.impact_sound = None
    
    def play_impact_sound(self):
        """Play the impact sound."""
        if self.impact_sound:
            self.impact_sound.play()
