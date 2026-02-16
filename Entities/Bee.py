from pygame import Surface
from pygame.sprite import Group
from settings import *
from Utils.Entity import Entity

class Bee ( Entity ):
	def __init__(self, frames: list[Surface], *groups: Group, **anchor: tuple[float, float]) -> None:
		super().__init__(frames, *groups, **anchor)

	def update ( self, dt: float ):
		self._animate(dt)
		# self._move(dt)