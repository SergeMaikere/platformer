from pygame import Surface
from pygame.sprite import Group
from settings import *
from Utils.Entity import Entity

class Player ( Entity ):
	def __init__(self, frames: list[Surface], collision_sprites, *groups: Group, **anchor: tuple[float, float]) -> None:
		super().__init__(frames, *groups, **anchor)

		self.frames = frames
		self.collision_sprites = collision_sprites
  

	def _get_direction( self ):
		keys = pygame.key.get_pressed()
		self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
		self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
		self.direction = self.direction.normalize() if self.direction else self.direction

	

	def update ( self, dt ):
		self._get_direction()
		self._manage_collision(self.collision_sprites, dt)
		self._move_after_collision(dt)
