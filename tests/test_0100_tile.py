import snake  # noqa: D100
from snake.classes import Dir

color_1=(0,0,0)
colors_2=(255,255,255)

columns=30
rows=20
size=30

##Class Tile
def test_creation() -> None :
    """Test if the coordonates of tile are correct."""
    t=snake.Tile(10,5, (0,255,0))
    assert t.coord==(10,5) # noqa: S101

## Class Checkerboard

def test_background() -> None :
    """Test if the background is correct."""
    cb=snake.CheckerBoard(color_1,colors_2,rows,columns)
    assert cb.background is True  # noqa: S101


## Class Snake

def test_direction() ->None :
    """Test if the dorection is correct."""
    s=snake.Snake.create_from_pos((255,0,0), 10,5,3, Dir.LEFT)
    assert s._direction==Dir.LEFT #code a property that gives the direction back


#For the movement of the Snake
def test_move_left()->None :
    """Check if the head gets the right coordonates."""
    sna=snake.Snake.create_from_pos((255,0,0), 10,5,3, Dir.LEFT)
    head=next(sna.tiles).coord #takes the first element of the iterator
    sna.move()
    assert next(sna.tiles).coord==(head[0]+Dir.LEFT.value[0], head[1]+Dir.LEFT.value[1])


