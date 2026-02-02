import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_SPACE, K_r
import sys
from bar_game import TopBar
from game import Game
from main_itrfc import MainMenu
from settings_menu import SettingsMenu
from settings import Setting
from slider import Slider
from score import Score

def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    settings = Setting()
    settings.play_music()

    WIDTH, HEIGHT = 800, 580
    BAR_HEIGHT = 80
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Final Fantasy Fruits")

    main_menu = MainMenu(WIDTH, HEIGHT)
    
    # MODIFICATION: Pass settings to SettingsMenu
    settings_menu = SettingsMenu(WIDTH, HEIGHT, settings=settings)
    
    score_manager = Score()  
    top_bar = TopBar(WIDTH, height=BAR_HEIGHT)
    
    # Pass settings to Game
    game = Game(WIDTH, HEIGHT - BAR_HEIGHT, settings=settings)
    
    clock = pygame.time.Clock()
    game_state = "MENU"
    running = True

    while running:
        if game_state == "MENU":
            main_menu.draw(screen)

            for event in pygame.event.get():
                # Handle TopBar events for mode changes
                top_bar.handle_event(event)
                
                action = main_menu.handle_event(event)

                if action == "START":
                    game_state = "PLAYING"
                    game.start_game()
                    top_bar.reset()
                    top_bar.start()
                elif action == "QUIT":
                    running = False
                elif action == "SETTINGS":
                    game_state = "SETTINGS"
                elif action == "SCORES":
                    game_state = "SCORES"
            
            # Sync the mode between TopBar and Game
            topbar_mode = top_bar.get_game_mode()
            game.set_game_mode(topbar_mode)
            
            # Update TopBar for hover effects
            top_bar.update()
            
            pygame.display.flip()
            clock.tick(60)

        elif game_state == "SETTINGS":
            settings_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                action = settings_menu.handle_event(event)
                if action == "BACK":
                    game_state = "MENU"
            pygame.display.flip()
            clock.tick(60)

        elif game_state == "SCORES":
            # Display the scores page
            action, screen = score_manager.page_scores(screen, clock)
            if action == "menu":
                game_state = "MENU"
            elif action == "quitter":
                running = False

        elif game_state == "PLAYING":

            for event in pygame.event.get():
                # Handle TopBar events
                top_bar.handle_event(event)
                
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        game_state = "MENU"
                        top_bar.pause()

                    elif event.key == K_SPACE:
                        top_bar.toggle()
                    elif event.key == K_r:
                        game.start_game()
                        top_bar.reset()
                        top_bar.start()
                    elif event.key == pygame.K_d:
                        game.toggle_debug()
                    else:
                        # MODE 2: Forward key presses to the game for letters
                        game.handle_keyboard_input(event)

            # SYNC GAME MODE
            topbar_mode = top_bar.get_game_mode()  # "jeu1" or "jeu2"
            game.set_game_mode(topbar_mode)  # Converts to 1 or 2
            
            # Reverse check
            game_mode_text = game.get_game_mode_text()  # "jeu1" or "jeu2"
            if game_mode_text != topbar_mode:
                top_bar.set_game_mode(game_mode_text)

            if top_bar.is_finished() and not game.is_game_over():
                game.end_game()
                top_bar.pause()
                game_state = "GAME_OVER"

            if game.is_game_over():
                game.end_game()
                top_bar.pause()
                game_state = "GAME_OVER"

            top_bar.update()
            game.update(y_offset=BAR_HEIGHT)
            screen.fill((0, 0, 0))
            top_bar.draw(screen)

            game.draw(screen, y_offset=BAR_HEIGHT)

            # Instructions adapted to the mode
            font_small = pygame.font.Font(None, 20)
            if game.get_game_mode() == 1:
                instructions = font_small.render(
                    "MODE 1 - SPACE: Timer | R: Reset | D: Debug | ESC: Menu",
                    True, (255, 255, 255)
                )
            else:
                instructions = font_small.render(
                    "MODE 2 - Type letters on keyboard! | SPACE: Timer | R: Reset | ESC: Menu",
                    True, (255, 255, 255)
                )
            screen.blit(instructions, (10, HEIGHT - 25))

            pygame.display.flip()
            clock.tick(game.FPS)

        elif game_state == "GAME_OVER":
            action = game.show_gameover_screen(screen, clock)

            if action == "RESTART":
                game_state = "PLAYING"
                game.start_game()
                top_bar.reset()
                top_bar.start()
            elif action == "MENU":
                game_state = "MENU"
                top_bar.reset()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
