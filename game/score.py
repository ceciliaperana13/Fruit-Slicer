import pygame
import math
import random
from datetime import datetime
from button_score import Button


class Score:
    """Class to handle displaying and saving scores with a Fruit Ninja style"""
    
    def __init__(self):
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLUE = (70, 130, 180)
        self.GREEN = (46, 125, 50)
        self.RED = (220, 50, 50)
        self.FOND = (30, 30, 50)
        self.GRAY = (200, 200, 200)
        self.ORANGE = (255, 140, 0)
        self.YELLOW = (255, 215, 0)
        
        # File configuration
        self.SCORES_FILE = "scores.txt"
        
        # Animation variables
        self.particles = []
        self.wave_offset = 0
        
    def draw_title(self, screen, text, size, color):
        """Draw a centered title with style effect"""
        try:
            font = pygame.font.Font('./images/comic.ttf', size)
        except:
            font = pygame.font.Font(None, size)
        
        title_surf = font.render(text, True, color)
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 60))
        
        # Shadow
        shadow_surf = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surf.get_rect(center=(screen.get_width() // 2 + 3, 63))
        screen.blit(shadow_surf, shadow_rect)
        
        # Title
        screen.blit(title_surf, title_rect)
    
    def create_particles(self, screen_width, screen_height):
        """Create particles for Fruit Ninja effect"""
        particles = []
        for _ in range(30):
            # Generate random position on the screen
            x = random.uniform(0, screen_width)
            y = random.uniform(0, screen_height)
            
            # Generate random speed
            speed_x = random.uniform(-2, 2)
            speed_y = random.uniform(-2, 2)
            
            # Random size and color
            size = random.uniform(2, 5)
            color = self.ORANGE if random.random() > 0.5 else self.YELLOW
            
            particle = {
                'x': [x, y],
                'speed': [speed_x, speed_y],
                'size': size,
                'alpha': 255,
                'color': color
            }
            particles.append(particle)
        return particles
    
    def update_particles(self, particles, screen_width, screen_height):
        """Update particles for animation"""
        for particle in particles:
            particle['x'][0] += particle['speed'][0]
            particle['x'][1] += particle['speed'][1]
            particle['alpha'] = max(0, particle['alpha'] - 2)
            
            # Reset if off-screen or invisible
            if (particle['x'][0] < 0 or particle['x'][0] > screen_width or 
                particle['x'][1] < 0 or particle['x'][1] > screen_height or 
                particle['alpha'] <= 0):
                particle['x'][0] = random.uniform(0, screen_width)
                particle['x'][1] = random.uniform(0, screen_height)
                particle['alpha'] = 255
    
    def draw_background(self, screen):
        """Draw a Fruit Ninja style background with gradient and particles"""
        screen_width, screen_height = screen.get_size()
        
        # Background gradient
        for y in range(screen_height):
            progress = y / screen_height
            r = int(20 + progress * 30)
            g = int(20 + progress * 40)
            b = int(40 + progress * 20)
            pygame.draw.line(screen, (r, g, b), (0, y), (screen_width, y))
        
        # Decorative waves
        self.wave_offset += 0.5
        for i in range(3):
            points = []
            for x in range(0, screen_width + 10, 10):
                y = screen_height // 2 + math.sin((x + self.wave_offset + i * 100) * 0.01) * (30 + i * 20)
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(screen, (60 + i * 20, 70 + i * 20, 90 + i * 20), False, points, 2)
        
        # Draw particles
        for particle in self.particles:
            if particle['alpha'] > 0:
                surf = pygame.Surface((int(particle['size'] * 2), int(particle['size'] * 2)), pygame.SRCALPHA)
                color_with_alpha = particle['color'] + (int(particle['alpha']),)
                pygame.draw.circle(surf, color_with_alpha, 
                                 (int(particle['size']), int(particle['size'])), 
                                 int(particle['size']))
                screen.blit(surf, (int(particle['x'][0] - particle['size']), 
                                  int(particle['x'][1] - particle['size'])))
    
    def load_scores(self):
        """Load scores from scores.txt"""
        try:
            with open(self.SCORES_FILE, "r", encoding="utf-8") as f:
                scores = []
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split("|")
                        if len(parts) >= 7:
                            score_entry = {
                                "player": parts[0],
                                "mode": parts[1],  # Changed from "word" to "mode"
                                "result": parts[2],
                                "score": int(parts[3]),
                                "attempts": int(parts[4]),
                                "max_attempts": int(parts[5]),
                                "date": parts[6],
                                "timestamp": float(parts[7]) if len(parts) > 7 else 0
                            }
                            scores.append(score_entry)
                return scores
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error loading scores: {e}")
            return []

    def save_all_scores(self, scores):
        """Save all scores to the file"""
        try:
            with open(self.SCORES_FILE, "w", encoding="utf-8") as f:
                for score in scores:
                    line = f"{score['player']}|{score['mode']}|{score['result']}|{score['score']}|{score['attempts']}|{score['max_attempts']}|{score['date']}|{score['timestamp']}\n"
                    f.write(line)
        except Exception as e:
            print(f"Error saving scores: {e}")

    def add_score(self, player_name, word, result, attempts, max_attempts, final_score=None):
        """
        Add a new score to scores.txt
        
        Args:
            player_name: Player name
            word: Game mode (e.g., "Mode 1" or "Mode 2")
            result: "WIN" or "LOSE"
            attempts: Number of mistakes made
            max_attempts: Maximum allowed mistakes
            final_score: Final score of the game (NEW - required)
        """
        scores = self.load_scores()
        
        # Use the final score passed as parameter
        if final_score is not None:
            score_value = final_score  # Keep score as is, even if 0
        else:
            # Old calculation (fallback)
            if result == "WIN":
                score_value = max(100 - (attempts * 10), 10)
            else:
                score_value = 0
        
        new_score = {
            "player": player_name,
            "mode": word,  # "Mode 1" or "Mode 2"
            "result": result,
            "score": score_value,  # Final score, even if LOSE
            "attempts": attempts,
            "max_attempts": max_attempts,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "timestamp": datetime.now().timestamp()
        }
        
        scores.append(new_score)
        
        # Sort by descending score, then by date
        scores.sort(key=lambda x: (-x["score"], -x["timestamp"]))
        
        # Save to file
        self.save_all_scores(scores)
        
        print(f"✓ Score saved: {player_name} - {word} - {result} - {score_value} points")

    def clear_scores(self):
        """Clear all scores from the file"""
        try:
            with open(self.SCORES_FILE, "w", encoding="utf-8") as f:
                f.write("")
            print("Scores cleared")
        except Exception as e:
            print(f"Error clearing scores: {e}")

    def page_scores(self, screen, clock):
        """Display score history in real-time from scores.txt with all effects"""
        
        btn_return = Button(300, 520, 200, 50, "RETURN", self.GREEN)
        btn_clear = Button(100, 520, 180, 50, "CLEAR ALL", self.RED)
        
        scroll_offset = 0
        
        # Initialize particles
        self.particles = self.create_particles(screen.get_width(), screen.get_height())
        
        while True:
            pos = pygame.mouse.get_pos()
            
            # Reload scores from file each frame
            scores_data = self.load_scores()
            max_scroll = max(0, len(scores_data) * 35 - 300)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quitter", screen
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_return.for_clic(pos):
                        return "menu", screen
                    
                    if btn_clear.for_clic(pos):
                        self.clear_scores()
                
                # Scroll with mouse wheel
                if event.type == pygame.MOUSEWHEEL:
                    scroll_offset = max(0, min(scroll_offset - event.y * 20, max_scroll))
            
            btn_return.check_hover(pos)
            btn_clear.check_hover(pos)
            
            # Draw animated background with particles
            self.draw_background(screen)
            self.update_particles(self.particles, screen.get_width(), screen.get_height())
            
            # Title with shine effect
            self.draw_title(screen, "SCOREBOARD", 40, self.WHITE)
            
            # Display scores
            font = pygame.font.Font(None, 28)
            y_offset = 150
            
            if not scores_data:
                no_scores = font.render("No scores yet! Play to add scores.", True, self.GRAY)
                screen.blit(no_scores, (screen.get_width() // 2 - no_scores.get_width() // 2, 250))
            else:
                # Table headers with semi-transparent background
                header_font = pygame.font.Font(None, 26)
                header_bg = pygame.Surface((760, 30), pygame.SRCALPHA)
                header_bg.fill((255, 255, 255, 30))
                screen.blit(header_bg, (20, y_offset - 5))
                
                rank_text = header_font.render("#", True, self.WHITE)
                player_text = header_font.render("Player", True, self.WHITE)
                mode_text = header_font.render("Mode", True, self.WHITE)
                result_text = header_font.render("Result", True, self.WHITE)
                score_text = header_font.render("Score", True, self.WHITE)
                date_text = header_font.render("Date", True, self.WHITE)
                
                screen.blit(rank_text, (30, y_offset))
                screen.blit(player_text, (80, y_offset))
                screen.blit(mode_text, (220, y_offset))
                screen.blit(result_text, (320, y_offset))
                screen.blit(score_text, (420, y_offset))
                screen.blit(date_text, (520, y_offset))
                
                y_offset += 35
                
                # Separator line with shine effect
                pygame.draw.line(screen, self.WHITE, (20, y_offset), (780, y_offset), 2)
                y_offset += 10
                
                # Display each score
                for i, score_entry in enumerate(scores_data):
                    item_y = y_offset + (i * 35) - scroll_offset
                    
                    # Only draw if visible
                    if item_y < y_offset - 40 or item_y > y_offset + 300:
                        continue
                    
                    # Alternating row background with semi-transparent effect
                    if i % 2 == 0:
                        row_bg = pygame.Surface((760, 32), pygame.SRCALPHA)
                        row_bg.fill((255, 255, 255, 10))
                        screen.blit(row_bg, (20, item_y - 2))
                    
                    # Rank with style
                    rank_color = self.YELLOW if i < 3 else self.GRAY
                    rank = font.render(f"#{i+1}", True, rank_color)
                    
                    # Player
                    player = font.render(score_entry["player"][:12], True, self.WHITE)
                    
                    # Mode with color based on mode
                    mode_value = score_entry["mode"]
                    mode_color = self.GREEN if "1" in mode_value else self.BLUE
                    mode = font.render(mode_value, True, mode_color)
                    
                    # Color based on result
                    result_color = self.GREEN if score_entry["result"] == "WIN" else self.RED
                    result = font.render(score_entry["result"], True, result_color)
                    
                    # Score - ALWAYS displayed, even if 0
                    score_val = font.render(str(score_entry["score"]), True, self.YELLOW)
                    
                    # Date
                    date = font.render(score_entry["date"].split()[0], True, self.GRAY)
                    
                    screen.blit(rank, (30, item_y))
                    screen.blit(player, (80, item_y))
                    screen.blit(mode, (220, item_y))
                    screen.blit(result, (320, item_y))
                    screen.blit(score_val, (420, item_y))
                    screen.blit(date, (520, item_y))
                
                # Scroll indicator with effect
                if max_scroll > 0:
                    info_text = font.render("Use mouse wheel to scroll", True, self.GRAY)
                    screen.blit(info_text, (screen.get_width() // 2 - info_text.get_width() // 2, 470))
            
            # Buttons with hover effects
            btn_clear.draw(screen)
            btn_return.draw(screen)
            
            pygame.display.flip()
            clock.tick(60)
