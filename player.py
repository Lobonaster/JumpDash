import pygame
from support2 import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles):
        super().__init__()
        self.import_character_animations()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        self.jump_sound = pygame.mixer.Sound('assets/audio/effects/jump.wav')

        # Dust Particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15

        # Movement
        self.direction = pygame.math.Vector2(0, 0)
        self.grav = 0.8
        self.jump_speed = -16
        self.speed = 6

        # Status
        self.status = 'idle'
        self.facing_right = True
        self.isgrounded = False
        self.walljump = False
        self.shouldfall = True
        self.candash = True

    def import_character_animations(self):
        character_path = 'assets/player/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'slide': [], 'dash': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        if self.isgrounded:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        else:
            self.rect = self.image.get_rect(center=self.rect.center)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('assets/player/dust_particles/run/')

    def run_dust_anim(self):
        if self.status == 'run' and self.isgrounded:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)

            elif not self.facing_right:
                pos = self.rect.bottomright - pygame.Vector2(0, 10)
                self.display_surface.blit(dust_particle, pos)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True

        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False

        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            if self.isgrounded and self.walljump:
                self.jump()
                self.create_jump_particles(self.rect.midbottom)

            elif self.isgrounded and not self.walljump:
                self.jump()
                self.create_jump_particles(self.rect.midbottom)

            elif self.walljump and not self.isgrounded:
                self.wall_jump()

        if keys[pygame.K_LSHIFT] and keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            if self.candash:
                self.candash = False
                self.direction.y = -15
                self.speed = 15

        elif keys[pygame.K_LSHIFT] and keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            if self.candash:
                self.candash = False
                self.direction.y = -15
                self.speed = 15

        elif keys[pygame.K_LSHIFT] and keys[pygame.K_UP]:
            if self.candash:
                self.candash = False
                self.direction.y = -15

        elif keys[pygame.K_LSHIFT] and keys[pygame.K_DOWN]:
            if self.candash:
                self.candash = False
                self.direction.y = 15

        elif keys[pygame.K_LSHIFT] and keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            if self.candash:
                self.candash = False
                self.direction.y = 15
                self.speed = 20

        elif keys[pygame.K_LSHIFT] and keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            if self.candash:
                self.candash = False
                self.direction.y = 15
                self.speed = 20

        elif keys[pygame.K_LSHIFT] and keys[pygame.K_RIGHT]:
            if self.candash:
                self.candash = False
                self.direction.y = 0
                self.speed = 15

        elif keys[pygame.K_LSHIFT] and keys[pygame.K_LEFT]:
            if self.candash:
                self.candash = False
                self.direction.y = 0
                self.speed = 15

    def apply_gravity(self):
        if self.shouldfall:
            self.direction.y += self.grav
            self.rect.y += self.direction.y

        if self.direction.y > 10:
            self.direction.y = 10

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 3:
            self.status = 'fall'
        elif self.direction.x != 0 and self.direction.y == 0:
            self.status = 'run'
        elif self.direction.x == 0 and self.direction.y == 0:
            self.status = 'idle'

        if self.walljump:
            self.status = 'slide'

    def checkdash(self):
        if not self.candash and self.speed != 6:
            self.status = 'dash'

    def jump(self):
        if self.isgrounded:
            self.direction.y = self.jump_speed
            self.jump_sound.play()
            self.isgrounded = False

    def wall_jump(self):
        if self.walljump:
            self.direction.y = self.jump_speed * 0.75
            self.walljump = False

    def update(self):
        self.get_input()
        self.rect.x += (self.direction.x * self.speed)
        self.get_status()
        self.checkdash()
        self.animate()
        self.run_dust_anim()
