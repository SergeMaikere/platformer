from typing import Callable
from settings import *

class Timer ():
	def __init__(self, duration: int, func: Callable | None = None, repeat: bool = False, autostart: bool = False) -> None:
		self.duration = duration
		self.func = func
		self.repeat = repeat
		self.active = autostart

		self.time_start = 0


	def start ( self ):
		self.active = True
		self.time_start = pygame.time.get_ticks()

	def stop ( self ):
		self.active = False
		self.time_start = 0

	def __cooldown_is_over ( self ): return pygame.time.get_ticks() - self.time_start >= self.duration

	def __execute_func ( self ):
		if not self.func or self.time_start == 0: return
		self.func()

	def __repeat ( self ):
		if not self.repeat: return
		self.start()

	def update ( self ):
		if self.__cooldown_is_over(): 
			self.__execute_func()
			self.stop()
			self.__repeat()