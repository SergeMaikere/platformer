from pygame import Surface
from settings import *
from pygame.sprite import Group

class GameSprite ( pygame.sprite.Sprite ):
	def __init__(self, image: Surface, *groups: Group, **anchor: tuple[float, float]) -> None:
		super().__init__(*groups)

		self.image = image
		self.rect = image.get_frect(**anchor)