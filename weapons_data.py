from addons import import_tileset

graph = import_tileset("graphic/tile/weapons.png")
weapon_data = {
    "sword_1":{'cooldown':400 , 'base_damage':10 , "graphic": graph[0]},
    "sword_2":{'cooldown':350 , 'base_damage':10 , "graphic": graph[1]},
    "sword_3":{'cooldown':300 , 'base_damage':15 , "graphic": graph[2]},
    "sword_4":{'cooldown':250 , 'base_damage':15 , "graphic": graph[3]},
    "sword_5":{'cooldown':250 , 'base_damage':20 , "graphic": graph[4]},
    "sword_6":{'cooldown':200 , 'base_damage':20 , "graphic": graph[5]},
    "sword_7":{'cooldown':200 , 'base_damage':25 , "graphic": graph[6]},
    "sword_8":{'cooldown':100 , 'base_damage':30 , "graphic": graph[7]}
}