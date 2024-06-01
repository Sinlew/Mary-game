import pygame
from settings import *
from entity import Entity
from addons import import_tileset

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles):
        super().__init__(groups)
        self.sprite_type = "enemy"

        #graphic
        self.import_graphics(monster_name)
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index] 
        

        #move
        self.rect = self.image.get_rect(topleft= pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprite = obstacle_sprites

        #stats
        self.monster_name = monster_name
        monstaer_info = enemy[monster_name]
        self.health = monstaer_info['health']
        self.exp = monstaer_info['exp']
        self.damage = monstaer_info['damage']
        self.attack_type = monstaer_info["attack_type"]
        self.speed = monstaer_info["speed"]
        self.resist = monstaer_info["resist"]
        self.attack_radius = monstaer_info["attack_radius"]
        self.notice_radius = monstaer_info["notice_radius"]

        #interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles

        #immortal time
        self.can_get_damage = True
        self.hit_time = None
        self.immortal_duration = 300

    def import_graphics(self, name):
        self.animations = {"idle":[], "move":[], "attack":[]}
        # path=f"graphics/tile/{name}.png"
        path=f"graphics/tile/borb.png"
        tile = import_tileset(path=path, scale=True)
        if name == "borb":pos = ((1,3),(3,8),(8,10))
        else: pos = ((1,3),(3,8),(8,10))
        for i,y in enumerate(self.animations.keys()):
            self.animations[y] = tile[pos[i][0]:pos[i][1]]

    def get_player_direction(self, player):
        enemy_vec =  pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_direction(player)[0]
        if distance <= self.attack_radius and self.can_attack:
            if self.status != "attack":
                self.frame_index = 0
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.attack_cooldowns()
        self.check_death()

    def actions(self, player):
        if self.status == "attack":
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.damage, self.attack_type)
        elif self.status == "move":
            self.direction = self.get_player_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]
    
        self.frame_index+= self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.can_get_damage:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def attack_cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.can_get_damage:
            if current_time - self.hit_time >= self.immortal_duration:
                self.can_get_damage = True

    def get_damage(self,player, attack_type):

        if self.can_get_damage:
            self.direction = self.get_player_direction(player)[1]
            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()
                player.energy += 1
            else:
                self.health -= player.get_full_magic_damage()   
            self.hit_time = pygame.time.get_ticks()
            self.can_get_damage = False
    
    def check_death(self):
        if self.health < 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, "white")
    
    def hit_reaction(self):
        if not self.can_get_damage:
            self.direction *= -self.resist

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
        

