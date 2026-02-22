from pygame import Surface
from pygame.sprite import Group
from Entities.Player import Player
from Utils.GameSprite import GameSprite
from settings import *

class Bullet (GameSprite):
	def __init__(self, images: tuple[Surface, Surface], map_width: int, player: Player, *groups: Group) -> None:
		super().__init__(images[0 if not player.flip else 1], *groups, topleft= (self.__set_spawn_pos(player), player.rect.centery))

		self.map_width = map_width

		self.rightheous_frame, self.flipped_frame = images
		
		self.player = player

		self.direction = 1 if not self.player.flip else -1
		self.speed = 850

	def __set_spawn_pos ( self, player: Player ):
		if player.flip: return player.rect.centerx - (34 + player.rect.width)
		return player.rect.centerx + 34

	def __move ( self, dt: float ):
		self.rect.x += self.direction * self.speed * dt

	def __constraint ( self ):
		if self.rect.right < 0 or self.rect.left > self.map_width: self.kill()

	def update ( self, dt: float ):
		self.__move(dt)
		self.__constraint()

