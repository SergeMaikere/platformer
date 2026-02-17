from random import randint
from pygame import Surface
from pygame.rect import FRect
from pygame.sprite import Group
from settings import *
from Utils.Entity import Entity

class Worm ( Entity ):
	def __init__(self, frames: tuple[list[Surface], list[Surface]], patrol_area: FRect, *groups: Group) -> None:
		super().__init__(frames[0], *groups, bottomleft=patrol_area.bottomleft)

		self.rightheous_frames, self.flipped_frames = frames
		self.frames = self.rightheous_frames
		self.flipped = False

		self.patrol_area = patrol_area

		self.speed = randint(150, 200)
		self.direction.x = 1

	def _set_direction(self):
		if not self.patrol_area.contains(self.rect): 
			self.direction.x *= -1
			self.flipped = not self.flipped

	def _constraint(self):
		if not self.patrol_area.contains(self.rect): 
			self.frames = self.flipped_frames if not self.flipped else self.rightheous_frames
		
	
