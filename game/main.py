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
    settings_menu = SettingsMenu(WIDTH, HEIGHT)
    score_manager = Score()  
    top_bar = TopBar(WIDTH, height=BAR_HEIGHT)
    game = Game(WIDTH, HEIGHT - BAR_HEIGHT)
    clock = pygame.time.Clock()
    game_state = "MENU"
    running = True

    while running:
        if game_state == "MENU":
            main_menu.draw(screen)

            for event in pygame.event.get():
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
            # Affichage de la page des scores
            action, screen = score_manager.page_scores(screen, clock)
            if action == "menu":
                game_state = "MENU"
            elif action == "quitter":
                running = False

        elif game_state == "PLAYING":

            for event in pygame.event.get():
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

            font_small = pygame.font.Font(None, 20)
            instructions = font_small.render(
                "ESPACE: Timer | R: Reset | D: Debug | ESC: Menu",
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