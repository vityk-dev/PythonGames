import pygame, time, math, sys

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

class PatrolEnemy:
    def __init__(self, x, y, maze):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.maze = maze
        self.speed = 1.5
        self.direction = -1
        self.hit_time = 0

    def move(self):
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

class FollowingEnemy:
    def __init__(self, x, y, maze):
        self.rect = pygame.Rect(x, y, 12, 12)
        self.maze = maze
        self.speed = 3
        self.hit_time = 0
        self.range = 150 
        self.patrol_direction_x = 1
        self.patrol_direction_y = 0
        self.is_following = False
        self.direction_change_timer = 0
        self.direction_change_interval = 2 
        
        self.stuck_timer = 0
        
    def see_player(self, player_rect):
        start_x, start_y = self.rect.center
        end_x, end_y = player_rect.center
        dx = end_x - start_x
        dy = end_y - start_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance == 0:
            return True
            
        steps = int(distance // 5)
        if steps == 0:
            return True
        
        step_x = dx / steps
        step_y = dy / steps
        
        for i in range(steps):
            check_x = start_x + step_x * i
            check_y = start_y + step_y * i
            if self.maze.isWall(int(check_x), int(check_y)):
                return False
        
        return True
        
    def move(self, player_rect):
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery 
        distance = math.sqrt(dx**2 + dy**2)
        # direction = pygame.math.Vector2(player_rect.center) - pygame.math.Vector2(self.rect.center)
        # distance = direction.length()

        if distance <= self.range and self.see_player(player_rect):
            self.is_following = True
            if distance > 0:
                dx = dx / distance
                dy = dy / distance
                old_pos = self.rect.topleft
                
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed
                if not self.maze.movement(self.rect):
                    self.rect.topleft = old_pos 
                    self.stuck_timer += 1/60 
                    if self.stuck_timer >= 5:  
                        import random
                        self.patrol_direction_x = random.choice([-1, 1])
                        self.patrol_direction_y = random.choice([-1, 1])
                        self.stuck_timer = 0
                        self._patrol()
                else:
                    self.stuck_timer = 0 
        else:
            self.is_following = False
            self._patrol()
    
    def _patrol(self):
        current_time = time.time()
        if current_time - self.direction_change_timer > self.direction_change_interval:
            self.direction_change_timer = current_time
            import random
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            self.patrol_direction_x, self.patrol_direction_y = random.choice(directions)
        
        old_pos = self.rect.topleft
        self.rect.x += self.patrol_direction_x * (self.speed * 0.5) 
        self.rect.y += self.patrol_direction_y * (self.speed * 0.5)
        
        if not self.maze.movement(self.rect):
            self.rect.topleft = old_pos
            self.patrol_direction_x *= -1
            self.patrol_direction_y *= -1

    def check1(self, player):
        return self.rect.colliderect(player)

    def can_damage(self):
        return time.time() - self.hit_time > 1

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 100, 255), self.rect)

class Trap:
    def __init__(self,x,y,maze):
        self.rect = pygame.Rect(x,y,20,20)
        self.maze = maze
        self.hit_time = 0
    
    def check1(self,player):
        return self.rect.colliderect(player)
    
    def can_damage(self):
        return time.time() - self.hit_time > 1
    
    def draw(self,screen):
        pygame.draw.rect(screen, (75, 0, 130), self.rect)
        
class Levels:
    def __init__(self):
        self.collectLvl = 0
        self.collectibles = []
        self.enemies = []
        self.score = 0

    def createEnemies(self, maze, selected_lvl):
        enemies = []
        if selected_lvl == 1:
            enemies = [PatrolEnemy(250, 100, maze)]
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


def draw_text(surface, text, font, color, center):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=center)
    surface.blit(rendered, rect)

def menu(screen, clock, font):
    selected_level = 1
    in_menu = True
    while in_menu:
        screen.fill((30, 30, 30))

        draw_text(screen, "Maze", font, (255, 255, 255), (550, 150))
        draw_text(screen, f"Уровень: {selected_level}", font, (200, 200, 200), (550, 300))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        start_rect = pygame.Rect(450, 400, 200, 50)
        pygame.draw.rect(screen, (0, 200, 0), start_rect)
        draw_text(screen, "Старт", font, (0, 0, 0), start_rect.center)

        left_rect = pygame.Rect(370, 290, 50, 50)
        pygame.draw.rect(screen, (100, 100, 255), left_rect)
        draw_text(screen, "<", font, (255, 255, 255), left_rect.center)

        right_rect = pygame.Rect(730, 290, 50, 50)
        pygame.draw.rect(screen, (100, 100, 255), right_rect)
        draw_text(screen, ">", font, (255, 255, 255), right_rect.center)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(mouse):
                    in_menu = False
                elif left_rect.collidepoint(mouse):
                    selected_level = max(1, selected_level - 1)
                elif right_rect.collidepoint(mouse):
                    selected_level = min(3, selected_level + 1)  # допустим 3 уровня

        pygame.display.flip()
        clock.tick(60)

    return selected_level

def main():
    pygame.init()
    SCREEN_WIDTH = 1100
    SCREEN_HEIGHT = 800
    UI_WIDTH = 400
    GAME_UI_WIDTH = 700

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    selected_level = menu(screen, clock, font)
    maze_path = f"png/maze{selected_level}.png"

    game_rect = pygame.Rect(0, 0, GAME_UI_WIDTH, SCREEN_HEIGHT)
    ui_rect = pygame.Rect(GAME_UI_WIDTH, 0, UI_WIDTH, SCREEN_HEIGHT)

    maze = Maze(maze_path)
    player = Player(100, 100, maze)

    levels = Levels()
    enemies = levels.createEnemies(maze, selected_level)
    collectibles = levels.createColectibles(selected_level)

    score = 0
    life = 3
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
                        selected_level += 1
                        if selected_level > 3:
                            game_over = True
                            running = False
                            break
                        maze = Maze(f"png/maze{selected_level}.png")
                        player = Player(100, 100, maze)
                        enemies = levels.createEnemies(maze, selected_level)
                        collectibles = levels.createColectibles(selected_level)
                        score = 0
                        player.inventory = []

            for e in enemies:
                if isinstance(e, FollowingEnemy):
                    e.move(player.rect)
                elif isinstance(e, Trap):
                    pass
                else:
                    e.move()

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
