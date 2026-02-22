from pygame import Surface
from Utils.Entity import Entity
from Utils.Group import Group
from Utils.Timer import Timer
from settings import *

class Enemy ( Entity ):
	def __init__(self, frames: list[Surface], *groups: Group, **anchor: tuple[float, float]) -> None:
		super().__init__(frames, *groups, **anchor)

		self.death_timer = Timer(200, self.kill)


	def _destroy( self ):
		self.death_timer.start()
		self.animation_speed = 0
		self.image = self.mask.to_surface()
		self.image.set_colorkey('black')

	def update ( self, dt: float ):
		if self.death_timer.active: 
			self.death_timer.update()

		if not self.death_timer.active:
			self._set_direction()
			self._move(dt)
			self._animate(dt)
			self._constraint()