from pygame import FRect, Surface
from settings import *
from pygame.sprite import Group

class GameSprite ( pygame.sprite.Sprite ):
	def __init__(self, image: Surface, *groups: Group, **anchor: tuple[float, float]) -> None:
		super().__init__(*groups)

		self.image = image
		self.rect: FRect = image.get_frect(**anchor)
		self.mask = pygame.mask.from_surface(self.image)