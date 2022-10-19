from os import path
import pickle
import pygame
from constants.BackgroundConstants import BackgroundConstants
from classes.button.Button import Button 

from classes.player.Player import Player
from classes.world.World import World, blob_group, lava_group, exit_group

from levels.levels_data import LEVEL_1_MAP_DIMENSIONS

pygame.init()

clock = pygame.time.Clock()

fps = 60
game_over = 0
main_menu = True
level = 0
max_levels = 7

screen_width = BackgroundConstants.SCREEN_WIDTH
screen_height = BackgroundConstants.SCREEN_HEIGHT

screen = BackgroundConstants.SCREEN

pygame.display.set_caption('House of cats')

tile_size = BackgroundConstants.TILE_SIZE
# load images
sun_img = pygame.image.load(path.join('assets', 'background', 'sun.png'))
bg_img = pygame.image.load(path.join('assets', 'background', 'sky.png'))
lib_img = pygame.image.load(path.join('assets', 'background','library2.png'))

restart_img = pygame.image.load(path.join('assets', 'menu','restart_btn.png'))
start_img = pygame.image.load(path.join('assets', 'menu','start_btn.png'))
exit_img = pygame.image.load(path.join('assets', 'menu', 'exit_btn.png'))

restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)

""" if path.exists(f'levels/level{level}_data'):
    pickle_in = open(f'levels/level{level}_data', 'rb')
    
    world_data = pickle.load(pickle_in) """
    
world_data = LEVEL_1_MAP_DIMENSIONS
world = World(world_data)

player = Player(88,screen_height - 102)



# lib_img = pygame.transform.scale(lib_img,(1000,1000))

def draw_grid(): # Just to call the lines
    for line in range(0,20): # 20
        pygame.draw.line(screen, (255,255,255), (0,line*tile_size), (screen_width, line*tile_size))
        pygame.draw.line(screen, (255,255,255), (line*tile_size,0), (line*tile_size, screen_height))

def reset_level(level):
    blob_group.empty()
    lava_group.empty()
    exit_group.empty()

    print(level)

    # Load in level data and create world
    """  if path.exists(f'levels/level{level}_data'):
        pickle_in = open(f'levels/level{level}_data', 'rb') """
        
    world_data = LEVEL_1_MAP_DIMENSIONS
    world = World(world_data)

    return world

run = True

# All game run here.
while(run == True):
    
    clock.tick(fps)

    # Tela base do jogo. Colocaremos algumas condições no futuro para o plano de fundo mudar com o nível.
    screen.blit(bg_img, (0,0))
    screen.blit(sun_img, (100,100))

    if main_menu == True:
        if exit_button.draw() == True:
            run = False

        if start_button.draw() == True:
            main_menu = False

    else:

        world.draw()

        if game_over == 0:
            blob_group.update()
        
        blob_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)

        game_over = player.update(game_over, world)

        # If player died
        if game_over == -1:
            if restart_button.draw() == True:
                # Precisei criar uma classe reset no player
                # para o botão do reset funcionar.
                world_data = []
                world = reset_level(level)
                player.reset(88,screen_height - 102)
                game_over = 0

        # If player has completed the lvl
        if game_over == 1:
            # Reset game and go to next level
            level += 1
            if level <= max_levels:
                # Reset level
                world_data = []
                world = reset_level(level)
                player.reset(88,screen_height - 102)
                game_over = 0

            else:
                if restart_button.draw():
                    level = 1

                    world_data = []
                    world = reset_level(level)
                    player.reset(88,screen_height - 102)
                    game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()