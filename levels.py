from collectible import Collectible
from door import Door
from enemy import PatrolEnemy, FollowingEnemy, Trap

import pygame

class Levels:
    def __init__(self):
        self.collectLvl = 0
        self.collectibles = []
        self.enemies = []
        self.doors = []
        self.score = 0

    def createEnemies(self, maze, selected_lvl):
        enemies = []
        if selected_lvl == 1:
            enemies = [
                PatrolEnemy(250, 100, maze)
            ]
        elif selected_lvl == 2:
            enemies = [
                PatrolEnemy(250, 100, maze),
                Trap(250, 140, maze)
            ]
        elif selected_lvl == 3:
            enemies = [
                PatrolEnemy(250, 100, maze),
                FollowingEnemy(360, 380, maze),
                Trap(250, 140, maze)
            ]
        return enemies

    def createColectibles(self, selected_lvl):
        collectibles = []
        if selected_lvl == 1:
            collectibles = [
                Collectible(50, 150, "Key 1", "png/1.png"),
            ]
        elif selected_lvl == 2:
            collectibles = [
                Collectible(200, 180, "Key 2", "png/2.png"),
                Collectible(320, 380, "Key 3", "png/3.png"),
            ]
        elif selected_lvl == 3:
            collectibles = [
                Collectible(50, 150, "Key 1", "png/1.png"),
                Collectible(200, 180, "Key 2", "png/2.png"),
                Collectible(320, 380, "Key 3", "png/3.png"),
                Collectible(205, 440, "Key 4", "png/4.png")
            ]
        return collectibles
    
    def createDoors(self, selected_lvl):
        doors = []
        if selected_lvl == 1:
            doors = [
                Door(450, 150, "Key 1")
            ]
        elif selected_lvl == 2:
            doors = [
                Door(500, 180, "Key 2")
            ]
        elif selected_lvl == 3:
            doors = [
                Door(520, 380, "Key 3"),
                Door(505, 440, "Key 4")
            ]
        return doors
