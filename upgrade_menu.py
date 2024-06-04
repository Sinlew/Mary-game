import pygame
from settings import *

class Upgrade:
    def __init__(self, player) -> None:
        
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attr_kol = len(player.stats)
        self.max_value = list(player.max_stats.values())
        self.attr_name = list(player.stats.keys())
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()


        self.selected_id = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()
        
        if self.can_move:
            if keys[pygame.K_RIGHT] and (self.selected_id < self.attr_kol - 1):
                self.selected_id +=1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            elif keys[pygame.K_LEFT] and (self.selected_id > 0):     
                self.selected_id -=1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()


            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.items_list[self.selected_id].trigger(self.player)
            

    def display(self):
        self.input()
        self.cooldowns()

        for index, item in enumerate(self.items_list):

            #attr
            name = self.attr_name[index]
            value = self.player.get_value_by_id(index)
            max_value = self.max_value[index]
            cost = self.player.cost_by_id(index)

            item.display(self.display_surface, self.selected_id, name, value, max_value, cost)


    def cooldowns(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 400:
                self.can_move = True

    def create_items(self):
        self.items_list = []

        for item, index in enumerate(range(self.attr_kol)):

            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attr_kol

            left = (item * increment) + (increment - self.width) // 2

            top = self.display_surface.get_size()[1]*0.1
            

            item = Item(left, top, self.width, self.height, index, self.font)
            self.items_list.append(item)

                

class Item:
    def __init__(self, left, top, width, height, index, font) -> None:
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font

    def display(self, surface, section_num, name, value, max_value, cost):

        if self.index == section_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_name(surface, name, cost, self.index == section_num)
        self.display_bar(surface, value, max_value, self.index == section_num)

    def display_name(self, surface, name, cost, selected):


        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))

        cost_surf = self.font.render(f"{int(cost)}", False,  color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom + pygame.math.Vector2(0, - 20))



        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def trigger(self, player):
        upgrade_attr = list(player.stats.keys())[self.index]
        print(upgrade_attr)

        if player.exp >= player.upgrade_cost[upgrade_attr] and player.stats[upgrade_attr] < player.max_stats[upgrade_attr]:
            player.exp -= player.upgrade_cost[upgrade_attr]
            player.stats[upgrade_attr] *= 1.1
            player.upgrade_cost[upgrade_attr] *= 1.2

            
        if player.stats[upgrade_attr] > player.max_stats[upgrade_attr]:
            player.stats[upgrade_attr] = player.max_stats[upgrade_attr]

    def display_bar(self, surface, value, max_value, selected):
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60) 
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        height_bar = bottom[1] - top[1]
        relative_number = (value / max_value) * height_bar
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30 ,10)

        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

