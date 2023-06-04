import pygame
from tiles import Tile
from settings import *
from player import Player


class Level:
    def __init__(self, level_data, surface):
        # level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x, y), self.display_surface)
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                rect_x = player.rect.x
                if sprite.rect.left <= player.rect.left <= sprite.rect.right and sprite.rect.top <= player.rect.center[1] <= sprite.rect.bottom:
                    player.on_left = True
                    player.rect.left = sprite.rect.right
                    self.current_x = player.rect.left
                    if not player.on_ground:
                        player.rect.x = rect_x + 25
                        player.rect.bottom = player.rect.bottom
                if sprite.rect.left <= player.rect.right <= sprite.rect.right and sprite.rect.top <= player.rect.center[1] <= sprite.rect.bottom:
                    player.on_right = True
                    player.rect.right = sprite.rect.left
                    self.current_x = player.rect.right
                    if not player.on_ground:
                        player.rect.x = rect_x - 25
                        player.rect.bottom = player.rect.bottom

        if player.on_left and not (sprite.rect.left <= player.rect.left <= sprite.rect.right and sprite.rect.top <= player.rect.center[1] <= sprite.rect.bottom):
            player.on_left = False
        if player.on_right and not (sprite.rect.left <= player.rect.right <= sprite.rect.right and sprite.rect.top <= player.rect.center[1] <= sprite.rect.bottom):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0.5:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    if player.bottom_value == player.rect.bottom:
                        player.on_ground = True
                        player.on_ceiling = False
                        player.bottom_value = player.rect.bottom
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                    player.on_ground = False

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 1:
            player.on_ceiling = False

    def run(self):
        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
