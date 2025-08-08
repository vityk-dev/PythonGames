import pygame

class Maze:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def isWall(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return True
        wallPixel = self.image.get_at((x, y))
        return wallPixel.r < 128

    def draw(self, screen):
        screen.blit(self.image, (0, 0))