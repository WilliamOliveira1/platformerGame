import pygame

from support import import_folder


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, surface):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.dust_particles = import_folder('./graphics/character/dust_particles/run')

        # dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 0.5
        self.gravity = 0.2
        self.jump_speed = -6
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.bottom_value = 0

        # player status
        self.status = 'idle'

    def import_character_assets(self):
        character_path = './graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        pass

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center=self.rect.center)

    # Get keyboard input to move the player
    def get_input(self):
        keys = pygame.key.get_pressed()
        self.bottom_value = self.rect.bottom
        if keys[pygame.K_RIGHT]:
            self.facing_right = True
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.facing_right = False
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground and not self.on_ceiling:
            if self.on_left or self.on_right:
                print(1)
                self.direction.x = 0
            else:
                print(2)
                self.jump()

    '''def not_move_vertical(self):
        print(f'self.direction.y: {self.direction.y}')
        print(f'self.direction.y: {self.direction.y}')
        if self.direction.x == 1 or self.direction.x == -1:
            self.direction.y = 0.36'''

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            elif self.on_ground:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    # update the position of the player
    def update(self):
        self.get_input()

        # To move faster the player change the multiplier value
        self.rect.x += self.direction.x * self.speed
        self.apply_gravity()
        self.get_status()
        self.animate()
        # self.not_move_vertical()
