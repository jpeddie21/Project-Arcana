"""
Jonathan Pedernera
PROJECT ARCANA Version 0.8

RULES:
Press the arrow keys to move.
Press the Z key to cast regular spells.
Press the X key to cast a bomb that destroys all enemies on screen.
Shoot enemies with spells to get points and survive.
Do not collide with enemies or you lose a life.

KNOWN BUGS:
Enemies will spawn on top of each other and overlap

TODOS:
- Add collision so enemy blocks do not spawn on top of each other.
"""

import pygame
import random
from classes import globals
from classes import blocks
from classes import player
from classes import player_bullets
from classes import enemy_bullets
from classes import explosions


class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    # Sprite lists
    block_list = None
    all_sprites_list = None
    player_bullet_list = None
    player_bullet = None
    enemy_bullet_list = None
    enemy_bullet = None
    explosion_list = None
    player_list = None

    # Boolean values
    game_over = False
    game_start = False
    feedback = False
    collision = True
    invulnerable = False

    # Integer values
    score = 0
    enemy_count = 0
    lives = 0
    bomb_count = 0
    enemy_defeats = 0
    collision_time = 0

    def __init__(self):
        """ Constructor of the game class. """

        # Boolean values
        self.game_over = False
        self.game_start = False
        self.feedback = False
        self.collision = True
        self.invulnerable = False

        # Integer values
        self.score = 0
        self.lives = 5
        self.bomb_count = 3
        self.enemy_defeats = 0
        self.enemy_count = 0
        self.collision_time = 0

        # Create sprite lists
        self.block_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.player_bullet_list = pygame.sprite.Group()
        self.enemy_bullet_list = pygame.sprite.Group()
        self.explosion_list = pygame.sprite.Group()
        self.player_list = pygame.sprite.Group()

        # Load the sound clip
        self.bullet_sound = pygame.mixer.Sound("audio/player_spell_sound.wav")
        pygame.mixer.Sound.set_volume(self.bullet_sound, 0.25)
        self.bomb_sound = pygame.mixer.Sound("audio/bomb_spell.ogg")
        pygame.mixer.Sound.set_volume(self.bomb_sound, 0.2)
        self.enemy_defeat = pygame.mixer.Sound("audio/enemy_defeat.wav")
        pygame.mixer.Sound.set_volume(self.enemy_defeat, 0.15)
        self.lost_life = pygame.mixer.Sound("audio/lost_life.wav")
        pygame.mixer.Sound.set_volume(self.lost_life, 0.25)

        # Load the music
        pygame.mixer.music.load("audio/game_bgm.mp3")
        pygame.mixer.music.set_volume(0.15)
        pygame.mixer.music.play(-1)

        # Timer for enemy shooting
        self.timer_shoot = 3000
        self.shoot_event = pygame.USEREVENT
        pygame.time.set_timer(self.shoot_event, self.timer_shoot)

        # Timer for enemy spawning
        self.timer_spawn = 750
        self.spawn_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_event, self.timer_spawn)

        # Create the player
        self.player = player.Player(350, 800)
        self.player_list.add(self.player)
        self.all_sprites_list.add(self.player)

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            # Changes the title screen to the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_start = True
                    self.feedback = True
                    if self.game_over:
                        self.__init__()

            if (self.game_over is False) and (self.game_start is True):

                # Set the speed based on the key pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.change_speed(-4, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.player.change_speed(4, 0)
                    elif event.key == pygame.K_UP:
                        self.player.change_speed(0, -4)
                    elif event.key == pygame.K_DOWN:
                        self.player.change_speed(0, 4)

                    # Fire a bullet if the user clicks the mouse button
                    elif event.key == pygame.K_z:
                        self.player_shoot()

                    # Uses a bomb spell, removing all enemies from the screen.
                    elif event.key == pygame.K_x:
                        self.bomb_cast()

                    """ debug statements
                    elif event.key == pygame.K_ESCAPE:
                        # self.game_over = True
                    elif event.key == pygame.K_s:
                        self.bomb_count += 1 """

                # Reset speed when key goes up
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.change_speed(4, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.player.change_speed(-4, 0)
                    elif event.key == pygame.K_UP:
                        self.player.change_speed(0, 4)
                    elif event.key == pygame.K_DOWN:
                        self.player.change_speed(0, -4)

                # Timer events for enemy shooting
                if event.type == self.shoot_event:
                    self.enemy_shoot()
                if event.type == self.spawn_event:
                    self.spawn_enemy()

                # Update the position of the player
                self.player.update()

        return False

    def run_logic(self):
        """ This method is run each time through the frame. It
        updates positions and checks for collisions. """

        if (self.game_over is False) and (self.game_start is True):

            self.all_sprites_list.update()

            if pygame.time.get_ticks() - self.collision_time > 1000:
                self.invulnerable = False
                self.block_player_collision()
                self.bullet_player_collision()

            self.bullet_block_collision()

            self.bomb_replenish()

            if self.lives <= 0:
                self.game_over = True

    def spawn_enemy(self):
        """ Spawns enemy to a maximum of 15 enemies. """

        block = blocks.Block()

        block.rect.x = random.randrange(20, globals.SCREEN_WIDTH - 60)
        block.rect.y = random.randrange(-300, 0)

        self.block_list.add(block)
        self.all_sprites_list.add(block)

    def enemy_shoot(self):
        """ Spawns the bullets the enemy shoots. """
        for block in self.block_list:
            if block.shoot_num == random.randint(0, 4) and block.rect.y < 700:
                self.enemy_bullet = enemy_bullets.Bullet()
                # Set the bullet so it is where the player is
                self.enemy_bullet.rect.x = (block.rect.x + 10)
                self.enemy_bullet.rect.y = block.rect.y
                # Add the bullet to the lists
                self.all_sprites_list.add(self.enemy_bullet)
                self.enemy_bullet_list.add(self.enemy_bullet)

    def player_shoot(self):
        self.player_bullet = player_bullets.Bullet()
        # Set the bullet so it is where the player is
        self.player_bullet.rect.x = (self.player.rect.x + 20)
        self.player_bullet.rect.y = self.player.rect.y
        # Add the bullet to the lists
        self.all_sprites_list.add(self.player_bullet)
        self.player_bullet_list.add(self.player_bullet)
        self.bullet_sound.play()

    def block_player_collision(self):
        """ Detects collision between enemies and the player. """

        # See if the player block has collided with anything.
        blocks_hit_list = pygame.sprite.spritecollide(self.player, self.block_list, True)

        # Check the list of collisions
        if self.collision is True:
            for _ in blocks_hit_list:
                self.lives -= 1
                self.enemy_count -= 1
                self.invulnerable = True
                self.collision_time = pygame.time.get_ticks()
                self.lost_life.play()

    def bullet_block_collision(self):
        """ Detects collision between the enemies and player bullets. """

        # Calculate mechanics for each bullet
        for self.player_bullet in self.player_bullet_list:
            # See if it hit a block
            block_hit_list = pygame.sprite.spritecollide(self.player_bullet, self.block_list, True)

            # For each block hit, remove the bullet and add to the score
            for block in block_hit_list:
                self.player_bullet_list.remove(self.player_bullet)
                self.all_sprites_list.remove(self.player_bullet)
                self.score += 100
                self.enemy_defeats += 1
                self.enemy_count += 1
                self.enemy_defeat.play()
                self.draw_explosion(block)

            if self.enemy_count >= 50:
                if self.timer_spawn > 250:
                    self.timer_spawn -= 50
                if self.timer_shoot > 500:
                    self.timer_shoot -= 250
                self.enemy_count = 0

    def bullet_player_collision(self):
        """ Detects collision between the player and enemy bullets. """

        for self.enemy_bullet in self.enemy_bullet_list:

            player_hit_list = pygame.sprite.spritecollide(self.player, self.enemy_bullet_list, True)

            if self.collision is True:
                for _ in player_hit_list:
                    self.lives -= 1
                    self.invulnerable = True
                    self.collision_time = pygame.get_ticks()
                    self.lost_life.play()

    def bomb_cast(self):
        """ Removes all enemies and player bullets from the screen. """

        if self.bomb_count != 0:
            self.bomb_count -= 1
            if self.bullet_sound.play() is True:
                self.bullet_sound.stop()
            self.bomb_sound.play()
            for self.player_bullet in self.player_bullet_list:
                self.player_bullet_list.remove(self.player_bullet)
                self.all_sprites_list.remove(self.player_bullet)
            for self.enemy_bullet in self.enemy_bullet_list:
                self.enemy_bullet_list.remove(self.enemy_bullet)
                self.all_sprites_list.remove(self.enemy_bullet)
            for block in self.block_list:
                if block.rect.y > -40:
                    self.block_list.remove(block)
                    self.all_sprites_list.remove(block)
                    self.enemy_count -= 1
                    self.enemy_defeats += 1
                    self.score += 100
                    self.draw_explosion(block)

    def bomb_replenish(self):
        """ Gain another bomb from reaching a certain number of enemy defeats. """

        if self.enemy_defeats >= 100 and self.bomb_count <= 3:
            self.bomb_count += 1
            self.enemy_defeats = 0

    def draw_explosion(self, block):
        """ Creates and draws the explosions sprites. """

        expl = explosions.Explosion(block.rect.x + 20, block.rect.y + 20)
        self.all_sprites_list.add(expl)

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """

        # Declare font type and size
        serif = pygame.font.SysFont("serif", 30)
        serif_bold = pygame.font.SysFont("serif", 50, bold=pygame.font.Font.bold)

        # Text statements
        text_restart = serif.render("Game Over, press RETURN to restart.", True, globals.BLACK)
        text_score = serif.render("Your score was: " + str(self.score), True, globals.BLACK)
        text_start = serif_bold.render("Project Arcana", True, globals.BLACK)
        text_press_enter = serif.render("Press RETURN to start", True, globals.BLACK)
        text_name = serif.render("by Jonathan Pedernera", True, globals.BLACK)

        center_x = (globals.SCREEN_WIDTH // 2) - (text_restart.get_width() // 2)
        center_y = (globals.SCREEN_HEIGHT // 2) - (text_restart.get_height() // 2)

        # Display the game over screen
        if self.game_over:
            self.feedback = False
            screen.blit(text_restart, [center_x, center_y])
            screen.blit(text_score, [center_x, center_y + 40])

        elif not self.game_start:
            screen.blit(text_start, [220, 350])
            screen.blit(text_press_enter, [262, 425])
            screen.blit(text_name, [267, 460])

        if not self.game_over and self.game_start:
            self.all_sprites_list.draw(screen)

        self.display_feedback(screen)

        pygame.display.flip()

    def display_feedback(self, screen):
        """ Displays the game feedback, this being lives, score, and bomb count. """

        if self.feedback:
            pygame.draw.rect(screen, globals.PURPLE, (0, 0, 900, 45), 0)
            font = pygame.font.SysFont('Serif', 20, True, False)
            score_str = font.render("Score: " + str(self.score), True, globals.WHITE)
            bomb_str = font.render("Bombs: " + str(self.bomb_count), True, globals.WHITE)
            live_str = font.render("Lives: " + str(self.lives), True, globals.WHITE)
            screen.blit(score_str, [12, 12])
            screen.blit(bomb_str, [312, 12])
            screen.blit(live_str, [712, 12])


def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()

    size = [globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("PROJECT ARCANA")
    pygame.mouse.set_visible(False)

    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = Game()

    # Main game loop
    while not done:
        screen.blit(globals.background, [0, 0])

        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()

        # Update object positions, check for collisions
        game.run_logic()

        # Draw the current frame
        game.display_frame(screen)

        # Pause for the next frame
        clock.tick(60)

    # Close window and exit
    pygame.quit()


# Call the main function, start up the game
if __name__ == "__main__":
    main()
