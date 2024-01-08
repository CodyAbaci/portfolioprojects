# ui_module.py

import pygame
import os
import sys

# Constants for UI dimensions
UI_WIDTH = 300
UI_HEIGHT = 800

pygame.init()

# Load the "Press Start 2P" font
FONT_FILENAME = "font.ttf"
FONT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), FONT_FILENAME))
press_start_font = pygame.font.Font(FONT_PATH, 20)

# Create a surface for the character sheet UI
ui_surface = pygame.Surface((UI_WIDTH, UI_HEIGHT))

# Global variable for screen width
SCREEN_WIDTH = None

# Function to set the screen width
def set_screen_width(width):
    global SCREEN_WIDTH
    SCREEN_WIDTH = width

# Function to draw the character sheet UI
def draw_character_sheet(screen, selected_option, stats={}):
    global SCREEN_WIDTH  # Ensure we use the global variable

    ui_surface.fill((50, 50, 50))  # Background color of the UI

    # Example: Draw character stats on the UI surface
    text = press_start_font.render("Character Stats", True, (255, 255, 255))
    ui_surface.blit(text, (10, 10))

    # Example: Draw character skills on the UI surface
    skills_text = "Skills:\nSkill 1: Level 3\nSkill 2: Level 2"
    skills_rendered = press_start_font.render(skills_text, True, (255, 255, 255))
    ui_surface.blit(skills_rendered, (10, 60))

    # Draw action options
    options_text = ["Move", "Attack", "Use Item", "End Turn", "Moves: " + str(stats.get('moves', 0))]  # Added "End Turn"
    for i, option in enumerate(options_text):
        color = (255, 255, 255) if i == selected_option else (150, 150, 150)
        option_rendered = press_start_font.render(option, True, color)
        ui_surface.blit(option_rendered, (10, 150 + i * 40))

    # Draw the character sheet UI on the main screen
    screen.blit(ui_surface, (SCREEN_WIDTH - UI_WIDTH, 0))
