from pygame import Surface
from pygame.sprite import Group
from settings import *
from Utils.GameSprite import GameSprite

class Entity ( GameSprite ):
	def __init__(self, frames: list[Surface], *groups: Group, **anchor: tuple[float, float]) -> None:
		super().__init__(frames[0], *groups, **anchor)

		self.frames = frames
		self.frames_i = 0
		self.animation_speed = 10

		self.direction = pygame.Vector2()
		self.speed = 300

		self.hitbox = self.rect.copy()


	def _get_direction ( self ):
		pass

	def _move ( self, dt: float ): 
		self.rect.center += self.direction * self.speed * dt

	def _animate ( self, dt: float ):
		self.frames_i = self.frames_i + self.animation_speed * dt
		self.image = self.frames[ int(self.frames_i) % len(self.frames) ]

	def _move_x_wise ( self, dt: float ):
		self.hitbox.x += self.direction.x * self.speed * dt

	def _move_y_wise ( self, dt: float ):
		self.hitbox.y += self.direction.y * self.speed * dt

	def _x_collision_manager ( self, collision_sprites: Group ):
		for sprite in collision_sprites:
			if sprite.rect.colliderect(self.hitbox):
				if self.direction.x > 0: self.hitbox.right = sprite.rect.left
				if self.direction.x < 0: self.hitbox.left = sprite.rect.right

	def _y_collision_manager ( self, collision_sprites: Group ):
		for sprite in collision_sprites:
			if sprite.rect.colliderect(self.hitbox):
				if self.direction.y > 0: self.hitbox.bottom = sprite.rect.top
				if self.direction.y < 0: self.hitbox.top = sprite.rect.bottom

	def _manage_collision ( self, collision_sprites: Group, dt: float ):
		self._move_x_wise(dt)
		self._x_collision_manager(collision_sprites)
		self._move_y_wise(dt)
		self._y_collision_manager(collision_sprites)

	def _move_after_collision ( self, dt ): self.rect.center = self.hitbox.center
