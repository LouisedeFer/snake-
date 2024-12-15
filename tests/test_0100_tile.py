import snake

def test_creation() -> bool :
    t=snake.Tile(10,5, (0,255,0))
    assert t.coord==(10,5)
