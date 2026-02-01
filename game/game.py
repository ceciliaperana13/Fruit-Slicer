import pygame
import random
from score import Score


class Game:
    def __init__(self, width=800, height=580, settings=None):
        """Initialise le jeu"""
        self.WIDTH = width
        self.HEIGHT = height
        self.FPS = 12
        
        # Référence aux settings pour accéder au son d'impact
        self.settings = settings

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
        self.mode_just_changed = False  # Flag pour détecter un changement de mode
        
        # Score manager
        self.score_manager = Score()
        self.player_name = "Player"  
        self.max_score_reached = 0  # Score max atteint dans la partie

        # COMBO
        self.combo = 1
        self.max_combo = 10

        # MODE 1: Fruits
        self.fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb', 'ice_cube2']
        
        # MODE 2: Lettres (réduites à 10)
        self.letters = list('ABCDEFGHIJ')
        
        # Liste des éléments actifs selon le mode
        self.active_items = []

        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.ORANGE = (255, 128, 0)
        self.BLUE = (100, 150, 255)
        self.GREEN = (0, 255, 0)
        self.YELLOW = (255, 255, 0)

        # Charger ressources
        self._load_resources()
        self.data = {}
        self._update_active_items()
        self._generate_all_items()

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

        try:
            self.mode_button_img = pygame.image.load('images/ff8_logo.png')
        except:
            self.mode_button_img = pygame.Surface((200, 200))
            self.mode_button_img.fill((100, 100, 100))

        try:
            freeze_img = pygame.image.load('images/freeze_overlay.png')
            self.freeze_overlay = pygame.transform.scale(freeze_img, (self.WIDTH, self.HEIGHT))
        except:
            self.freeze_overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
            self.freeze_overlay.fill((200, 220, 255, 100))

    def _update_active_items(self):
        """Met à jour la liste des éléments actifs selon le mode de jeu"""
        if self.game_mode == 1:
            # Mode 1 : seulement les fruits
            self.active_items = self.fruits.copy()
        else:
            # Mode 2 : seulement les lettres
            self.active_items = ['letter_' + letter for letter in self.letters]

    def _create_letter_image(self, letter):
        """Crée une image pour une lettre"""
        size = 80
        img = pygame.Surface((size, size), pygame.SRCALPHA)
        
        colors = [
            (255, 100, 100),  # Rouge
            (100, 255, 100),  # Vert
            (100, 100, 255),  # Bleu
            (255, 255, 100),  # Jaune
            (255, 100, 255),  # Magenta
            (100, 255, 255),  # Cyan
        ]
        color = random.choice(colors)
        
        pygame.draw.circle(img, color, (size//2, size//2), size//2 - 2)
        pygame.draw.circle(img, self.BLACK, (size//2, size//2), size//2 - 2, 3)
        
        try:
            letter_font = pygame.font.Font(self.font_name, 50) if self.font_name else pygame.font.Font(None, 50)
        except:
            letter_font = pygame.font.Font(None, 50)
        
        text = letter_font.render(letter, True, self.BLACK)
        text_rect = text.get_rect(center=(size//2, size//2))
        img.blit(text, text_rect)
        
        return img

    def _generate_random_items(self, item):
        """Génère un élément aléatoire (fruit ou lettre)"""
        is_letter = item.startswith('letter_')
        
        if is_letter:
            letter = item.split('_')[1]
            img = self._create_letter_image(letter)
            item_size = 80
        else:
            try:
                img = pygame.image.load(f"images/{item}.png")
            except:
                img = pygame.Surface((60, 60))
                img.fill((255, 0, 0) if item == 'bomb' else (0, 255, 0))
            item_size = 60

        self.data[item] = {
            'img': img,
            'x': random.randint(100, self.WIDTH - 100),
            'y': self.HEIGHT,
            'speed_x': random.randint(-10, 10),
            'speed_y': random.randint(-80, -60),
            'throw': True,
            'hit': False,
            'is_letter': is_letter,
            'size': item_size
        }

    def _generate_all_items(self):
        """Génère tous les éléments selon le mode actif"""
        self.data.clear()
        for item in self.active_items:
            self._generate_random_items(item)

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
    
    def get_game_mode_text(self):
        """Retourne le mode de jeu au format texte pour la TopBar"""
        return f"jeu{self.game_mode}"
    
    def mode_has_changed(self):
        """Vérifie si le mode vient de changer (pour forcer un reset dans main.py)"""
        if self.mode_just_changed:
            self.mode_just_changed = False
            return True
        return False

    def set_game_mode(self, mode):
        """Définit le mode de jeu (1 ou 2, ou 'jeu1' ou 'jeu2')"""
        # Convertir les modes textuels de la TopBar en numéros
        if mode == "jeu1":
            mode = 1
        elif mode == "jeu2":
            mode = 2
        
        if mode in [1, 2]:
            old_mode = self.game_mode
            self.game_mode = mode
            
            # Si le mode a changé, nettoyer TOUT et régénérer
            if old_mode != mode:
                self.mode_just_changed = True
                self._update_active_items()
                self._generate_all_items()
                # Reset complet pour éviter les mélanges
                self.spawn_timer = 0
                self.slow_motion_timer = 0
                self.SPEED_FACTOR = self.NORMAL_SPEED_FACTOR

    def start_game(self):
        self.player_lives = 3
        self.score = 0
        self.max_score_reached = 0
        self.spawn_timer = 0
        self.game_over = False
        self.mode_just_changed = False
        self._update_active_items()
        self._generate_all_items()
        self.slow_motion_timer = 0
        self.SPEED_FACTOR = self.NORMAL_SPEED_FACTOR
        self.combo = 1

    def end_game(self):
        """Termine la partie et sauvegarde le score"""
        if not self.game_over:
            self.game_over = True
            
            # On sauvegarde TOUJOURS le score, même si c'est 0
            result = "WIN" if self.player_lives > 0 else "LOSE"
            attempts = 3 - self.player_lives
            max_attempts = 3
            
            # Format: afficher le mode de jeu proprement
            mode_text = f"Mode {self.game_mode}"
            
            # Passer le score actuel directement (même s'il est 0)
            self.score_manager.add_score(
                player_name=self.player_name,
                word=mode_text,
                result=result,
                attempts=attempts,
                max_attempts=max_attempts,
                final_score=self.score  # Nouveau paramètre pour le score final
            )

    def is_game_over(self):
        return self.game_over

    def toggle_debug(self):
        self.debug_mode = not self.debug_mode

    def handle_keyboard_input(self, event):
        """Gère les entrées clavier pour le Mode 2 (lettres)"""
        if self.game_mode != 2 or self.game_over:
            return
        
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key).upper()
            
            if len(key_name) == 1 and key_name in self.letters:
                letter_key = f'letter_{key_name}'
                
                if letter_key in self.data and self.data[letter_key]['throw'] and not self.data[letter_key]['hit']:
                    self.data[letter_key]['hit'] = True
                    
                    # Effet visuel
                    img = self._create_letter_image(key_name)
                    img.set_alpha(150)
                    self.data[letter_key]['img'] = img
                    
                    # JOUER LE SON D'IMPACT
                    if self.settings:
                        self.settings.play_impact_sound()
                    
                    # COMBO UP + SCORE
                    self.combo = min(self.combo + 1, self.max_combo)
                    self.score += self.combo
                    self.max_score_reached = max(self.max_score_reached, self.score)

    def update(self, y_offset=0):
        if self.game_over:
            return

        # MODE 1: Gestion souris
        if self.game_mode == 1:
            current_position = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
        
        self.spawn_timer += 1

        # Slow motion (Mode 1 uniquement)
        if self.game_mode == 1 and self.slow_motion_timer > 0:
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

                # Élément raté
                if value['y'] > self.HEIGHT:
                    value['throw'] = False
                    
                    if self.game_mode == 1:
                        if not value['hit'] and key != 'bomb':
                            self.player_lives -= 1
                            self.combo = 1
                            if self.player_lives <= 0:
                                self.end_game()
                    else:
                        if not value['hit']:
                            self.player_lives -= 1
                            self.combo = 1
                            if self.player_lives <= 0:
                                self.end_game()

                # MODE 1: Collision souris
                if self.game_mode == 1 and not value['hit'] and mouse_pressed[0]:
                    item_size = value.get('size', 60)
                    if value['x'] < current_position[0] < value['x'] + item_size and \
                       value['y'] + y_offset < current_position[1] < value['y'] + y_offset + item_size:
                        value['hit'] = True

                        if key == 'bomb':
                            self.player_lives -= 3
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

                            # JOUER LE SON D'IMPACT (même son pour tous)
                            if self.settings:
                                self.settings.play_impact_sound()

                            self.combo = min(self.combo + 1, self.max_combo)
                            self.score += self.combo
                            self.max_score_reached = max(self.max_score_reached, self.score)

                            if key == 'ice_cube2':
                                self.slow_motion_timer = self.SLOW_MOTION_DURATION * self.FPS

            else:
                if self.spawn_timer >= self.SPAWN_DELAY:
                    self._generate_random_items(key)
                    self.spawn_timer = 0

    def draw(self, display, y_offset=0):
        display.blit(self.background, (0, y_offset))

        # Score
        score_text = self.font.render(f'Score : {self.score}', True, self.WHITE)
        display.blit(score_text, (0, y_offset))

        # Combo
        combo_text = self.font.render(f'Combo x{self.combo}', True, self.ORANGE)
        display.blit(combo_text, (0, y_offset + 40))

        # Mode
        mode_color = self.GREEN if self.game_mode == 1 else self.YELLOW
        mode_text = self.font.render(f'Mode {self.game_mode}', True, mode_color)
        display.blit(mode_text, (0, y_offset + 80))
        
        # Instructions
        instruction_font = pygame.font.Font(self.font_name, 24) if self.font_name else pygame.font.Font(None, 24)
        instruction = "Cliquez sur les fruits!" if self.game_mode == 1 else "Tapez les lettres au clavier!"
        instruction_text = instruction_font.render(instruction, True, self.WHITE)
        display.blit(instruction_text, (0, y_offset + 120))

        # Vies
        self._draw_lives(display, 690, y_offset + 5, self.player_lives, 'images/ff8_vie4(1).png')

        # Éléments
        for value in self.data.values():
            if value['throw'] and value['y'] <= self.HEIGHT:
                display.blit(value['img'], (value['x'], value['y'] + y_offset))

        # Effet gel (Mode 1)
        if self.game_mode == 1 and self.slow_motion_timer > 0:
            screen_width, screen_height = display.get_size()
            if self.freeze_overlay.get_width() != screen_width or self.freeze_overlay.get_height() != screen_height:
                try:
                    freeze_img = pygame.image.load('./images/gel3.png')
                    freeze_scaled = pygame.transform.scale(freeze_img, (screen_width, screen_height))
                except:
                    freeze_scaled = pygame.transform.scale(self.freeze_overlay, (screen_width, screen_height))
            else:
                freeze_scaled = self.freeze_overlay
            display.blit(freeze_scaled, (0, y_offset))

        # Debug
        if self.debug_mode:
            debug_font = pygame.font.Font(None, 24)
            active_items = len([v for v in self.data.values() if v['throw']])
            debug_text = debug_font.render(
                f"FPS: {self.FPS} | Items: {active_items} | Mode: {self.game_mode}",
                True, self.ORANGE
            )
            display.blit(debug_text, (10, y_offset + 160))

    def show_gameover_screen(self, display, clock):
        """Affiche l'écran game over"""
        screen_width, screen_height = display.get_size()
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        
        waiting = True
        while waiting:
            clock.tick(self.FPS)
            display.fill((0, 0, 0))
            
            bg_scaled = pygame.transform.scale(self.background, (screen_width, screen_height))
            display.blit(bg_scaled, (0, 0))
            display.blit(overlay, (0, 0))
            
            center_x = screen_width // 2
            
            self._draw_text(display, "GAME OVER", 90, center_x, int(screen_height * 0.20), self.RED)
            
            mode_color = self.GREEN if self.game_mode == 1 else self.YELLOW
            self._draw_text(display, f"Mode {self.game_mode}", 50, center_x, int(screen_height * 0.35), mode_color)
            self._draw_text(display, f"Score Final: {self.score}", 60, center_x, int(screen_height * 0.45), self.WHITE)
            self._draw_text(display, "Score sauvegardé!", 35, center_x, int(screen_height * 0.57), self.ORANGE)
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