import pygame

pygame.display.init()
pygame.display.set_mode((1600, 800))

tutorial_level = {
    'grass': 'tutorial_level.csv'
}

level1 = {
    'terrain': 'assets/layouts/layout1/level_1_Terrain.csv',
    'grass': 'assets/layouts/layout1/level_1_Grass.csv',
    'constraints': 'assets/layouts/layout1/level_1_Constraints.csv',
    'enemy': 'assets/layouts/layout1/level_1_Enemy.csv',
    'player': 'assets/layouts/layout1/level_1_Player.csv',
    'spikes': 'assets/layouts/layout1/level_1_spikes.csv'
}

level2 = {
    'terrain': 'assets/layouts/layout2/level_2_terrain.csv',
    'grass': 'assets/layouts/layout2/level_2_grass.csv',
    'constraints': 'assets/layouts/layout2/level_2_constraints.csv',
    'enemy': 'assets/layouts/layout2/level_2_enemy.csv',
    'player': 'assets/layouts/layout2/level_2_player.csv',
    'spikes': 'assets/layouts/layout2/level_2_spikes.csv'
}

level3 = {
    'terrain': 'assets/layouts/layout3/level_3_terrain.csv',
    'grass': 'assets/layouts/layout3/level_3_grass.csv',
    'constraints': 'assets/layouts/layout3/level_3_constraints.csv',
    'enemy': 'assets/layouts/layout3/level_3_enemy.csv',
    'player': 'assets/layouts/layout3/level_3_player.csv',
    'spikes': 'assets/layouts/layout3/level_3_spikes.csv'
}


def get_terrain(img_index, level):
    level = str(level)
    terrain_data = {
        0: 'bottom.png',
        1: 'bridge.png',
        2: 'center.png',
        3: 'corner.png',
        4: 'corner2.png',
        5: 'corner3.png',
        6: 'corner4.png',
        7: 'grasstop.png',
        8: 'side.png',
        9: 'side2.png',
        10: 'top.png'
    }

    path = f"assets/level_art/terrain/{level}/{terrain_data[int(img_index)]}"
    path = str(path)
    img = pygame.image.load(path).convert_alpha()
    return img
