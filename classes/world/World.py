import os
import pygame
from constants.BackgroundConstants import BackgroundConstants
from classes.enemies.Enemy import Enemy
from classes.exit.Exit import Exit
from classes.lava.Lava import Lava

tile_size = BackgroundConstants.TILE_SIZE

blob_group, lava_group, exit_group = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()

screen = BackgroundConstants.SCREEN
class World():
    def __init__(self, world_data):
        self.tile_list = []

        dirt_img = pygame.image.load(os.path.join('assets', 'background', 'dirt.png'))
        grass_img = pygame.image.load(os.path.join('assets', 'background','grass.png'))

        row_count = 0
        for row in world_data:
            col_count = 0
            for tile in row:
                if tile == 1: 
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 2: # Grama
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 3: # Para mudarmos o inimigo iremos precisar mexer aqui.
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15) # argumentos: Depende da coluna * tile_size, o msm p/ linha  
                    
                    blob_group.add(blob)

                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)

                if tile == 8:
                    exit_action = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    
                    exit_group.add(exit_action)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen,(255,255,255), tile[1], 2)