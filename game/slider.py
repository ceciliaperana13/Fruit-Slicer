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
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        # Curseur
        pygame.draw.rect(screen, self.handle_color, self.handle, border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), self.handle, 2, border_radius=5)