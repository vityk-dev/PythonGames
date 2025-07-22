import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("экран")

red = (255,0,0)
ballC = (0,0,0)
color = (0,0,0)
screen.fill(red)

running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 screen.fill(red)
#                 pygame.draw.rect(screen,color,(300,300,100,100))
#             elif event.key == pygame.K_BACKSPACE:
#                 screen.fill(color)
#                 pygame.draw.rect(screen,red,(300,300,100,100))
#     pygame.display.flip()


# class Ball:
#     def __init__(self,x,y,speed_x,speed_y,width,height):
#         self.rect = pygame.Rect(x, y,width,height)
#         self.speed = [speed_x,speed_y]

#     def move(self):
#         self.rect.x += self.speed[0]
#         self.rect.y += self.speed[1]

#         if self.rect.left <= 0 or self.rect.right >= WIDTH:
#             self.speed[0] *= -1
#         if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
#             self.speed[1] *= -1

#     def draw(self,surface):
#         pygame.draw.ellipse(surface,(ballC),self.rect)

# ball = Ball(250,250,20,20,5,5)

image = pygame.image.load("test.png")
image = pygame.transform.scale(image, (500,500))
screen.blit(image,(0,500))
pygame.display.flip()




# clock = pygame.time.Clock()
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#             running = False
#     screen.fill(red)
#     # ball.move()
#     # ball.draw(screen)
#     pygame.display.flip()
#     clock.tick(60)


    
