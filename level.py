import pygame
from player import Player
from support import import_csv_layout
from tile import *
from game_data import get_terrain
from particles import ParticleEffect
from enemy import Enemy


class Level:
    def __init__(self, level_data, level_num, surface):
        super().__init__()

        self.enemy_hit_sound = pygame.mixer.Sound('assets/audio/effects/stomp.wav')
        self.player_hit_sound = pygame.mixer.Sound('assets/audio/effects/hit.wav')

        self.level_num = level_num
        self.display_surface = surface
        self.world_shift = 0
        self.total_world_shift = 0

        self.sky = pygame.image.load('assets/sky/sky.png').convert_alpha()

        self.player_spawn = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.setup_player(self.player_spawn)

        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        enemy_layout = import_csv_layout(level_data['enemy'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemy')

        constraints = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraints, 'constraints')

        spike_layout = import_csv_layout(level_data['spikes'])
        self.spike_sprites = self.create_tile_group(spike_layout, 'spikes')

        self.player_max_health = 100
        self.player_current_health = 100

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_isgrounded = False

        # explosion
        self.explosion_anim = pygame.sprite.Group()

        # invincibility frames
        self.invincible = False
        self.invinciblity_duration = 500
        self.hurt_time = 0

    def get_player_on_ground(self):
        if self.player.sprite.isgrounded:
            self.player_isgrounded = True
        else:
            self.player_isgrounded = False

    def create_landing_dust(self):
        if not self.player_isgrounded and self.player.sprite.isgrounded and not self.dust_sprite.sprites():
            offset = pygame.math.Vector2(0, 10)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def create_jump_particles(self, pos):
        jump_particle_effect = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_effect)

    def create_tile_group(self, layout, _type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1' and val != 'P':
                    x = col_index * 48
                    y = row_index * 48

                    if _type == 'terrain':
                        if val == '1':
                            sprite = Bridge(x, y, get_terrain(val, self.level_num))
                            sprite_group.add(sprite)
                            continue
                        sprite = Terrain(48, x, y, get_terrain(val, self.level_num))
                        sprite_group.add(sprite)

                    elif _type == 'grass':
                        sprite = Terrain(48, x, y, get_terrain(7, self.level_num))
                        sprite_group.add(sprite)

                    elif _type == 'enemy':
                        sprite = Enemy(48, x, y)
                        sprite_group.add(sprite)

                    elif _type == 'constraints':
                        sprite = Tile(64, x, y)
                        sprite_group.add(sprite)

                    elif _type == 'spikes':
                        sprite = Spike(48, x, y, val)
                        sprite_group.add(sprite)

        return sprite_group

    def setup_player(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = 48 * col_index
                y = 48 * row_index

                if val == '2':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)

                elif val == '3':
                    goal_surface = pygame.image.load('assets/level_art/flag/flag.png').convert_alpha()
                    sprite = Goal(192, x, y, goal_surface)
                    self.goal.add(sprite)

    def enemy_collision(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse_speed()

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < 550 and direction_x < 0:
            self.world_shift = 8
            self.total_world_shift += self.world_shift
            player.speed = 0
        elif player_x > 850 and direction_x > 0:
            self.world_shift = -8
            self.total_world_shift += self.world_shift
            player.speed = 0
        else:
            self.world_shift = 0
            if player.speed > 6:
                player.speed -= 0.5

            else:
                player.speed = 6

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        player.shouldfall = True

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.direction.x = 0
                    player.walljump = True
                    player.shouldfall = False
                    if player.direction.y != 0:
                        player.rect.y += 1

                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.direction.x = 0
                    player.walljump = True
                    player.shouldfall = False
                    if player.direction.y != 0:
                        player.rect.y += 1

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom + 1
                    player.direction.y = 0
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.isgrounded = True
                    player.walljump = False
                    player.candash = True

    def check_enemy_collision(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y *= -2
                    explosion_sprite = ParticleEffect(enemy.rect.center, 'explosion')
                    self.explosion_anim.add(explosion_sprite)
                    enemy.kill()
                    self.enemy_hit_sound.play()

                else:
                    self.give_dmg(10)

    def check_spike_collision(self):
        spike_collisions = pygame.sprite.spritecollide(self.player.sprite, self.spike_sprites, False)

        if spike_collisions:
            self.give_dmg(10)

    def give_dmg(self, hp):
        if not self.invincible:
            self.player_current_health -= hp
            self.invincible = True
            self.player_hit_sound.play()
            self.hurt_time = pygame.time.get_ticks()

    def i_frame_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invinciblity_duration:
                self.invincible = False

    def check_living_status(self):
        if self.player_current_health <= 0:
            return False

        else:
            return True

    def check_end(self):
        if self.player.sprite.rect.colliderect(self.goal.sprite.rect):
            return True
        else:
            return False

    def check_void_death(self):
        if self.player.sprite.rect.top > 1000:
            return True

    def run(self):

        self.display_surface.blit(self.sky, (0, 0))

        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision()
        self.check_spike_collision()
        self.enemy_sprites.draw(self.display_surface)
        self.spike_sprites.update(self.world_shift)
        self.spike_sprites.draw(self.display_surface)

        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.scroll_x()

        # dust
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.i_frame_timer()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.check_enemy_collision()
        self.explosion_anim.update(self.world_shift)
        self.explosion_anim.draw(self.display_surface)
        self.player.draw(self.display_surface)
