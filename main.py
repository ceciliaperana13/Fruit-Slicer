import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_f
import sys
from settings import Setting
from settings_menu import *


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

            # Gérer les événements du menu des paramètres
            if show_settings:
                show_settings = settings_menu.handle_event(event)

        # Remplir le fond
        screen.fill(settings.bg_color)

        if show_settings:
            # Afficher le menu des paramètres
            settings_menu.draw(screen)
        else:
            # Jeu normal - dessiner un rectangle violet pour test
            pygame.draw.rect(screen, settings.VIOLET, (100, 100, 200, 150))
            
            # Bouton pour ouvrir les paramètres
            font = pygame.font.Font(None, 36)
            text = font.render("Appuyez sur S pour Settings", True, settings.NOIR)
            screen.blit(text, (200, 500))
            
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