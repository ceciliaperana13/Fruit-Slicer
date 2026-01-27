import pygame
import random
import sys


class Game:
    def __init__(self, width=800, height=500):
        """Initialise le jeu avec tous les paramètres nécessaires"""
        self.WIDTH = width
        self.HEIGHT = height
        self.FPS = 12
        
        # Paramètres de physique
        self.GRAVITY = 1.2
        self.SPEED_FACTOR = 0.3
        self.SPAWN_DELAY = 15
        self.spawn_timer = 0
        
        # État du jeu
        self.player_lives = 3
        self.score = 0
        self.game_over = False
        self.game_running = True
        self.game_state = "MENU"  # MENU, PLAYING, GAME_OVER
        self.debug_mode = False
        
        # Liste des fruits
        self.fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']
        
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.ORANGE = (255, 128, 0)
        
        # Charger les ressources
        self._load_resources()
        
        # Initialiser les données des fruits
        self.data = {}
        self._generate_all_fruits()
    
    def _load_resources(self):
        """Charge toutes les images et polices nécessaires"""
        # Charger le fond
        try:
            bg_img = pygame.image.load('./images/572603.jpg')
            self.background = pygame.transform.scale(bg_img, (self.WIDTH, self.HEIGHT))
        except:
            # Créer un fond par défaut si l'image n'existe pas
            self.background = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.background.fill((50, 50, 50))
        
        # Charger la police
        try:
            self.font = pygame.font.Font('./images/comic.ttf', 42)
            self.font_name = './images/comic.ttf'
        except:
            self.font = pygame.font.Font(None, 42)
            self.font_name = None
        
        # Charger l'icône de vie
        try:
            self.lives_icon = pygame.image.load('images/white_lives.png')
        except:
            # Créer une icône par défaut
            self.lives_icon = pygame.Surface((30, 30))
            self.lives_icon.fill((255, 0, 0))
    
    def _generate_random_fruits(self, fruit):
        """Génère les données aléatoires pour un fruit"""
        fruit_path = "images/" + fruit + ".png"
        try:
            img = pygame.image.load(fruit_path)
        except:
            # Image par défaut si le fichier n'existe pas
            img = pygame.Surface((60, 60))
            img.fill((255, 0, 0) if fruit == 'bomb' else (0, 255, 0))
        
        self.data[fruit] = {
            'img': img,
            'x': random.randint(100, 500),
            'y': self.HEIGHT,
            'speed_x': random.randint(-10, 10),
            'speed_y': random.randint(-80, -60),
            'throw': True,
            'hit': False,
        }
    
    def _generate_all_fruits(self):
        """Génère tous les fruits au début"""
        for fruit in self.fruits:
            self._generate_random_fruits(fruit)
    
    def _draw_text(self, display, text, size, x, y, color=None):
        """Dessine du texte à l'écran"""
        if color is None:
            color = self.BLACK
        
        if self.font_name:
            font = pygame.font.Font(self.font_name, size)
        else:
            font = pygame.font.Font(None, size)
        
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        display.blit(text_surface, text_rect)
    
    def _draw_lives(self, display, x, y, lives, image_path):
        """Dessine les vies restantes"""
        for i in range(lives):
            try:
                img = pygame.image.load(image_path)
            except:
                img = pygame.Surface((30, 30))
                img.fill((255, 0, 0))
            
            img_rect = img.get_rect()
            img_rect.x = int(x + 35 * i)
            img_rect.y = y
            display.blit(img, img_rect)
    
    def show_gameover_screen(self, display, clock):
        """Affiche l'écran de game over"""
        display.blit(self.background, (0, 0))
        
        # Titre Game Over
        self._draw_text(display, "GAME OVER", 90, self.WIDTH / 2, self.HEIGHT / 4, self.RED)
        
        # Afficher le score
        self._draw_text(display, f"Score Final: {self.score}", 60, self.WIDTH / 2, self.HEIGHT / 2 - 50, self.WHITE)
        
        # Instructions
        self._draw_text(display, "Press R to Restart", 40, self.WIDTH / 2, self.HEIGHT / 2 + 50, self.WHITE)
        self._draw_text(display, "Press ESC for Menu", 40, self.WIDTH / 2, self.HEIGHT / 2 + 100, self.WHITE)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_r:
                        return "RESTART"
                    elif event.key == pygame.K_ESCAPE:
                        return "MENU"
        
        return "MENU"
    
    def show_menu_screen(self, display, clock):
        """Affiche l'écran de menu (ne devrait pas être utilisé, remplacé par MainMenu)"""
        return "START"
    
    def start_game(self):
        """Démarre une nouvelle partie"""
        self.game_state = "PLAYING"
        self.game_over = False
        self.player_lives = 3
        self.score = 0
        self.spawn_timer = 0
        self._generate_all_fruits()
    
    def end_game(self):
        """Termine la partie"""
        self.game_state = "GAME_OVER"
        self.game_over = True
    
    def return_to_menu(self):
        """Retourne au menu"""
        self.game_state = "MENU"
        self.game_over = False
    
    def get_game_state(self):
        """Retourne l'état actuel du jeu"""
        return self.game_state
    
    def toggle_debug(self):
        """Active/Désactive le mode debug"""
        self.debug_mode = not self.debug_mode
    
    def reset_game(self):
        """Réinitialise le jeu"""
        self.game_over = False
        self.player_lives = 3
        self.score = 0
        self.spawn_timer = 0
        self._generate_all_fruits()
    
    def handle_events(self):
        """Gère les événements pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def update(self, y_offset=0):
        """Met à jour la logique du jeu
        
        Args:
            y_offset: Décalage vertical pour ajuster la détection de collision
        """
        if self.game_over:
            return
        
        current_position = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        self.spawn_timer += 1
        
        for key, value in self.data.items():
            if value['throw']:
                # Mouvement
                value['x'] += value['speed_x'] * self.SPEED_FACTOR
                value['y'] += value['speed_y'] * self.SPEED_FACTOR
                value['speed_y'] += self.GRAVITY
                
                # Limiter la vitesse de chute
                if value['speed_y'] > 35:
                    value['speed_y'] = 35
                
                # Vérifier si le fruit est sorti de l'écran
                if value['y'] > self.HEIGHT:
                    value['throw'] = False
                
                # Détection de collision avec la souris (ajusté avec y_offset)
                if mouse_pressed[0] and not value['hit']:
                    # Calculer la position réelle du fruit à l'écran
                    fruit_screen_y = value['y'] + y_offset
                    
                    if value['x'] < current_position[0] < value['x'] + 60 and \
                       fruit_screen_y < current_position[1] < fruit_screen_y + 60:
                        
                        value['hit'] = True
                        
                        if key == 'bomb':
                            self.player_lives -= 1
                            try:
                                value['img'] = pygame.image.load("images/explosion.png")
                            except:
                                value['img'] = pygame.Surface((60, 60))
                                value['img'].fill((255, 100, 0))
                            
                            if self.player_lives <= 0:
                                self.game_over = True
                        else:
                            try:
                                value['img'] = pygame.image.load("images/half_" + key + ".png")
                            except:
                                value['img'] = pygame.Surface((60, 60))
                                value['img'].fill((0, 255, 0))
                            self.score += 1
            
            else:
                # Respawn contrôlé
                if self.spawn_timer >= self.SPAWN_DELAY:
                    self._generate_random_fruits(key)
                    self.spawn_timer = 0
    
    def draw(self, display, y_offset=0):
        """Dessine tous les éléments du jeu
        
        Args:
            display: Surface pygame où dessiner
            y_offset: Décalage vertical pour laisser de la place à la barre supérieure
        """
        # Dessiner le fond
        display.blit(self.background, (0, y_offset))
        
        # Dessiner le score
        score_text = self.font.render('Score : ' + str(self.score), True, self.WHITE)
        display.blit(score_text, (0, y_offset))
        
        # Dessiner les vies
        self._draw_lives(display, 690, y_offset + 5, self.player_lives, 'images/red_lives.png')
        
        # Dessiner les fruits
        for key, value in self.data.items():
            if value['throw'] and value['y'] <= self.HEIGHT:
                display.blit(value['img'], (value['x'], value['y'] + y_offset))
        
        # Mode debug
        if self.debug_mode:
            debug_font = pygame.font.Font(None, 24)
            debug_text = debug_font.render(f"FPS: {self.FPS} | Fruits: {len([v for v in self.data.values() if v['throw']])}", True, self.ORANGE)
            display.blit(debug_text, (10, y_offset + 50))
    
    def is_game_over(self):
        """Retourne True si le jeu est terminé"""
        return self.game_over
    
    def get_score(self):
        """Retourne le score actuel"""
        return self.score
    
    def get_lives(self):
        """Retourne les vies restantes"""
        return self.player_lives