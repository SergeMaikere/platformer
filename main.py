from settings import * 

class Game ():
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("PLATFORMER VII --> I'm just a platfomer...")
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()

        self.running = True

    def __quit_game_manager ( self ):
        for event in pygame.event.get():
            self.running =  not event.type == pygame.QUIT

    def __set_background ( self ): self.screen.fill(BG_COLOR)

    def run ( self ):

        while self.running:

            dt = self.clock.tick(FRAMERATE) / 1000

            self.__quit_game_manager()

            self.__set_background()

            self.all_sprites.update(dt)

            self.all_sprites.draw(self.screen)

            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    new_game = Game()
    new_game.run()