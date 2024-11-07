import pygame
# Initialiser le module
import argparse
#Sert a donner des instructions
DEFAULT_HEIGHT=300
DEFAULT_WIGHT=400
MIN_H=100 ; MAX_H=700
MIN_W=200 ; MAX_W=800
# lancer le jeu : donner les arguments : poetry run jeu -H valeur -W valeur
def argu() :
    parser = argparse.ArgumentParser(description='Width and height of the screen')
    parser.add_argument('-W','--width', type=int, default=DEFAULT_WIGHT,  help="Screen width")
    parser.add_argument('-H','--height', type=int, default=DEFAULT_HEIGHT, help="Screen height")
    args = parser.parse_args()
    #if args.W < MIN_W or args.W>MAX_W:
     #   raise ValueError("The size (-W argument) must be in [200,800]")
   # if args.H < MIN_H or args.H<MAX_H:
   #    raise ValueError("The size (-H argument) must be in [100,700]")                    
    return args

def jeu() : 
    args=argu()

    pygame.init()

    screen = pygame.display.set_mode( (400, 300) )

    pygame.display.set_caption("Ecran de jeu")

    clock = pygame.time.Clock()

    while True:

        clock.tick(1)

        for event in pygame.event.get():
            pass

        screen.fill( (0, 0, 0 ))

        pygame.display.update()


pygame.quit()



