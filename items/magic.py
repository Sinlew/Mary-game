import pygame

from addons.settings import *
from random import randint
class MagicPlayer:
    def __init__(self, animation_player):
        self.aniamtion_player = animation_player

    def heal(self, player, strength, cost, group):
        if player.energy >= cost:
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats["health"]:
                player.health = player.stats["health"]
            self.aniamtion_player.create_particles("heal", player.rect.center, group)
            
    def flame(self, player, cost, group):
        if player.energy >= cost:
            player.energy -= cost

            if player.status.split("_")[0] == "right":
                direction = pygame.math.Vector2(1,0)
            elif player.status.split("_")[0] == "left":
                direction = pygame.math.Vector2(-1,0)
            elif player.status.split("_")[0] == "up":
                direction = pygame.math.Vector2(0,-1)
            else:
                direction = pygame.math.Vector2(0,1)
            
            for i in range(1, 6):
                if direction.x:
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint( -TILESIZE // 3, TILESIZE // 4)
                    y = player.rect.centery + randint(-TILESIZE // 4, TILESIZE // 3)
                    self.aniamtion_player.create_particles("aura", (x, y), group)
                else:
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint( -TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.aniamtion_player.create_particles("aura", (x, y), group)