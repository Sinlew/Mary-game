from typing import Iterable
import pygame, random
from pygame.sprite import AbstractGroup
from addons.settings import *
from map.tile import Tile
from entity.player import Player
from addons.debug import debug
from addons.addons import *
from items.weapon import Weapon
from ui.ui import Ui
from entity.enemy import Enemy
from addons.particle import AnimationPlayer 
from items.magic import MagicPlayer
from ui.upgrade_menu import  Upgrade
from random import choice

class Level:
    def __init__(self) -> None:
        
        #get display 
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        #sprite group setup
        self.visible_sprites = SortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        #spec_sprite
        self.curr_attack_sprite = None
        self.attack_sprite = pygame.sprite.Group()
        self.attackable_sprite = pygame.sprite.Group()

        #spawn
        self.last_spawn = pygame.time.get_ticks()

        #sprite setup
        self.create_map()

        #ui
        self.ui = Ui()
        self.ui.get_weapon_graphic(self.player)

        self.upgrade = Upgrade(self.player)

        #particle
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        
        
    def create_map(self):
        print("map create")
        
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
                            if col == "1":
                                self.player = Player(
                                            (x,y), 
                                            [self.visible_sprites], 
                                            self.obstacle_sprites, 
                                            self.create_attack, 
                                            self.destroy_attack, 
                                            self.create_magic)
                            else:
                                Enemy((x,y), 
                                      [self.visible_sprites, self.attackable_sprite], 
                                      self.obstacle_sprites, 
                                      self.damage_player,
                                      self.trigger_death_particle, 
                                      self.add_exp)
                                
                                
                                      
    def create_attack(self):
        self.curr_attack_sprite = Weapon(self.player, [self.visible_sprites, self.attack_sprite])

    def create_magic(self, style, strength, cost):
        if style == "heal":
            self.magic_player.heal(self.player, strength, cost, self.visible_sprites)
            
        if style == "fire":
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprite])

    def destroy_attack(self):
        if self.curr_attack_sprite:
            self.curr_attack_sprite.kill()
        self.curr_attack_sprite = None

    def damage_player(self, damage, attack_type):
        if self.player.can_get_damage:
            if self.player.health>=0:

                self.player.health -= damage
                self.player.can_get_damage = False
                self.player.hurt_time = pygame.time.get_ticks()
                self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])
            
    def hero_is_dead(self):
        if self.player.health <= 0:
            return True
        return False
                

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

    def add_exp(self, amout):
        self.player.exp += amout

    def toggle_menu(self):

        self.game_paused = not self.game_paused

    def enemy_spawn(self):
        cur_time = pygame.time.get_ticks()
        
        if cur_time - self.last_spawn >= random.randint(1000, 10000):
            pose = (random.randint(2560, 5440),random.randint(2112, 5312))
            
            Enemy(pose,
                  [self.visible_sprites, self.attackable_sprite], 
                    self.obstacle_sprites, 
                    self.damage_player,
                    self.trigger_death_particle, 
                    self.add_exp)
            self.last_spawn = pygame.time.get_ticks()


    def run(self):
        """
        update and draw game
        """
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            self.enemy_spawn()
        
        
        
        
        # debug(self.player.hitbox.center)

class SortCameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = (self.display_surface.get_size()[0] // 2)
        self.half_height = (self.display_surface.get_size()[1] // 2)
        self.offset = pygame.math.Vector2() 

        #подключение текстуры пола 
        self.floor_surface = pygame.transform.scale2x(pygame.image.load("graphics/map/map.png").convert())
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,15))


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