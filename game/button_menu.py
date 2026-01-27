import pygame

class Button_menu:
    """Classe pour créer des boutons dans le menu"""
    
    def __init__(self, text, x, y, width, height, base_color, hover_color, font, border_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.base_color = base_color
        self.hover_color = hover_color
        self.font = font
        self.border_color = border_color

    def draw(self, surface):
        """Dessine le bouton avec effet hover"""
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        
        # Dessiner le bouton avec bordures arrondies
        pygame.draw.rect(surface, color, self.rect, border_radius=20)
        pygame.draw.rect(surface, self.border_color, self.rect, 4, border_radius=20)

        # Dessiner le texte centré
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        """Vérifie si le bouton a été cliqué"""
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
    
    def is_hovered(self):
        """Vérifie si la souris survole le bouton"""
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)