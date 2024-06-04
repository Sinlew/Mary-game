WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64



#ui settings

BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = "graphics/font/Samson.ttf"
UI_FONT_SIZE = 25

#general color
WATER_COLOR = "#71ddee"
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#EEEEEE"

#ui color
HEALTH_COLOR = "red"
ENERGY_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"

TEXT_COLOR_SELECTED = "#111111"
BAR_COLOR = "#EEEEEE"
BAR_COLOR_SELECTED = "#111111"
UPGRADE_BG_COLOR_SELECTED = "#EEEEEE"

weapon_data = {
    "sword_1":{'cooldown':400 , 'base_damage':10 , "graphic_start": 1, "graphic_end":5},
    "sword_2":{'cooldown':350 , 'base_damage':10 , "graphic_start": 5, "graphic_end":9},
    "sword_3":{'cooldown':300 , 'base_damage':1500 , "graphic_start": 9, "graphic_end":13}
}

magic_spells = {
    "fire":{"strength": 5, "cost":20, "icon":"graphics/magic/fire1.png"},
    "heal":{"strength": 20, "cost":10, "icon":"graphics/magic/light3.png"}
}



tier = ["0", "0", "0", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2", "2", "3", "3", "3", "4"]

enemy_tier_stats = {
    "0":{"health":(10, 50), "exp": (30, 100), "damage": (1, 15), "attack_type":"punch", "speed": (1, 4), "resist": (1, 10), "attack_radius":(30, 100), "notice_radius":(100, 300), "attack_cooldown":(500, 900)},
    "1":{"health":(40, 150), "exp": (80, 175), "damage": (5, 20), "attack_type":"punch", "speed": (2, 5), "resist": (2,9), "attack_radius":(40, 150), "notice_radius":(150, 350), "attack_cooldown":(500, 900)},
    "2":{"health":(130, 240), "exp": (150, 300), "damage": (10, 30), "attack_type":"punch", "speed": (3, 6), "resist": (3,8), "attack_radius":(50, 150), "notice_radius":(200, 400), "attack_cooldown":(500, 900)},
    "3":{"health":(200, 300), "exp": (260, 350), "damage": (12, 40), "attack_type":"punch", "speed": (3, 7), "resist": (4,7), "attack_radius":(60, 200), "notice_radius":(250, 500), "attack_cooldown":(500, 900)},
    "4":{"health":(230, 700), "exp": (300, 600), "damage": (15, 60), "attack_type":"punch", "speed": (2, 8), "resist": (4, 8), "attack_radius":(90, 200), "notice_radius":(200, 600), "attack_cooldown":(500, 900)}
}