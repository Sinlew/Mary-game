import pygame
from addons.settings import *
from addons.addons import *
from entity.entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprite, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.transform.scale2x(pygame.image.load('graphics/tile/char_start.png').convert_alpha())
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-15, -20)#изменяет размер хитбокса играка игрока сверху и сниху
        

        #graphics
        self.import_player_assets() 
        self.status = 'down'
        
        
        #move
        
        self.speed = 4
        self.attacking = False
        self.attack_cooldown = 100
        self.attack_time = None
        self.obstacle_sprite = obstacle_sprite

        #weapons
        self.weapons_lib = weapon_generate(weapon_data, "graphics/tile/weapons.png")

        #cur_weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_id = 0
        self.weapon = list(weapon_data.keys())[self.weapon_id]
        self.switchable_weapon = True
        self.weapon_switch_time = None 
        self.switch_cooldown = 200

        #magic
        self.create_magic = create_magic
        self.magic_id = 0
        self.magic = list(magic_spells.keys())[self.magic_id]
        self.switchable_magic = True
        self.magic_switch_time = None


        #stats
        self.stats = {"health":100, 'energy':60, "damage":10, "magic":4, "speed":6}
        self.max_stats = {"health":500, 'energy':200, "damage":40, "magic":20, "speed":10}
        self.upgrade_cost = {"health":100, 'energy':150, "damage":150, "magic":200, "speed":200}
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.speed = self.stats["speed"]
        self.exp = 500

        #get damage
        self.can_get_damage = True
        self.hurt_time = None
        self.immortal_duration = 500   


    def import_player_assets(self): 
        path = "graphics/tile/charr2F.png"
        sprites = import_tileset(path, scale=True)[:0:-1]
        self.animations = {
            'down_idle':[], 'down':[], 'up_idle':[], 'up':[], 'right_idle':[], 'right':[], 'left_idle':[], 'left':[]
        }
        for i in self.animations.keys():
            if i[-1:-5:-1] == 'eldi':
                self.animations[i] = [sprites.pop() for i in range(2)]
            else:
                self.animations[i] = [sprites.pop() for i in range(4)]
        self.animations["up_attack"] = self.animations["up_idle"]
        self.animations["down_attack"] = self.animations["down_idle"]
        self.animations["right_attack"] = self.animations["right_idle"]
        self.animations["left_attack"] = self.animations["left_idle"]
        
        

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
                style = list(magic_spells.keys())[self.magic_id] 
                
                strength = list(magic_spells.values())[self.magic_id]['strength'] + self.stats['magic']
                cost = list(magic_spells.values())[self.magic_id]['cost']

                self.create_magic(style, strength, cost)
            #switch weapon qe
            if keys[pygame.K_q] and self.switchable_weapon:
                self.switchable_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_id < len(list(weapon_data.keys())) - 1:
                    self.weapon_id +=1
                else:
                    self.weapon_id = 0

                self.weapon = list(weapon_data.keys())[self.weapon_id] 
            if keys[pygame.K_e] and self.switchable_weapon:
                self.switchable_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_id > 0:
                    self.weapon_id -=1
                else:
                    self.weapon_id = len(list(weapon_data.keys()))-1
                self.weapon = list(weapon_data.keys())[self.weapon_id] 

            #switch magic ad
            if keys[pygame.K_a] and self.switchable_magic:
                self.switchable_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                if self.magic_id < len(list(magic_spells.keys())) - 1:
                    self.magic_id +=1
                else:
                    self.magic_id = 0
                self.magic = list(magic_spells.keys())[self.magic_id] 

            if keys[pygame.K_d] and self.switchable_magic:
                self.switchable_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                if self.magic_id > 0:
                    self.magic_id -=1
                else:
                    self.magic_id = len(list(magic_spells.keys()))-1
                self.magic = list(magic_spells.keys())[self.magic_id] 
 
    
    def cooldowns(self):
        cur_time = pygame.time.get_ticks()

        if self.attacking:
            if cur_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]["cooldown"]:
                self.attacking = False
                self.destroy_attack()
        
        if not self.switchable_weapon:
            if cur_time - self.weapon_switch_time >= self.switch_cooldown:
                self.switchable_weapon = True

        if not self.switchable_magic:
            if cur_time - self.magic_switch_time >= self.switch_cooldown:
                self.switchable_magic = True

        if not self.can_get_damage:
            if cur_time - self.hurt_time >= self.immortal_duration:
                self.can_get_damage = True

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

        if not self.can_get_damage:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def energy_recovery(self):
        if self.energy < self.stats["energy"]:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats["energy"]

    def get_full_weapon_damage(self):
        base_damage = self.stats['damage']
        weapon_damage = weapon_data[self.weapon]["base_damage"]
        return base_damage + weapon_damage
    
    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_spells[self.magic]["strength"]
        return base_damage + spell_damage

    def get_value_by_id(self , id):
        return list(self.stats.values())[id]

    def cost_by_id(self, id):
        return list(self.upgrade_cost.values())[id]

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animation()
        self.move(self.stats['speed'])
        self.energy_recovery()

