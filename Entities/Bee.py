from math import sin
from random import randint
from pygame import Surface
from pygame.sprite import Group
from settings import *
from Utils.Enemy import Enemy

class Bee ( Enemy ):
	def __init__(self, frames: list[Surface], *groups: Group, **anchor: tuple[float, float]) -> None:
		super().__init__(frames, *groups, **anchor)

		self.speed = randint(300, 500)
		self.frequency = randint(300, 600)
		self.direction.x = -1


	def _set_direction(self): 
		self.direction.y = sin(pygame.time.get_ticks() / self.frequency)

	def _constraint(self):
		if self.rect.right < 0: self.kill()