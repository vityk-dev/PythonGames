# Урок: Багатовіконний інтерфейс та багаторівнева гра

---

## Частина 1: Багатовіконний інтерфейс (40 хвилин)

### Теорія (20 хвилин)

**Чи можна мати 2 екрани одночасно в pygame?**

**Відповідь:** Ні, але є 3 способи створити схожий ефект:

#### **Варіант 1: Розділення одного екрану**
```python
import pygame

pygame.init()

# Один великий екран розділений на зони
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
GAME_WIDTH = 800
UI_WIDTH = 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Ігрова зона (ліворуч)
game_rect = pygame.Rect(0, 0, GAME_WIDTH, SCREEN_HEIGHT)

# UI зона (праворуч)  
ui_rect = pygame.Rect(GAME_WIDTH, 0, UI_WIDTH, SCREEN_HEIGHT)

# Малювання розділення
pygame.draw.line(screen, (255, 255, 255), (GAME_WIDTH, 0), (GAME_WIDTH, SCREEN_HEIGHT), 3)
```

#### **Варіант 2: Overlay інтерфейс**
```python
class InventoryUI:
    def __init__(self):
        self.visible = False
        self.items = []
        self.font = pygame.font.Font(None, 24)
        
        # Напівпрозора панель
        self.surface = pygame.Surface((300, 400))
        self.surface.set_alpha(200)  # Напівпрозорість
        self.surface.fill((50, 50, 50))
        
        self.rect = pygame.Rect(500, 100, 300, 400)
    
    def toggle(self):
        self.visible = not self.visible
    
    def add_item(self, item_name):
        self.items.append(item_name)
    
    def draw(self, screen):
        if self.visible:
            # Малюємо напівпрозору панель
            screen.blit(self.surface, self.rect)
            
            # Заголовок
            title = self.font.render("ІНВЕНТАР", True, (255, 255, 255))
            screen.blit(title, (self.rect.x + 10, self.rect.y + 10))
            
            # Список предметів
            for i, item in enumerate(self.items):
                item_text = self.font.render(f"• {item}", True, (200, 200, 200))
                screen.blit(item_text, (self.rect.x + 20, self.rect.y + 50 + i * 30))
```

#### **Варіант 3: Два окремі вікна (складно)**
```python
import tkinter as tk
import threading

class SecondWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Інвентар")
        self.root.geometry("300x400")
        
        self.inventory_list = tk.Listbox(self.root)
        self.inventory_list.pack(fill="both", expand=True)
    
    def add_item(self, item):
        self.inventory_list.insert(tk.END, item)
    
    def run(self):
        self.root.mainloop()

# Запуск у окремому потоці
def start_second_window():
    window = SecondWindow()
    window.run()

thread = threading.Thread(target=start_second_window)
thread.daemon = True
thread.start()
```

**Рекомендація:** Використовуй **Варіант 1** або **Варіант 2** - вони найпростіші та найнадійніші.

### Практика (20 хвилин)

**Завдання 1 (початковий рівень):**
Створи екран розділений навпіл: ліва частина для гри, права для UI з текстом.

**Завдання 2 (середній рівень):**
Створи overlay інвентар що з'являється/зникає при натисканні TAB.

**Завдання 3 (складний рівень):**
Створи міні-карту у правому верхньому куті що показує позицію гравця.

---

## Частина 2: Система збору предметів (25 хвилин)

### Теорія (10 хвилин)

**Створення ключів та інвентарю:**
```python
class Key:
    def __init__(self, x, y, key_type="gold"):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.key_type = key_type
        self.collected = False
        
        # Кольори для різних типів ключів
        self.colors = {
            "gold": (255, 215, 0),
            "silver": (192, 192, 192),
            "bronze": (205, 127, 50)
        }
    
    def collect(self):
        if not self.collected:
            self.collected = True
            return True
        return False
    
    def draw(self, screen):
        if not self.collected:
            color = self.colors.get(self.key_type, (255, 255, 255))
            pygame.draw.rect(screen, color, self.rect)
            # Малюємо символ ключа
            pygame.draw.circle(screen, (0, 0, 0), 
                             (self.rect.centerx, self.rect.y + 5), 3)

class Inventory:
    def __init__(self):
        self.keys = []
        self.visible = False
        
    def add_key(self, key_type):
        self.keys.append(key_type)
        print(f"Зібрано {key_type} ключ! Всього ключів: {len(self.keys)}")
    
    def has_key(self, key_type):
        return key_type in self.keys
    
    def get_key_count(self):
        return len(self.keys)
```

### Практика (15 хвилин)

