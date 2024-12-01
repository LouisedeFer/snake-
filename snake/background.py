import pygame
# Initialiser le module
import argparse
#Sert a donner des instructions

from .classes import CheckerBoard, Snake, Tiles

DEFAULT_LINES=12 #Nombre de lignes par defaut
DEFAULT_COLUMNS=20 #Nombre de colonnes par defaut
DEFAULT_SIZE= 50# Taille du carre par defaut
SNAKE=[3,1]


#MIN_H=100 ; MAX_H=700
#MIN_W=200 ; MAX_W=800


# lancer le jeu : donner les arguments : poetry run jeu -L valeur -C valeur
def argu() :
    parser = argparse.ArgumentParser(description='Width and height of the screen')
    parser.add_argument('-L','--lines', type=int, default=DEFAULT_LINES,  help="Screen wight (number of columns)")
    parser.add_argument('-C','--columns', type=int, default=DEFAULT_COLUMNS, help="Screen height (number of lines)")
    parser.add_argument('-S','--square_size', type=int, default=DEFAULT_SIZE, help="Size of a square")
    args = parser.parse_args()
    #if args.W < MIN_W or args.W>MAX_W:
     #   raise ValueError("The size (-W argument) must be in [200,800]")
   # if args.H < MIN_H or args.H<MAX_H:
   #    raise ValueError("The size (-H argument) must be in [100,700]")                    
    return args




def tracer_noir(screen,size) :
    args=argu()

    color = (0, 0, 0) #on part d"un ecran blanc et on va tracer les carres noirs

    for i in range (args.columns) : #on parcourt les colonnes
        for j in range(args.lines) : #on parcourt les lignes
            if (i+j)%2==0 : 
                rect = pygame.Rect(i*size, j*size, size, size)
                pygame.draw.rect(screen, color, rect)
     

def tracer_snake(screen, snake, lines, columns, size) : #prend en argument le screen, le tuple de la taille du serpent, sa ligne de depart et sa ligne d'arrivee
    sna=pygame.Rect(columns*size, lines*size,snake[0]*size, snake[1]*size )

    color=(0,255,0)
    pygame.draw.rect(screen, color, sna)

    

def jeu() : 
    args=argu()

    size=args.square_size
    largeur=args.lines * size
    hauteur=args.columns * size
    



    pygame.init()

    screen = pygame.display.set_mode( (hauteur, largeur) )

    pygame.display.set_caption("Ecran de jeu")

    clock = pygame.time.Clock()

    #on initialise pour sortir du jeu correctement entre autres
    game=True
    while game==True:

        clock.tick(20)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game=False
            if event.type == pygame.KEYDOWN : #on precise qu'il s'agit d'un evnt qui concerne le clavier
                if event.key ==pygame.K_q :
                    game=False

        
        
        #bien laisser la boucle d'evnt avant d'afficher
        screen.fill( (255, 255, 255)) #on fait un grand écran blanc où on va rajouter les carrés noirs
        tracer_noir(screen, size)

        tracer_snake(screen,SNAKE,10,5,size)


        pygame.display.update() #afficher a la fin


    pygame.quit()


def jeu_bis() : 
    
    color_1=(0,0,0)
    colors_2=(255,255,255)

    columns=20
    lines=15
    size=30

    hauteur=lines*size
    largeur=columns*size

    color_sna=(0,255,0)
    color_head=(0,0,255)
    l_sna=10 # ligne de départ du snake
    c_sna=5 # colonne de départ (position de la tête)
    #taille_sna=[3,1]
    taille_sna=5


    color_fruit=(255,0,0)
    col_fruit_1=3
    line_fruit_1=3
    col_fruit_2=15
    line_fruit_2=10


    screen = pygame.display.set_mode( (hauteur, largeur) )

    MyCheckerBoard=CheckerBoard(color_1,colors_2,columns,lines,size)
    MySnake=Snake(color_sna,color_head,l_sna,c_sna,taille_sna, size)

    direction = 'LEFT' # le serpent va commencer par se déplacer vers la gauche


    Myfruit=Tiles(color_fruit,size, col_fruit_1,line_fruit_1) # on commence par placer le fruit


    
 

    pygame.init()

    

    pygame.display.set_caption("Ecran de jeu")

    clock = pygame.time.Clock()

    #on initialise pour sortir du jeu correctement entre autres
    game=True
    while game==True:

        clock.tick(5)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game=False
            if event.type == pygame.KEYDOWN : #on precise qu'il s'agit d'un evnt qui concerne le clavier
                if event.key ==pygame.K_q :
                    game=False
                if event.key==pygame.K_RIGHT :
                    MySnake.move_right(screen, lines)
                    direction='RIGHT'
                    MySnake.fruit_meeting(screen, Myfruit, color_fruit, col_fruit_1, line_fruit_1, col_fruit_2, line_fruit_2)
                if event.key == pygame.K_LEFT :
                    MySnake.move_left(screen) 
                    direction='LEFT'
                    MySnake.fruit_meeting(screen, Myfruit, color_fruit, col_fruit_1, line_fruit_1, col_fruit_2, line_fruit_2)
                if event.key == pygame.K_UP :
                    MySnake.move_up(screen)
                    direction='UP'
                    MySnake.fruit_meeting(screen, Myfruit, color_fruit, col_fruit_1, line_fruit_1, col_fruit_2, line_fruit_2)
                if event.key == pygame.K_DOWN :
                    MySnake.move_down(screen,columns) 
                    direction = 'DOWN'
                    MySnake.fruit_meeting(screen, Myfruit, color_fruit, col_fruit_1, line_fruit_1, col_fruit_2, line_fruit_2)  

        
        
        #bien laisser la boucle d'evnt avant d'afficher
        

        MyCheckerBoard.tracer(screen)
        MySnake.draw(screen)

        MySnake.move_global(direction, screen, columns, lines)
        Myfruit.draw(screen)

    

    


        pygame.display.update() #afficher a la fin


    pygame.quit()




