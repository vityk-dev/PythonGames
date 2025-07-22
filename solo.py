import pygame
import time

# === Maze Class ===
class Maze:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def is_wall(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return True
        pixel = self.image.get_at((x, y))
        return pixel[0] < 128  # wall if red channel is dark

    def can_move(self, rect):
        corners = [
            (rect.left, rect.top),
            (rect.left, rect.bottom - 1),
            (rect.right - 1, rect.top),
            (rect.right - 1, rect.bottom - 1)
        ]
        return all(not self.is_wall(x, y) for x, y in corners)

    def draw(self, screen):
        screen.blit(self.image, (0, 0))


# === Player Class ===
class Player:
    def __init__(self, x, y, maze):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.speed = 5
        self.maze = maze
        self.color = (255, 0, 0)
        self.inventory = []

    def move(self, dx, dy):
        old_pos = self.rect.topleft
        self.rect.move_ip(dx, dy)
        if not self.maze.can_move(self.rect):
            self.rect.topleft = old_pos

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]: dx -= self.speed
        if keys[pygame.K_RIGHT]: dx += self.speed
        if keys[pygame.K_UP]: dy -= self.speed
        if keys[pygame.K_DOWN]: dy += self.speed
        self.move(dx, dy)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


# === Collectible Class ===
class Collectible:
    def __init__(self, x, y, name, image_path):
        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.name = name
        self.picked_up = False

    def check_collision(self, player_rect):
        if not self.picked_up and self.rect.colliderect(player_rect):
            self.picked_up = True
            return True
        return False

    def draw(self, screen):
        if not self.picked_up:
            screen.blit(self.image, self.rect.topleft)


# === Enemy Class ===
class Enemy:
    def __init__(self, x, y, maze):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.maze = maze
        self.speed = 1.5
        self.direction = -1
        self.last_hit_time = 0

    def move_vertical(self):
        old_y = self.rect.y
        self.rect.y += self.speed * self.direction
        if not self.maze.can_move(self.rect):
            self.rect.y = old_y
            self.direction *= -1

    def can_damage(self):
        return time.time() - self.last_hit_time > 1

    def collides_with_player(self, player_rect):
        return self.rect.colliderect(player_rect)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)


# === Main Game Loop ===
def main():
    pygame.init()
    screen_width, screen_height = 1100, 800
    ui_width = 400
    game_width = screen_width - ui_width

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    maze = Maze("png/maze.png")
    player = Player(100, 100, maze)

    enemies = [Enemy(250, 100, maze)]

    collectibles = [
        Collectible(50, 150, "Key 1", "png/1.png"),
        Collectible(200, 180, "Key 2", "png/2.png"),
        Collectible(320, 380, "Key 3", "png/3.png"),
        Collectible(205, 440, "Key 4", "png/4.png")
    ]

    score = 0
    lives = 3
    running = True
    game_over = False

    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            player.handle_input()

            # Check collectibles
            for item in collectibles:
                if item.check_collision(player.rect):
                    score += 1
                    player.inventory.append(item)
                    if score == len(collectibles):
                        game_over = True

            # Check enemy collisions
            for enemy in enemies:
                enemy.move_vertical()
                if enemy.collides_with_player(player.rect) and enemy.can_damage():
                    lives -= 1
                    enemy.last_hit_time = time.time()
                    print(f"Player hit! Lives left: {lives}")
                    if lives == 0:
                        game_over = True

        # --- Drawing ---
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (game_width, 0, ui_width, screen_height))

        maze.draw(screen)
        for item in collectibles:
            item.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        player.draw(screen)

        # HUD
        screen.blit(font.render(f"Score: {score}", True, (0, 0, 0)), (10, 10))
        screen.blit(font.render(f"Lives: {lives}", True, (255, 0, 0)), (120, 10))

        # Inventory UI
        title = font.render("Inventory", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(game_width + ui_width // 2, 50)))

        for idx, item in enumerate(player.inventory):
            label = font.render(f"{idx + 1}: {item.name}", True, (255, 255, 255))
            screen.blit(label, (game_width + 20, 100 + idx * 60))
            icon = pygame.transform.scale(item.image, (30, 30))
            screen.blit(icon, (game_width + 250, 100 + idx * 60))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
