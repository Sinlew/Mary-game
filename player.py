import pygame
from settings import *
from addons import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprite, create_attack):
        super().__init__(groups)
        self.image = pygame.transform.scale2x(pygame.image.load('graphics/tile/char_start.png').convert_alpha())
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -5)#изменяет размер хитбокса играка игрока сверху и сниху
        

        #graphics
        self.import_player_assets() 
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.11
        
        #move
        self.direction = pygame.math.Vector2()
        self.speed = 4
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.create_attack = create_attack

        self.obstacle_sprite = obstacle_sprite

    def import_player_assets(self):
        path = "graphics/tile/charr2F.png"
        sprites = import_tileset(path, scale=True)[:0:-1]
        self.animations = {
            'down_idle':[], 'down':[], 'up_idle':[], 'up':[], 'right_idle':[], 'right':[], 'left_idle':[], 'left':[]
        }
        print('down_idle'[-1:-5:-1])
        for i in self.animations.keys():
            if i[-1:-5:-1] == 'eldi':
                self.animations[i] = [sprites.pop() for i in range(2)]
            else:
                self.animations[i] = [sprites.pop() for i in range(4)]
        self.animations["up_attack"] = self.animations["up_idle"]
        self.animations["down_attack"] = self.animations["down_idle"]
        self.animations["right_attack"] = self.animations["right_idle"]
        self.animations["left_attack"] = self.animations["left_idle"]
        print(self.animations)
        

    def input(self):
        keys = pygame.key.get_pressed()
            #movement
        if not self.attacking:    
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.animation_speed = 0.1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.animation_speed = 0.1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.animation_speed = 0.1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.animation_speed = 0.1
                self.status = 'left'
            else:
                self.direction.x = 0

            #attack
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
            #magic
            if keys[pygame.K_LCTRL]:
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

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"
                self.animation_speed = 0.03

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("idle", "attack")
                    self.animation_speed = 0.1
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack","")

    def animation(self):
        animation = self.animations[self.status]

        #обход 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image:pygame.Surface = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animation()
        self.move(self.speed)

