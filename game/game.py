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
        
        # MODE 2: Lettres (10 lettres seulement, sans D, P, R)
        # Voyelles: A, E, I, O, U
        # Consonnes faciles: B, C, F, G, H
        self.letters = list('AEIOBCFGH')  # 10 lettres
        
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
            # Mode 2 : UNIQUEMENT des fruits avec des lettres dessus
            
            self.active_items = []
            
            # Les 4 fruits de base
            base_fruits = ['melon', 'orange', 'pomegranate', 'guava']
            
            # Créer 10 fruits avec index pour leur assigner une lettre spécifique
            for i, letter in enumerate(self.letters):
                fruit = base_fruits[i % 4]  # Alterner entre les 4 fruits
                # Créer un identifiant unique avec la lettre assignée
                fruit_key = f"{fruit}_{letter}"
                self.active_items.append(fruit_key)
            
            # Ajouter la bombe et le glaçon
            self.active_items.append('bomb')
            self.active_items.append('ice_cube2')

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

    def _add_letter_to_item(self, base_img, letter):
        """Ajoute une lettre sur une image d'item (bombe ou glaçon)"""
        # Créer une copie de l'image de base
        new_img = base_img.copy()
        
        # Créer le texte de la lettre
        try:
            letter_font = pygame.font.Font(self.font_name, 40) if self.font_name else pygame.font.Font(None, 40)
        except:
            letter_font = pygame.font.Font(None, 40)
        
        # Texte avec contour blanc pour visibilité
        text = letter_font.render(letter, True, self.WHITE)
        text_outline = letter_font.render(letter, True, self.BLACK)
        
        # Centrer la lettre sur l'image
        img_width, img_height = new_img.get_size()
        text_rect = text.get_rect(center=(img_width//2, img_height//2))
        
        # Dessiner le contour (décalé de 2px dans chaque direction)
        for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2), (-2, 0), (2, 0), (0, -2), (0, 2)]:
            outline_rect = text_rect.copy()
            outline_rect.x += dx
            outline_rect.y += dy
            new_img.blit(text_outline, outline_rect)
        
        # Dessiner la lettre blanche par-dessus
        new_img.blit(text, text_rect)
        
        return new_img

    def _generate_random_items(self, item):
        """Génère un élément aléatoire (fruit ou lettre)"""
        is_letter = item.startswith('letter_')
        assigned_letter = None
        
        if is_letter:
            # Cercle coloré avec lettre (Mode 1 seulement, ne devrait pas arriver en Mode 2)
            letter = item.split('_')[1]
            img = self._create_letter_image(letter)
            item_size = 80
        else:
            # C'est un fruit, bombe ou glaçon
            # En Mode 2, extraire le nom du fruit et la lettre assignée (format: fruit_LETTRE)
            fruit_name = item
            if self.game_mode == 2 and '_' in item:
                parts = item.split('_')
                if parts[0] in ['melon', 'orange', 'pomegranate', 'guava']:
                    fruit_name = parts[0]
                    assigned_letter = parts[1]  # La lettre assignée à ce fruit
            
            # Charger l'image du fruit/bombe/glaçon
            try:
                img = pygame.image.load(f"images/{fruit_name}.png")
            except:
                img = pygame.Surface((60, 60))
                img.fill((255, 0, 0) if fruit_name == 'bomb' else (0, 255, 0))
            item_size = 60
            
            # MODE 2: Ajouter une lettre sur l'item
            if self.game_mode == 2:
                # Si pas de lettre assignée (bombe ou glaçon), en choisir une aléatoire
                if assigned_letter is None:
                    assigned_letter = random.choice(self.letters)
                
                # Superposer la lettre sur l'image
                img = self._add_letter_to_item(img, assigned_letter)

        self.data[item] = {
            'img': img,
            'x': random.randint(item_size, self.WIDTH - item_size),  # Tenir compte de la taille
            'y': self.HEIGHT,
            'speed_x': random.randint(-10, 10),
            'speed_y': random.randint(-80, -60),
            'throw': True,
            'hit': False,
            'is_letter': is_letter,
            'size': item_size,
            'assigned_letter': assigned_letter
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
        """Gère les entrées clavier pour le Mode 2 (fruits avec lettres)"""
        if self.game_mode != 2 or self.game_over:
            return
        
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key).upper()
            
            # Vérifier que c'est une lettre valide
            if len(key_name) == 1 and key_name in self.letters:
                
                # Chercher tous les items avec cette lettre assignée
                for item_key, item_data in self.data.items():
                    if item_data['throw'] and not item_data['hit']:
                        # Vérifier si cet item a la lettre assignée
                        if item_data.get('assigned_letter') == key_name:
                            item_data['hit'] = True
                            
                            # Extraire le nom de base du fruit (sans la lettre)
                            if '_' in item_key:
                                base_name = item_key.split('_')[0]
                            else:
                                base_name = item_key
                            
                            if base_name == 'bomb':
                                # BOMBE TOUCHÉE
                                self.player_lives -= 3
                                self.combo = 1
                                try:
                                    item_data['img'] = pygame.image.load("images/explosion.png")
                                except:
                                    item_data['img'] = pygame.Surface((60, 60))
                                    item_data['img'].fill((255, 100, 0))
                                if self.player_lives <= 0:
                                    self.end_game()
                            
                            elif base_name == 'ice_cube2':
                                # GLAÇON TOUCHÉ - RALENTISSEMENT
                                self.slow_motion_timer = self.SLOW_MOTION_DURATION * self.FPS
                                
                                # Créer un effet visuel "brisé" pour le glaçon
                                try:
                                    # Essayer de charger l'image half_ice_cube2
                                    ice_img = pygame.image.load("images/half_ice_cube2.png")
                                    item_data['img'] = ice_img
                                except:
                                    # Si l'image n'existe pas, créer un effet visuel bleu clair
                                    ice_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
                                    # Dessiner des éclats de glace (plusieurs rectangles bleus)
                                    ice_surface.fill((150, 220, 255, 200))  # Bleu clair translucide
                                    # Ajouter des lignes blanches pour effet "brisé"
                                    pygame.draw.line(ice_surface, (255, 255, 255), (10, 10), (50, 50), 2)
                                    pygame.draw.line(ice_surface, (255, 255, 255), (50, 10), (10, 50), 2)
                                    pygame.draw.line(ice_surface, (200, 230, 255), (30, 0), (30, 60), 2)
                                    item_data['img'] = ice_surface
                                
                                if self.settings:
                                    self.settings.play_impact_sound()
                                
                                self.combo = min(self.combo + 1, self.max_combo)
                                self.score += self.combo
                                self.max_score_reached = max(self.max_score_reached, self.score)
                            
                            else:
                                # C'EST UN FRUIT
                                try:
                                    item_data['img'] = pygame.image.load(f"images/half_{base_name}.png")
                                except:
                                    item_data['img'] = pygame.Surface((60, 60))
                                    item_data['img'].fill((0, 255, 0))
                                
                                if self.settings:
                                    self.settings.play_impact_sound()
                                
                                self.combo = min(self.combo + 1, self.max_combo)
                                self.score += self.combo
                                self.max_score_reached = max(self.max_score_reached, self.score)
                            
                            # Sortir après avoir trouvé le premier item
                            break

    def update(self, y_offset=0):
        if self.game_over:
            return

        # MODE 1: Gestion souris
        if self.game_mode == 1:
            current_position = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
        
        self.spawn_timer += 1

        # Slow motion (fonctionne dans les deux modes)
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
                
                # Empêcher les fruits de sortir par les côtés de l'écran
                item_size = value.get('size', 60)
                if value['x'] < 0:
                    value['x'] = 0
                    value['speed_x'] = abs(value['speed_x'])  # Rebondir
                elif value['x'] > self.WIDTH - item_size:
                    value['x'] = self.WIDTH - item_size
                    value['speed_x'] = -abs(value['speed_x'])  # Rebondir

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
                        # Mode 2 : pénaliser tous les fruits ratés (sauf bombe et glaçon)
                        # Extraire le nom de base
                        if '_' in key:
                            base_name = key.split('_')[0]
                        else:
                            base_name = key
                        
                        # Pénaliser si c'est un fruit (pas bombe ni glaçon)
                        if not value['hit'] and base_name not in ['bomb', 'ice_cube2']:
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
                            # Effet visuel pour fruit ou glaçon coupé
                            if key == 'ice_cube2':
                                # Effet spécial pour le glaçon
                                try:
                                    value['img'] = pygame.image.load("images/half_ice_cube2.png")
                                except:
                                    # Effet visuel bleu "brisé"
                                    ice_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
                                    ice_surface.fill((150, 220, 255, 200))
                                    pygame.draw.line(ice_surface, (255, 255, 255), (10, 10), (50, 50), 2)
                                    pygame.draw.line(ice_surface, (255, 255, 255), (50, 10), (10, 50), 2)
                                    pygame.draw.line(ice_surface, (200, 230, 255), (30, 0), (30, 60), 2)
                                    value['img'] = ice_surface
                            else:
                                # Fruits normaux
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

        # Effet gel (fonctionne dans les deux modes)
        if self.slow_motion_timer > 0:
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