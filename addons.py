from csv import reader
from os import walk

import pygame
from settings import TILESIZE

def import_csv_layout(path:str) -> list:
    terrarian_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrarian_map.append(list(row))
        return terrarian_map

 
def import_folder(path:str)-> list:
    surface_list = []
    for x, y, image_files in walk(path):
        for image in image_files:
            full_path = path + "/" + image
            image_surface = pygame.image.load(full_path).convert_alpha()    
            surface_list.append(image_surface)
        
        return surface_list
    
def import_tileset(path:str, scale=False) -> list:
    #res
    surface_list = []
    
    if scale:
        tileset = pygame.transform.scale2x(pygame.image.load(path).convert_alpha())
    else:
        tileset = pygame.image.load(path).convert_alpha()
        
    tileset_w, tileset_h = tileset.get_size()
    tile_width, tile_height = TILESIZE, TILESIZE
    
    for i in range(tileset_h//tile_height):
        for j in range(tileset_w//tile_width):
            x = j*tile_width
            y = i*tile_height

            tile = tileset.subsurface((x,y,tile_width, tile_height))
            
            surface_list.append(tile)

    return surface_list

def weapon_generate(weapons:dict, path:str):
    tile =  import_tileset(path, scale=True)
    for i in weapons.keys():
        weapons[i]["right"]=tile[weapons[i]["graphic_start"]]
        weapons[i]["left"]=tile[weapons[i]["graphic_start"]+1]
        weapons[i]["down"]=tile[weapons[i]["graphic_start"]+2]
        weapons[i]["up"]=tile[weapons[i]["graphic_start"]+3]
    return weapons
    