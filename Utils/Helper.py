from os import PathLike
from pygame import Surface
from settings import *
from typing import Callable
from pytmx import TiledMap
from functools import reduce

pipe = lambda *funcs: lambda arg: reduce( lambda g, f: f(g), funcs, arg )

load_map: Callable[ [], TiledMap ] = lambda : load_pygame( join('assets', 'data', 'maps', 'world.tmx') )

load_image: Callable[ [PathLike], Surface ] = lambda path: pygame.image.load(path)

convert_image: Callable[ [Surface], Surface ] = lambda image: image.convert_alpha()

get_frame: Callable[ [str, str], Surface ] = lambda path, filename: pipe( load_image, convert_image )( join(path, filename) )

def get_frames ( *path: str ) -> list[Surface] | None:
	frames = None
	for root, _directories, files in walk( join(*path) ):
		if files: frames = [ get_frame(root, file) for file in files ]
	return frames