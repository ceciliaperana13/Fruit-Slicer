import pygame
from datetime import datetime


class TopBar:
    """Classe pour gérer la barre supérieure avec le chronomètre, la date et le bouton de mode"""
    
    def __init__(self, width, height=80, button_image_path='./images/chococo.png'):
        self.width = width
        self.height = height
        self.total_time = 90  # 1min 30sec (90 secondes)
        self.time_left = self.total_time
        self.timer_running = False
        self.last_tick = 0
        
        # Couleurs pour le dégradé de fond
        self.color1 = (128, 128, 128)  # Gris
        self.color2 = (59, 130, 246)  # Bleu
        self.white = (255, 255, 255)
        self.red = (239, 68, 68)
        self.orange = (255, 165, 0)
        
        # Couleurs pour la barre de progression
        self.bar_color_green = (0, 200, 0)
        self.bar_color_orange = (255, 165, 0)
        self.bar_color_red = (255, 0, 0)
        self.bar_bg_color = (50, 50, 50)
        
        # Polices - Chronomètre plus petit
        try:
            self.font_large = pygame.font.Font('./images/comic.ttf', 36)  # Réduit de 48 à 36
            self.font_small = pygame.font.Font('./images/comic.ttf', 24)
        except:
            self.font_large = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)
        
        # Bouton de mode de jeu - Déplacé à droite
        self.button_width = 60
        self.button_height = 60
        self.button_x = self.width - 80  # Plus à droite
        self.button_y = 10
        self.button_rect = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
        
        # États du bouton
        self.button_hovered = False
        self.button_pressed = False
        
        # Image du bouton
        self.button_image = None
        if button_image_path:
            try:
                self.button_image = pygame.image.load(button_image_path)
                self.button_image = pygame.transform.scale(self.button_image, (self.button_width - 10, self.button_height - 10))
            except Exception as e:
                print(f"Erreur: Impossible de charger l'image {button_image_path}: {e}")
                self.button_image = None
        
        # Mode de jeu
        self.game_mode = "jeu1"  # Modes: "jeu1", "jeu2"
        self.available_modes = ["jeu1", "jeu2"]
    
    def get_current_date(self):
        """Retourne la date actuelle en français"""
        months = {
            1: "janvier", 2: "février", 3: "mars", 4: "avril",
            5: "mai", 6: "juin", 7: "juillet", 8: "août",
            9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"
        }
        days = {
            0: "lundi", 1: "mardi", 2: "mercredi", 3: "jeudi",
            4: "vendredi", 5: "samedi", 6: "dimanche"
        }
        
        now = datetime.now()
        day_name = days[now.weekday()]
        month_name = months[now.month]
        
        return f"{day_name} {now.day} {month_name} {now.year}"
    
    def format_time(self):
        """Formate le temps restant en MM:SS"""
        mins = int(self.time_left // 60)
        secs = int(self.time_left % 60)
        return f"{mins}:{secs:02d}"
    
    def draw_gradient(self, surface):
        """Dessine le dégradé de fond (gris vers bleu)"""
        for i in range(self.height):
            ratio = i / self.height
            r = int(self.color1[0] * (1 - ratio) + self.color2[0] * ratio)
            g = int(self.color1[1] * (1 - ratio) + self.color2[1] * ratio)
            b = int(self.color1[2] * (1 - ratio) + self.color2[2] * ratio)
            pygame.draw.line(surface, (r, g, b), (0, i), (self.width, i))
    
    def handle_event(self, event):
        """Gère les événements de la souris pour le bouton"""
        if event.type == pygame.MOUSEMOTION:
            self.button_hovered = self.button_rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                if self.button_hovered:
                    self.button_pressed = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.button_pressed and self.button_hovered:
                    self.on_button_click()
                self.button_pressed = False
    
    def on_button_click(self):
        """Action lors du clic sur le bouton - Change le mode de jeu"""
        current_index = self.available_modes.index(self.game_mode)
        next_index = (current_index + 1) % len(self.available_modes)
        self.game_mode = self.available_modes[next_index]
        
        print(f"Mode de jeu changé: {self.game_mode}")
    
    def draw_button(self, surface):
        """Dessine le bouton de mode de jeu"""
        # Fond semi-transparent
        bg_surface = pygame.Surface((self.button_width, self.button_height), pygame.SRCALPHA)
        
        if self.button_pressed:
            bg_surface.fill((200, 200, 200, 150))
        elif self.button_hovered:
            bg_surface.fill((255, 255, 255, 180))
        else:
            bg_surface.fill((255, 255, 255, 120))
        
        surface.blit(bg_surface, (self.button_x, self.button_y))
        
        # Bordure
        border_width = 3 if self.button_hovered else 2
        pygame.draw.rect(surface, self.white, self.button_rect, border_width, border_radius=10)
        
        # Image du bouton (centrée) avec effet hover
        if self.button_image:
            # Position de base
            image_x = self.button_x + (self.button_width - self.button_image.get_width()) // 2
            image_y = self.button_y + (self.button_height - self.button_image.get_height()) // 2
            
            # Effet hover : image légèrement plus grande
            if self.button_hovered or self.button_pressed:
                # Agrandir l'image de 10%
                scale_factor = 1.1 if self.button_hovered and not self.button_pressed else 0.95
                new_width = int(self.button_image.get_width() * scale_factor)
                new_height = int(self.button_image.get_height() * scale_factor)
                scaled_image = pygame.transform.scale(self.button_image, (new_width, new_height))
                
                # Recentrer l'image agrandie
                image_x = self.button_x + (self.button_width - new_width) // 2
                image_y = self.button_y + (self.button_height - new_height) // 2
                
                # Ajouter un effet de luminosité
                hover_surface = scaled_image.copy()
                hover_surface.set_alpha(255 if self.button_pressed else 230)
                surface.blit(hover_surface, (image_x, image_y))
            else:
                surface.blit(self.button_image, (image_x, image_y))
    
    def start(self):
        """Démarre le chronomètre"""
        self.timer_running = True
        self.last_tick = pygame.time.get_ticks()
    
    def pause(self):
        """Met en pause le chronomètre"""
        self.timer_running = False
    
    def toggle(self):
        """Alterne entre démarrer et pause"""
        if self.timer_running:
            self.pause()
        else:
            self.start()
    
    def reset(self):
        """Réinitialise le chronomètre"""
        self.time_left = self.total_time
        self.timer_running = False
    
    def update(self):
        """Met à jour le chronomètre"""
        if self.timer_running and self.time_left > 0:
            current_tick = pygame.time.get_ticks()
            if current_tick - self.last_tick >= 1000:
                self.time_left -= 1
                self.last_tick = current_tick
            
            if self.time_left <= 0:
                self.time_left = 0
                self.timer_running = False
    
    def draw(self, surface):
        """Dessine la barre complète avec dégradé, date, chronomètre, bouton et barre de progression"""
        # Dégradé de fond
        self.draw_gradient(surface)
        
        # Date à gauche
        date_text = self.font_small.render(self.get_current_date(), True, self.white)
        surface.blit(date_text, (20, 20))
        
        # Bouton de mode (à droite)
        self.draw_button(surface)
        
        # Chronomètre au centre avec fond semi-transparent
        time_color = self.red if self.time_left <= 10 else self.white
        time_text = self.font_large.render(self.format_time(), True, time_color)
        time_rect = time_text.get_rect(center=(self.width // 2, self.height // 2 - 10))  # Centré au milieu
        
        # Fond du chronomètre
        timer_bg = pygame.Rect(time_rect.x - 15, time_rect.y - 8, 
                               time_rect.width + 30, time_rect.height + 16)
        # Créer une surface semi-transparente
        bg_surface = pygame.Surface((timer_bg.width, timer_bg.height), pygame.SRCALPHA)
        bg_surface.fill((255, 255, 255, 80))
        surface.blit(bg_surface, (timer_bg.x, timer_bg.y))
        pygame.draw.rect(surface, self.white, timer_bg, 2, border_radius=10)
        
        surface.blit(time_text, time_rect)
        
        # Barre de progression en bas
        bar_width = self.width - 40
        bar_height = 12
        bar_x = 20
        bar_y = self.height - 18
        
        # Fond de la barre
        pygame.draw.rect(surface, self.bar_bg_color, (bar_x, bar_y, bar_width, bar_height), border_radius=6)
        
        # Barre de progression (qui descend avec le temps)
        progress = self.time_left / self.total_time
        progress_width = int(bar_width * progress)
        
        # Changer la couleur selon le temps restant
        if self.time_left <= 10:
            bar_color = self.bar_color_red
        elif self.time_left <= 30:
            bar_color = self.bar_color_orange
        else:
            bar_color = self.bar_color_green
        
        if progress_width > 0:
            pygame.draw.rect(surface, bar_color, (bar_x, bar_y, progress_width, bar_height), border_radius=6)
    
    def is_finished(self):
        """Retourne True si le temps est écoulé"""
        return self.time_left <= 0
    
    def get_game_mode(self):
        """Retourne le mode de jeu actuel"""
        return self.game_mode
    
    def set_game_mode(self, mode):
        """Définit le mode de jeu"""
        if mode in self.available_modes:
            self.game_mode = mode
        else:
            print(f"Mode '{mode}' non valide. Modes disponibles: {self.available_modes}")