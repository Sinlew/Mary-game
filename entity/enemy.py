import pygame
from addons.settings import *
from entity.entity import Entity
from addons.addons import import_tileset
from random import randint, choice

class Enemy(Entity):
    def __init__(self, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp):
        super().__init__(groups)
        self.sprite_type = "enemy"

        #graphic
        self.import_graphics("borb")
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index] 
        

        #move
        self.rect = self.image.get_rect(topleft= pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprite = obstacle_sprites

        #stats
        self.tier = choice(tier)
        self.monster_name = "borb"
        monster_stats = enemy_tier_stats[self.tier]
        self.health = randint(monster_stats['health'][0],monster_stats['health'][1])
        self.damage = randint(monster_stats['damage'][0],monster_stats['damage'][1])
        self.attack_type = "punch"
        self.speed = randint(monster_stats['speed'][0],monster_stats['speed'][1])
        self.resist = randint(monster_stats["resist"][0],monster_stats["resist"][1])
        self.attack_radius = randint(monster_stats["attack_radius"][0],monster_stats["attack_radius"][1])
        self.notice_radius = randint(monster_stats["notice_radius"][0],monster_stats["notice_radius"][1])

        #interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = randint(monster_stats['attack_cooldown'][0],monster_stats['attack_cooldown'][1])
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp


        #immortal time
        self.can_get_damage = True
        self.hit_time = None
        self.immortal_duration = 300

        self.exp = (self.health + self.damage*3 + self.speed*10 + self.resist*10 + self.attack_radius//2 + self.notice_radius //2 + self.attack_cooldown // 2) //2
        
        print(f'tier: {self.tier}, exp: {self.exp}')

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
            self.add_exp(self.exp)
    
    def hit_reaction(self):
        if not self.can_get_damage:
            self.direction *= -self.resist

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
        

