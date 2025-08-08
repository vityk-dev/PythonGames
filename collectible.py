import pygame

class Collectible:
    def __init__(self, x, y, name, image_path):
        load_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(load_image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.picked = False
        self.name = name

    def checkCollision(self, playerRect):
        if not self.picked and self.rect.colliderect(playerRect):
            self.picked = True
            return True
        return False

    def draw(self, screen):
        if not self.picked:
            screen.blit(self.image, self.rect.topleft)