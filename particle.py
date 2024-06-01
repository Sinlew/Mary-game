import pygame
from addons import import_tileset
from random import choice


class AnimationPlayer:
    def __init__(self):
        tile = import_tileset("graphics/particle/pa.png")
        tile_green = import_tileset("graphics/particle/pa2.png", scale=True)
        tile_white = import_tileset("graphics/particle/pa3.png")
        self.frames = {
            "heal": tile[0:6],
            "flame": tile[6:12],
            "punch": tile[12:18],
            "aura": tile[18:24],
            "green":( tile_green[0:4],
            tile_green[4:8],
            tile_green[8:12],
            tile_green[12:16]),
            "white":(tile_white[0:7],
                     tile_white[7:14],
                     tile_white[14:21])
        }

    def create_grass_prt(self, pos, groups):
        animation_frame = choice(self.frames["green"])
        Particle(pos, animation_frame, groups)
    
    def create_random_particle(self, prt_group, pos, groups):
        animation_frame = choice(self.frames[prt_group])
        Particle(pos, animation_frame, groups)

    def create_particles(self, type, pos, groups):
        animation = self.frames[type]
        Particle(pos, animation, groups)

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups) -> None:
        super().__init__(groups)
        self.sprite_type = "magic"
        self.frame_id = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_id]
        self.rect = self.image.get_rect(center = pos)
        

    def animete(self):
        self.frame_id += self.animation_speed
        if self.frame_id >= len(self.frames):
            self.kill()
        else:
            
            self.image = self.frames[int(self.frame_id)]

    def update(self) -> None:
        self.animete()