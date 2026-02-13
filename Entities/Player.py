from pygame import Surface
from pygame.sprite import Group
from settings import *
from Utils.Entity import Entity

class Player ( Entity ):
	def __init__(self, frames: list[Surface], *groups: Group, **anchor: tuple[float, float]) -> None:
		super().__init__(frames, *groups, **anchor)

		self.frames = frames


	def _get_direction( self ):
		keys = pygame.key.get_pressed()
		self.direction.x = int(keys[pygame.K_f]) - int(keys[pygame.K_s])
		self.direction.y = int(keys[pygame.K_d]) - int(keys[pygame.K_e])
		self.direction = self.direction.normalize() if self.direction else self.direction