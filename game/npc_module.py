# npc_module.py

import pygame
import os
import random

class Goblin:
    def __init__(self, position):
        self.position = position
        self.sprite_sheet = pygame.image.load(os.path.join(os.path.dirname(__file__), "goblinscout.png"))
        self.sprite_size = (500, 500)
        self.idle_frames = [(1950, 1500, 500, 500), (2450, 1500, 500, 500)]

    def update(self, current_frame):
        return pygame.transform.scale(self.sprite_sheet.subsurface(self.idle_frames[current_frame // 100 % len(self.idle_frames)]), (64, 64))

    def move_random(self, roomWidth, roomHeight):
        # Move the goblin to a random adjacent tile
        possible_moves = [
            (self.position[0] + 1, self.position[1]),
            (self.position[0] - 1, self.position[1]),
            (self.position[0], self.position[1] + 1),
            (self.position[0], self.position[1] - 1),
        ]
        random.shuffle(possible_moves)
        for move in possible_moves:
            if 0 <= move[0] < roomWidth and 0 <= move[1] < roomHeight:
                self.position = move
                break

class Slayer:
    def __init__(self, position):
        self.position = position
        self.sprite_frames = [pygame.image.load(os.path.join(os.path.dirname(__file__), "slayer.png")),
                              pygame.image.load(os.path.join(os.path.dirname(__file__), "slayer2.png")),
                              pygame.image.load(os.path.join(os.path.dirname(__file__), "slayer3.png"))]

    def update(self, current_frame):
        return pygame.transform.scale(self.sprite_frames[current_frame // 100 % len(self.sprite_frames)], (64, 64))

    def move_random(self, roomWidth, roomHeight):
        # Move the slayer to a random adjacent tile
        possible_moves = [
            (self.position[0] + 1, self.position[1]),
            (self.position[0] - 1, self.position[1]),
            (self.position[0], self.position[1] + 1),
            (self.position[0], self.position[1] - 1),
        ]
        random.shuffle(possible_moves)
        for move in possible_moves:
            if 0 <= move[0] < roomWidth and 0 <= move[1] < roomHeight:
                self.position = move
                break
