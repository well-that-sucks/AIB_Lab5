import pygame
from spritesheetutil import SpriteSheetUtil
from csv import writer


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
SPRITE_SIZE = 48
TOTAL_SPRITES_H = SCREEN_WIDTH // SPRITE_SIZE
TOTAL_SPRITES_V = SCREEN_HEIGHT // SPRITE_SIZE
SPRITE_CHANGE_INTERVAL = 5
BLINKING_BASE_INTERVAL = 20
BOT_CHANGE_DIRECTION_INTERVAL = 80
PACMAN_CHANGE_DIRECTION_INTERVAL = 12
KILLER_MODE_DURATION = 600
ANIM_FRAME_DURATION = 10
RESPAWN_TIME = 300
ALLOWANCE_THRESHOLD = 0.35
BLINKING_WARNING_THRESHOLD = 200
EATEN_ENEMY_REWARD = 200
COIN_VALUE = 10
MIN_COLLISION_DISTANCE = 25
FPS = 60
TRAVERSAL_FUNCTIONS_AMOUNT = 2

random_level_name = 'random_level'
levels = [random_level_name, 'level1', 'level2', 'level3']
level_idx = 0

results_filename = 'results.csv'

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load('resources/icon.png')

transition_font = pygame.font.Font('freesansbold.ttf', 32)
hud_font = pygame.font.Font('freesansbold.ttf', 24)

spritesheet_util = SpriteSheetUtil('pacman.png')

ghost_sprites = [spritesheet_util.get_image(1, 83, 16, 16, 3),
    spritesheet_util.get_image(601, 269, 16, 16, 3),
    spritesheet_util.get_image(601, 641, 16, 16, 3),
    spritesheet_util.get_image(401, 83, 16, 16, 3)]
pacman_death_anim = [spritesheet_util.get_image(201, 692, 16, 16, 3),
    spritesheet_util.get_image(218, 692, 16, 16, 3),
    spritesheet_util.get_image(235, 692, 16, 16, 3),
    spritesheet_util.get_image(252, 692, 16, 16, 3),
    spritesheet_util.get_image(269, 692, 16, 16, 3),
    spritesheet_util.get_image(286, 692, 16, 16, 3),
    spritesheet_util.get_image(201, 709, 16, 16, 3),
    spritesheet_util.get_image(218, 709, 16, 16, 3),
    spritesheet_util.get_image(235, 709, 16, 16, 3),
    spritesheet_util.get_image(252, 709, 16, 16, 3),
    spritesheet_util.get_image(269, 709, 16, 16, 3),
    spritesheet_util.get_image(286, 709, 16, 16, 3)]
ghost_killer_mode_sprite = spritesheet_util.get_image(201, 168, 16, 16, 3)
blank_sprite = spritesheet_util.get_image(286, 709, 16, 16, 3)
wall_sprite = spritesheet_util.get_image(801, 604, 48, 48, 1)
coin_sprite = spritesheet_util.get_image(536, 586, 8, 8, 2)
cherry_sprite = spritesheet_util.get_image(601, 489, 16, 16, 3)
strawberry_sprite = spritesheet_util.get_image(618, 489, 16, 16, 3)
booster_sprite = spritesheet_util.get_image(669, 489, 16, 16, 3)
pacman_sprite1 = spritesheet_util.get_image(303, 709, 16, 16, 3)
pacman_sprite2 = spritesheet_util.get_image(303, 692, 16, 16, 3)

def find_dist(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

def find_next_cell(path_matrix):
    cell = (-1, -1)
    for i in range(len(path_matrix)):
        for j in range(len(path_matrix[0])):
            if path_matrix[i][j] == 1:
                cell = (j, i)
            elif path_matrix[i][j] == 2:
                return (j, i)
    return cell

def get_direction(coord1, coord2):
    if coord1 - coord2 > 0:
        return 1
    if coord1 - coord2 < 0:
        return -1
    return 0

def apply_ghost_sprites(ghosts, sprites):
    ind = 0
    for ghost in ghosts:
        ghost.set_sprite(sprites[ind % len(sprites)])
        ind += 1

def append_row_to_csv(filename, list_of_elem):
    with open(filename, 'a+', newline = '') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)