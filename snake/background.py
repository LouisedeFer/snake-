# Initialiser le module
#import argparse

import pygame

#Sert a donner des instructions
from .classes import Board, CheckerBoard, Fruit, Snake, Dir

DEFAULT_LINES=20 #Nombre de lignes par defaut
DEFAULT_COLUMNS=30 #Nombre de colonnes par defaut
DEFAULT_SIZE= 50# Taille du carre par defaut





# lancer le jeu : donner les arguments : poetry run jeu -L valeur -C valeur
"""#def argu() :
    parser = argparse.ArgumentParser(description="Width and height of the screen")
    parser.add_argument("-L","--lines", type=int, default=DEFAULT_LINES,  help="Screen wight (number of columns)")
    parser.add_argument("-C","--columns", type=int, default=DEFAULT_COLUMNS, help="Screen height (number of lines)")
    parser.add_argument("-S","--square_size", type=int, default=DEFAULT_SIZE, help="Size of a square")
    #if args.W < MIN_W or args.W>MAX_W:
     #   raise ValueError("The size (-W argument) must be in [200,800]")  # noqa: ERA001
   # if args.H < MIN_H or args.H<MAX_H:
   #    raise ValueError("The size (-H argument) must be in [100,700]")  # noqa: ERA001
    return parser.parse_args()

def tracer_noir(screen,size) -> None:
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

def jeu() :  # plus utile maintenant
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

    """

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
    rows=20
    size=30

    height=rows*size
    width=columns*size

    color_sna=(0,255,0)
    #color_head=(0,0,255)
    r_sna=10 # ligne de départ du snake
    c_sna=5 # colonne de départ (position de la tête)
    size_sna=5
    
    speed=5

    color_fruit=(255,0,0)
    pos_fruit_1=[3,3] #row, column
    pos_fruit_2=[10,15]

    direction = Dir.LEFT #the snake starts by moving toward left

    screen = pygame.display.set_mode( (width, height) )

    MyCheckerBoard=CheckerBoard(color_1,colors_2,rows,columns)
    MySnake=Snake(color_sna,r_sna,c_sna,size_sna, direction)
    Myfruit=Fruit(color_fruit, pos_fruit_1[1],pos_fruit_1[0]) # on commence par placer le fruit en position 1
    


    score=0


    board=Board(screen=screen, tile_size=size)
    board.add_object(MyCheckerBoard) # the order matters ! checkerboard first
    board.add_object(MySnake)
    board.add_object(Myfruit)


    pygame.init()


    




    clock = pygame.time.Clock()

    #on initialise pour sortir du jeu correctement entre autres
    game=True
    while game==True:

        clock.tick(speed)


        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                game=False
            if event.type == pygame.KEYDOWN : #on precise qu'il s'agit d'un evnt qui concerne le clavier
                if event.key ==pygame.K_q :
                    game=False
                

                if event.key==pygame.K_RIGHT :
                    MySnake.dir=Dir.RIGHT
                    #score=Myfruit.collusion(MySnake, pos_fruit_1, pos_fruit_2, score)
                    direction=(0,1)
                    break
                    
                    
                if event.key == pygame.K_LEFT :
                    MySnake.dir=Dir.LEFT
                    #score=Myfruit.collusion(MySnake, pos_fruit_1, pos_fruit_2, score)
                    direction=(0,-1)
                    break
                
                    
                if event.key == pygame.K_UP :
                    MySnake.dir=Dir.UP
                    #score=Myfruit.collusion(MySnake, pos_fruit_1, pos_fruit_2, score)
                    direction=(-1,0)
                    break
                   
                if event.key == pygame.K_DOWN :
                    MySnake.dir=Dir.DOWN
                    #score=Myfruit.collusion(MySnake, pos_fruit_1, pos_fruit_2, score)
                    direction =(1,0)
                    break
                
            
   

        
        
        #bien laisser la boucle d'evnt avant d'afficher
        

        #MyCheckerBoard.tracer(screen)
        #MySnake.draw(screen)
        #Myfruit.draw(screen)

        score=MySnake.move(Myfruit, score, pos_fruit_1, pos_fruit_2)
        board.draw()


        


        display_score(screen, score)
        pygame.display.set_caption(f"Ecran de jeu {score}")


    

    


        pygame.display.update() #afficher a la fin


    pygame.quit()




