import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

class Slider:
    """A slider widget to adjust numerical values (e.g., volume)."""
    
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, color, handle_color):
        """
        Initialize the slider.
        
        Args:
            x, y: Top-left coordinates of the slider bar.
            width, height: Dimensions of the slider bar.
            min_val, max_val: Minimum and maximum slider values.
            initial_val: Starting value of the slider.
            color: Color of the slider bar.
            handle_color: Color of the draggable handle.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.color = color
        self.handle_color = handle_color
        self.dragging = False
        
        # Initial handle rectangle
        handle_x = self._value_to_x(initial_val)
        self.handle = pygame.Rect(handle_x - 10, y - 5, 20, height + 10)
    
    def _value_to_x(self, value):
        """Convert a slider value to an x-coordinate for the handle."""
        ratio = (value - self.min_val) / (self.max_val - self.min_val)
        return self.rect.x + int(ratio * self.rect.width)
    
    def _x_to_value(self, x):
        """Convert an x-coordinate to a slider value."""
        x = max(self.rect.x, min(x, self.rect.x + self.rect.width))
        ratio = (x - self.rect.x) / self.rect.width
        return self.min_val + ratio * (self.max_val - self.min_val)
    
    def handle_event(self, event):
        """
        Handle mouse events for the slider.
        
        Returns True if the value changed, else False.
        """
        if event.type == MOUSEBUTTONDOWN:
            if self.handle.collidepoint(event.pos):
                self.dragging = True
        elif event.type == MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == MOUSEMOTION and self.dragging:
            self.value = self._x_to_value(event.pos[0])
            self.handle.x = self._value_to_x(self.value) - self.handle.width // 2
            return True
        return False
    
    def draw(self, screen):
        """Draw the slider bar and handle."""
        # Draw the main slider bar
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        # Draw the handle
        pygame.draw.rect(screen, self.handle_color, self.handle, border_radius=5)
        # Optional border for the handle
        pygame.draw.rect(screen, (0, 0, 0), self.handle, 2, border_radius=5)
