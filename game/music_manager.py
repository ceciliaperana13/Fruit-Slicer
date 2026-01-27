import pygame
import os
from button_manager import*




class MusicManager:
    """Gestionnaire de musique avec sélection et contrôle"""
    
    def __init__(self):
        """Initialise le gestionnaire de musique"""
        pygame.mixer.init()
        
        # Dossier contenant les musiques
        self.music_folder = "musique"
        
        # Liste des musiques disponibles (nom d'affichage, fichier)
        self.available_music = [
            ("Zelda", "/musique/Zelda_Main_Theme_Song.mp3"),
            ("Final FANTASY", "/musique/Liberi_Fatali_[FINAL FANTASY VIII].mp3"),
            ("Primal", "/musique/Primal Judgment (From Final Fantasy XIV).mp3"),
            ("NieRAutomata", "/musique/Birth of a Wish (NieRAutomata Original Soundtrack)【Audio】.mp3"),
            ("No Music", None)  # Option sans musique
        ]
        
        
        
        # État de lecture
        self.is_playing = False
        self.music_enabled = True
        
        
    
    def get_music_list(self):
        """Retourne la liste des noms de musiques disponibles"""
        return [name for name, _ in self.available_music]
    
    def get_current_music_name(self):
        """Retourne le nom de la musique actuelle"""
        return self.available_music[self.current_music_index][0]
    
    def get_current_music_index(self):
        """Retourne l'index de la musique actuelle"""
        return self.current_music_index
    
    def set_music(self, index):
        """Change la musique sélectionnée
        
        Args:
            index: Index de la musique dans la liste
        """
        if 0 <= index < len(self.available_music):
            self.current_music_index = index
            self.stop()
            if self.music_enabled:
                self.play()
    
    
    
    def play(self):
        """Démarre la lecture de la musique actuelle"""
        if not self.music_enabled:
            return
        
        music_name, music_file = self.available_music[self.current_music_index]
        
        # Si "No Music" est sélectionné
        if music_file is None:
            self.stop()
            return
        
        music_path = os.path.join(self.music_folder, music_file)
        
        # Vérifier si le fichier existe
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play(-1)  # -1 = boucle infinie
                self.is_playing = True
            except Exception as e:
                print(f"Erreur lors du chargement de la musique {music_file}: {e}")
                self.is_playing = False
        else:
            print(f"Fichier musical introuvable: {music_path}")
            # Essayer de jouer un son par défaut ou continuer sans musique
            self.is_playing = False
    
    def stop(self):
        """Arrête la musique"""
        pygame.mixer.music.stop()
        self.is_playing = False
    
    
    
    
    def get_volume(self):
        """Retourne le volume actuel"""
        return self.volume
    
    
    def is_music_enabled(self):
        """Retourne True si la musique est activée"""
        return self.music_enabled