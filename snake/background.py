import pygame
# Initialiser le module
import argparse
#Sert a donner des instructions

from .classes import CheckerBoard, Snake, Fruit

DEFAULT_LINES=20 #Nombre de lignes par defaut
DEFAULT_COLUMNS=30 #Nombre de colonnes par defaut
DEFAULT_SIZE= 50# Taille du carre par defaut
#SNAKE=[3,1]


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

## Meilleure version du jeu 

# Function to display the score

def display_score(screen, score):
    font = pygame.font.Font(None, 40)  # Default font and size
    score_surface = font.render(f'Score: {score}', True, (255, 0, 0))
    screen.blit(score_surface, (10, 10))  # Draw score at (10,10)



def jeu_bis() : 
    
    color_1=(0,0,0)
    colors_2=(255,255,255)

    columns=30
    lines=20
    size=30

    hauteur=lines*size
    largeur=columns*size

    color_sna=(0,255,0)
    color_head=(0,0,255)
    l_sna=10 # ligne de départ du snake
    c_sna=5 # colonne de départ (position de la tête)
    #taille_sna=[3,1]
    taille_sna=5
    
    speed=5

    color_fruit=(255,0,0)
    pos_fruit_1=[3,3] #line, column
    pos_fruit_2=[10,15]



    screen = pygame.display.set_mode( (hauteur, largeur) )

    MyCheckerBoard=CheckerBoard(color_1,colors_2,columns,lines,size)
    MySnake=Snake(color_sna,color_head,l_sna,c_sna,taille_sna, size)
    Myfruit=Fruit(color_fruit, pos_fruit_1[1],pos_fruit_1[0], size) # on commence par placer le fruit en position 1
    
    direction = 'LEFT' # le serpent va commencer par se déplacer vers la gauche

    score=0


    pygame.init()


    pygame.display.set_caption("Ecran de jeu")




    clock = pygame.time.Clock()

    #on initialise pour sortir du jeu correctement entre autres
    game=True
    while game==True:

        clock.tick(speed)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game=False
            if event.type == pygame.KEYDOWN : #on precise qu'il s'agit d'un evnt qui concerne le clavier
                if event.key ==pygame.K_q :
                    game=False
                

                if event.key==pygame.K_RIGHT :
                    score=MySnake.move_right(screen, lines, score) #remettre le score à 0 si on touche les bords
                    direction='RIGHT'
                    break # permet de ne pas appuyer sur plusieurs touches
                    
                if event.key == pygame.K_LEFT :
                    score=MySnake.move_left(screen, score) 
                    direction='LEFT'
                    break
                    
                if event.key == pygame.K_UP :
                    score=MySnake.move_up(screen, score)
                    direction='UP'
                    break
                   
                if event.key == pygame.K_DOWN :
                    score=MySnake.move_down(screen,columns, score) 
                    direction = 'DOWN'
                    break
   

        
        
        #bien laisser la boucle d'evnt avant d'afficher
        

        MyCheckerBoard.tracer(screen)
        MySnake.draw(screen)
        Myfruit.draw(screen)

        MySnake.move_global(direction, screen, columns, lines, score)
        score=Myfruit.collusion(MySnake, pos_fruit_1, pos_fruit_2, screen, direction, score)

        display_score(screen, score)


    

    


        pygame.display.update() #afficher a la fin


    pygame.quit()




