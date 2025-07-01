import pygame


class Maze:
    def __init__(self,imageP):
        self.image = pygame.image.load(imageP)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def isWall(self,x,y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return True
        wallPixel = self.image.get_at((x, y))
        return wallPixel[0] < 128
    
    def movement(self,rect):
        # if self.isWall(rect_.left, rect_.top):
        #     return False
        # if self.isWall(rect_.left, rect_.bottom -1):
        #     return False
        # if self.isWall(rect_.right - 1, rect_.top):
        #     return False
        # if self.isWall(rect_.right - 1, rect_.bottom - 1):
        #     return False
        # return True

        corners = [(rect.left, rect.top),
            (rect.left, rect.bottom -1),
            (rect.right -1, rect.top),
            (rect.right - 1,rect.bottom - 1)
        ]
        return all(not self.isWall(x,y) for x, y in corners)
    
    def draw(self,screen):
        screen.blit(self.image, (0,0))

class Player:
    def __init__(self,x,y,maze):
        self.rect = pygame.Rect(x,y,10,10)
        self.speed = 5
        self.maze = maze
        self.color = (255,0,0)

    def move(self,dx,dy):
        old_pos = self.rect.topleft
        self.rect.x += dx
        self.rect.y += dy
        if not self.maze.movement(self.rect):
            self.rect.topleft = old_pos

    def binds(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]: dx = -self.speed
        if keys[pygame.K_RIGHT]: dx = self.speed
        if keys[pygame.K_UP]: dy = -self.speed
        if keys[pygame.K_DOWN]: dy = self.speed
        # if dx or dy:
        self.move(dx,dy)

    def draw(self,screen):
        pygame.draw.rect(screen,self.color,self.rect)

class Collectible:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,30,30)
        self.picked = False
        self.color = (0,255,0)

    def checkCollision(self,playerRect):
        if not self.picked and self.rect.colliderect(playerRect):
            self.picked = True
            return True
        return False
    
    def draw(self,screen):
        if not self.picked:
            pygame.draw.rect(screen,self.color,self.rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Maze")
    clock = pygame.time.Clock()

    maze = Maze("maze.png")
    player = Player(100, 100, maze)

    collectibles = [
        Collectible(400, 100),
        Collectible(200, 200),
        Collectible(300, 300)
    ]

    score = 0
    font = pygame.font.SysFont(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.binds()

        for c in collectibles:
            if c.checkCollision(player.rect):
                score += 1

        screen.fill((100, 100, 100))
        maze.draw(screen)
        
        for c in collectibles:
            c.draw(screen)

        player.draw(screen)

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()



if __name__ == "__main__":
    main()