import pygame
from addons.settings import *

class Ui:
    def __init__(self) -> None:
        
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        self.healthbar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energybar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH, BAR_HEIGHT)

        self.weapon_graphics = []

        self.magic_icons = []
        for magic in magic_spells.values():
            magic = pygame.transform.scale2x(pygame.image.load(magic['icon']).convert_alpha())
            self.magic_icons.append(magic)                
        

    def show_bar(self, curruent, max_amout, bg_rect, color):

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        ratio = curruent/ max_amout
        curruent_width = bg_rect.width * ratio
        curruent_rect = bg_rect.copy()
        curruent_rect.width = curruent_width
        
        pygame.draw.rect(self.display_surface, color, curruent_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 4)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,5))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,5),4)

    def get_weapon_graphic(self,player):
        for weapon in player.weapons_lib.values():
            self.weapon_graphics.append(weapon["up"])
       

    def selection_box(self, left, top, switchable):
        bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if switchable:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect,4)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect,4)
        return bg_rect

    def weapon_overlay(self, weapon_id, has_switched):
        bg_rect =  self.selection_box(75, 630, has_switched)
        weapon_surf = self.weapon_graphics[weapon_id]       
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
        
        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_id, has_switched):
        bg_rect =  self.selection_box(10, 600, has_switched)
        magic_surf = self.magic_icons[magic_id]       
        magic_rect = magic_surf.get_rect(center = bg_rect.center)
        
        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.healthbar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energybar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)
        self.magic_overlay(player.magic_id, not player.switchable_magic)
        self.weapon_overlay(player.weapon_id, not player.switchable_weapon)
        
        