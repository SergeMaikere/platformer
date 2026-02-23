from functools import partial
from settings import * 
from random import randint
from pytmx import TiledMap
from pytmx.pytmx import TiledObject
from GameObjects.Bullet import Bullet
from GameObjects.Fire import Fire
from Entities.Player import Player
from Entities.Worm import Worm
from Entities.Bee import Bee
from Utils.AllSprites import AllSprites
from Utils.GameSprite import GameSprite
from Utils.Group import Group
from Utils.Helper import get_frames, get_frame, load_sounds, load_map, pipe, get_flipped_surface
from Utils.Timer import Timer

class Game ():
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("PLATFORMER VII --> I'm just a platfomer...")
        self.clock = pygame.time.Clock()

        self.map = load_map()
        self.map_size = { 'width': self.map.width * TILE_SIZE, 'height': self.map.height * TILE_SIZE }

        self.all_sprites = AllSprites('all_sprites')
        self.collision_sprites = Group('collision_sprites')
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        self.bee_frames = get_frames('assets', 'images', 'enemies', 'bee')
        self.bee_timer = Timer(1000, self.__make_bee, repeat=True, autostart=True)

        self.running = True

    def game_over ( self ): self.running = False

    def __is_player_exiting_game ( self ): return any( event.type == pygame.QUIT for event in pygame.event.get() )

    def __has_player_fallen ( self ): return self.player.rect.y > self.map_size['height'] + 900

    def __check_quit_game ( self ):
        self.running = not ( self.__is_player_exiting_game() or self.__has_player_fallen() )

    def __set_background ( self ): self.screen.fill(BG_COLOR)

    def __load_assets ( self ):
        self.player_frames = get_frames('assets', 'images', 'player')
        
        self.bee_frames = get_frames('assets', 'images', 'enemies', 'bee')

        self.worm_frames = get_frames('assets', 'images', 'enemies', 'worm')
        if self.worm_frames: self.worm_flipped_frames = [ pygame.transform.flip(frame, True, False) for frame in self.worm_frames ]
        
        self.bullet_surface, self.flipped_bullet_surface = get_flipped_surface( get_frame(join('assets', 'images', 'gun'), 'bullet.png') )
        
        self.fire_surface, self.flipped_fire_surface = get_flipped_surface( get_frame(join('assets', 'images', 'gun'), 'fire.png') )
        
        self.sounds = load_sounds('assets', 'audio')

    def __play_sound ( self, sound: str, loops: int = 0 ): 
        if self.sounds: self.sounds[sound].play(loops)

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

        if self.player_frames: 
            self.player = Player(self.player_frames, self.__make_bullet, self.__make_fire, self.collision_sprites, self.all_sprites, topleft=(entity.x, entity.y))
        return entity

    def __make_worm ( self, entity: TiledObject ):
        if not entity.name == 'Worm': return entity

        patrol_area = pygame.FRect(entity.x, entity.y, entity.width, entity.height)
        if self.worm_frames: Worm((self.worm_frames, self.worm_flipped_frames), patrol_area, self.all_sprites, self.enemy_sprites)
        return entity

    def __make_bee ( self ):
        if self.bee_frames: 
            Bee( self.bee_frames, self.all_sprites, self.enemy_sprites, topleft=(self.map_size['width'], randint(0, self.map_size['height'])) )

    def __make_bullet ( self ):
        Bullet((self.bullet_surface, self.flipped_bullet_surface), self.map_size['width'], self.player, self.all_sprites, self.bullet_sprites )

    def __make_fire ( self ):   
        Fire((self.fire_surface, self.flipped_fire_surface), self.player, self.all_sprites)
        self.__play_sound('shoot')

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

    def __set_volumes ( self ):
        if self.sounds:
            self.sounds['music'].set_volume(0.1)
            self.sounds['shoot'].set_volume(0.3)
            self.sounds['impact'].set_volume(0.3)

    def __setup_sounds ( self ):
            self.__set_volumes()
            self.__play_sound('music', loops=-1)

    def __get_bullet_collisions ( self, bullet: Bullet ):
        return pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)

    def __kill_bullet ( self, bullet: Bullet, enemies: list[Bee | Worm] ):
        if not enemies: return enemies
        bullet.kill()
        return enemies

    def __kill_enemies ( self, enemies: list[Bee | Worm] ):
        if not enemies: return
        for enemy in enemies: 
            enemy._destroy()
            self.__play_sound('impact')

    def __bullet_enemy_collision ( self ):
        for bullet in self.bullet_sprites:
            pipe(
                self.__get_bullet_collisions,
                partial(self.__kill_bullet, bullet),
                self.__kill_enemies
            )(bullet)

    def __player_enemy_collision ( self ):
        collisions = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask)
        if collisions: 
            for enemy in collisions:
                if not enemy.death_timer.active: self.game_over()

    def __collisions ( self ):
        self.__player_enemy_collision()
        self.__bullet_enemy_collision()

    def run ( self ):
        self.__load_assets()
        self.__setup_map_assets()
        self.__setup_sounds()

        while self.running:

            dt = self.clock.tick(FRAMERATE) / 1000

            self.__check_quit_game()

            self.__set_background()

            self.__collisions()
            
            self.bee_timer.update()

            self.all_sprites.update(dt)

            self.all_sprites.draw(self.player.rect.center)

            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    new_game = Game()
    new_game.run()