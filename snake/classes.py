
import pygame


class CheckerBoard :

    #le constructeur

    def __init__(self, color_1, color_2, nb_lines, nb_columns, size_square) :
        self.color_1=color_1
        self.color_2=color_2
        self.nb_lines=nb_lines
        self.nb_columns=nb_columns
        self.size_square=size_square
    
    #la fonction pour tracer
    def tracer(self, screen) : #tracer le checkerboard

        hauteur=self.nb_lines*self.size_square
        largeur=self.nb_columns*self.size_square

        screen.fill( self.color_1)

        for i in range(self.nb_columns) :
            for j in range(self.nb_lines) :
               if (i+j)%2==0 :
                   tile=Tiles(self.color_2,self.size_square,i,j)
                   tile.draw(screen)




     
        

        

class Tiles:
    
    #le constructeur
    def __init__(self, color, size, top,left) :
        self.color=color
        self.size=size
        self.top=top
        self.left=left
    
    #l'afficheur

    def __repr__(self) :
        return f"Les carreaus sont {self.color}, de taille {self.size} et de coordonnées {self.coordonates} "
    

    #tracer les cases

    def draw(self, screen) :
        rect = pygame.Rect(self.top*self.size, self.left*self.size, self.size, self.size)
        pygame.draw.rect(screen, self.color, rect)

    
class Snake:

    def __init__(self, color, size, line, column) :
        self.color=color
        self.size=size
        self.line=line
                 


def tracer_snake(screen, snake, lines, columns, size) : #prend en argument le screen, le tuple de la taille du serpent, sa ligne de depart et sa ligne d'arrivee
    sna=pygame.Rect(columns*size, lines*size,snake[0]*size, snake[1]*size )

    color=(0,255,0)
    pygame.draw.rect(screen, color, sna)
