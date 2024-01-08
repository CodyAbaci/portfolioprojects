# main.py

import pygame
import os
from npc_module import Goblin, Slayer
from ui_module import draw_character_sheet, set_screen_width

# Initialize Pygame
pygame.init()

# Set the dimensions of the screen
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the screen width for ui_module
set_screen_width(SCREEN_WIDTH)

# Load the "Press Start 2P" font
FONT_FILENAME = "font.ttf"
FONT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), FONT_FILENAME))
press_start_font = pygame.font.Font(FONT_PATH, 20)

# Load the sprites
sprite_sheet = pygame.image.load(os.path.join(os.path.dirname(__file__), "dungeontiles.png"))

# Define the coordinates and dimensions of each sprite
floor_tile = (32, 96, 32, 32)

# Define the desired display size
DISPLAY_SIZE = (64, 64)

# Define the size of the room
ROOM_WIDTH = 16
ROOM_HEIGHT = 16

# Create a 2D list to represent the room layout
room_layout = [[floor_tile for _ in range(ROOM_WIDTH)] for _ in range(ROOM_HEIGHT)]

# Load player sprites
wizard_sprites = [pygame.image.load(os.path.join(os.path.dirname(__file__), "wiz.png")),
                  pygame.image.load(os.path.join(os.path.dirname(__file__), "wiz2.png"))]

# Resize the player sprites to 64x64 pixels
wizard_sprites = [pygame.transform.scale(sprite, DISPLAY_SIZE) for sprite in wizard_sprites]

# Create player object
class Player:
    def __init__(self, position):
        self.position = position

    def update(self, current_frame):
        return wizard_sprites[current_frame // 100 % len(wizard_sprites)]

# Create player instance
player = Player((2, 2))

# Create NPC instances
goblin = Goblin((8, 8))
slayer = Slayer((5, 5))

# Constants for movement and turns
MAX_PLAYER_MOVEMENT = 5
MAX_NPC_MOVEMENT = 1

# Additional variables to keep track of player's movement and turns
remaining_player_movement = MAX_PLAYER_MOVEMENT
current_turn = "player"  # Can be "player" or "npc"
selected_option = 0  # Default selection is the first option
movement_steps = 0  # Number of tiles the player has moved in the current movement action

# Main game loop
running = True
clock = pygame.time.Clock()

mode = 'menu' 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            print(event.type, event.key, current_turn, mode)
            if current_turn == "player" and mode == 'movement':
                if event.key == pygame.K_UP:
                    if remaining_player_movement > 0:
                        player.position = (player.position[0], max(player.position[1] - 1, 0))
                        remaining_player_movement -= 1
                elif event.key == pygame.K_DOWN:
                    if remaining_player_movement > 0:
                        player.position = (player.position[0], min(player.position[1] + 1, ROOM_HEIGHT - 1))
                        remaining_player_movement -= 1
                elif event.key == pygame.K_LEFT:
                    if remaining_player_movement > 0:
                        player.position = (max(player.position[0] - 1, 0), player.position[1])
                        remaining_player_movement -= 1
                elif event.key == pygame.K_RIGHT:
                    if remaining_player_movement > 0:
                        player.position = (min(player.position[0] + 1, ROOM_WIDTH - 1), player.position[1])
                        remaining_player_movement -= 1
                
            if event.key == pygame.K_SPACE:
                # Spacebar advances the menu by 1
                selected_option = (selected_option + 1) % 4
            elif event.key == pygame.K_RETURN:
                # Enter key selects the menu item
                print("Selected option:", selected_option)
                print("Current turn:", current_turn)
                if selected_option == 0:
                    print("Mode set to movement")
                    mode = 'movement'
                if selected_option == 1:
                    print("Mode set to attack")
                    # Attack code here
                if selected_option == 3:
                    # End Turn selected
                    current_turn = "npc"  # Switch to NPC turn
                    remaining_player_movement = MAX_PLAYER_MOVEMENT  # Reset movement for the next turn

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the room
    for y in range(ROOM_HEIGHT):
        for x in range(ROOM_WIDTH):
            sprite_rect = pygame.Rect(x * DISPLAY_SIZE[0], y * DISPLAY_SIZE[1], DISPLAY_SIZE[0], DISPLAY_SIZE[1])
            screen.blit(pygame.transform.scale(sprite_sheet.subsurface(floor_tile), DISPLAY_SIZE), sprite_rect)

    # Update the current frame based on time
    current_frame = pygame.time.get_ticks() - clock.get_rawtime()

    # Draw characters
    # Draw wizard at (2, 2)
    wizard_rect = pygame.Rect(player.position[0] * DISPLAY_SIZE[0], player.position[1] * DISPLAY_SIZE[1], DISPLAY_SIZE[0], DISPLAY_SIZE[1])
    screen.blit(player.update(current_frame), wizard_rect)

    # Draw goblin at (8, 8)
    goblin_rect = pygame.Rect(goblin.position[0] * DISPLAY_SIZE[0], goblin.position[1] * DISPLAY_SIZE[1], DISPLAY_SIZE[0], DISPLAY_SIZE[1])
    screen.blit(goblin.update(current_frame), goblin_rect)

    # Draw slayer at (5, 5)
    slayer_rect = pygame.Rect(slayer.position[0] * DISPLAY_SIZE[0], slayer.position[1] * DISPLAY_SIZE[1], DISPLAY_SIZE[0], DISPLAY_SIZE[1])
    screen.blit(slayer.update(current_frame), slayer_rect)

    # Draw the character sheet UI
    draw_character_sheet(screen, selected_option, {"moves": remaining_player_movement})

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

    # Handle NPC turns
    if current_turn == "npc":
        for npc in [goblin, slayer]:
            # NPC movement logic (move one tile per turn)
            npc.move_random(ROOM_WIDTH, ROOM_HEIGHT)
        current_turn = "player"  # Switch back to player turn
