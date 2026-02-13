from pygame import Surface
from pygame.sprite import Group
from settings import *
from Utils.GameSprite import GameSprite

class Entity ( GameSprite ):
	def __init__(self, frames: list[Surface], *groups: Group, **anchor: tuple[float, float]) -> None:
		super().__init__(frames[0], *groups, **anchor)

		self.frames = frames
		self.frames_i = 0

		self.direction = pygame.Vector2()
		self.speed = 300


	def _get_direction ( self ):
		pass

	def _move ( self, dt: float ): 
		self.rect.center += self.direction * self.speed * dt

	def _animate ( self, dt: float ):
		self.frames_i = self.frames_i + 5 * dt if self.direction else 0
		self.image = self.frames[ int(self.frames_i) % len(self.frames) ]

	def update ( self, dt: float ):
		self._get_direction()
		self._move(dt)
