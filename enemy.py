import pygame, random, time, math

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