**Завдання 1 (початковий рівень):**
Створи 3 ключі на карті та систему їх збору при дотику.

**Завдання 2 (середній рівень):**
Додай інвентар що показує зібрані ключі з їх кольорами.

**Завдання 3 (складний рівень):**
Створи двері що відкриваються тільки при наявності потрібного ключа.

---

## Частина 3: Багаторівневий геймплей (50 хвилин)

### Теорія (25 хвилин)

#### **Рівень 1: Простий ворог**
```python
class SimpleEnemy:
    def __init__(self, x, y, maze, direction=1):
        self.rect = pygame.Rect(x, y, 18, 18)
        self.maze = maze
        self.speed = 2
        self.direction = direction  # 1 або -1
        self.axis = "horizontal"  # "horizontal" або "vertical"
    
    def update(self):
        old_x, old_y = self.rect.x, self.rect.y
        
        if self.axis == "horizontal":
            self.rect.x += self.speed * self.direction
        else:
            self.rect.y += self.speed * self.direction
        
        # Перевірка колізії зі стіною
        if not self.maze.can_move_to(self.rect):
            self.rect.x, self.rect.y = old_x, old_y
            self.direction *= -1  # Зміна напрямку
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 100, 100), self.rect)
```

#### **Рівень 2: Два вороги**
```python
class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.enemies = []
        self.keys = []
        self.completed = False
        
    def create_level_1(self, maze):
        # 1 ворог горизонтально
        enemy1 = SimpleEnemy(100, 100, maze, direction=1)
        enemy1.axis = "horizontal"
        self.enemies.append(enemy1)
        
        # 1 ключ
        self.keys.append(Key(300, 200, "gold"))
    
    def create_level_2(self, maze):
        # 2 вороги
        enemy1 = SimpleEnemy(100, 100, maze, direction=1)
        enemy1.axis = "horizontal"
        
        enemy2 = SimpleEnemy(200, 150, maze, direction=-1)
        enemy2.axis = "vertical"
        
        self.enemies.extend([enemy1, enemy2])
        
        # 2 ключі
        self.keys.extend([
            Key(300, 200, "gold"),
            Key(400, 250, "silver")
        ])
    
    def create_level_3(self, maze):
        # 2 простих + 1 що переслідує
        enemy1 = SimpleEnemy(100, 100, maze, direction=1)
        enemy1.axis = "horizontal"
        
        enemy2 = SimpleEnemy(200, 150, maze, direction=-1)
        enemy2.axis = "vertical"
        
        chasing_enemy = ChasingEnemy(300, 300, maze)
        
        self.enemies.extend([enemy1, enemy2, chasing_enemy])
        
        # 3 ключі
        self.keys.extend([
            Key(350, 200, "gold"),
            Key(450, 250, "silver"),
            Key(500, 300, "bronze")
        ])
```

#### **Рівень 3: Ворог що переслідує**
```python
class ChasingEnemy:
    def __init__(self, x, y, maze):
        self.rect = pygame.Rect(x, y, 18, 18)
        self.maze = maze
        self.speed = 1  # Повільніше за гравця
    
    def update(self, player_rect):
        old_x, old_y = self.rect.x, self.rect.y
        
        # Простий AI - рух до гравця
        dx, dy = 0, 0
        
        if self.rect.centerx < player_rect.centerx:
            dx = self.speed
        elif self.rect.centerx > player_rect.centerx:
            dx = -self.speed
            
        if self.rect.centery < player_rect.centery:
            dy = self.speed
        elif self.rect.centery > player_rect.centery:
            dy = -self.speed
        
        # Спочатку рух по X
        self.rect.x += dx
        if not self.maze.can_move_to(self.rect):
            self.rect.x = old_x
        
        # Потім рух по Y
        old_y = self.rect.y
        self.rect.y += dy
        if not self.maze.can_move_to(self.rect):
            self.rect.y = old_y
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 100), self.rect)  # Рожевий
```

#### **Система рівнів**
```python
class GameManager:
    def __init__(self):
        self.current_level = 1
        self.max_level = 3
        self.level = None
        self.player_lives = 3
        
    def load_level(self, level_number, maze):
        self.level = Level(level_number)
        
        if level_number == 1:
            self.level.create_level_1(maze)
        elif level_number == 2:
            self.level.create_level_2(maze)
        elif level_number == 3:
            self.level.create_level_3(maze)
        
        print(f"Завантажено рівень {level_number}")
    
    def check_level_completion(self, inventory):
        # Рівень завершений якщо зібрані всі ключі
        required_keys = len(self.level.keys)
        collected_keys = inventory.get_key_count()
        
        if collected_keys >= required_keys and not self.level.completed:
            self.level.completed = True
            return True
        return False
    
    def next_level(self, maze, inventory):
        if self.current_level < self.max_level:
            self.current_level += 1
            inventory.keys.clear()  # Очищуємо інвентар
            self.load_level(self.current_level, maze)
            return True
        return False  # Гра завершена
```

