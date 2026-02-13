from pygame.sprite import Sprite
from Entities.Player import Player
from settings import *

class AllSprites ( pygame.sprite.Group ):
	def __init__(self, *sprites: Sprite) -> None:
		super().__init__(*sprites)

		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.Vector2()

	def __set_offset ( self, player_pos: tuple[float, float] ):
		x, y = player_pos
		self.offset.x = - ( x - WINDOW_WIDTH/2 )
		self.offset.y = - ( y - WINDOW_HEIGHT/2 )

	def __draw_with_offset ( self ):
		for sprite in self:
			self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

	def draw ( self, player_pos: tuple[float, float] ):
		self.__set_offset(player_pos)
		self.__draw_with_offset()