import pygame, time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабиринт")

player = pygame.Rect(50, 50, 20, 20)
enemy = pygame.Rect(200, 200, 20, 20)
collectibles = [pygame.Rect(100, 100, 20, 20), pygame.Rect(300, 150, 20, 20)]
walls = [pygame.Rect(150, 0, 20, 500), pygame.Rect(400, 100, 20, 500)]

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
inventory = []
lives = 3
score = 0
enemy_dir = 1
last_hit_time = 0

running = True
while running:
    screen.fill((30, 30, 30))
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_LEFT]: dx = -3
    if keys[pygame.K_RIGHT]: dx = 3
    if keys[pygame.K_UP]: dy = -3
    if keys[pygame.K_DOWN]: dy = 3

    new_player = player.move(dx, dy)
    if not any(new_player.colliderect(w) for w in walls):
        player = new_player

    enemy.y += int(2 * enemy_dir)
    if any(enemy.colliderect(w) for w in walls):
        enemy_dir *= -1
        enemy.y += int(2 * enemy_dir)

    if player.colliderect(enemy) and time.time() - last_hit_time > 1:
        lives -= 1
        last_hit_time = time.time()

    for item in collectibles[:]:
        if player.colliderect(item):
            collectibles.remove(item)
            inventory.append("Item")
            score += 1

    pygame.draw.rect(screen, (255, 0, 0), player)
    pygame.draw.rect(screen, (0, 0, 255), enemy)
    for wall in walls:
        pygame.draw.rect(screen, (100, 100, 100), wall)
    for item in collectibles:
        pygame.draw.rect(screen, (0, 255, 0), item)

    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
    screen.blit(font.render(f"Lives: {lives}", True, (255, 255, 255)), (10, 40))
    screen.blit(font.render("Inventory:", True, (255, 255, 255)), (600, 10))
    for i, name in enumerate(inventory):
        screen.blit(font.render(name, True, (255, 255, 255)), (600, 40 + i * 30))

    if lives <= 0 or score == 2:
        end_text = "You Win!" if score == 2 else "Game Over"
        text = font.render(end_text, True, (255, 255, 0))
        screen.blit(text, (WIDTH//2 - 50, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        break

    pygame.display.flip()

pygame.quit()
