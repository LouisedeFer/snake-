from __future__ import annotations  # noqa: D100

import abc
import random as rd
from enum import Enum

import pygame


class Observer(abc.ABC):  # noqa: B024, D101

    def __init__(self) -> None:
        """Define the observer."""
        super().__init__()

    def notify_object_eaten(self, obj: GameObject) -> None :  # noqa: B027
        """Notify if an object is eaten."""


    def notify_object_moved(self, obj: GameObject) -> None:  # noqa: B027
        """Notify an object is moved."""


    def notify_collision(self, obj : GameObject) -> None:  # noqa: B027
        """Notify a collision."""



class Subject(abc.ABC):  # noqa: B024, D101

    def __init__(self) -> None:
        """Define the subject."""
        super().__init__()
        self._observers : list[Observer] = []

    @property
    def observers(self) -> list[Observer]:
        """Return the the observers."""
        return self._observers

    def attach_obs(self, obs: Observer) -> None:
        """Attach the observers."""
        print(f"Attach {obs} as observer of {self}.")  # noqa: T201
        self._observers.append(obs)

    def detach_obs(self, obs: Observer) -> None:
        """Detach the observers."""
        print(f"Detach observer {obs} from {self}.")  # noqa: T201
        self._observers.remove(obs)


class GameObject(Subject, Observer) :
    """Define the contract every GameObject should respect."""

    #class first (Subject), then interfaces

    def __init__(self) -> None :
        """Define the GameObject."""
        super().__init__()

    def __contains__(self, obj:object)-> bool :
        """Define the in for an object."""
        if isinstance(obj, GameObject) :
            return any(t in obj.tiles for t in self.tiles) # automatiquement sous forme d'iterateur, s'arrete des que True
        return False

    # on va creer une propriete tiles

    @property # fait voir la fonction comme un attribut
    @abc.abstractmethod # cette methode est une methode abstraite : elle n'a pas d'implementation
    def tiles(self) -> None :
        """Create the tiles'property."""
        raise NotImplementedError # tout objet heritant de gameobject doit definir une propriete utile

    @property
    def background(self) -> bool :
        """Create the background's property."""
        return False # by default, gameobject is not a background




class Dir(Enum) :
    """Enumerate the directions."""

    DOWN=(1,0)
    UP=(-1,0)
    LEFT=(0,-1)
    RIGHT=(0,1)

class Board(Subject, Observer) :
    """Define the board used to draw globally."""

    def __init__(self, screen : pygame.Surface, tile_size : int, nb_rows : int, nb_cols : int)-> None : # on va devoir dessiner donc on rentre un screen  # noqa: D107
        self._screen=screen
        self._tile_size=tile_size
        self._object : list[object]=[]# to have snake, board, fruit
        self._nb_rows=nb_rows
        self._nb_cols=nb_cols

    def draw(self) -> None:
        """Draw the tiles for the objects."""
        for obj in self._object :
            for tile in obj.tiles:
                tile.draw(self._screen,self._tile_size)


    def add_object(self, gameobject: GameObject) -> None:
        """Add the objects as observers."""
        self._object.append(gameobject)
        gameobject.attach_obs(self) #becomes a global observer

    def remove_object(self, gameobject : GameObject) -> None:
        """Remove the objects of the observers."""
        gameobject.detach_obs(self)
        self._object.remove(gameobject)

    def create_fruit(self) -> Fruit :
        """Create fruits."""
        fruit=None
        while fruit is None or self.detect_collision(fruit) is not None :
            fruit=Fruit(color_fruit=pygame.Color("red"), col=rd.randint(0,self._nb_cols-1), row=rd.randint(0, self._nb_rows-1))  # noqa: E501, S311

    def detect_collision(self, obj : GameObject) -> GameObject | None :
        """Detect wether or not there has been a collision."""
        for o in self._object :
            if o != obj and not o.background and o in obj :
                return o
        return None


    def notify_object_moved(self, obj:GameObject) -> None :
        """Detecte the collision with others."""  # noqa: D401
        o=self.detect_collision(obj)
        if o is not None:
            obj.notify_collision(o)

    def notify_object_eaten(self, obj:GameObject)  -> None :
        """Remove the old fruit and create a new one."""
        self.remove_object(obj)
        self.create_fruit()

