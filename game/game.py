import pygame
import random
from score import Score


class Game:
    def __init__(self, width=800, height=580, settings=None):
        """Init the game"""
        self.WIDTH = width
        self.HEIGHT = height
        self.FPS = 12
        
        # Reference to the settings to access the impact sound
        self.settings = settings

        # Physics
        self.GRAVITY = 1.2
        self.NORMAL_SPEED_FACTOR = 0.3
        self.SPEED_FACTOR = self.NORMAL_SPEED_FACTOR
        self.SPAWN_DELAY = 15
        self.spawn_timer = 0

        # State of game
        self.player_lives = 3
        self.score = 0
        self.game_over = False
        self.debug_mode = False
        self.slow_motion_timer = 0
        self.SLOW_MOTION_DURATION = 3  # seconds
        self.game_mode = 1  # game mode (1 ou 2)
        self.mode_just_changed = False  # Flag game mode
        
        # Score manager
        self.score_manager = Score()
        self.player_name = "Player"  
        self.max_score_reached = 0  # Score max atteint dans la partie

        # COMBO
        self.combo = 1
        self.max_combo = 10

        # MODE 1: Fruits
        self.fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb', 'ice_cube2']
        
        # MODE 2: Letters (only 10)
        self.letters = list('AEIOBCFGH')  # 10 letters
        
        # List of active elements according to the mode
        self.active_items = []

        # Coulors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.ORANGE = (255, 128, 0)
        self.BLUE = (100, 150, 255)
        self.GREEN = (0, 255, 0)
        self.YELLOW = (255, 255, 0)

        # Load resources
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
            # Mode 1 
            self.active_items = self.fruits.copy()
        else:
            # Mode 2 : fruits with letters
            self.active_items = []
            
            # Fruits
            base_fruits = ['melon', 'orange', 'pomegranate', 'guava']
            
            # 10 fruits with index
            for i, letter in enumerate(self.letters):
                fruit = base_fruits[i % 4]  
                # ID for each fruits
                fruit_key = f"{fruit}_{letter}"
                self.active_items.append(fruit_key)
            
            # Add bomb + ice cube
            self.active_items.append('bomb')
            self.active_items.append('ice_cube2')

    def _create_letter_image(self, letter):
        """image per letter"""
        size = 80
        img = pygame.Surface((size, size), pygame.SRCALPHA)
        
        colors = [
            (255, 100, 100),  # RED
            (100, 255, 100),  # green
            (100, 100, 255),  # Blue
            (255, 255, 100),  # yellow
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
        # Create a copy of the base image
        new_img = base_img.copy()
        
        # Create the text of the letter
        try:
            letter_font = pygame.font.Font(self.font_name, 40) if self.font_name else pygame.font.Font(None, 40)
        except:
            letter_font = pygame.font.Font(None, 40)
        
        # Text with a white outline for visibility
        text = letter_font.render(letter, True, self.WHITE)
        text_outline = letter_font.render(letter, True, self.BLACK)
        
        # Center the letter on the image
        img_width, img_height = new_img.get_size()
        text_rect = text.get_rect(center=(img_width//2, img_height//2))
        
        # Draw the outline (offset by 2px in each direction)
        for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2), (-2, 0), (2, 0), (0, -2), (0, 2)]:
            outline_rect = text_rect.copy()
            outline_rect.x += dx
            outline_rect.y += dy
            new_img.blit(text_outline, outline_rect)
        
        # Draw letters
        new_img.blit(text, text_rect)
        
        return new_img

    def _generate_random_items(self, item):
        """Generates a random element (fruit or letter)"""
        is_letter = item.startswith('letter_')
        assigned_letter = None
        
        if is_letter:
            # Colored circle with letter (Mode 1 only, should not appear in Mode 2)
            letter = item.split('_')[1]
            img = self._create_letter_image(letter)
            item_size = 80
        else:
            # Mode 2, extract the fruit name and the assigned letter (format: fruit_LETTER)
            fruit_name = item
            if self.game_mode == 2 and '_' in item:
                parts = item.split('_')
                if parts[0] in ['melon', 'orange', 'pomegranate', 'guava']:
                    fruit_name = parts[0]
                    assigned_letter = parts[1]  # The letter assigned to this fruit
            
            # load images
            try:
                img = pygame.image.load(f"images/{fruit_name}.png")
            except:
                img = pygame.Surface((60, 60))
                img.fill((255, 0, 0) if fruit_name == 'bomb' else (0, 255, 0))
            item_size = 60
            
            # MODE 2: add letters
            if self.game_mode == 2:
                # If no letter is assigned (bomb or ice cube), choose a random one.
                if assigned_letter is None:
                    assigned_letter = random.choice(self.letters)
                
                # Overlay the letter onto the image
                img = self._add_letter_to_item(img, assigned_letter)

        self.data[item] = {
            'img': img,
            'x': random.randint(item_size, self.WIDTH - item_size),  
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
        """Generates all elements according to the active mode"""
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
        """player name"""
        self.player_name = name if name.strip() else "Player"

    def get_game_mode(self):
        return self.game_mode
    """return game mode"""
    def get_game_mode_text(self):
        """Returns the game mode to text format for the TopBar"""
        return f"jeu{self.game_mode}"
    
    def mode_has_changed(self):
        """Check if the mode has just changed (to force a reset in main.py)"""
        if self.mode_just_changed:
            self.mode_just_changed = False
            return True
        return False

    def set_game_mode(self, mode):
        """Sets the game mode (1 or 2, or 'game1' or 'game2')"""
        # Convert the text modes of the TopBar into numbers
        if mode == "jeu1":
            mode = 1
        elif mode == "jeu2":
            mode = 2
        
        if mode in [1, 2]:
            old_mode = self.game_mode
            self.game_mode = mode
            
            # If the mode has changed, clean EVERYTHING and regenerate.
            if old_mode != mode:
                self.mode_just_changed = True
                self._update_active_items()
                self._generate_all_items()
                # Complete reset to avoid mixing
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
        """End the game and save"""
        if not self.game_over:
            self.game_over = True
            
            # save score
            result = "WIN" if self.player_lives > 0 else "LOSE"
            attempts = 3 - self.player_lives
            max_attempts = 3
            
            # Format: Display the game mode properly
            mode_text = f"Mode {self.game_mode}"
            
            # Pass the current score directly (even if it is 0)
            self.score_manager.add_score(
                player_name=self.player_name,
                word=mode_text,
                result=result,
                attempts=attempts,
                max_attempts=max_attempts,
                final_score=self.score  # New parameters, final score
            )

    def is_game_over(self):
        return self.game_over

    def toggle_debug(self):
        self.debug_mode = not self.debug_mode

    def handle_keyboard_input(self, event):
        """Handles keyboard input for Mode 2 (fruits with letters)"""
        if self.game_mode != 2 or self.game_over:
            return
        
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key).upper()
            
            # check valid letters
            if len(key_name) == 1 and key_name in self.letters:
                
                # Search for all items with this assigned letter.
                for item_key, item_data in self.data.items():
                    if item_data['throw'] and not item_data['hit']:
                        # Check if this item has the assigned letter
                        if item_data.get('assigned_letter') == key_name:
                            item_data['hit'] = True
                            
                            # Extract the base name of the fruit (without the letter)
                            if '_' in item_key:
                                base_name = item_key.split('_')[0]
                            else:
                                base_name = item_key
                            
                            if base_name == 'bomb':
                                # touch BOMB 
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
                                # ice cube freezing
                                self.slow_motion_timer = self.SLOW_MOTION_DURATION * self.FPS
                                
                                # broken ice cube
                                try:
                                    # loadf half_ice_cube2
                                    ice_img = pygame.image.load("images/half_ice_cube2.png")
                                    item_data['img'] = ice_img
                                except:
                                    # Si l'image n'existe pas, créer un effet visuel bleu LIGTH
                                    ice_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
                                    # Draw ice effect
                                    ice_surface.fill((150, 220, 255, 200))  # Blue LIGTH translucent
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
                                # its a fruit
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
                            
                            # Exit after finding the first item
                            break

    def update(self, y_offset=0):
        if self.game_over:
            return

        # MODE 1: mouse
        if self.game_mode == 1:
            current_position = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
        
        self.spawn_timer += 1

        # Slow motion (game mode 1 and 2)
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
                
                # Prevent the fruit from spilling out the sides of the screen
                item_size = value.get('size', 60)
                if value['x'] < 0:
                    value['x'] = 0
                    value['speed_x'] = abs(value['speed_x'])  # Rebond
                elif value['x'] > self.WIDTH - item_size:
                    value['x'] = self.WIDTH - item_size
                    value['speed_x'] = -abs(value['speed_x'])  # Rebond

                # failed elements
                if value['y'] > self.HEIGHT:
                    value['throw'] = False
                    
                    if self.game_mode == 1:
                        if not value['hit'] and key != 'bomb':
                            self.player_lives -= 1
                            self.combo = 1
                            if self.player_lives <= 0:
                                self.end_game()
                    else:
                        # Mode 2 : Penalize all failed fruit (except bomb and ice cube)
                        # Extract base name
                        if '_' in key:
                            base_name = key.split('_')[0]
                        else:
                            base_name = key
                        
                        # Penalize if it's a piece of fruit (not a bomb or an ice cube)
                        if not value['hit'] and base_name not in ['bomb', 'ice_cube2']:
                            self.player_lives -= 1
                            self.combo = 1
                            if self.player_lives <= 0:
                                self.end_game()

                # MODE 1: Collision 
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
                            # visual effect
                            if key == 'ice_cube2':
                                # visual effect ice cube
                                try:
                                    value['img'] = pygame.image.load("images/half_ice_cube2.png")
                                except:
                                    # "Broken" blue visual effect
                                    ice_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
                                    ice_surface.fill((150, 220, 255, 200))
                                    pygame.draw.line(ice_surface, (255, 255, 255), (10, 10), (50, 50), 2)
                                    pygame.draw.line(ice_surface, (255, 255, 255), (50, 10), (10, 50), 2)
                                    pygame.draw.line(ice_surface, (200, 230, 255), (30, 0), (30, 60), 2)
                                    value['img'] = ice_surface
                            else:
                                # Normals fruits
                                try:
                                    value['img'] = pygame.image.load(f"images/half_{key}.png")
                                except:
                                    value['img'] = pygame.Surface((60, 60))
                                    value['img'].fill((0, 255, 0))

                            # Impact(sound)
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

        # lifes
        self._draw_lives(display, 690, y_offset + 5, self.player_lives, 'images/ff8_vie4(1).png')

        # elements
        for value in self.data.values():
            if value['throw'] and value['y'] <= self.HEIGHT:
                display.blit(value['img'], (value['x'], value['y'] + y_offset))

        # ice effect
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
        """Load game over screen"""
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