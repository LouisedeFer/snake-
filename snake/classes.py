
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

    def __init__(self, color, color_head,line, column, taille, square_size) : #on met une couleur differente pour le corps et la tête
        self.color=color
        self.color_head=color_head
        self.line=line
        self.column=column
        self.taille=taille # prend une liste avec largeur et hauteur (toujours 1)
        self.square_size=square_size
    
    def draw(self, screen) : #on va différentier le corps et la tête
        sna=pygame.Rect((self.column+1)*self.square_size,self.line*self.square_size,(self.taille[0]-1)*self.square_size, self.taille[1]*self.square_size )
        head=pygame.Rect(self.column*self.square_size,self.line*self.square_size,self.square_size,self.square_size)
        pygame.draw.rect(screen, self.color, sna)  
        pygame.draw.rect(screen,self.color_head,head )    