### Практика (25 хвилин)

**Завдання 1 (початковий рівень):**
Створи ворога що рухається горизонтально та відскакує від стін.

**Завдання 2 (середній рівень):**
Додай систему рівнів з прогресією складності.

**Завдання 3 (складний рівень):**
Створи розумного ворога що намагається обійти перешкоди для досягнення гравця.

---

## Частина 4: Інтеграція всіх систем (25 хвилин)

### Створення повної гри з усіма елементами

```python
class AdvancedMazeGame:
    def __init__(self):
        pygame.init()
        
        # Екран з двома зонами
        self.screen_width = 1200
        self.screen_height = 600
        self.game_width = 800
        self.ui_width = 400
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Багаторівневий лабіринт")
        self.clock = pygame.time.Clock()
        
        # Ігрові об'єкти
        self.maze = Maze("maze.png")
        self.player = Player(50, 50, self.maze)
        self.inventory = Inventory()
        self.game_manager = GameManager()
        
        # UI
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 36)
        
        # Стан гри
        self.running = True
        self.game_over = False
        self.victory = False
        
        # Завантаження першого рівня
        self.game_manager.load_level(1, self.maze)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.inventory.visible = not self.inventory.visible
                elif event.key == pygame.K_r and (self.game_over or self.victory):
                    self.__init__()  # Перезапуск
    
    def update(self):
        if not self.game_over and not self.victory:
            # Оновлення гравця
            self.player.update()
            
            # Оновлення ворогів
            for enemy in self.game_manager.level.enemies:
                if isinstance(enemy, ChasingEnemy):
                    enemy.update(self.player.rect)
                else:
                    enemy.update()
                
                # Перевірка зіткнення з ворогом
                if enemy.rect.colliderect(self.player.rect):
                    self.game_manager.player_lives -= 1
                    if self.game_manager.player_lives <= 0:
                        self.game_over = True
                    else:
                        # Повернути гравця на початок
                        self.player.rect.x, self.player.rect.y = 50, 50
                    break
            
            # Збір ключів
            for key in self.game_manager.level.keys:
                if not key.collected and key.rect.colliderect(self.player.rect):
                    if key.collect():
                        self.inventory.add_key(key.key_type)
            
            # Перевірка завершення рівня
            if self.game_manager.check_level_completion(self.inventory):
                if not self.game_manager.next_level(self.maze, self.inventory):
                    self.victory = True  # Усі рівні пройдені
                else:
                    # Повернути гравця на початок для нового рівня
                    self.player.rect.x, self.player.rect.y = 50, 50
    
    def draw_game_area(self):
        # Ігрова зона (ліворуч)
        game_surface = pygame.Surface((self.game_width, self.screen_height))
        
        # Малювання ігрових об'єктів
        self.maze.draw(game_surface)
        self.player.draw(game_surface)
        
        # Малювання ключів
        for key in self.game_manager.level.keys:
            key.draw(game_surface)
        
        # Малювання ворогів
        for enemy in self.game_manager.level.enemies:
            enemy.draw(game_surface)
        
        # Переносимо на основний екран
        self.screen.blit(game_surface, (0, 0))
    
    def draw_ui_area(self):
        # UI зона (праворуч)
        ui_x = self.game_width
        
        # Фон UI
        ui_rect = pygame.Rect(ui_x, 0, self.ui_width, self.screen_height)
        pygame.draw.rect(self.screen, (40, 40, 60), ui_rect)
        
        # Розділювач
        pygame.draw.line(self.screen, (255, 255, 255), 
                        (self.game_width, 0), (self.game_width, self.screen_height), 3)
        
        # Інформація про рівень
        level_text = self.large_font.render(f"РІВЕНЬ {self.game_manager.current_level}", 
                                          True, (255, 255, 255))
        self.screen.blit(level_text, (ui_x + 20, 20))
        
        # Життя
        lives_text = self.font.render(f"Життя: {self.game_manager.player_lives}", 
                                    True, (255, 255, 255))
        self.screen.blit(lives_text, (ui_x + 20, 60))
        
        # Прогрес збору ключів
        total_keys = len(self.game_manager.level.keys)
        collected_keys = self.inventory.get_key_count()
        progress_text = self.font.render(f"Ключі: {collected_keys}/{total_keys}", 
                                       True, (255, 255, 255))
        self.screen.blit(progress_text, (ui_x + 20, 90))
        
        # Інвентар
        inv_title = self.font.render("ІНВЕНТАР:", True, (255, 255, 255))
        self.screen.blit(inv_title, (ui_x + 20, 130))
        
        for i, key_type in enumerate(self.inventory.keys):
            key_colors = {"gold": (255, 215, 0), "silver": (192, 192, 192), "bronze": (205, 127, 50)}
            color = key_colors.get(key_type, (255, 255, 255))
            
            # Малюємо іконку ключа
            key_rect = pygame.Rect(ui_x + 30, 160 + i * 30, 20, 20)
            pygame.draw.rect(self.screen, color, key_rect)
            
            # Назва ключа
            key_text = self.font.render(f"{key_type.capitalize()} ключ", True, (255, 255, 255))
            self.screen.blit(key_text, (ui_x + 60, 165 + i * 30))
        
        # Інструкції
        instructions = [
            "Керування:",
            "↑↓←→ - рух",
            "TAB - інвентар",
            "",
            "Мета:",
            "Збери всі ключі",
            "Уникай ворогів",
            "",
            f"Рівень {self.game_manager.current_level}/3"
        ]
        
        for i, instruction in enumerate(instructions):
            color = (200, 200, 200) if instruction else (255, 255, 255)
            inst_text = self.font.render(instruction, True, color)
            self.screen.blit(inst_text, (ui_x + 20, 300 + i * 25))
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        
        # Малювання ігрової зони
        self.draw_game_area()
        
        # Малювання UI зони
        self.draw_ui_area()
        
        # Overlay повідомлення
        if self.game_over:
            game_over_text = self.large_font.render("ПРОГРАШ! Натисни R для перезапуску", 
                                                   True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
            self.screen.blit(game_over_text, text_rect)
        
        elif self.victory:
            victory_text = self.large_font.render("ПЕРЕМОГА! Усі рівні пройдені!", True, (0, 255, 0))
            restart_text = self.font.render("Натисни R для нової гри", True, (255, 255, 255))
            
            victory_rect = victory_text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 20))
            restart_rect = restart_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 20))
            
            self.screen.blit(victory_text, victory_rect)
            self.screen.blit(restart_text, restart_rect)
        
        # Показати інвентар overlay якщо активний
        if self.inventory.visible:
            overlay = pygame.Surface((300, 200))
            overlay.set_alpha(220)
            overlay.fill((0, 0, 0))
            
            overlay_rect = pygame.Rect(450, 200, 300, 200)
            self.screen.blit(overlay, overlay_rect)
            
            inv_title = self.font.render("ДЕТАЛЬНИЙ ІНВЕНТАР", True, (255, 255, 255))
            self.screen.blit(inv_title, (overlay_rect.x + 10, overlay_rect.y + 10))
            
            for i, key_type in enumerate(self.inventory.keys):
                item_text = self.font.render(f"• {key_type.capitalize()} ключ", True, (200, 200, 200))
                self.screen.blit(item_text, (overlay_rect.x + 20, overlay_rect.y + 50 + i * 25))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

# Запуск гри
if __name__ == "__main__":
    game = AdvancedMazeGame()
    game.run()
```

---

## Jupyter Notebook версія для тестування частин

### Секція 1: Тестування багатовіконного UI
```python
%matplotlib inline
import pygame
import matplotlib.pyplot as plt

# Код для тестування UI...
```

### Секція 2: Тестування ворогів
```python
# Код для тестування різних типів ворогів...
```

### Секція 3: Тестування системи рівнів
```python
# Код для тестування переходів між рівнями...
```

---

## Домашнє завдання

1. **Додати новий тип ворога** що рухається по діагоналі
2. **Створити 4-й рівень** з комбінацією всіх типів ворогів
3. **Додати звукові ефекти** для збору ключів та зміни рівнів
4. **Реалізувати систему очок** з бонусами за швидке проходження
5. **Створити збереження прогресу** між сесіями гри

**Структура проекту:**
```
advanced_maze/
├── main.py              # Основна гра
├── game_classes.py      # Всі класи
├── levels.py           # Конфігурація рівнів
├── assets/
│   ├── maze.png
│   ├── sounds/
│   └── images/
└── saves/
    └── progress.json
```

**Наступна лекція:** AI та алгоритми пошуку шляху, процедурна генерація лабіринтів
