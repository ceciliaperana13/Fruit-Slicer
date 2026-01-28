import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION
import os


class ButtonManager:
    """Bouton cliquable avec support d'images PNG."""
    
    def __init__(self, x, y, width, height, text="", font=None, color=(100, 100, 100), 
                 hover_color=(150, 150, 150), text_color=(255, 255, 255), 
                 image_path=None, hover_image_path=None):
        """Initialise un bouton
        
        Args:
            x, y: Position du bouton
            width, height: Taille du bouton
            text: Texte du bouton (optionnel si image)
            font: Police pour le texte
            color: Couleur normale (si pas d'image)
            hover_color: Couleur au survol (si pas d'image)
            text_color: Couleur du texte
            image_path: Chemin vers l'image PNG normale
            hover_image_path: Chemin vers l'image PNG au survol (optionnel)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
        
        # Support des images
        self.image = None
        self.hover_image = None
        self.use_image = False
        
        # Charger les images si fournies
        if image_path and os.path.exists(image_path):
            try:
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image, (width, height))
                self.use_image = True
                
                # Charger l'image de survol si fournie
                if hover_image_path and os.path.exists(hover_image_path):
                    self.hover_image = pygame.image.load(hover_image_path)
                    self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
                else:
                    # Si pas d'image de survol, créer un effet de luminosité
                    self.hover_image = self.image.copy()
                    self.hover_image.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_ADD)
            except Exception as e:
                print(f"Erreur lors du chargement de l'image {image_path}: {e}")
                self.use_image = False
    
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
        if self.use_image:
            # Dessiner l'image
            current_image = self.hover_image if self.hovered else self.image
            screen.blit(current_image, self.rect)
            
            # Ajouter un contour si survolé
            if self.hovered:
                pygame.draw.rect(screen, (255, 215, 0), self.rect, 3, border_radius=10)
        else:
            # Dessiner un bouton rectangulaire classique
            color = self.hover_color if self.hovered else self.color
            pygame.draw.rect(screen, color, self.rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=10)
        
        # Dessiner le texte si présent
        if self.text and self.font:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)


class ImageButton:
    """Bouton avec image PNG et état sélectionné."""
    
    def __init__(self, x, y, width, height, image_path, music_index, music_name=""):
        """Initialise un bouton d'image pour la sélection de musique
        
        Args:
            x, y: Position du bouton
            width, height: Taille du bouton
            image_path: Chemin vers l'image PNG
            music_index: Index de la musique associée
            music_name: Nom de la musique (pour affichage)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.music_index = music_index
        self.music_name = music_name
        self.hovered = False
        self.selected = False
        
        # Charger l'image
        self.image = None
        if os.path.exists(image_path):
            try:
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image, (width, height))
            except Exception as e:
                print(f"Erreur lors du chargement de {image_path}: {e}")
        
        # Créer une version assombrie pour l'effet hover
        if self.image:
            self.hover_image = self.image.copy()
            self.hover_image.fill((30, 30, 30), special_flags=pygame.BLEND_RGB_ADD)
            
            self.selected_image = self.image.copy()
            self.selected_image.fill((100, 100, 0), special_flags=pygame.BLEND_RGB_ADD)
    
    def handle_event(self, event):
        """Gère les événements de la souris."""
        if event.type == MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    def set_selected(self, selected):
        """Définit l'état de sélection du bouton."""
        self.selected = selected
    
    def draw(self, screen, font=None):
        """Dessine le bouton avec l'image."""
        if not self.image:
            # Fallback: dessiner un rectangle si pas d'image
            color = (100, 200, 100) if self.selected else (100, 100, 100)
            if self.hovered:
                color = (150, 150, 150)
            pygame.draw.rect(screen, color, self.rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=10)
        else:
            # Dessiner l'image
            if self.selected:
                screen.blit(self.selected_image, self.rect)
            elif self.hovered:
                screen.blit(self.hover_image, self.rect)
            else:
                screen.blit(self.image, self.rect)
        
        # Contour de sélection
        if self.selected:
            pygame.draw.rect(screen, (255, 215, 0), self.rect, 4, border_radius=10)
        elif self.hovered:
            pygame.draw.rect(screen, (200, 200, 200), self.rect, 3, border_radius=10)
        
        # Afficher le nom de la musique en dessous
        if self.music_name and font:
            text_surface = font.render(self.music_name, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.bottom + 20))
            screen.blit(text_surface, text_rect)