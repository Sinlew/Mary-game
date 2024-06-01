from typing import Iterable
import pygame, random
from pygame.sprite import AbstractGroup
from settings import *
from tile import Tile
from player import Player
from debug import debug
from addons import *
from weapon import Weapon
from ui import Ui
from enemy import Enemy
from particle import AnimationPlayer 
from magic import MagicPlayer


class Level:
    def __init__(self) -> None:
        
        #get display 
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.visible_sprites = SortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        #spec_sprite
        self.curr_attack_sprite = None
        self.attack_sprite = pygame.sprite.Group()
        self.attackable_sprite = pygame.sprite.Group()

        #sprite setup
        self.create_map()

        #ui
        self.ui = Ui()
        self.ui.get_weapon_graphic(self.player)

        #particle
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)
        
    def create_map(self):
        layouts = {
            'borders': import_csv_layout("graphics/map/map_zone.csv"),
            'decor': import_csv_layout("graphics/map/map_decor.csv"),
            'green': import_csv_layout("graphics/map/map_green.csv"),
            'entity': import_csv_layout("graphics/map/map_entities.csv")
        }

        graphics = {
            'green': import_tileset("graphics/tile/tf_flower.png", scale=True),
            'objects': import_tileset("graphics/tile/props.png", scale=True)
        }

    
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index*TILESIZE
                        y = row_index*TILESIZE
                        if style == 'borders':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')
                        if style == 'decor':
                            obj = graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites, self.obstacle_sprites], "objects", obj)
                        if style == 'green':
                            flower = graphics['green'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.attackable_sprite], 'green', flower)
                        if style == "entity":
                            if col == "27":
                                self.player = Player(
                                            (x,y), 
                                            [self.visible_sprites], 
                                            self.obstacle_sprites, 
                                            self.create_attack, 
                                            self.destroy_attack, 
                                            self.create_magic)
                            else:
                                if col == "2":monster_name = "c"
                                elif col == "0": monster_name = "b"
                                elif col == "7": monster_name = "borb"
                                elif col == "9": monster_name = "d"
                                elif col == "50":monster_name = "e"
                                Enemy(monster_name, 
                                      (x,y), 
                                      [self.visible_sprites, self.attackable_sprite], 
                                      self.obstacle_sprites, 
                                      self.damage_player,
                                      self.trigger_death_particle)
        
    def create_attack(self):
        self.curr_attack_sprite = Weapon(self.player, [self.visible_sprites, self.attack_sprite])

    def create_magic(self, style, strength, cost):
        if style == "heal":
            self.magic_player.heal(self.player, strength, cost, self.visible_sprites)
            
        if style == "fire":
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprite])
            print("flame")

    def destroy_attack(self):
        if self.curr_attack_sprite:
            self.curr_attack_sprite.kill()
        self.curr_attack_sprite = None

    def damage_player(self, damage, attack_type):
        if self.player.can_get_damage:
            self.player.health -= damage
            self.player.can_get_damage = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particle(self, pos, particle_type):

        self.animation_player.create_random_particle(particle_type, pos, self.visible_sprites)

    def player_attack_logic(self):
        if self.attack_sprite:
            for attack_sprite in self.attack_sprite:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprite, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "green":
                            pos = target_sprite.rect.center
                            self.animation_player.create_random_particle("green", pos, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def run(self):
        """
        update and draw game
        """
        
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)
        # debug(self.player.status)

class SortCameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = (self.display_surface.get_size()[0] // 2)
        self.half_height = (self.display_surface.get_size()[1] // 2)
        self.offset = pygame.math.Vector2() 

        #подключение текстуры пола 
        self.floor_surface = pygame.transform.scale2x(pygame.image.load("graphics/map/map.png").convert())
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))


    def custom_draw(self, player):

        #get pos player
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        #texture_draw
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery ):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)