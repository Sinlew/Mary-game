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
UI_FONT_SIZE = 18

#general color
WATER_COLOR = "#71ddee"
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#EEEEEE"

#ui color
HEALTH_COLOR = "red"
ENERGY_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"

weapon_data = {
    "sword_1":{'cooldown':400 , 'base_damage':10 , "graphic_start": 1, "graphic_end":5},
    "sword_2":{'cooldown':350 , 'base_damage':10 , "graphic_start": 5, "graphic_end":9},
    "sword_3":{'cooldown':300 , 'base_damage':1500 , "graphic_start": 9, "graphic_end":13}
}

magic_spells = {
    "fire":{"strength": 5, "cost":20, "icon":"graphics/magic/fire1.png"},
    "heal":{"strength": 20, "cost":10, "icon":"graphics/magic/light3.png"}
}

enemy = {
    "borb":{"health":10, "exp": 50, "damage": 50, "attack_type":"punch", "speed": 4 , "resist": 8, "attack_radius":100, "notice_radius":300},
    "b":{"health":100, "exp": 150, "damage": 10, "attack_type":"punch", "speed": 5, "resist": 8, "attack_radius": 100, "notice_radius":300},
    "c":{"health":300, "exp": 100, "damage": 5, "attack_type":"punch", "speed": 3, "resist": 8, "attack_radius":20, "notice_radius":300},
    "d":{"health":200, "exp": 400, "damage": 35, "attack_type":"punch", "speed": 6, "resist": 8, "attack_radius": 100, "notice_radius":300},
    "e":{"health":100, "exp": 1, "damage": 100, "attack_type":"punch", "speed": 6, "resist": 8, "attack_radius": 10, "notice_radius":100}
}