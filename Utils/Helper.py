from os import PathLike
from pygame import Surface
from pygame.mixer import Sound
from settings import *
from typing import Any, Callable, Iterable
from pytmx import TiledMap
from functools import partial, reduce
from random import uniform

pipe = lambda *funcs: lambda arg: reduce( lambda g, f: f(g), funcs, arg )

load_map: Callable[ [], TiledMap ] = lambda : load_pygame( join('assets', 'data', 'maps', 'world.tmx') )

load_image: Callable[ [PathLike], Surface ] = lambda path: pygame.image.load(path)

convert_image: Callable[ [Surface], Surface ] = lambda image: image.convert_alpha()

get_frame: Callable[ [str, str], Surface ] = lambda path, filename: pipe( load_image, convert_image )( join(path, filename) )

load_sound = lambda path: pygame.mixer.Sound(path)

def get_frames ( *path: str ) -> list[Surface] | None:
	frames = None
	for root, _, files in walk( join(*path) ):
		if files: 
			frames = [ get_frame(root, file) for file in sorted(files, key= lambda filename: int(filename.split('.')[0])) ]
	return frames


def add_sound ( root: str, acc: dict[str, Sound], filename: str ):
	acc[filename.split('.')[0]] = load_sound(join(root, filename))
	return acc

def load_sounds ( *path: str ):
	sounds = None
	for root, _, files in walk( join(*path) ):
		if files: sounds = reduce( partial(add_sound, root), files, {} )
	return sounds

def get_random_pos ( x: float, y: float ): return ( uniform(0, x), uniform(0, y) ) 