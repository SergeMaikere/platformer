from pygame import Surface
from pygame.rect import FRect
from pygame.sprite import Group
from settings import *
from Utils.Entity import Entity

class Worm ( Entity ):
	def __init__(self, frames: list[Surface], patrol_area: FRect, *groups: Group) -> None:
		super().__init__(frames, *groups, bottomleft=patrol_area.bottomleft)

		self.patrol_area = patrol_area

		self.speed = 150
		self.direction.x = 1

	def _set_direction(self):
		if not self.patrol_area.contains(self.rect): self.direction.x *= -1

	def _constraint(self):
		if not self.patrol_area.contains(self.rect): 
			self.frames = [ pygame.transform.flip(frame, True, False) for frame in self.frames ]
		
	
