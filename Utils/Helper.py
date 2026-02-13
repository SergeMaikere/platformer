from settings import *
from typing import Callable
from pytmx import TiledMap
from functools import reduce

pipe = lambda *funcs: lambda arg: reduce( lambda g, f: f(g), funcs, arg )

load_map: Callable[ [], TiledMap ] = lambda : load_pygame( join('assets', 'data', 'maps', 'world.tmx') )