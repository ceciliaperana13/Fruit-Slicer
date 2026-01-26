import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_f
import sys
from settings import Setting
from settings_menu import *
from bar_game import TopBar


def main():
    pygame.init()
    
    settings = Setting()

    # Appliquer l'écran
    screen = settings.apply_screen()
    pygame.display.set_caption("Fruit Slicer")

    # Lancer la musique
    settings.play_music()

    # Menu des paramètres
    settings_menu = SettingsMenu(settings)

    # Créer la barre de jeu
    top_bar = TopBar(settings.screen_width, height=80)

    # Boucle principale
    clock = pygame.time.Clock()
    running = True
    show_settings = False
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if show_settings:
                        show_settings = False
                    else:
                        running = False
                elif event.key == K_f:
                    settings.fullscreen = not settings.fullscreen
                    screen = settings.apply_screen()
                    if settings.fullscreen:
                        info = pygame.display.Info()
                        settings.screen_width = info.current_w
                        settings.screen_height = info.current_h
                        # Recréer la barre avec la nouvelle largeur
                        top_bar = TopBar(settings.screen_width, height=80)
                elif event.key == pygame.K_SPACE and not show_settings:
                    top_bar.toggle()  # Démarrer/Pause le chronomètre
                elif event.key == pygame.K_r and not show_settings:
                    top_bar.reset()   # Réinitialiser le chronomètre

            # Gérer les événements du menu des paramètres
            if show_settings:
                show_settings = settings_menu.handle_event(event)

        # Mettre à jour le chronomètre
        if not show_settings:
            top_bar.update()

        # Remplir le fond
        screen.fill(settings.bg_color)

        if show_settings:
            # Afficher le menu des paramètres
            settings_menu.draw(screen)
        else:
            # Dessiner la barre EN PREMIER après le fill
            top_bar.draw(screen)
            
            # Jeu normal - dessiner un rectangle violet pour test (sous la barre)
            pygame.draw.rect(screen, settings.VIOLET, (100, 100, 200, 150))
            
            # Bouton pour ouvrir les paramètres
            font = pygame.font.Font(None, 36)
            text = font.render("Appuyez sur S pour Settings", True, settings.NOIR)
            screen.blit(text, (200, 500))
            
            # Instructions pour le timer
            timer_info = font.render("ESPACE: Start/Pause | R: Reset", True, settings.NOIR)
            screen.blit(timer_info, (150, 300))
            
            # Vérifier si on appuie sur S
            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                show_settings = True

        # Mettre à jour l'affichage
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()