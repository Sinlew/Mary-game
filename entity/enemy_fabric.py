import pygame
from addons.settings import *
from entity.entity import Entity
from addons.addons import import_tileset
from random import randint
from entity.enemy import Enemy

class Enemy_spawner(Entity):
    def __init__(self, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp):
        self.pos = pos
        self.groups = groups
        self.obstacle = obstacle_sprites
        self.damage_player = damage_player
        self.trigger_death_particle = trigger_death_particles
        self.add_exp = add_exp
        self.spawn_time = pygame.time.get_ticks()


        
      
    def update(self):
        self.spawn_check()
        print("ddsds")

    def spawn_check(self):
        cur_time = pygame.time.get_ticks()
        if cur_time - self.spawn_time > 1000:
            Enemy(self.pos, 
                self.groups, 
                self.obstacle, 
                self.damage_player,
                self.trigger_death_particle, 
                self.add_exp)
            self.spawn_time = pygame.time.get_ticks()
