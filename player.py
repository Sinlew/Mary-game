import pygame
from settings import *
from addons import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprite):
        super().__init__(groups)
        self.image = pygame.transform.scale2x(pygame.image.load('graphics/tile/char_start.png').convert_alpha())
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -5)#изменяет размер хитбокса играка игрока сверху и сниху
        self.hitbox.move_ip(100,100)

        #graphics
        self.import_player_assets() 
        # self.image =  pygame.transform.scale2x(self.image)
        
        #move
        self.direction = pygame.math.Vector2()
        self.speed = 4
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None


        self.obstacle_sprite = obstacle_sprite

    def import_player_assets(self):
        path = "graphics/tile/charr2F.png"
        sprites = import_tileset(path, scale=True)[:0:-1]
        self.animations = {
            'idle_down':[], 'down':[], 'idle_up':[], 'up':[], 'idle_right':[], 'right':[], 'idle_left':[], 'left':[]
        }
        
        for i in self.animations.keys():
            if i[0:4] == 'idle':
                self.animations[i] = [sprites.pop() for i in range(2)]
            else:
                self.animations[i] = [sprites.pop() for i in range(4)]


    def input(self):
        keys = pygame.key.get_pressed()
        #movement
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        #attack
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print("attack")
        #magic
        if keys[pygame.K_LCTRL] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print("magic")

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        # self.rect.center += self.direction * speed
        self.hitbox.x += self.direction.x * speed
        self.collisson("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collisson("vertical")
        self.rect.center = self.hitbox.center

    def collisson(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right 

        if direction == "vertical":
             for sprite in self.obstacle_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top 
    
    def cooldowns(self):
        cur_time = pygame.time.get_ticks()

        if self.attacking:
            if cur_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def update(self):
        self.input()
        self.cooldowns()
        self.move(self.speed)

