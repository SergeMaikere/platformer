from pygame import Surface
from pygame.key import ScancodeWrapper
from pygame.sprite import Group
from settings import *
from Utils.Entity import Entity

class Player ( Entity ):
	def __init__(self, frames: list[Surface], collision_sprites, *groups: Group, **anchor: tuple[float, float]) -> None:
		super().__init__(frames, *groups, **anchor)

		self.frames = frames
		self.collision_sprites = collision_sprites

		self.is_grounded = False
		self.gravity = 50
		self.jump_force = 10
  

	def __left_or_right ( self, keys: ScancodeWrapper ): 
		self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])

	def __jump ( self, keys: ScancodeWrapper ):
		if keys[pygame.K_SPACE] and self.is_grounded: 
			self.direction.y = -self.jump_force
			self.is_grounded = False


	def _get_direction( self ):
		keys = pygame.key.get_pressed()
		self.__jump(keys)
		self.__left_or_right(keys)

	def __set_gravity ( self, dt: float ): self.direction.y += self.gravity * dt

	def __update_gravity_datas ( self ):
		self.direction.y = 0
		self.is_grounded = True

	def _y_collision_manager ( self, collision_sprites: Group ):
		for sprite in collision_sprites:
			if sprite.rect.colliderect(self.hitbox):

				if self.direction.y >= 0: 
					self.hitbox.bottom = sprite.rect.top
					self.__update_gravity_datas()

				if self.direction.y < 0: 
					self.hitbox.top = sprite.rect.bottom

	def update ( self, dt ):
		self._get_direction()
		self.__set_gravity(dt)
		self._manage_collision(self.collision_sprites, dt)
		self._move_after_collision(dt)