class Tile():
    """Create the tiles."""

    #le constructeur
    def __init__(self,row : int ,column : int , color : tuple) -> None:
        """Initialize the tile."""
        self._color=color
        #self.size=size pas utile car la taille est la meme pour tout le monde : on le met dans la classe Board
        self._row=row
        self._column=column

    def __repr__(self) -> str:
        """Represent what a tile consists of."""
        return f"({self._row}, {self._column})"

    @property
    def coord(self) -> tuple :
        """Return the coordonates of a tile."""
        return (self._row, self._column)
    #tracer les cases

    def draw(self, screen : pygame.Surface, tile_size : int) -> None:
        """Draw the tiles."""
        rect = pygame.Rect(self._column*tile_size, self._row*tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, self._color, rect)


class CheckerBoard(GameObject) :
    """Define the CheckerBoard."""

    def __init__(self, color_1 : tuple, color_2 : tuple , nb_rows : int , nb_columns : int) -> None :  # noqa: E501
        """Initialize the Checkerboard."""
        self._color_1=color_1
        self._color_2=color_2
        self._nb_rows=nb_rows
        self._nb_columns=nb_columns
        #self.size_square=size_square inutile a present

    #la fonction pour tracer

    @property
    def background(self)->bool:
        """Says the checkerboard is a background."""
        return True

    @property
    def tiles(self)-> None : # type: ignore  # noqa: PGH003
        """Generate the tiles."""
        for column in range(self._nb_columns) :
            for row in range(self._nb_rows) :
                yield(Tile(row=row, column=column, color=self._color_1 if (column+row)%2==0 else self._color_2))  # noqa: E501



class Snake(GameObject):
    """" this class is used to create the snake controlled by the player."""

    def __init__(self, tiles : list[Tile], direction : Dir) -> None :
        """Define the parameters of the snake."""
        self._tiles=tiles
        self._direction=direction
        self._size=len(self._tiles)

    @classmethod
    def create_from_pos(cls, color : tuple,row : int , column : int, size : int, direction : Dir) -> Snake :  # noqa: E501
        """Create the snake."""
        tiles=[Tile(row, column+p, color) for p in range(size)]
        return Snake(tiles=tiles, direction=direction)

    """#
    def __contains__(self, fruit : Fruit)  -> bool:
    Test if fruit is in snake.
        return fruit.coord==self._tiles[0].coord
    """


    def __len__(self) -> int :
        """Give the len of the snake, useful for the score."""
        return len(self._tiles)


    @property
    def tiles (self) -> None :
        """Return the list of the tiles."""
        iter(self._tiles)

    @property
    def dir(self) -> Dir:
        """Return the direction."""
        return self._direction

    @dir.setter
    def dir(self, new_direction: Dir)-> None:
        """Return the new direction."""
        self._direction = new_direction

     # making the snake move
    def move(self) -> None:
        """Move the snake one tile."""
        #add a new head
        x,y=self._tiles[0].coord
        coord=(x + self._direction.value[0], y + self._direction.value[1])
        self._tiles.insert(0, Tile(coord[0], coord[1], color=pygame.Color("green")))

        #notify observers
        for obs in self.observers :
            obs.notify_object_moved(self)

        #shrink
        if self._size < len(self._tiles) :
            self._tiles=self._tiles[:self._size]

    def notify_collision(self, obj : GameObject)-> None :
        """Notify an eatable object has been eaten."""
        if isinstance(obj, Fruit) :
            self._size+=1
            for obs in self._observers :
                obs.notify_object_eaten(obj)



class Fruit(GameObject) :
    """" Define the fruit eaten by the snake."""

    def __init__(self, color_fruit : tuple , col : int , row : int) -> None :
        """Define the fruit."""
        self._color_fruit=color_fruit
        self._col=col
        self._row=row
        self._tiles=[Tile(self._row, self._col,self._color_fruit)]


    """#def __contains__(self, snake: ) : # test if snake contains fruit, prend en arg les positions du snake
       return snake==[self._row, self._col]"""

    @property
    def tiles(self) -> None:
        """Return the tiles."""
        iter(self._tiles)

    @property
    def coord(self)->tuple :
        """Return the coordonates of the fruit."""
        return (self._row, self._col)


    """#def change(self, pos_1, pos_2) :
        if [self._row, self._col]==pos_1 :
            [self._row, self._col]=pos_2
        else :
            [self._row, self._col]=pos_1
        self._tiles=[Tile(self._row, self._col, self._color_fruit)]
        """
