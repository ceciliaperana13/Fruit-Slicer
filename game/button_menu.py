import pygame

class Button_menu:
    """Class to create buttons in the menu"""
    
    def __init__(self, text, x, y, width, height, base_color, hover_color, font, border_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.base_color = base_color
        self.hover_color = hover_color
        self.font = font
        self.border_color = border_color

    def draw(self, surface):
        """Draws the button with hover effect"""
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        
        # Draw the button with rounded borders
        pygame.draw.rect(surface, color, self.rect, border_radius=20)
        pygame.draw.rect(surface, self.border_color, self.rect, 4, border_radius=20)

        # Draw the centered text
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        """Checks if the button has been clicked"""
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
    
    def is_hovered(self):
        """Checks if the mouse is hovering over the button"""
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)
