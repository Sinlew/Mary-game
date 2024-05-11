from typing import Iterable
import pygame, random
from pygame.sprite import AbstractGroup
from settings import *
from tile import Tile
from player import Player
from debug import debug
from addons import *

class Level:
    def __init__(self) -> None:
        
        #get display 
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.visible_sprites = SortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        #sprite setup
        self.create_map()

    def create_map(self):
        layouts = {
            'borders': import_csv_layout("graphics/map/map_zone.csv"),
            'decor': import_csv_layout("graphics/map/map_decor.csv"),
            'green': import_csv_layout("graphics/map/map_green.csv")
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
                            Tile((x,y), [self.visible_sprites], 'green', flower)
                            
        #         if col == "x":
        #             Tile((x,y), [self.visible_sprites, self.obstacle_sprites])
        #         if col == "p":

        self.player = Player((1000,1300), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        """
        update and draw game
        """
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.direction)

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