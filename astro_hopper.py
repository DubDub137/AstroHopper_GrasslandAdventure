import pygame
from sys import exit
from math import ceil
from random import randint, choice
from time import sleep


class Alien(pygame.sprite.Sprite):
    """Class representing an alien object in the game."""
    def __init__(self, kind):
        """
        Initializes the alien object.

        Parameters:
        - kind: a list or a tuple containing images representing the alien's walking animation (kind[0], kind[1])
                and the image representing the alien's jump (kind[2]).
        """
        super().__init__()

        self.alien_walk = [kind[0], kind[1]]
        self.alien_index = 0
        self.alien_jump = kind[2]
        self.alien_hurt = kind[3]

        self.image = self.alien_walk[self.alien_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = jump_sound
        self.jump_sound.set_volume(0.3)

    def player_input(self):
        """
        Handles player input for the alien.
        Checks if the Space key is pressed and if the alien is on the ground.
        If so, sets the gravity value to -20 and plays the jump sound.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        """
        Applies gravity force to the alien.
        Increases the gravity value, updates the alien's position on the Y-axis.
        Checks if the alien is on the ground and sets it at the appropriate height.
        """
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        """
        Determines the current animation state of the alien based on its position.
        If the alien is in the air, sets the jump image.
        Otherwise, updates the animation index for the walking animation
        and sets the corresponding walking image.
        """
        if self.rect.bottom < 300:
            self.image = self.alien_jump
        else:
            self.alien_index += 0.1
            if self.alien_index >= len(self.alien_walk):
                self.alien_index = 0
            self.image = self.alien_walk[int(self.alien_index)]

    def update(self):
        """
        Updates the state of the alien.
        Calls the methods responsible for input handling, gravity, and animation state.
        """
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Enemy(pygame.sprite.Sprite):
    """Class representing an enemy object in the game."""
    def __init__(self, type):
        """
        Initializes the enemy object.

        Parameters:
        - type: The type of the enemy character ('bee', 'mouse', 'ladybug', 'frog').
        """
        super().__init__()

        # Dictionary with animation speeds for each enemy type
        animation_speed = {
            'bee': 0.15,
            'mouse': 0.04,
            'ladybug': 0.03,
            'frog': 0.02
        }

        if type == 'bee':
            # Load bee animation frames
            bee_1 = pygame.image.load('graphics/enemy/bee1.png').convert_alpha()
            bee_2 = pygame.image.load('graphics/enemy/bee2.png').convert_alpha()
            self.frames = [bee_1, bee_2]
            y_pos = 200
            self.is_jumping = False
            self.is_jumping_n_flying = False
            self.animation_speed = animation_speed['bee']

        elif type == 'mouse':
            # Load mouse animation frames
            mouse_1 = pygame.image.load('graphics/enemy/mouse1.png').convert_alpha()
            mouse_2 = pygame.image.load('graphics/enemy/mouse2.png').convert_alpha()
            self.frames = [mouse_1, mouse_2]
            y_pos = 300
            self.is_jumping = False
            self.is_jumping_n_flying = False
            self.animation_speed = animation_speed['mouse']
            
        elif type == 'ladybug':
            # Load ladybug animation frames
            ladybug_1 = pygame.image.load('graphics/enemy/ladybug1.png').convert_alpha()
            ladybug_2 = pygame.image.load('graphics/enemy/ladybug2.png').convert_alpha()
            ladybug_fly = pygame.image.load('graphics/enemy/ladybug_fly.png').convert_alpha()
            self.frames = [ladybug_1, ladybug_2, ladybug_fly]
            y_pos = 300
            y_fly = 230
            self.pos = [y_pos, y_fly]
            self.is_jumping = False
            self.is_jumping_n_flying = True
            self.animation_speed = animation_speed['ladybug']
        else:
            # Load frog animation frames
            frog_1 = pygame.image.load('graphics/enemy/frog1.png').convert_alpha()
            frog_2 = pygame.image.load('graphics/enemy/frog2.png').convert_alpha()
            self.frames = [frog_1, frog_2]
            y_pos = 300
            y_jump = 270
            self.pos = [y_pos, y_jump]
            self.is_jumping = True
            self.is_jumping_n_flying = False
            self.animation_speed = animation_speed['frog']

        # Initializing animation index, image, and rectangle position
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        """ Updates the animation state of the enemy object based on its type."""
        self.animation_index += self.animation_speed

        # Frog animation
        if self.is_jumping:
            if self.animation_index >= len(self.frames):
                self.animation_index = 0
            if 0 <= self.animation_index < 1:
                # Set the image and position for the first frame of frog animation
                self.image = self.frames[int(self.animation_index)]
                self.rect.bottom = self.pos[0]
            elif 1 <= self.animation_index < 2:
                # Set the image and position for the second frame of frog animation
                self.image = self.frames[int(self.animation_index)]
                self.rect.bottom = self.pos[1]
                self.rect.x -= 0.1

        # Ladybug animation
        elif self.is_jumping_n_flying:
            if self.animation_index >= len(self.frames):
                self.animation_index = 0
            if 0 <= self.animation_index < 2:
                # Set the image and position for the first two frames of ladybug animation
                self.image = self.frames[int(self.animation_index)]
                self.rect.bottom = self.pos[0]
            elif 2 <= self.animation_index < 3:
                # Set the image and position for the third frame of ladybug animation
                self.image = self.frames[int(self.animation_index)]
                self.rect.bottom = self.pos[1]
                self.rect.x -= 1

        # Bee and mouse animation
        else:
            if self.animation_index >= len(self.frames):
                self.animation_index = 0
            # Set the image based on the current animation index
            self.image = self.frames[int(self.animation_index)]

    def update(self):
        """Updates the position and animation of the enemy object."""
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        """Checks if the enemy object is off the screen and destroys it."""
        if self.rect.x <= -100:
            self.kill()


def selecting_alien(color):
    """Loading images for the chosen alien"""
    if color == 'blue':
        blue_walk1 = pygame.image.load('graphics/player/blue_alien/blue_walk1.png').convert_alpha()
        blue_walk2 = pygame.image.load('graphics/player/blue_alien/blue_walk2.png').convert_alpha()
        blue_jump = pygame.image.load('graphics/player/blue_alien/blue_jump.png').convert_alpha()
        blue_hurt = pygame.image.load('graphics/player/blue_alien/blue_hurt.png').convert_alpha()

        return blue_walk1, blue_walk2, blue_jump, blue_hurt

    elif color == 'pink':
        pink_walk1 = pygame.image.load('graphics/player/pink_alien/pink_walk1.png').convert_alpha()
        pink_walk2 = pygame.image.load('graphics/player/pink_alien/pink_walk2.png').convert_alpha()
        pink_jump = pygame.image.load('graphics/player/pink_alien/pink_jump.png').convert_alpha()
        pink_hurt = pygame.image.load('graphics/player/pink_alien/pink_hurt.png').convert_alpha()

        return pink_walk1, pink_walk2, pink_jump, pink_hurt

    else:
        yellow_walk1 = pygame.image.load('graphics/player/yellow_alien/yellow_walk1.png').convert_alpha()
        yellow_walk2 = pygame.image.load('graphics/player/yellow_alien/yellow_walk2.png').convert_alpha()
        yellow_jump = pygame.image.load('graphics/player/yellow_alien/yellow_jump.png').convert_alpha()
        yellow_hurt = pygame.image.load('graphics/player/yellow_alien/yellow_hurt.png').convert_alpha()

        return yellow_walk1, yellow_walk2, yellow_jump, yellow_hurt


def display_score():
    """Displaying the amount of time the alien managed to stay alive"""
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = game_font.render(f'Score: {current_time}', False, (16, 183, 100))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time


def collision_sprite():
    """
    Checks for collisions between the alien sprite and enemy sprites.
    If a collision occurs, performs appropriate actions and returns False.
    Otherwise, returns True.
    Later in the code, when "return False" is encountered,
    it sets the game_active state to False.
    Similarly, when "return True" is encountered,
    it sets the game_active state to True.
    """
    if pygame.sprite.spritecollide(alien.sprite, enemy_group, False):

        bg_music.stop()

        # Updating the alien image to 'alien_hurt'
        alien.sprite.image = alien.sprite.alien_hurt

        # Redrawing the alien and the enemies on the screen
        alien.draw(screen)
        enemy_group.draw(screen)

        pygame.display.update()

        game_over_music.play()
        game_over_music.set_volume(0.3)
        sleep(2)
        enemy_group.empty()
        intro_music.play(loops=-1)
        intro_music.set_volume(0.5)
        return False
    else:
        return True


# Initializing sub-parts of Pygame
pygame.init()

# Creating an icon, a game title and a font
icon_image = pygame.image.load('graphics/icon/icon.png')
pygame.display.set_icon(icon_image)
pygame.display.set_caption("Astro Hopper: Grassland Adventure")
game_font = pygame.font.Font('fonts/font1/public_pixel.ttf', 30)

# Creating a display surface and surfaces for background
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
sky_surface = pygame.image.load('graphics/background/sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/background/ground.png').convert_alpha()

# Parameters for creating the scrolling background
sky_scroll = 0
ground_scroll = 0
sky_width = sky_surface.get_width()
ground_width = ground_surface.get_width()
sky_tiles = ceil(screen_width / sky_width) + 1  # We are increasing it by 1 to ensure smooth background scrolling.
ground_tiles = ceil((screen_width / ground_width)) + 1

# Creating an intro screen
blue_alien_stand = pygame.image.load('graphics/player/blue_alien/blue_stand.png').convert_alpha()
pink_alien_stand = pygame.image.load('graphics/player/pink_alien/pink_stand.png').convert_alpha()
yellow_alien_stand = pygame.image.load('graphics/player/yellow_alien/yellow_stand.png').convert_alpha()

blue_stand_rect = blue_alien_stand.get_rect(center=(200, 200))
pink_stand_rect = pink_alien_stand.get_rect(center=(400, 200))
yellow_stand_rect = yellow_alien_stand.get_rect(center=(600, 200))

alien_list = [blue_stand_rect, pink_stand_rect, yellow_stand_rect]

game_name1 = game_font.render("Astro Hopper:", False, (61, 81, 74))
game_name2 = game_font.render("Grassland Adventure", False, (16, 183, 128))
game_name_rect1 = game_name1.get_rect(center=(400, 40))
game_name_rect2 = game_name2.get_rect(center=(400, 80))

game_message = game_font.render("Choose your character", False, (224, 224, 224))
game_message_rect = game_message.get_rect(center=(400, 320))

# Uploading music and sounds
intro_music = pygame.mixer.Sound('audio/opening_music.ogg')
bg_music = pygame.mixer.Sound('audio/background_music.mp3')
jump_sound = pygame.mixer.Sound('audio/jump.mp3')
game_over_music = pygame.mixer.Sound('audio/game_over.wav')

# Initial parameters for the game
game_active = False
start_time = 0
score = 0
score_list = [0]
best_score = 0
intro_music.play(loops=-1)
intro_music.set_volume(0.5)

# Groups
alien = pygame.sprite.GroupSingle()
enemy_group = pygame.sprite.Group()

# Creating a clock object to call it in the while loop
# that way our game is not going to run too fast
clock = pygame.time.Clock()

# Creating a timer for spawning different types of enemies
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)

while True:
    # Creating an event for closing the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == enemy_timer:
                # Creating an instance of the Enemy class with a randomly selected type
                # and adding it to the enemy_group
                enemy_group.add(Enemy(choice(['bee', 'ladybug', 'mouse', 'mouse', 'frog'])))
        else:
            # Checking which alien character the player chooses,
            # then creating an instance of the Alien class for it
            # and adding it to the alien group (which holds a single sprite)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if alien_list[0].collidepoint(event.pos):
                    alien_images = selecting_alien('blue')
                elif alien_list[1].collidepoint(event.pos):
                    alien_images = selecting_alien('pink')
                else:
                    alien_images = selecting_alien('yellow')
                alien.add(Alien(alien_images))

                # Modifying game parameters
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                intro_music.stop()
                bg_music.play(loops=-1)
                bg_music.set_volume(0.2)

    if game_active:
        # Drawing scrolling background
        for i in range(0, sky_tiles):
            screen.blit(sky_surface, (i * sky_width + sky_scroll, 0))
        for i in range(0, ground_tiles):
            screen.blit(ground_surface, (i * ground_width + ground_scroll, 300))

        # The speed of scrolling
        sky_scroll -= 1
        ground_scroll -= 3

        # Resetting scrolling
        if abs(sky_scroll) > sky_width:
            sky_scroll = 0
        if abs(ground_scroll) > ground_width:
            ground_scroll = 0

        # Showing the current value of the score
        score = display_score()

        # Collision
        game_active = collision_sprite()

        # Displaying aliens and enemies on the screen
        alien.draw(screen)
        alien.update()

        enemy_group.draw(screen)
        enemy_group.update()

    else:
        # Filling the screen with a specific color
        screen.fill((0, 153, 153))

        # Displaying 3 types of aliens on the screen
        screen.blit(blue_alien_stand, blue_stand_rect)
        screen.blit(pink_alien_stand, pink_stand_rect)
        screen.blit(yellow_alien_stand, yellow_stand_rect)

        # Rendering and setting the positions of messages
        game_over_message = game_font.render("GAME OVER", False, (61, 81, 74))
        game_over_message_rect = game_over_message.get_rect(center=(400, 30))
        best_score_message = game_font.render(f'Your best score: {best_score}', False, (16, 183, 128))
        best_score_message_rect = best_score_message.get_rect(center=(400, 70))
        score_message = game_font.render(f'Your last score: {score}', False, (16, 183, 128))
        score_message_rect = score_message.get_rect(center=(400, 110))
        its_best_score_message = game_font.render(f"It's your best score: {score} !", False, (16, 183, 128))
        its_best_score_message_rect = its_best_score_message.get_rect(center=(400, 90))

        if score == 0:
            # Displaying intro messages
            screen.blit(game_name1, game_name_rect1)
            screen.blit(game_name2, game_name_rect2)
            screen.blit(game_message, game_message_rect)
        else:
            if score == max(score_list):
                # Displaying messages when it's the player's best score
                screen.blit(game_over_message, game_over_message_rect)
                screen.blit(its_best_score_message, its_best_score_message_rect)
                screen.blit(game_message, game_message_rect)
            else:
                if score > max(score_list):
                    score_list.append(score)
                best_score = max(score_list)

                # Displaying messages about the best and current score
                screen.blit(game_over_message, game_over_message_rect)
                screen.blit(best_score_message, best_score_message_rect)
                screen.blit(score_message, score_message_rect)
                screen.blit(game_message, game_message_rect)

    # Updating the display surface
    pygame.display.update()
    clock.tick(60)
