
import pygame
import abc 

from enum import Enum

class Board :

    def __init__(self, screen, tile_size) : # on va devoir dessiner donc on rentre un screen
        self._screen=screen
        self._tile_size=tile_size
        self._object=[]
    

    def draw(self) :
        for obj in self._object :
            for tile in obj.tiles:
                tile.draw(self._screen,self._tile_size)


 
    def add_object(self, gameobject) :
        self._object.append(gameobject)


class GameObject(abc.ABC) :  # classe abstraite pour parler de tous les objets du jeu
    # on definit le "contrat" que chaque classe GameObject doit avoir

    def __init__(self) :
        super().__init__()
    
    # on va creer une propriete tiles

    @property # fait voir la fonction comme un attribut
    @abc.abstractmethod # cette methode est une methode abstraite : elle n'a pas d'implementation
    def tiles(self) :
        raise NotImplementedError # tout objet heritant de gameobject doit definir une propriete utile


class Dir(Enum) :
    DOWN=(1,0)
    UP=(-1,0)
    LEFT=(0,-1)
    RIGHT=(0,1)


class Tile():
    #le constructeur
    def __init__(self,row,column, color) :
        self._color=color
        #self.size=size pas utile car la taille est la meme pour tout le monde : on le met dans la classe Board
        self._row=row
        self._column=column

    
    def __repr__(self) :
        return f'({self._row}, {self._column})'
    
    @property
    def coord(self) :
        return (self._row, self._column)
    #tracer les cases

    def draw(self, screen, tile_size) :
        rect = pygame.Rect(self._column*tile_size, self._row*tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, self._color, rect)


class CheckerBoard(GameObject) :  # noqa: D101

    #le constructeur

    def __init__(self, color_1, color_2, nb_rows, nb_columns) :
        self._color_1=color_1
        self._color_2=color_2
        self._nb_rows=nb_rows
        self._nb_columns=nb_columns
        #self.size_square=size_square inutile a present
    
    #la fonction pour tracer

    
    @property
    def tiles(self) :
        for column in range(self._nb_columns) :
            for row in range(self._nb_rows) :
                yield(Tile(row=row, column=column, color=self._color_1 if (column+row)%2==0 else self._color_2))




    
class Snake(GameObject):

    def __init__(self, color,row, column, size, direction) : #on met une couleur differente pour le corps et la tête
        self._color=color
        #self.color_head=color_head
        self._row=row # line of the head
        self._column=column # colonne de la tête
        #self.taille=taille # prend une liste avec largeur et hauteur (hauteur de 1 à l'origine)
        self._size=size # prend la taille totale du serpent
        #self.square_size=square_size
        self._positions=[[self._row, self._column+i] for i in range(self._size)] # cette liste sert à quantifier les positions 
        # du corps du serpent (utile pour le faire monter/descendre car la tête se désolidarise du corps)
        #on commence par placer le serpent à l'horizontale toujours donc seules les valeurs des colonnes changent
        self._direction=direction
        self._tiles=[Tile(p[0], p[1], color) for p in self._positions]
    

    def __contains__(self, fruit) : # on testera if fruit in snake
       return fruit==self._tiles[0].coord


    @property
    def tiles (self) :
        return(self._tiles)
    
    @property
    def dir(self) :
        return self._direction

    @dir.setter
    def dir(self, new_direction):
        self._direction = new_direction

    
     # making the snake move
    def move(self, fruit, score, pos_1, pos_2):
        # moving the head, the snake becomes one tile longer
        x,y=self._tiles[0].coord
        coord=(x + self._direction.value[0], y + self._direction.value[1])
        self._tiles.insert(0, Tile(coord[0], coord[1], self._color))
        if not fruit.coord in self :
            self._tiles.pop()
        else :
            fruit.change(pos_1, pos_2)
            score+=1
        return score
    
            



        

