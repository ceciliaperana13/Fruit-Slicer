import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_SPACE, K_r
import sys
from bar_game import TopBar
from game import Game
from main_itrfc import MainMenu


def main():
    """Fonction principale du jeu"""
    pygame.init()
    
    # Configuration de l'écran
    WIDTH = 800
    HEIGHT = 580  # 500 pour le jeu + 80 pour la barre
    BAR_HEIGHT = 80
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Final Fantasy Fruits")
    
    # Créer le menu principal
    main_menu = MainMenu(WIDTH, HEIGHT)
    
    # Créer la barre supérieure
    top_bar = TopBar(WIDTH, height=BAR_HEIGHT)
    
    # Créer le jeu
    game = Game(WIDTH, HEIGHT - BAR_HEIGHT)
    
    # Horloge pour contrôler le FPS
    clock = pygame.time.Clock()
    
    # État du jeu
    game_state = "MENU"  # MENU, PLAYING, GAME_OVER
    
    # Boucle principale
    running = True
    while running:
        
        # ===== ÉTAT : MENU =====
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
                    print("Opening settings...")
                    # TODO: Implémenter l'écran des paramètres
                elif action == "SCORES":
                    print("Showing scores...")
                    # TODO: Implémenter l'écran des scores
            
            pygame.display.flip()
            clock.tick(60)
        
        # ===== ÉTAT : PLAYING =====
        elif game_state == "PLAYING":
            # Gérer les événements
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        # Retour au menu
                        game_state = "MENU"
                        top_bar.pause()
                        continue
                    elif event.key == K_SPACE:
                        top_bar.toggle()  # Démarrer/Pause le chronomètre
                    elif event.key == K_r:
                        top_bar.reset()   # Réinitialiser le chronomètre
                    elif event.key == pygame.K_d:
                        game.toggle_debug()  # Activer/Désactiver le mode debug
            
            # Vérifier si le temps est écoulé
            if top_bar.is_finished() and not game.is_game_over():
                game.end_game()
                top_bar.pause()
                game_state = "GAME_OVER"
            
            # Vérifier si le jeu est terminé (vies épuisées)
            if game.is_game_over():
                game.end_game()
                top_bar.pause()
                game_state = "GAME_OVER"
            
            # Mettre à jour
            top_bar.update()
            game.update(y_offset=BAR_HEIGHT)
            
            # Dessiner tout
            screen.fill((0, 0, 0))  # Fond noir
            
            # Dessiner la barre en haut
            top_bar.draw(screen)
            
            # Dessiner le jeu en dessous de la barre
            game.draw(screen, y_offset=BAR_HEIGHT)
            
            # Afficher les instructions
            font_small = pygame.font.Font(None, 20)
            instructions = font_small.render(
                "ESPACE: Timer | R: Reset | D: Debug | ESC: Menu", 
                True, 
                (255, 255, 255)
            )
            screen.blit(instructions, (10, HEIGHT - 25))
            
            # Mettre à jour l'affichage
            pygame.display.flip()
            clock.tick(game.FPS)
        
        # ===== ÉTAT : GAME OVER =====
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
            elif action == "QUIT":
                running = False
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()