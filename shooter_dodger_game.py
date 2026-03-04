import pygame
import random

# --- Configuration & Colors ---
WIDTH, HEIGHT = 600, 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0,0,0)

pygame.init()
screen = pygame.display.set_mode ((WIDTH, HEIGHT))
pygame.display.set_caption ("Square Dodger Game: Restart Edition")
clock = pygame.time.Clock()

# --- Fonts ---
font = pygame.font.SysFont ("monospace", 35)
big_font = pygame.font.SysFont("monospace", 60)

# --- Global Game Variables ---
PLAYER_SIZE = 65
ENEMY_SIZE = 50
BULLET_WIDTH = 25
BULLET_HEIGHT = 25

def reset_game():
    """Resets all game variables to start fresh"""
    global player_pos, bullets, enemies, score, game_over, enemy_speed
    player_pos = [WIDTH // 2, HEIGHT - PLAYER_SIZE - 10]
    bullets = []
    enemies = []
    score = 0
    enemy_speed = 5
    game_over = False

# Initialize the game variables
reset_game()
player_speed = 8
spawn_timer = 5
running = True

# --- Main Game Loop ---
while running:
    screen.fill(BLACK)

    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # If game is playing, allow shooting
            if event.key == pygame.K_SPACE and not game_over:
                new_bullet_x = player_pos[0] + (PLAYER_SIZE // 2) - (BULLET_WIDTH // 2)
                new_bullet_y = player_pos[1]
                bullets.append([new_bullet_x, new_bullet_y])

            # If game is over, allow restart
            if event.key == pygame.K_r and gama_over:
                reset_game()

    if not game_over:
        # 2. Player Movement
       keys = pygame.key.get_pressed()
       if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_pos[0] > 0:
           player_pos[0] -= player_speed
       if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_pos[0] < WIDTH - PLAYER_SIZE:
            player_pos[0] += player_speed

       # 3. Enemy Spawning
       spawn_timer += 1
       if spawn_timer > 30:
           x_pos = random.randint(0, WIDTH - ENEMY_SIZE)
           enemies.append([x_pos, -ENEMY_SIZE])
           spawn_timer = 0
           # Gradually increase difficulty
           if score > 0 and score % 50 == 0:
               enemy_speed += 0.01

       # 4. Movement Logic
       for b in bullets[:]:
           b[1] += -12
           if b[1] < -BULLET_HEIGHT: bullets.remove(b)

       for e in enemies[:]:
           e[1] += enemy_speed
           if e[1] > HEIGHT:
               enemies.remove(e)
               score += 1

       # 5. Collision Detection
       player_rect = pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE)
       for e in enemies[:]:
           enemy_rect = pygame.Rect(e[0], e[1], ENEMY_SIZE, ENEMY_SIZE)

           if enemy_rect.colliderect(player_rect):
               game_over = True # Switch to Game Over state

           for b in bullets[:]:
               bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
               if enemy_rect.colliderect(bullet_rect):
                   if e in enemies: enemies.remove(e)
                   if b in bullets: bullets.remove(b)
                   score += 5

    # 6. Drawing
    # Draw Player
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE))
   # Draw Bullets
    for b in bullets:
         pygame.draw.rect(screen, GREEN, (b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT))
     # Draw Enemies
    for e in enemies:
        pygame.draw.rect(screen, RED, (e[0], e[1], ENEMY_SIZE, ENEMY_SIZE))

     # Draw Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

     # 7. Game Over Overlay
    if game_over:
         # Create a dark overlay to make text pop
         overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
         overlay.fill((0, 0, 0, 150)) # Transparent black
         screen.blit(overlay, (0, 0))

         msg = big_font.render("GAME OVER", True, RED)
         restart_msg = font.render("Press 'R' to Restart", True, WHITE)

         # Center the text
         screen.blit(msg, (WIDTH//2 - 160, HEIGHT//2 - 50))
         screen.blit(restart_msg, (WIDTH//2 - 190, HEIGHT//2 - 20))

    pygame.display.update()
    clock.tick(60)

pygame.quit()