## Snake's move
'''#
    def move_up (self, screen, score) :
        li_init=10
        col_init=5 #on initialise une ligne et une colonne de départ
        taille_init=3# on revient à la taille normale
        #il faut vérifier que la tête ne touche pas le haut

        if self.positions[0][0] == 0 : #si on est déjà sur la première ligne
            self.positions=[[li_init,col_init+i] for i in range (taille_init)] # on renvient au début
            self.draw(screen)
            score=0

            
        else :
            indice=0
    
            for j in range(1,len(self.positions)) : # on va regarder si le serpent est sur une unique ligne ou non
                if self.positions[j][0] !=self.positions[0][0] and self.positions[j][1]==self.positions[0][1]:
                    indice =j
                 # on prend le dernier qui n'est pas sur la même ligne mais sur la même colonne
                 # on va faire monter les gens qu'il faut sur une même colonne


            if indice !=0 :

                if indice <len(self.positions)-1 :

                    for k in range(indice+1) :
                        self.positions[k][0]-=1

                    if self.positions[-1][1] < self.positions[0][1]: #si on vient de la gauche
                        for k in range (indice+1, len(self.positions)) :
                            self.positions[k][1]+=1 #les autres avancent sur la ligne
                    else : 
                        for k in range (indice+1, len(self.positions)) :
                            self.positions[k][1]-=1 #les autres reculent sur la ligne
                
                else : # tout le monde est sur la même colone
                    for k in range(len(self.positions)) :
                        self.positions[k][0]-=1




            else : # s'il n'y a que la tête qui monte (on est sur une seule ligne)
                if self.positions[1][1]<self.positions[0][1] : # on vient de la gauche
                    self.positions[0][0]-=1
                    self.positions[0][1]-=1
                else : #on vient de la droite
                    self.positions[0][0]-=1
                    self.positions[0][1]+=1
                    

        self.line=self.positions[0][0]
        self.column=self.positions[0][1]

        self.draw(screen)
        return score

    def move_down (self, screen, lines, score) :
        li_init=10
        col_init=5 #on initialise une ligne de départ
        taille_init=3# on revient à la taille normale
        #il faut vérifier que la tête ne touche pas le bas
        # ensuite il faut changer la valeur de la ligne (self.line)en lui ajoutant 1 :
        # on va reinitiliser MySnake en changeant la valeur de la 
        # ligne puis le retracer dans le programme global
        if self.positions[0][0] == lines : #si on est déjà sur la dernière ligne
            self.positions=[[li_init,col_init+i] for i in range (taille_init)] # on renvient au début
            self.draw(screen)
            score=0 #remettre le score à 0 si on touche les bords
        
        else :
            indice=0

            for j in range(1,len(self.positions)) : # on va regarder si le serpent est sur une unique ligne ou non
                if self.positions[j][0] !=self.positions[0][0] and self.positions[j][1]==self.positions[0][1]:
                    indice =j
                 # on prend le dernier qui n'est pas sur la même ligne mais sur la même colonne
                 # on va faire monter les gens qu'il faut sur une même colonne


            if indice !=0 :

                if indice < len(self.positions)-1 : 
                    for k in range(indice+1) :
                        self.positions[k][0]+=1


                    if self.positions[-1][1] < self.positions[0][1]: #si on vient de la gauche
                        for k in range (indice+1, len(self.positions)) :
                            self.positions[k][1]+=1 #les autres avancent sur la ligne
                    else : #si on vient de la droite
                        for k in range (indice+1, len(self.positions)) :
                            self.positions[k][1]-=1 #les autres reculent sur la ligne
                
                else : # tout le monde est sur la même colone
                    for k in range(len(self.positions)) :
                        self.positions[k][0]+=1               


            else : # s'il n'y a que la tête qui descend
                if self.positions[1][1]<self.positions[0][1] : # on vient de la gauche
                    self.positions[0][0]+=1
                    self.positions[0][1]-=1
                else : #on vient de la droite
                    self.positions[0][0]+=1
                    self.positions[0][1]+=1

        self.line=self.positions[0][0]
        self.column=self.positions[0][1]

        self.draw(screen)
        return score

    def move_right (self, screen, columns, score) :
        li_init=10
        col_init=5 #on initialise une ligne et une colonne de départ
        taille_init=3# on revient à la taille normale
        #il faut vérifier que la tête ne touche pas le bord de droite
        # ensuite il faut changer la valeur de la colonne (self.column)en lui ajoutant 1 :
        # on va reinitiliser MySnake en changeant la valeur de la 
        # colonne puis le retracer 
        if self.column == columns-1 : #si on est déjà sur la dernière colonne 
            self.positions=[[li_init,col_init+i] for i in range (taille_init)] # on renvient au début
            self.draw(screen)
            score=0
        else :
            indice=0
            for j in range(1,len(self.positions)) : # on va regarder si le serpent est sur une unique colonne ou non
                if self.positions[j][1] != self.positions[0][1] and self.positions[j][0]==self.positions[0][0]:
                    indice =j
                 # on fait avancer les gens qu'il faut sur une même ligne

            if indice !=0 :

                if indice <len(self.positions)-1 : 
                    for k in range(indice+1) :
                        self.positions[k][1]+=1


                    if self.positions[-1][0] < self.positions[0][0]: #si on vient du haut
                        for k in range (indice+1, len(self.positions)) :
                            self.positions[k][0]+=1 #les autres avancent sur la colonne
                    else : #si on vient du bas
                        for k in range (indice+1, len(self.positions)) :
                            self.positions[k][0]-=1 #les autres reculent sur la colonne

                else : 
                    for k in range(len(self.positions)) :
                        self.positions[k][1]+=1
                

            else : # s'il n'y a que la tête qui tourne
                if self.positions[1][0]<self.positions[0][0] : # on vient du haut
                    self.positions[0][0]-=1
                    self.positions[0][1]+=1
                else : #on vient du bas
                    self.positions[0][0]+=1
                    self.positions[0][1]+=1

        self.line=self.positions[0][0]
        self.column=self.positions[0][1]

        self.draw(screen)
        return score

    def move_left (self, screen, score) :
        li_init=10
        col_init=5 #on initialise une ligne et une colonne de départ
        taille_init=3# on revient à la taille normale
        #il faut vérifier que la tête ne touche pas le bord de gauche
        # ensuite il faut changer la valeur de la colonne (self.column)en lui enlevant 1 :
        # on va reinitiliser MySnake en changeant la valeur de la 
        # colonne puis le retracer 
        if self.column == 0 : #si on est déjà sur la première colonne 
            self.positions=[[li_init,col_init+i] for i in range (taille_init)] # on renvient au début
            self.draw(screen)
            score=0
            
        else :
            indice=0
            for j in range(1,len(self.positions)) : # on va regarder si le serpent est sur une unique colonne ou non
                if self.positions[j][1] != self.positions[0][1] and self.positions[j][0]==self.positions[0][0]:
                    indice =j
                 # on fait avancer les gens qu'il faut sur une même ligne

            if indice !=0 :

                if indice < len(self.positions)-1 : 
                    for k in range(indice+1) :
                        self.positions[k][1]-=1


                    if self.positions[-1][0] < self.positions[0][0]: #si on vient du haut
                        for k in range (indice+1, len(self.positions)) :
                            self.positions[k][0]+=1 #les autres avancent sur la colonne
                    else : #si on vient du bas
                        for k in range (indice+1, len(self.positions)) :
                            self.positions[k][0]-=1 #les autres reculent sur la colonne
                
                else :
                    for k in range(len(self.positions)) :
                        self.positions[k][1]-=1


            else : # s'il n'y a que la tête qui tourne
                if self.positions[1][0]<self.positions[0][0] : # on vient du haut
                    self.positions[0][0]-=1
                    self.positions[0][1]-=1
                else : #on vient du bas
                    self.positions[0][0]+=1
                    self.positions[0][1]-=1

        self.line=self.positions[0][0]
        self.column=self.positions[0][1]

        self.draw(screen)
        return score

# On propose une version beaucoup plus optimisée :

    def move_up_bis(self, screen, score, fruit) :
        li_init=10
        col_init=5 #on initialise une ligne de départ
        taille_init=3# on revient à la taille normale
        #il faut vérifier que la tête ne touche pas le haut
        # ensuite il faut changer la valeur de la ligne (self.line)en lui ajoutant 1 :
        # on va reinitiliser MySnake en changeant la valeur de la 
        # ligne puis le retracer dans le programme global
        if self.positions[0][0] ==0 : #si on est déjà sur la dernière ligne
            self.positions=[[li_init,col_init+i] for i in range (taille_init)] # on renvient au début
            self.draw(screen)
            score=0 #remettre le score à 0 si on touche les bords
        else : 
            self.positions.insert(0, [self.positions[0][0]-1, self.positions[0][1]])
            self.line=self.positions[0][0]
            self.column=self.positions[0][1]
            if self.positions[0] not in fruit : 
                self.positions.pop()
            self.draw(screen)
        return score
    
    def move_down_bis(self, screen, lines, score, fruit) :
        li_init=10
        col_init=5 #on initialise une ligne de départ
        taille_init=3# on revient à la taille normale
        #il faut vérifier que la tête ne touche pas le bas
        # ensuite il faut changer la valeur de la ligne (self.line)en lui ajoutant 1 :
        # on va reinitiliser MySnake en changeant la valeur de la 
        # ligne puis le retracer dans le programme global
        if self.positions[0][0] ==lines : #si on est déjà sur la dernière ligne
            self.positions=[[li_init,col_init+i] for i in range (taille_init)] # on renvient au début
            self.draw(screen)
            score=0 #remettre le score à 0 si on touche les bords
        else : 
            self.positions.insert(0, [self.positions[0][0]+1, self.positions[0][1]] )
            self.line=self.positions[0][0]
            self.column=self.positions[0][1]
            if self.positions[0] not in fruit : 
                self.positions.pop()
            self.draw(screen)
        return score
    
    def move_left_bis(self, screen, score, fruit) :
        li_init=10
        col_init=5 #on initialise une ligne de départ
        taille_init=3# on revient à la taille normale
        #il faut vérifier que la tête ne touche pas le bord gauche
        # ensuite il faut changer la valeur de la ligne (self.line)en lui ajoutant 1 :
        # on va reinitiliser MySnake en changeant la valeur de la 
        # ligne puis le retracer dans le programme global
        if self.positions[0][1] ==0 : #si on est déjà sur la ptrmiètr colonne
            self.positions=[[li_init,col_init+i] for i in range (taille_init)] # on renvient au début
            self.draw(screen)
            score=0 #remettre le score à 0 si on touche les bords
        else : 
            self.positions.insert(0, [self.positions[0][0], self.positions[0][1]-1])
            self.line=self.positions[0][0]
            self.column=self.positions[0][1]
            if self.positions[0] not in fruit : 
                self.positions.pop()        
            self.draw(screen)
        return score
    
    def move_right_bis(self, screen, columns, score, fruit) :
        li_init=10
        col_init=5 #on initialise une ligne de départ
        taille_init=3# on revient à la taille normale
        #il faut vérifier que la tête ne touche pas le bord droit
        # ensuite il faut changer la valeur de la ligne (self.line)en lui ajoutant 1 :
        # on va reinitiliser MySnake en changeant la valeur de la 
        # ligne puis le retracer dans le programme global
        if self.positions[0][0] ==columns : #si on est déjà sur la dernière colonne
            self.positions=[[li_init,col_init+i] for i in range (taille_init)] # on renvient au début
            self.draw(screen)
            score=0 #remettre le score à 0 si on touche les bords
        else : 
            self.positions.insert(0, [self.positions[0][0], self.positions[0][1]+1])
            self.line=self.positions[0][0]
            self.column=self.positions[0][1]
            if self.positions[0] not in fruit : 
                self.positions.pop()
            self.draw(screen)
        return score
    
                              

    def move_global(self, direction, screen, columns, lines, score, fruit) :
        if direction=='RIGHT' :
            self.move_right_bis(screen, columns, score, fruit)
        if direction == 'LEFT' :
            self.move_left_bis(screen, score, fruit) 
        if direction == 'UP' :
            self.move_up_bis(screen, score, fruit)
        if direction== 'DOWN' :
            self.move_down_bis(screen, lines, score, fruit)

'''
class Fruit(GameObject) :

    def __init__(self, color_fruit, col, row) :
        self._color_fruit=color_fruit
        self._col=col
        self._row=row
        self._tiles=[Tile(self._row, self._col,self._color_fruit)]

    
    def __contains__(self, snake) : # test if snake contains fruit, prend en arg les positions du snake
       return snake==[self._row, self._col]

    @property
    def tiles(self) :
        return(self._tiles)

    @property
    def coord(self) :
        return (self._row, self._col)


    def change(self, pos_1, pos_2) :
        if [self._row, self._col]==pos_1 :
            [self._row, self._col]=pos_2
        else :
            [self._row, self._col]=pos_1
        self._tiles=[Tile(self._row, self._col, self._color_fruit)]

    




    