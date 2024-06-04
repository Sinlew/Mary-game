import pygame
from player import Player

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player:Player, groups):
        super().__init__(groups)

        direction = player.status.split("_")[0]
        self.sprite_type = "weapon"
        
          
        #graphic
        self.image = player.weapons_lib[player.weapon][direction] 
        

        #place
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright+pygame.math.Vector2(-10,0))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(10,0))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(0,0)) 
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(0,5)) 
        else:
            self.rect = self.image.get_rect(center = player.rect.center)
        