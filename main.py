import pygame, time

class Maze:
    def __init__(self, imageP):
        self.image = pygame.image.load(imageP)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def isWall(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return True
        wallPixel = self.image.get_at((x, y))
        return wallPixel[0] < 128

    def movement(self, rect):
        corners = [
            (rect.left, rect.top),
            (rect.left, rect.bottom - 1),
            (rect.right - 1, rect.top),
            (rect.right - 1, rect.bottom - 1)
        ]
        return all(not self.isWall(x, y) for x, y in corners)

    def draw(self, screen):
        screen.blit(self.image, (0, 0))


class Player:
    def __init__(self, x, y, maze):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.speed = 5
        self.maze = maze
        self.color = (255, 0, 0)
        self.inventory = []

    def move(self, dx, dy):
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
        self.move(dx, dy)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


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


class Enemy:
    def __init__(self, x, y, maze):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.maze = maze
        self.speed = 1.5
        self.direction = -1
        self.hit_time = 0

    def moveY(self):
        old_y = self.rect.y
        self.rect.y += self.speed * self.direction
        if not self.maze.movement(self.rect):
            self.rect.y = old_y
            self.direction *= -1

    def check1(self, player):
        return self.rect.colliderect(player)

    def can_damage(self):
        return time.time() - self.hit_time > 1

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)


def main():
    pygame.init()
    SCREEN_WIDTH = 1100
    SCREEN_HEIGHT = 800
    UI_WIDTH = 400
    GAME_UI_WIDTH = 700

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze with Inventory")
    clock = pygame.time.Clock()
    game_rect = pygame.Rect(0, 0, GAME_UI_WIDTH, SCREEN_HEIGHT)
    ui_rect = pygame.Rect(GAME_UI_WIDTH, 0, UI_WIDTH, SCREEN_HEIGHT)

    maze = Maze("png/maze.png")
    player = Player(100, 100, maze)

    enemies = [
        Enemy(250, 100, maze),
    ]

    collectibles = [
        Collectible(50, 150, "Key 1", "png/1.png"),
        Collectible(200, 180, "Key 2", "png/2.png"),
        Collectible(320, 380, "Key 3", "png/3.png"),
        Collectible(205, 440, "Key 4", "png/4.png")
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
                    player.inventory.append(c)
                    if score == len(collectibles):
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

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (255, 255, 255), game_rect)
        pygame.draw.rect(screen, (0, 0, 0), ui_rect)

        maze.draw(screen)

        for c in collectibles:
            c.draw(screen)

        for e in enemies:
            e.draw(screen)

        player.draw(screen)

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        life_text = font.render(f"Lives: {life}", True, (255, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(life_text, (120, 10))

        ui_title = font.render("Inventory", True, (255, 255, 255))
        ui_title_rect = ui_title.get_rect(center=(GAME_UI_WIDTH + UI_WIDTH // 2, 50))
        screen.blit(ui_title, ui_title_rect)

        for index, item in enumerate(player.inventory):
            item_text = font.render(f"{index + 1}: {item.name}", True, (255, 255, 255))
            screen.blit(item_text, (GAME_UI_WIDTH + 20, 100 + index * 60))
            mini_image = pygame.transform.scale(item.image, (30, 30))
            screen.blit(mini_image, (GAME_UI_WIDTH + 250, 100 + index * 60))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
