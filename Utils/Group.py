from pygame.sprite import Sprite
from settings import *

class Group ( pygame.sprite.Group ):
	def __init__(self, name: str, *sprites: Sprite) -> None:
		super().__init__(*sprites)

		self.name = name