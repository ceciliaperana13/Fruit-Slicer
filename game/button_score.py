import pygame


class Button:
    """Simple button class for the scoreboard"""
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = tuple(min(c + 30, 255) for c in color)
        self.is_hovered = False
        
    def check_hover(self, pos):
        """Checks if the mouse is hovering over the button"""
        self.is_hovered = self.rect.collidepoint(pos)
        
    def for_clic(self, pos):
        """Checks if the button has been clicked"""
        return self.rect.collidepoint(pos)
        
    def draw(self, screen):
        """Draws the button on the screen"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=10)
        
        font = pygame.font.Font(None, 32)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
