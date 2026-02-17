from Utils.AllSprites import AllSprites
from Utils.Timer import Timer
from settings import * 
from pytmx import TiledMap
from pytmx.pytmx import TiledObject
from Utils.GameSprite import GameSprite
from Utils.Group import Group
from pygame import Event
from Utils.Helper import get_frames, get_random_pos, load_sounds, load_map, pipe
from Entities.Player import Player
from Entities.Worm import Worm
from Entities.Bee import Bee

class Game ():
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("PLATFORMER VII --> I'm just a platfomer...")
        self.clock = pygame.time.Clock()

        self.map = load_map()

        self.all_sprites = AllSprites('all_sprites')
        self.collision_sprites = Group('collision_sprites')

        self.bee_frames = get_frames('assets', 'images', 'enemies', 'bee')
        self.bee_timer = Timer(3000, self.__make_bee, repeat= True, autostart= True)

        self.running = True

    def __time_to_quit ( self, event: Event ):
        self.running = not event.type == pygame.QUIT
        return event

    def __check_event_loop ( self ):
        for event in pygame.event.get():
            self.__time_to_quit(event)

    def __set_background ( self ): self.screen.fill(BG_COLOR)

    def __set_ground ( self, map: TiledMap ) -> TiledMap:
        for x, y, image in map.get_layer_by_name('Main').tiles():
            GameSprite(image, self.all_sprites, self.collision_sprites, topleft=(x * TILE_SIZE, y * TILE_SIZE))
        return map

    def __set_objects ( self, map: TiledMap ) -> TiledMap:
        for x, y, image in map.get_layer_by_name('Decoration').tiles():
            GameSprite(image, self.all_sprites, topleft=(x * TILE_SIZE, y * TILE_SIZE))
        return map

    def __make_player ( self, entity: TiledObject ):
        if not entity.name == 'Player': return entity

        frames = get_frames('assets', 'images', 'player')
        if frames: self.player = Player(frames, self.collision_sprites, self.all_sprites, topleft=(entity.x, entity.y))
        return entity

    def __make_worm ( self, entity: TiledObject ):
        if not entity.name == 'Worm': return entity

        frames = get_frames('assets', 'images', 'enemies', 'worm')
        if frames: Worm(frames, self.all_sprites, topleft=(entity.x, entity.y))
        return entity

    def __make_bee ( self ):
        if self.bee_frames: Bee(self.bee_frames, self.all_sprites, topleft= get_random_pos( self.map.width * TILE_SIZE, self.map.height * TILE_SIZE ))

    def __set_entities ( self, map: TiledMap ) -> TiledMap:
        for entity in map.get_layer_by_name('Entities'):
            pipe( 
                self.__make_player, 
                self.__make_worm 
            )( entity )
        return map


    def __setup_map_assets ( self ):
        pipe(
            self.__set_ground,
            self.__set_objects,
            self.__set_entities
        )( self.map )

    def __set_sounds ( self): self.sounds = load_sounds('assets', 'audio')

    def __set_volumes ( self ):
        if self.sounds:
            self.sounds['music'].set_volume(3)
            self.sounds['shoot'].set_volume(3)
            self.sounds['impact'].set_volume(3)

    def __play_soundtrack( self ): 
        if self.sounds: self.sounds['music'].play()

    def __setup_sounds ( self ):
            self.__set_sounds()
            self.__set_volumes()
            self.__play_soundtrack()

    def run ( self ):

        self.__setup_map_assets()
        self.__setup_sounds()

        while self.running:

            dt = self.clock.tick(FRAMERATE) / 1000

            self.__check_event_loop()

            self.__set_background()

            self.bee_timer.update()

            self.all_sprites.update(dt)

            self.all_sprites.draw(self.player.rect.center)

            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    new_game = Game()
    new_game.run()