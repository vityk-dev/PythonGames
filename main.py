import pygame, time

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
        self.inventory = []

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
    def __init__(self,x,y,name):
        self.rect = pygame.Rect(x,y,10,10)
        self.image_list = ["png/1.png",
                           "png/2.png",
                           "png/3.png",
                           "png/4.png"
        ]
        for i in range(len(self.image_list)):
            self.image = pygame.image.load(self.image_list[i])
            i+=1
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.picked = False
        self.color = (0,255,0)
        self.name = name

    def checkCollision(self,playerRect):
        if not self.picked and self.rect.colliderect(playerRect):
            self.picked = True
            return True
        return False
    
    def draw(self,screen):
        if not self.picked:
            pygame.draw.rect(screen,self.color,self.rect)
            screen.blit(self.image, self.rect)

class Enemy:
    def __init__(self,x,y,maze):
        self.rect = pygame.Rect(x,y,10,10)
        self.maze = maze
        self.speed = 2
        self.direction = -1
        self.hit_time = 0

    def moveY(self):
        old_y = self.rect.y
        self.rect.y += self.speed * self.direction
        if not self.maze.movement(self.rect):
            self.rect.y = old_y
            self.direction *= -1

        # old_x = self.rect.x
        # self.rect.x += self.speed * self.direction
        # if not self.maze.movement(self.rect):
        #     self.rect.x = old_x
        #     self.direction *= -1
        
    def check1(self,player):
        return self.rect.colliderect(player)
    
    def can_damage(self):
        return time.time() - self.hit_time > 1
    
    def draw(self,screen):
        pygame.draw.rect(screen,(0,0,255), self.rect)

def main():
    pygame.init()
    SCREEN_WIDTH = 1100
    SCREEN_HEIGHT = 800
    UI_WIDTH = 400
    GAME_UI_WIDTH = 700
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze")
    clock = pygame.time.Clock()
    game_rect = pygame.Rect(0, 0, GAME_UI_WIDTH,SCREEN_HEIGHT)
    ui_rect = pygame.Rect(GAME_UI_WIDTH, 0, UI_WIDTH,SCREEN_HEIGHT)


    maze = Maze("maze.png")
    player = Player(100, 100, maze)

    enemies = [Enemy(250,100,maze),
             
    ]

    collectibles = [
        Collectible(50, 150, "Key"),
        Collectible(200, 200, "Key"),
        Collectible(300, 400, "Key"),
        Collectible(210,440, "Key")
    ]

    score = 0
    life = 3
    font = pygame.font.SysFont(None, 36)

    game_over = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True
        
        if not game_over:
            player.binds()
            for c in collectibles:
                if c.checkCollision(player.rect):
                    score += 1
                    player.inventory.append(c.name)
                    if score == 4:
                        game_over = True
                        running = False
                        break

            for e in enemies:
                e.moveY()
                if e.check1(player.rect) and e.can_damage():
                    life -= 1
                    e.hit_time = time.time()
                    print("Player hit! Remaining lives:", life)
                    if life == 0:
                        game_over = True
                        running = False
                        break

        screen.fill((100, 100, 100))
        pygame.draw.rect(screen, (50, 50, 150), game_rect)
        pygame.draw.rect(screen, (0, 0, 0), ui_rect)

        maze.draw(screen)
        
        for c in collectibles:
            c.draw(screen)

        for e in enemies:
            e.draw(screen)

        player.draw(screen)

        ui_text = font.render(f"Inventory", True, (255,255,255))
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        life_text = font.render(f"Life:{life}", True, (255,0,0))
        ui_text_rect = ui_text.get_rect(center = (GAME_UI_WIDTH + UI_WIDTH // 2, SCREEN_HEIGHT // 14))

        for index, i in enumerate(player.inventory):
            item_text = font.render(f"{index + 1}. {i}", True, (255,255,255))
            screen.blit(item_text, (820, 100 + index * 30))
            for c in collectibles:
                if c.name == i and c.picked:
                    screen.blit(c.image, (GAME_UI_WIDTH + 20, 100 + index * 30))
                    break



        screen.blit(score_text, (10, 10))
        screen.blit(life_text, (10, 40))
        screen.blit(ui_text,(ui_text_rect))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
