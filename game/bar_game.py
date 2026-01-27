import pygame
from datetime import datetime

class TopBar:
    def __init__(self, width, height=80):
        self.width = width
        self.height = height
        self.total_time = 90  # 1min 30sec
        self.time_left = self.total_time
        self.timer_running = False
        self.last_tick = 0
        
        # Couleurs
        self.color1 = (59, 130, 246)  # Bleu
        self.color2 = (147, 51, 234)  # Violet
        self.white = (255, 255, 255)
        self.red = (239, 68, 68)
        
        # Polices
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 24)
    
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
        """Dessine le dégradé de fond"""
        for i in range(self.height):
            ratio = i / self.height
            r = int(self.color1[0] * (1 - ratio) + self.color2[0] * ratio)
            g = int(self.color1[1] * (1 - ratio) + self.color2[1] * ratio)
            b = int(self.color1[2] * (1 - ratio) + self.color2[2] * ratio)
            pygame.draw.line(surface, (r, g, b), (0, i), (self.width, i))
    
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
        """Dessine la barre complète"""
        # Dégradé de fond
        self.draw_gradient(surface)
        
        # Date à gauche
        date_text = self.font_small.render(self.get_current_date(), True, self.white)
        surface.blit(date_text, (20, 30))
        
        # Chronomètre à droite
        time_color = self.red if self.time_left <= 10 else self.white
        time_text = self.font_large.render(self.format_time(), True, time_color)
        time_rect = time_text.get_rect(center=(self.width - 150, self.height // 2))
        
        # Fond du chronomètre
        timer_bg = pygame.Rect(time_rect.x - 20, time_rect.y - 10, 
                               time_rect.width + 40, time_rect.height + 20)
        # Créer une surface semi-transparente
        bg_surface = pygame.Surface((timer_bg.width, timer_bg.height), pygame.SRCALPHA)
        bg_surface.fill((255, 255, 255, 80))
        surface.blit(bg_surface, (timer_bg.x, timer_bg.y))
        pygame.draw.rect(surface, self.white, timer_bg, 2, border_radius=10)
        
        surface.blit(time_text, time_rect)
    
    def is_finished(self):
        """Retourne True si le temps est écoulé"""
        return self.time_left <= 0