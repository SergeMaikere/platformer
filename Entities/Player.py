from pygame import Surface
from pygame.key import ScancodeWrapper
from pygame.sprite import Group
from Utils.Timer import Timer
from settings import *
from Utils.Entity import Entity

class Player ( Entity ):
	def __init__(self, frames: list[Surface], collision_sprites, *groups: Group, **anchor: tuple[float, float]) -> None:
		super().__init__(frames, *groups, **anchor)

		self.frames = frames
		self.flip = False

		self.shoot_timer = Timer(500)

		self.collision_sprites = collision_sprites

		self.is_grounded = False
		self.gravity = 50
		self.jump_force = 12


	def __set_is_grounded ( self ):
		player_bottom = pygame.FRect((0, 0), (self.rect.width, 2)).move_to(midtop=self.rect.midbottom)
		self.is_grounded = player_bottom.collidelist( [sprite.rect for sprite in self.collision_sprites] ) >= 0

	def __left_or_right ( self, keys: ScancodeWrapper ): 
		self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])

	def __jump ( self, keys: ScancodeWrapper ):
		if keys[pygame.K_SPACE] and self.is_grounded: self.direction.y = -self.jump_force


	def __input ( self ):
		keys = pygame.key.get_pressed()
		self.__jump(keys)
		self.__left_or_right(keys)
		self.__shoot(keys)


	def _set_direction( self ): self.__input()

	def __shoot ( self, keys: ScancodeWrapper ):
		if keys[pygame.K_s] and not self.shoot_timer.active:
			print('BLAAAAM !!!')
			self.shoot_timer.start()

	def __set_flip ( self ): 
		if self.direction.x < 0: self.flip = True
		if self.direction.x > 0: self.flip = False

	def __set_gravity ( self, dt: float ): self.direction.y += self.gravity * dt

	def _y_collision_manager ( self, collision_sprites: Group ):
		for sprite in collision_sprites:
			if sprite.rect.colliderect(self.hitbox):
				if self.direction.y >= 0: self.hitbox.bottom = sprite.rect.top
				if self.direction.y < 0: self.hitbox.top = sprite.rect.bottom
				self.direction.y = 0

	def __set_frame_i ( self, dt: float ):
		if not self.is_grounded: 
			self.frames_i = 1
		else:
			self.frames_i = self.frames_i + self.animation_speed * dt if self.direction else 0

	def __set_image ( self ): 
		self.image = self.frames[ int(self.frames_i) % len(self.frames) ]
		self.image = pygame.transform.flip(self.image, self.flip, False)

	def _animate ( self, dt: float ):
		self.__set_frame_i(dt)
		self.__set_image()
		
	def update ( self, dt ):
		self.shoot_timer.update()
		self.__set_is_grounded()
		self._set_direction()
		self.__set_flip()
		self.__set_gravity(dt)
		self._manage_collision(self.collision_sprites, dt)
		self._move_after_collision(dt)
		self._animate(dt)
