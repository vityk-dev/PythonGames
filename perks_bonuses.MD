# Урок: Система бонусів та двері з ключами

## 📋 План уроку

1. [Створення системи дверей](#створення-системи-дверей)
2. [Покращення системи ключів](#покращення-системи-ключів)
3. [Система power-ups](#система-power-ups)
4. [Інтеграція в гру](#інтеграція-в-гру)
5. [Тестування нової механіки](#тестування-нової-механіки)

---

## Створення системи дверей

### Мета: Двері що відкриваються коли маєш ключі

#### Планування:
- Двері заблоковані поки не зібрані всі ключі
- Візуальне відображення стану (відкрито/закрито)
- Перехід до наступного рівня при контакті з відкритими дверима

#### Код класу Door:

```python
class Door:
    def __init__(self, x, y, keys_required=2):
        self.rect = pygame.Rect(x, y, 30, 40)
        self.keys_required = keys_required
        self.is_open = False
        self.color_closed = (139, 69, 19)  # Коричневий
        self.color_open = (0, 255, 0)     # Зелений
    
    def update(self, keys_collected):
        """Оновлює стан дверей на основі зібраних ключів"""
        if keys_collected >= self.keys_required:
            self.is_open = True
        else:
            self.is_open = False
    
    def can_pass_through(self):
        """Чи можна пройти крізь двері"""
        return self.is_open
    
    def draw(self, screen):
        """Малює двері"""
        # Основні двері
        color = self.color_open if self.is_open else self.color_closed
        pygame.draw.rect(screen, color, self.rect)
        
        # Рамка
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Ручка
        handle_color = YELLOW if self.is_open else GRAY
        pygame.draw.circle(screen, handle_color, 
                          (self.rect.right - 8, self.rect.centery), 3)
        
        # Текст стану
        font = pygame.font.Font(None, 24)
        if self.is_open:
            text = font.render("ВІДКРИТО", True, WHITE)
            screen.blit(text, (self.rect.x - 10, self.rect.y - 25))
        else:
            text = font.render(f"Потрібно {self.keys_required} ключів", True, RED)
            screen.blit(text, (self.rect.x - 20, self.rect.y - 25))
```

---

## Покращення системи ключів

### Мета: Інвентар ключів та кращий контроль

#### Удосконалений клас ключа:

```python
class Key:
    def __init__(self, x, y, key_type="gold", door_id=None):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.key_type = key_type
        self.door_id = door_id  # До якої двері підходить (опціонально)
        self.collected = False
        
        # Кольори для різних типів ключів
        self.colors = {
            "gold": YELLOW,
            "silver": (192, 192, 192),
            "red": RED,
            "green": GREEN,
            "blue": BLUE,
            "master": (255, 215, 0)  # Золотий - підходить до всіх дверей
        }
        self.color = self.colors.get(key_type, YELLOW)
    
    def collect(self):
        """Збирає ключ"""
        if not self.collected:
            self.collected = True
            return True
        return False
    
    def draw(self, screen):
        """Малює ключ якщо він не зібраний"""
        if not self.collected:
            # Основна частина ключа
            pygame.draw.rect(screen, self.color, self.rect)
            
            # Деталі ключа
            pygame.draw.circle(screen, BLACK, 
                             (self.rect.centerx, self.rect.y + 3), 2)
            
            # Зубці ключа
            pygame.draw.rect(screen, BLACK, 
                           (self.rect.right - 3, self.rect.bottom - 5, 2, 3))
```

#### Система інвентаря:

```python
class KeyInventory:
    def __init__(self):
        self.keys = []  # Список зібраних ключів
        self.total_collected = 0
    
    def add_key(self, key):
        """Додає ключ до інвентаря"""
        self.keys.append(key)
        self.total_collected += 1
        print(f"Додано {key.key_type} ключ! Всього: {self.total_collected}")
    
    def has_key_for_door(self, door_id):
        """Перевіряє чи є ключ для конкретної двері"""
        for key in self.keys:
            if key.door_id == door_id or key.key_type == "master":
                return True
        return False
    
    def get_total_keys(self):
        """Повертає загальну кількість ключів"""
        return self.total_collected
    
    def draw_inventory(self, screen, x, y):
        """Малює інвентар на екрані"""
        font = pygame.font.Font(None, 24)
        
        # Заголовок
        title = font.render("Інвентар ключів:", True, BLACK)
        screen.blit(title, (x, y))
        
        # Показуємо зібрані ключі
        for i, key in enumerate(self.keys):
            key_rect = pygame.Rect(x + i * 20, y + 25, 15, 15)
            pygame.draw.rect(screen, key.color, key_rect)
            pygame.draw.rect(screen, BLACK, key_rect, 1)
```

---

## Система Power-ups

### Мета: Тимчасові та постійні бонуси

#### Базовий клас PowerUp:

```python
class PowerUp:
    def __init__(self, x, y, power_type, duration=5000):  # 5 секунд
        self.rect = pygame.Rect(x, y, 20, 20)
        self.power_type = power_type
        self.duration = duration  # В мілісекундах
        self.collected = False
        
        # Конфігурація різних типів
        self.configs = {
            "speed": {
                "color": (0, 255, 255),  # Блакитний
                "symbol": "S",
                "description": "Швидкість x2"
            },
            "shield": {
                "color": (255, 215, 0),  # Золотий
                "symbol": "🛡",
                "description": "Захист від ворогів"
            },
            "ghost": {
                "color": (128, 128, 128, 100),  # Прозорий сірий
                "symbol": "G",
                "description": "Прохід крізь стіни"
            },
            "life": {
                "color": (255, 20, 147),  # Рожевий
                "symbol": "+",
                "description": "Додаткове життя"
            },
            "freeze": {
                "color": (173, 216, 230),  # Світло-блакитний
                "symbol": "F",
                "description": "Заморожує ворогів"
            }
        }
        
        self.config = self.configs.get(power_type, self.configs["speed"])
    
    def collect(self):
        """Збирає power-up"""
        if not self.collected:
            self.collected = True
            return True
        return False
    
    def draw(self, screen):
        """Малює power-up"""
        if not self.collected:
            # Основний круг
            pygame.draw.circle(screen, self.config["color"], 
                             self.rect.center, 10)
            
            # Рамка
            pygame.draw.circle(screen, BLACK, self.rect.center, 10, 2)
            
            # Символ
            font = pygame.font.Font(None, 16)
            symbol = font.render(self.config["symbol"], True, BLACK)
            symbol_rect = symbol.get_rect(center=self.rect.center)
            screen.blit(symbol, symbol_rect)
```

#### Менеджер активних ефектів:

```python
class EffectManager:
    def __init__(self):
        self.active_effects = {}  # {effect_type: end_time}
    
    def add_effect(self, effect_type, duration):
        """Додає тимчасовий ефект"""
        end_time = pygame.time.get_ticks() + duration
        self.active_effects[effect_type] = end_time
        print(f"Активовано ефект: {effect_type}")
    
    def update(self):
        """Оновлює стан ефектів (видаляє закінчені)"""
        current_time = pygame.time.get_ticks()
        expired_effects = []
        
        for effect_type, end_time in self.active_effects.items():
            if current_time >= end_time:
                expired_effects.append(effect_type)
        
        for effect in expired_effects:
            del self.active_effects[effect]
            print(f"Ефект закінчився: {effect}")
    
    def has_effect(self, effect_type):
        """Перевіряє чи активний певний ефект"""
        return effect_type in self.active_effects
    
    def get_remaining_time(self, effect_type):
        """Повертає час що залишився для ефекту"""
        if effect_type in self.active_effects:
            remaining = self.active_effects[effect_type] - pygame.time.get_ticks()
            return max(0, remaining)
        return 0
    
    def draw_effects(self, screen, x, y):
        """Малює активні ефекти"""
        font = pygame.font.Font(None, 24)
        
        if self.active_effects:
            title = font.render("Активні ефекти:", True, BLACK)
            screen.blit(title, (x, y))
            
            for i, (effect, end_time) in enumerate(self.active_effects.items()):
                remaining = (end_time - pygame.time.get_ticks()) / 1000
                text = font.render(f"{effect}: {remaining:.1f}с", True, BLACK)
                screen.blit(text, (x, y + 25 + i * 20))
```

---

## Інтеграція в гру

### Удосконалення Player класу:

```python
class Player:
    def __init__(self, x, y, maze):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.base_speed = 4
        self.speed = self.base_speed
        self.maze = maze
        self.color = BLUE
        self.lives = 3
        
        # Нові системи
        self.inventory = KeyInventory()
        self.effects = EffectManager()
        self.invincible = False
        self.ghost_mode = False
    
    def move(self, dx, dy):
        """Рух з урахуванням ефектів"""
        old_pos = self.rect.topleft
        
        # Застосовуємо швидкість з ефектами
        actual_speed = self.speed
        if self.effects.has_effect("speed"):
            actual_speed *= 2
        
        # Рухаємося
        self.rect.x += dx * (actual_speed / self.base_speed)
        self.rect.y += dy * (actual_speed / self.base_speed)
        
        # Перевіряємо колізії (якщо не в режимі привида)
        if not self.effects.has_effect("ghost"):
            if not self.maze.can_move_to(self.rect):
                self.rect.topleft = old_pos
    
    def collect_powerup(self, powerup):
        """Збирає power-up та застосовує ефект"""
        if powerup.power_type == "life":
            self.lives += 1
        elif powerup.power_type == "shield":
            self.effects.add_effect("shield", 5000)
        elif powerup.power_type == "speed":
            self.effects.add_effect("speed", 8000)
        elif powerup.power_type == "ghost":
            self.effects.add_effect("ghost", 3000)
        elif powerup.power_type == "freeze":
            self.effects.add_effect("freeze", 4000)
    
    def update(self):
        """Оновлення гравця"""
        # Оновлюємо ефекти
        self.effects.update()
        
        # Обробляємо введення
        keys = pygame.key.get_pressed()
        dx = dy = 0
        
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed
        
        if dx or dy:
            self.move(dx, dy)
    
    def draw(self, screen):
        """Малює гравця з ефектами"""
        color = self.color
        
        # Змінюємо колір залежно від ефектів
        if self.effects.has_effect("shield"):
            color = YELLOW
        elif self.effects.has_effect("ghost"):
            color = (self.color[0], self.color[1], self.color[2], 128)  # Прозорий
        
        pygame.draw.rect(screen, color, self.rect)
        
        # Очі
        pygame.draw.circle(screen, WHITE, (self.rect.x + 5, self.rect.y + 5), 2)
        pygame.draw.circle(screen, WHITE, (self.rect.x + 15, self.rect.y + 5), 2)
```

### Удосконалення Level класу:

```python
class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.keys_needed = 2
        self.enemies = []
        self.keys = []
        self.powerups = []  # Нова система
        self.door = None    # Двері для переходу
        self.completed = False
        
        self.create_level_content()
    
    def create_level_content(self):
        """Створює конфігурацію для рівня"""
        
        if self.level_number == 1:
            print(f"Створюємо Рівень {self.level_number}: Базові механіки")
            
            # Вороги
            self.enemies = [
                {"type": "simple", "x": 100, "y": 200, "direction": 1, 
                 "axis": "horizontal", "speed": 1},
                {"type": "simple", "x": 400, "y": 150, "direction": -1, 
                 "axis": "vertical", "speed": 1}
            ]
            
            # Ключі
            self.keys = [
                {"x": 300, "y": 100, "type": "gold"},
                {"x": 600, "y": 300, "type": "silver"}
            ]
            
            # Power-ups (нові!)
            self.powerups = [
                {"x": 250, "y": 250, "type": "speed"},
                {"x": 500, "y": 400, "type": "life"}
            ]
            
            # Двері (нові!)
            self.door = {"x": 750, "y": 280, "keys_required": 2}
            
        elif self.level_number == 2:
            print(f"Створюємо Рівень {self.level_number}: Більше викликів")
            
            self.enemies = [
                {"type": "simple", "x": 80, "y": 180, "direction": 1, 
                 "axis": "horizontal", "speed": 2},
                {"type": "simple", "x": 350, "y": 120, "direction": -1, 
                 "axis": "vertical", "speed": 2},
                {"type": "simple", "x": 550, "y": 400, "direction": 1, 
                 "axis": "horizontal", "speed": 2}
            ]
            
            self.keys = [
                {"x": 250, "y": 350, "type": "red"},
                {"x": 650, "y": 150, "type": "green"}
            ]
            
            self.powerups = [
                {"x": 200, "y": 300, "type": "shield"},
                {"x": 450, "y": 250, "type": "ghost"},
                {"x": 600, "y": 450, "type": "freeze"}
            ]
            
            self.door = {"x": 750, "y": 280, "keys_required": 2}
            
        elif self.level_number == 3:
            print(f"Створюємо Рівень {self.level_number}: Фінальний виклик")
            
            self.enemies = [
                {"type": "simple", "x": 120, "y": 300, "direction": 1, 
                 "axis": "horizontal", "speed": 2},
                {"type": "simple", "x": 450, "y": 200, "direction": -1, 
                 "axis": "vertical", "speed": 2},
                {"type": "chasing", "x": 600, "y": 500, "speed": 1}
            ]
            
            self.keys = [
                {"x": 200, "y": 200, "type": "gold"},
                {"x": 550, "y": 450, "type": "master"}  # Спеціальний ключ
            ]
            
            self.powerups = [
                {"x": 300, "y": 350, "type": "speed"},
                {"x": 400, "y": 300, "type": "shield"},
                {"x": 180, "y": 450, "type": "life"}
            ]
            
            self.door = {"x": 750, "y": 280, "keys_required": 2}
    
    def create_objects(self, maze):
        """Створює реальні об'єкти з конфігурації"""
        # Вороги
        enemy_objects = []
        for enemy_data in self.enemies:
            if enemy_data["type"] == "simple":
                enemy = SimpleEnemy(
                    enemy_data["x"], enemy_data["y"], maze,
                    enemy_data["direction"], enemy_data["axis"], 
                    enemy_data["speed"]
                )
            elif enemy_data["type"] == "chasing":
                enemy = ChasingEnemy(
                    enemy_data["x"], enemy_data["y"], maze, 
                    enemy_data["speed"]
                )
            enemy_objects.append(enemy)
        
        # Ключі
        key_objects = []
        for key_data in self.keys:
            key = Key(key_data["x"], key_data["y"], key_data["type"])
            key_objects.append(key)
        
        # Power-ups (нові!)
        powerup_objects = []
        for powerup_data in self.powerups:
            powerup = PowerUp(powerup_data["x"], powerup_data["y"], 
                            powerup_data["type"])
            powerup_objects.append(powerup)
        
        # Двері (нові!)
        door_object = None
        if self.door:
            door_object = Door(self.door["x"], self.door["y"], 
                             self.door["keys_required"])
        
        return enemy_objects, key_objects, powerup_objects, door_object
```

---

## Тестування нової механіки

### Тест системи дверей:

```python
def test_doors_and_powerups():
    """Тест нової механіки"""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Тест дверей та бонусів")
    clock = pygame.time.Clock()
    
    # Створюємо об'єкти
    maze = Maze()
    player = Player(50, 50, maze)
    
    # Ключі
    keys = [
        Key(300, 100, "gold"),
        Key(600, 300, "silver")
    ]
    
    # Power-ups
    powerups = [
        PowerUp(250, 250, "speed"),
        PowerUp(400, 400, "shield"),
        PowerUp(150, 300, "life")
    ]
    
    # Двері
    door = Door(750, 280, 2)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Оновлення
        player.update()
        
        # Перевірка збору ключів
        for key in keys:
            if not key.collected and key.rect.colliderect(player.rect):
                if key.collect():
                    player.inventory.add_key(key)
        
        # Перевірка збору power-ups
        for powerup in powerups:
            if not powerup.collected and powerup.rect.colliderect(player.rect):
                if powerup.collect():
                    player.collect_powerup(powerup)
        
        # Оновлення дверей
        door.update(player.inventory.get_total_keys())
        
        # Перевірка проходу через двері
        if door.can_pass_through() and door.rect.colliderect(player.rect):
            print("Перехід до наступного рівня!")
            # Тут буде логіка переходу
        
        # Малювання
        maze.draw(screen)
        player.draw(screen)
        
        for key in keys:
            key.draw(screen)
        
        for powerup in powerups:
            powerup.draw(screen)
        
        door.draw(screen)
        
        # UI
        player.inventory.draw_inventory(screen, 10, 150)
        player.effects.draw_effects(screen, 10, 200)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

# Запуск тесту
if __name__ == "__main__":
    test_doors_and_powerups()
```

---

## Домашнє завдання

### Завдання 1: Додай новий power-up
Створи power-up "invisible" що робить гравця невидимим для ворогів на 3 секунди.

### Завдання 2: Покращ двері
Додай анімацію відкриття дверей (поступове зміни кольору).

### Завдання 3: Додаткові ефекти
Придумай та реалізуй свій унікальний power-up.

---

## Підсумок уроку

**Що ми навчилися:**
- Створювати систему дверей з умовами
- Робити інвентар для ключів
- Створювати power-ups з тимчасовими ефектами
- Інтегрувати все в єдину систему

**Наступний урок:** Система анімації та звуків!
