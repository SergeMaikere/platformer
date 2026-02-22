from pygame import Surface
from Entities.Player import Player
from Utils.GameSprite import GameSprite
from Utils.Group import Group
from Utils.Timer import Timer
from settings import *

class Fire ( GameSprite ):
	def __init__(self, images: tuple[Surface, Surface], player: Player, *groups: Group) -> None:
		super().__init__(images[0 if player.flip else 1], *groups, topleft= self.__set_spawn_pos(player))

		self.lifespan = Timer(200, self.kill, autostart=True)
		self.player = player
		self.flip = self.player.flip

	def __set_spawn_pos ( self, player: Player ):
		if player.flip: return (player.rect.centerx - player.rect.width, player.rect.centery - 10)
		return (player.rect.centerx + 33, player.rect.centery - 10)

	def constraint ( self ):
		if not self.flip == self.player.flip: self.kill()

	def update ( self, dt: float ):
		self.lifespan.update()