## Tips in Python

### Alias
```py
type Vector2 = Tuple[float, float]
```

### Typing
```py
class Stress:
    xx: float = 0
    xy: float = 0
    yy: float = 0
    def __init__(self, xx: float, xy: float, yy: float) -> None:
        self.xx = xx
        self.xy = xy
        self.yy = yy
```