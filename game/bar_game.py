import pygame
from datetime import datetime


class TopBar:
    """Class to manage the top bar with timer, date and mode button"""
    
    def __init__(self, width, height=80, button_image_path='./images/chococo.png'):
        self.width = width
        self.height = height
        self.total_time = 90  # 1min 30sec (90 seconds)
        self.time_left = self.total_time
        self.timer_running = False
        self.last_tick = 0
        
        # Background gradient colors
        self.color1 = (128, 128, 128)  # Grey
        self.color2 = (59, 130, 246)  # Blue
        self.white = (255, 255, 255)
        self.red = (239, 68, 68)
        self.orange = (255, 165, 0)
        
        # Progress bar colors
        self.bar_color_green = (0, 200, 0)
        self.bar_color_orange = (255, 165, 0)
        self.bar_color_red = (255, 0, 0)
        self.bar_bg_color = (50, 50, 50)
        
        # Fonts - Smaller timer font
        try:
            self.font_large = pygame.font.Font('./images/comic.ttf', 36)  # Reduced from 48 to 36
            self.font_small = pygame.font.Font('./images/comic.ttf', 24)
        except:
            self.font_large = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)
        
        # Game mode button - Moved to the right
        self.button_width = 60
        self.button_height = 60
        self.button_x = self.width - 80  # Further to the right
        self.button_y = 10
        self.button_rect = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
        
        # Button states
        self.button_hovered = False
        self.button_pressed = False
        
        # Button image
        self.button_image = None
        if button_image_path:
            try:
                self.button_image = pygame.image.load(button_image_path)
                self.button_image = pygame.transform.scale(
                    self.button_image,
                    (self.button_width - 10, self.button_height - 10)
                )
            except Exception as e:
                print(f"Error: Unable to load image {button_image_path}: {e}")
                self.button_image = None
        
        # Game mode
        self.game_mode = "jeu1"  # Modes: "jeu1", "jeu2"
        self.available_modes = ["jeu1", "jeu2"]
    
    def get_current_date(self):
        """Returns the current date in French"""
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
        """Formats remaining time as MM:SS"""
        mins = int(self.time_left // 60)
        secs = int(self.time_left % 60)
        return f"{mins}:{secs:02d}"
    
    def draw_gradient(self, surface):
        """Draws the background gradient (grey to blue)"""
        for i in range(self.height):
            ratio = i / self.height
            r = int(self.color1[0] * (1 - ratio) + self.color2[0] * ratio)
            g = int(self.color1[1] * (1 - ratio) + self.color2[1] * ratio)
            b = int(self.color1[2] * (1 - ratio) + self.color2[2] * ratio)
            pygame.draw.line(surface, (r, g, b), (0, i), (self.width, i))
    
    def handle_event(self, event):
        """Handles mouse events for the button"""
        if event.type == pygame.MOUSEMOTION:
            # Detect hover
            old_hover = self.button_hovered
            self.button_hovered = self.button_rect.collidepoint(event.pos)
            
            # Change cursor
            if self.button_hovered:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.button_hovered:
                    self.button_pressed = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.button_pressed and self.button_hovered:
                    self.on_button_click()
                self.button_pressed = False
    
    def on_button_click(self):
        """Action on button click - Switches game mode"""
        current_index = self.available_modes.index(self.game_mode)
        next_index = (current_index + 1) % len(self.available_modes)
        self.game_mode = self.available_modes[next_index]
        
        print(f"Game mode changed: {self.game_mode}")
    
    def draw_button(self, surface):
        """Draws the game mode button - Image only with hover effect"""
        # Button image with hover effect
        if self.button_image:
            # Determine scale based on state
            if self.button_pressed:
                # Slightly smaller when pressed
                scale_factor = 0.9
            elif self.button_hovered:
                # Larger on hover
                scale_factor = 1.3
            else:
                # Normal size
                scale_factor = 1.0
            
            # Calculate new size
            base_size = self.button_width - 10
            new_width = int(base_size * scale_factor)
            new_height = int(base_size * scale_factor)
            
            # Resize image from original loaded image
            if scale_factor != 1.0:
                # Reload original image to avoid quality loss
                try:
                    original_image = pygame.image.load('./images/chococo.png')
                    scaled_image = pygame.transform.smoothscale(
                        original_image,
                        (new_width, new_height)
                    )
                except:
                    scaled_image = pygame.transform.smoothscale(
                        self.button_image,
                        (new_width, new_height)
                    )
            else:
                scaled_image = self.button_image
            
            # Center the image
            image_x = self.button_x + (self.button_width - scaled_image.get_width()) // 2
            image_y = self.button_y + (self.button_height - scaled_image.get_height()) // 2
            
            # Draw the image - THAT'S IT!
            surface.blit(scaled_image, (image_x, image_y))
    
    def start(self):
        """Starts the timer"""
        self.timer_running = True
        self.last_tick = pygame.time.get_ticks()
    
    def pause(self):
        """Pauses the timer"""
        self.timer_running = False
    
    def toggle(self):
        """Toggles between start and pause"""
        if self.timer_running:
            self.pause()
        else:
            self.start()
    
    def reset(self):
        """Resets the timer"""
        self.time_left = self.total_time
        self.timer_running = False
    
    def update(self):
        """Updates the timer and checks button hover"""
        # Continuously check button hover
        mouse_pos = pygame.mouse.get_pos()
        old_hover = self.button_hovered
        self.button_hovered = self.button_rect.collidepoint(mouse_pos)
        
        # Update cursor if state changed
        if self.button_hovered != old_hover:
            if self.button_hovered:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        # Timer update
        if self.timer_running and self.time_left > 0:
            current_tick = pygame.time.get_ticks()
            if current_tick - self.last_tick >= 1000:
                self.time_left -= 1
                self.last_tick = current_tick
            
            if self.time_left <= 0:
                self.time_left = 0
                self.timer_running = False
    
    def draw(self, surface):
        """Draws the full bar with gradient, date, timer, button and progress bar"""
        # Background gradient
        self.draw_gradient(surface)
        
        # Date on the left
        date_text = self.font_small.render(self.get_current_date(), True, self.white)
        surface.blit(date_text, (20, 20))
        
        # Mode button (right)
        self.draw_button(surface)
        
        # Timer in the center with semi-transparent background
        time_color = self.red if self.time_left <= 10 else self.white
        time_text = self.font_large.render(self.format_time(), True, time_color)
        time_rect = time_text.get_rect(center=(self.width // 2, self.height // 2 - 10))
        
        # Timer background
        timer_bg = pygame.Rect(
            time_rect.x - 15,
            time_rect.y - 8,
            time_rect.width + 30,
            time_rect.height + 16
        )
        
        # Semi-transparent background surface
        bg_surface = pygame.Surface((timer_bg.width, timer_bg.height), pygame.SRCALPHA)
        bg_surface.fill((255, 255, 255, 80))
        surface.blit(bg_surface, (timer_bg.x, timer_bg.y))
        pygame.draw.rect(surface, self.white, timer_bg, 2, border_radius=10)
        
        surface.blit(time_text, time_rect)
        
        # Progress bar at the bottom
        bar_width = self.width - 40
        bar_height = 12
        bar_x = 20
        bar_y = self.height - 18
        
        # Bar background
        pygame.draw.rect(
            surface,
            self.bar_bg_color,
            (bar_x, bar_y, bar_width, bar_height),
            border_radius=6
        )
        
        # Progress bar (decreases over time)
        progress = self.time_left / self.total_time
        progress_width = int(bar_width * progress)
        
        # Change color based on remaining time
        if self.time_left <= 10:
            bar_color = self.bar_color_red
        elif self.time_left <= 30:
            bar_color = self.bar_color_orange
        else:
            bar_color = self.bar_color_green
        
        if progress_width > 0:
            pygame.draw.rect(
                surface,
                bar_color,
                (bar_x, bar_y, progress_width, bar_height),
                border_radius=6
            )
    
    def is_finished(self):
        """Returns True if time is over"""
        return self.time_left <= 0
    
    def get_game_mode(self):
        """Returns the current game mode"""
        return self.game_mode
    
    def set_game_mode(self, mode):
        """Sets the game mode"""
        if mode in self.available_modes:
            self.game_mode = mode
        else:
            print(f"Invalid mode '{mode}'. Available modes: {self.available_modes}")
