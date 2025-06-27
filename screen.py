import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("экран")

image = pygame.image.load("test.png")
image = pygame.transform.scale(image, (500,500))


clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0,0,0))
    screen.blit(image,(0,0))
    pygame.display.flip()
    clock.tick(60)