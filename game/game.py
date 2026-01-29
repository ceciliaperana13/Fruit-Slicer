import pygame
import random
from score import Score


class Game:
    def __init__(self, width=800, height=580):
        """Initialise le jeu"""
        self.WIDTH = width
        self.HEIGHT = height
        self.FPS = 12

        # Physique
        self.GRAVITY = 1.2
        self.NORMAL_SPEED_FACTOR = 0.3
        self.SPEED_FACTOR = self.NORMAL_SPEED_FACTOR
        self.SPAWN_DELAY = 15
        self.spawn_timer = 0

        # État du jeu
        self.player_lives = 3
        self.score = 0
        self.game_over = False
        self.debug_mode = False
        self.slow_motion_timer = 0
        self.SLOW_MOTION_DURATION = 3  # secondes
        self.game_mode = 1  # Mode de jeu (1 ou 2)
        
        # Score manager
        self.score_manager = Score()
        self.player_name = "Player"  # Nom par défaut
        self.max_score_reached = 0  # Score max atteint dans la partie

        # COMBO
        self.combo = 1
        self.max_combo = 10

        # Fruits
        self.fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb', 'ice_cube2']

        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.ORANGE = (255, 128, 0)

        # Charger ressources
        self._load_resources()
        self.data = {}
        self._generate_all_fruits()

    def _load_resources(self):
        try:
            bg_img = pygame.image.load('./images/572603.jpg')
            self.background = pygame.transform.scale(bg_img, (self.WIDTH, self.HEIGHT))
        except:
            self.background = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.background.fill((50, 50, 50))

        try:
            self.font_name = './images/comic.ttf'
            self.font = pygame.font.Font(self.font_name, 42)
        except:
            self.font = pygame.font.Font(None, 42)
            self.font_name = None

        try:
            self.lives_icon = pygame.image.load('images/white_lives.png')
        except:
            self.lives_icon = pygame.Surface((30, 30))
            self.lives_icon.fill((255, 0, 0))

        # Charger l'image du logo pour le bouton de changement de mode
        try:
            self.mode_button_img = pygame.image.load('images/ff8_logo.png')
        except:
            # Image de fallback si le logo n'est pas trouvé
            self.mode_button_img = pygame.Surface((200, 200))
            self.mode_button_img.fill((100, 100, 100))

    def _generate_random_fruits(self, fruit):
        try:
            img = pygame.image.load(f"images/{fruit}.png")
        except:
            img = pygame.Surface((60, 60))
            img.fill((255, 0, 0) if fruit == 'bomb' else (0, 255, 0))

        self.data[fruit] = {
            'img': img,
            'x': random.randint(100, 500),
            'y': self.HEIGHT,
            'speed_x': random.randint(-10, 10),
            'speed_y': random.randint(-80, -60),
            'throw': True,
            'hit': False
        }

    def _generate_all_fruits(self):
        for fruit in self.fruits:
            self._generate_random_fruits(fruit)

    def _draw_text(self, display, text, size, x, y, color=None):
        color = color or self.BLACK
        font = pygame.font.Font(self.font_name, size) if self.font_name else pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect()
        rect.midtop = (x, y)
        display.blit(text_surface, rect)

    def _draw_lives(self, display, x, y, lives, image_path):
        for i in range(lives):
            try:
                img = pygame.image.load(image_path)
            except:
                img = pygame.Surface((30, 30))
                img.fill((255, 0, 0))
            rect = img.get_rect()
            rect.x = int(x + 35 * i)
            rect.y = y
            display.blit(img, rect)

    def set_player_name(self, name):
        """Définit le nom du joueur"""
        self.player_name = name if name.strip() else "Player"

    def get_game_mode(self):
        """Retourne le mode de jeu actuel"""
        return self.game_mode

    def set_game_mode(self, mode):
        """Définit le mode de jeu (1 ou 2)"""
        if mode in [1, 2]:
            self.game_mode = mode

    def start_game(self):
        self.player_lives = 3
        self.score = 0
        self.max_score_reached = 0
        self.spawn_timer = 0
        self.game_over = False
        self._generate_all_fruits()
        self.slow_motion_timer = 0
        self.SPEED_FACTOR = self.NORMAL_SPEED_FACTOR

        # COMBO
        self.combo = 1

    def end_game(self):
        """Termine la partie et sauvegarde le score"""
        if not self.game_over:  # Éviter de sauvegarder plusieurs fois
            self.game_over = True
            
            # Déterminer le résultat
            result = "WIN" if self.score > 0 else "LOSE"
            
            # Calculer les tentatives (erreurs) basées sur les vies perdues
            attempts = 3 - self.player_lives
            max_attempts = 3
            
            # Sauvegarder le score
            self.score_manager.add_score(
                player_name=self.player_name,
                word=f"Score-{self.score}",  # Mot = indicateur de score
                result=result,
                attempts=attempts,
                max_attempts=max_attempts
            )

    def is_game_over(self):
        return self.game_over

    def toggle_debug(self):
        self.debug_mode = not self.debug_mode

    def update(self, y_offset=0):
        if self.game_over:
            return

        current_position = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        self.spawn_timer += 1

        # Slow motion
        if self.slow_motion_timer > 0:
            self.SPEED_FACTOR = 0
            self.slow_motion_timer -= 1
        else:
            self.SPEED_FACTOR = self.NORMAL_SPEED_FACTOR

        for key, value in self.data.items():
            if value['throw']:
                value['x'] += value['speed_x'] * self.SPEED_FACTOR
                value['y'] += value['speed_y'] * self.SPEED_FACTOR
                value['speed_y'] += self.GRAVITY

                if value['speed_y'] > 35:
                    value['speed_y'] = 35

                # Fruit raté → perte de vie + reset combo
                if value['y'] > self.HEIGHT:
                    value['throw'] = False
                    if not value['hit'] and key != 'bomb':
                        self.player_lives -= 1

                        # COMBO RESET
                        self.combo = 1

                        if self.player_lives <= 0:
                            self.end_game()

                # Collision souris
                if mouse_pressed[0] and not value['hit']:
                    if value['x'] < current_position[0] < value['x'] + 60 and \
                       value['y'] + y_offset < current_position[1] < value['y'] + y_offset + 60:
                        value['hit'] = True

                        if key == 'bomb':
                            self.player_lives -= 3

                            # COMBO RESET
                            self.combo = 1

                            try:
                                value['img'] = pygame.image.load("images/explosion.png")
                            except:
                                value['img'] = pygame.Surface((60, 60))
                                value['img'].fill((255, 100, 0))

                            if self.player_lives <= 0:
                                self.end_game()
                        else:
                            try:
                                value['img'] = pygame.image.load(f"images/half_{key}.png")
                            except:
                                value['img'] = pygame.Surface((60, 60))
                                value['img'].fill((0, 255, 0))

                            # COMBO UP + SCORE MULTIPLIÉ
                            self.combo = min(self.combo + 1, self.max_combo)
                            self.score += self.combo
                            
                            # Suivre le score max
                            self.max_score_reached = max(self.max_score_reached, self.score)

                            if key == 'ice_cube2':
                                self.slow_motion_timer = self.SLOW_MOTION_DURATION * self.FPS

            else:
                if self.spawn_timer >= self.SPAWN_DELAY:
                    self._generate_random_fruits(key)
                    self.spawn_timer = 0

    def draw(self, display, y_offset=0):
        display.blit(self.background, (0, y_offset))

        # Score
        score_text = self.font.render(f'Score : {self.score}', True, self.WHITE)
        display.blit(score_text, (0, y_offset))

        # Combo
        combo_text = self.font.render(f'Combo x{self.combo}', True, self.ORANGE)
        display.blit(combo_text, (0, y_offset + 40))

        # Vies
        self._draw_lives(display, 690, y_offset + 5, self.player_lives, 'images/ff8_vie4(1).png')

        # Fruits
        for value in self.data.values():
            if value['throw'] and value['y'] <= self.HEIGHT:
                display.blit(value['img'], (value['x'], value['y'] + y_offset))

        # Debug
        if self.debug_mode:
            debug_font = pygame.font.Font(None, 24)
            debug_text = debug_font.render(
                f"FPS: {self.FPS} | Fruits: {len([v for v in self.data.values() if v['throw']])}",
                True, self.ORANGE
            )
            display.blit(debug_text, (10, y_offset + 50))

    def show_gameover_screen(self, display, clock):
        """Affiche l'écran game over qui remplit tout l'écran"""
        # Obtenir les dimensions réelles de la fenêtre
        screen_width, screen_height = display.get_size()
        
        # Créer un fond semi-transparent sombre qui couvre tout l'écran
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        
        waiting = True
        while waiting:
            clock.tick(self.FPS)
            
            # Remplir tout l'écran avec le fond noir
            display.fill((0, 0, 0))
            
            # Redessiner le fond de jeu (scalé si nécessaire)
            bg_scaled = pygame.transform.scale(self.background, (screen_width, screen_height))
            display.blit(bg_scaled, (0, 0))
            display.blit(overlay, (0, 0))
            
            # Calculer le centre de l'écran réel
            center_x = screen_width // 2
            
            # Titre "GAME OVER"
            self._draw_text(display, "GAME OVER", 90, center_x, int(screen_height * 0.20), self.RED)
            
            # Score final
            self._draw_text(display, f"Score Final: {self.score}", 60, center_x, int(screen_height * 0.40), self.WHITE)
            
            # Message de sauvegarde
            self._draw_text(display, "Score sauvegardé!", 35, center_x, int(screen_height * 0.52), self.ORANGE)
            
            # Instructions
            self._draw_text(display, "Press R to Restart", 40, center_x, int(screen_height * 0.70), self.WHITE)
            self._draw_text(display, "Press ESC for Menu", 40, center_x, int(screen_height * 0.78), self.WHITE)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "MENU"
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_r:
                        return "RESTART"
                    elif event.key == pygame.K_ESCAPE:
                        return "MENU"
        
        return "MENU"