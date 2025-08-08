import pygame, time, math, sys, json
from levels import Levels
from collectible import Collectible
from door import Door
from enemy import PatrolEnemy, FollowingEnemy, Trap

#TODO!!!! Stats per each level: hp, level
#TODO Добавить сохранение в json и систему уровней из json файла 
#TODO Экран победы(переход в следующий уровень по нажатию, а не автоматически)
#TODO Экран поражения
#TODO изменить повтроряющийся код в функции чтоб можно было их просто вызвать
#TODO сделать анимацию получения урона(полоска зеленная пока все нормально, и перекрашивается при получении урона на некоторое время)
#NOTE добавить звуки и удалить все не нужное из кода

pygame.init()

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 800
UI_WIDTH = 400
GAME_UI_WIDTH = 700


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

    def move(self, dx, dy, doors):
        old_pos = self.rect.topleft
        self.rect.x += dx
        if not self.maze.movement(self.rect) or self.collidDoor(doors):
            self.rect.x = old_pos[0]
        old_pos_y = self.rect.topleft
        self.rect.y += dy
        if not self.maze.movement(self.rect) or self.collidDoor(doors):
            self.rect.y = old_pos[1]
        
    def collidDoor(self, doors) -> bool:

        for door in doors:
            if self.rect.colliderect(door.rect):
                if not door.checkOp(self.inventory):
                    return True
        return False

    def binds(self, doors):
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        length = math.hypot(dx, dy)
        if length != 0:
            dx = dx / length * self.speed
            dy = dy / length * self.speed

        self.move(dx, dy, doors)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

def draw_text(surface, text, font, color, center):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=center)
    surface.blit(rendered, rect)
    
def menu(screen, clock, font, max_level):
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
                if start_rect.collidepoint(mouse) and selected_level <= max_level:
                    in_menu = False
                elif left_rect.collidepoint(mouse):
                    selected_level = max(1, selected_level - 1)
                elif right_rect.collidepoint(mouse):
                    selected_level = min(max_level, selected_level + 1)

        pygame.display.flip()
        clock.tick(60)

    return selected_level

def saveGame(level,life,inventory,max_level):
    data = {
        "level": level,
        "life": life,
        "inventory": [item.name for item in inventory],
        "max_level": max_level
    }
    with open("save.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def loadGame():
    try:
        with open("save.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return None
        
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    
    load = loadGame()
    if load:
        level = load.get("level", 1)
        life = load.get("life", 3)
        t_inventory = load.get("inventory", [])
        max_level = load.get("max_level", 1)
    
    else:
        level = 1
        life = 3
        t_inventory = []
        max_level = 1
    
    levels = Levels()
    selected_level = menu(screen, clock, font,max_level)
    
    maze_path = f"png/maze{selected_level}.png"
    maze = Maze(maze_path)
    player = Player(100, 100, maze)
    collectibles = levels.createColectibles(selected_level)
    
    for item in collectibles:
        if item.name in t_inventory:
            player.inventory.append(item)
    

    enemies = levels.createEnemies(maze, selected_level)
    doors = levels.createDoors(selected_level)
    
    game_rect = pygame.Rect(0, 0, GAME_UI_WIDTH, SCREEN_HEIGHT)
    ui_rect = pygame.Rect(GAME_UI_WIDTH, 0, UI_WIDTH, SCREEN_HEIGHT)

    score = 0
    game_over = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True

        if not game_over:
            player.binds(doors)
            
            for c in collectibles:
                if c.checkCollision(player.rect):
                    score += 1
                    player.inventory.append(c)
        
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
                    if life <= 0:
                        game_over = True
                        running = False
                        break
            #TODO screen of defeat
            if game_over:
                pass

                    
            for door in doors:
                if player.rect.colliderect(door.rect):
                    door.try_doors(player.inventory)
                            
            for door in doors:
                if player.rect.colliderect(door.rect) and score == len(collectibles):
                    if all(door.checkOp(player.inventory) for door in doors):
                        selected_level += 1
                        max_level = max(max_level, selected_level)
                        if selected_level > 3:
                            saveGame(selected_level - 1, life, player.inventory, max_level)
                            game_over = True
                            running = False
                            break
                        else:
                            saveGame(selected_level - 1, life, player.inventory, max_level)
                        maze = Maze(f"png/maze{selected_level}.png")
                        player = Player(100, 100, maze)
                        enemies = levels.createEnemies(maze, selected_level)
                        collectibles = levels.createColectibles(selected_level)
                        doors = levels.createDoors(selected_level)
                        score = 0
                        player.inventory.clear()
                        break 
        
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (255, 255, 255), game_rect)
        pygame.draw.rect(screen, (0, 0, 0), ui_rect)

        maze.draw(screen)

        for c in collectibles:
            c.draw(screen)

        for e in enemies:
            e.draw(screen)
            
        for door in doors:
            door.draw(screen)
            
        player.draw(screen)

        ui_title = font.render("Inventory", True, (255, 255, 255))
        ui_title_rect = ui_title.get_rect(center=(GAME_UI_WIDTH + UI_WIDTH // 2, 50))
        screen.blit(ui_title, ui_title_rect)
        maxHP = 3
        sizeX = GAME_UI_WIDTH + 55
        sizeY = 70
        widthX = 300
        heightY = 25
        
        pygame.draw.rect(screen, (0,0,0), (sizeX, sizeY, widthX, heightY), 2)
        
        fill = int((life / maxHP) * widthX)
        pygame.draw.rect(screen, (255,0,0), (sizeX, sizeY, fill, heightY))
        
        life_text = font.render(f"Lives: {life}/{maxHP}", True, (255, 255, 255))
        screen.blit(life_text, (sizeX + 90, sizeY - 60))

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


