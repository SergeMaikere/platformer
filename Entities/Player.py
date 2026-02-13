from pygame import Surface
from pygame.sprite import Group
from settings import *
from Utils.GameSprite import GameSprite

class Player ( GameSprite ):
	def __init__(self, frames: list[Surface], *groups: Group, **anchor: tuple[float, float]) -> None:
		super().__init__(frames[0], *groups, **anchor)

		self.frames = frames
