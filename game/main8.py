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
wizard_sprites = [
    pygame.image.load(os.path.join(os.path.dirname(__file__), "wiz.png")),
    pygame.image.load(os.path.join(os.path.dirname(__file__), "wiz2.png")),
]

# Resize the player sprites to 64x64 pixels
wizard_sprites = [pygame.transform.scale(sprite, DISPLAY_SIZE) for sprite in wizard_sprites]

# Helper function to get the NPC that was clicked
def get_clicked_npc(mouse_x, mouse_y, npcs):
    for npc in npcs:
        npc_rect = pygame.Rect(
            npc.position[0] * DISPLAY_SIZE[0],
            npc.position[1] * DISPLAY_SIZE[1],
            DISPLAY_SIZE[0],
            DISPLAY_SIZE[1],
        )
        if npc_rect.collidepoint(mouse_x, mouse_y):
            return npc
    return None

# Create player object
class Player:
    def __init__(self, position):
        self.position = position
        self.stamina = 20
        self.health = 100

    def update(self, current_frame):
        return wizard_sprites[current_frame // 100 % len(wizard_sprites)]

    def fireball_attack(self, target):
        if self.stamina >= 10:
            distance = abs(target.position[0] - self.position[0]) + abs(target.position[1] - self.position[1])
            if distance <= 9:
                target.health -= 40
                self.stamina -= 10

    def dagger_attack(self, target):
        if self.stamina >= 5:
            distance = abs(target.position[0] - self.position[0]) + abs(target.position[1] - self.position[1])
            if distance <= 1:
                target.health -= 25
                self.stamina -= 5

# Create player instance
player = Player((2, 2))

# Create a list to store active NPCs
active_npcs = [Goblin((8, 8)), Slayer((5, 5))]

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
attack_initiated = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if current_turn == "player" and mode == 'movement':
                if event.key == pygame.K_UP:
                    if remaining_player_movement > 0:
                        player.position = (player.position[0], max(player.position[1] - 1, 0))
                        remaining_player_movement -= 1
                        movement_steps += 1
                elif event.key == pygame.K_DOWN:
                    if remaining_player_movement > 0:
                        player.position = (player.position[0], min(player.position[1] + 1, ROOM_HEIGHT - 1))
                        remaining_player_movement -= 1
                        movement_steps += 1
                elif event.key == pygame.K_LEFT:
                    if remaining_player_movement > 0:
                        player.position = (max(player.position[0] - 1, 0), player.position[1])
                        remaining_player_movement -= 1
                        movement_steps += 1
                elif event.key == pygame.K_RIGHT:
                    if remaining_player_movement > 0:
                        player.position = (min(player.position[0] + 1, ROOM_WIDTH - 1), player.position[1])
                        remaining_player_movement -= 1
                        movement_steps += 1

            if event.key == pygame.K_SPACE:
                # Spacebar advances the menu by 1
                selected_option = (selected_option + 1) % 6
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:
                    mode = 'movement'
                elif selected_option == 1:
                    # Attack code here
                    pass
                elif selected_option == 2:
                    mode = 'attack'

                    # Check for mouse click during attack mode
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    clicked_npc = get_clicked_npc(mouse_x, mouse_y, active_npcs)

                    if clicked_npc:
                        # Check if the clicked NPC is in range for fireball attack
                        distance = abs(clicked_npc.position[0] - player.position[0]) + abs(clicked_npc.position[1] - player.position[1])
                        if distance <= 9:
                            # Execute fireball attack
                            player.fireball_attack(clicked_npc)
                            mode = 'movement'  # Switch back to movement mode

                            # Check if the NPC is defeated after the attack
                            if clicked_npc.health <= 0:
                                active_npcs.remove(clicked_npc)
                                print(f"{clicked_npc} has been defeated!")

                elif selected_option == 3:
                    mode = 'attack'
                    # Add dagger attack logic here

                    # Check for mouse click during attack mode
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    clicked_npc = get_clicked_npc(mouse_x, mouse_y, active_npcs)

                    if clicked_npc:
                        # Check if the clicked NPC is in range for fireball attack
                        distance = abs(clicked_npc.position[0] - player.position[0]) + abs(clicked_npc.position[1] - player.position[1])
                        if distance <= 1:
                            # Execute dagger attack
                            player.dagger_attack(clicked_npc)
                            print(f"Dagger attack on {clicked_npc} successful!")
                            mode = 'movement'  # Switch back to movement mode

                            # Check if the NPC is defeated after the attack
                            if clicked_npc.health <= 0:
                                active_npcs.remove(clicked_npc)
                                print(f"{clicked_npc} has been defeated!")

                elif selected_option == 5:
                    # End Turn selected
                    current_turn = "npc"  # Switch to NPC turn
                    remaining_player_movement = MAX_PLAYER_MOVEMENT  # Reset movement for the next turn
                    movement_steps = 0  # Reset movement steps
                    player.stamina = 20  # Reset player's stamina

    # Draw the room
    screen.fill((0, 0, 0))
    for y in range(ROOM_HEIGHT):
        for x in range(ROOM_WIDTH):
            sprite_rect = pygame.Rect(x * DISPLAY_SIZE[0], y * DISPLAY_SIZE[1], DISPLAY_SIZE[0], DISPLAY_SIZE[1])
            screen.blit(pygame.transform.scale(sprite_sheet.subsurface(floor_tile), DISPLAY_SIZE), sprite_rect)

    # Update the current frame based on time
    current_frame = pygame.time.get_ticks() - clock.get_rawtime()

    # Draw characters
    wizard_rect = pygame.Rect(player.position[0] * DISPLAY_SIZE[0], player.position[1] * DISPLAY_SIZE[1], DISPLAY_SIZE[0], DISPLAY_SIZE[1])
    screen.blit(player.update(current_frame), wizard_rect)

    for npc in active_npcs:
        npc_rect = pygame.Rect(npc.position[0] * DISPLAY_SIZE[0], npc.position[1] * DISPLAY_SIZE[1], DISPLAY_SIZE[0], DISPLAY_SIZE[1])
        screen.blit(npc.update(current_frame), npc_rect)

    # Draw the character sheet UI
    draw_character_sheet(screen, selected_option, {"moves": remaining_player_movement})

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

    # Handle NPC turns
    if current_turn == "npc":
        defeated_npcs = []  # List to store defeated NPCs
        for npc in active_npcs:
            # NPC movement logic (move one tile per turn)
            npc.move_random(ROOM_WIDTH, ROOM_HEIGHT)
            if npc.health <= 0:
                # Remove the NPC from the list if its health is 0 or below
                defeated_npcs.append(npc)
                print(f"{npc} has been defeated!")

        # Remove defeated NPCs from the list
        for defeated_npc in defeated_npcs:
            active_npcs.remove(defeated_npc)

        # Switch turns after all NPCs have moved
        current_turn = "player"
