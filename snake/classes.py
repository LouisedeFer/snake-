
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
        self.line=line # ligne de la tête
        self.column=column # colonne de la tête
        #self.taille=taille # prend une liste avec largeur et hauteur (hauteur de 1 à l'origine)
        self.taille=taille # prend la taille totale du serpent
        self.square_size=square_size
        self.positions=[[self.line, self.column+i] for i in range(self.taille)] # cette liste sert à quantifier les positions 
        # du corps du serpent (utile pour le faire monter/descendre car la tête se désolidarise du corps)
        #on commence par placer le serpent à l'horizontale toujours donc seules les valeurs des colonnes changent
    

    def __contains__(self, fruit) : # on testera if fruit in snake
       return fruit==self.positions[0]


    def draw(self, screen) : #on va différentier le corps et la tête pour des questions de couleur
        head=pygame.Rect(self.positions[0][1]*self.square_size,self.positions[0][0]*self.square_size,self.square_size,self.square_size)
        pygame.draw.rect(screen,self.color_head,head )
        for j in range(1,len(self.positions)) : # on trace le serpent carré par carré
            pos=pygame.Rect(self.positions[j][1]*self.square_size,self.positions[j][0]*self.square_size,self.square_size,self.square_size)
            pygame.draw.rect(screen, self.color, pos)  
        
    def grow(self, direction) : # plus utile maintenant 
        if direction=='DOWN' :
            self.positions.append([self.positions[-1][0], self.positions[-1][1]+1])
        if direction=='UP' :
            self.positions.append([self.positions[-1][0], self.positions[-1][1]-1])
        if direction=='RIGHT' :
            self.positions.append([self.positions[-1][0]+1, self.positions[-1][1]])
        if direction =='LEFT' :
            self.positions.append([self.positions[-1][0]-1, self.positions[-1][1]])

    

        

## Snake's move

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



class Fruit :

    def __init__(self, color_fruit, col, line,size) :
        self.color_fruit=color_fruit
        self.col=col
        self.line=line
        self.size=size
    
    def __contains__(self, snake) : # on testera if snake in fruit
       return snake==[self.line, self.col]
    
    def draw(self, screen) :
        fruit=Tiles(self.color_fruit, self.size, self.col, self.line)
        fruit.draw(screen)
    
    def collusion(self, snake, pos_1, pos_2, screen,score) :
        if [self.line, self.col] in snake :
            if [self.line, self.col]==pos_1 :
                [self.line, self.col]=pos_2
            else :
                [self.line, self.col]=pos_1

            score+=1
            #snake.grow(direction)
            self.draw(screen)
        

        return score
    




    