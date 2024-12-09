import pygame
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Multiverse Survival Game")

# Colors
WHITE = (255, 255, 255)

# Clock for controlling FPS
clock = pygame.time.Clock()
FPS = 60

# Load and Resize Images
player_img = pygame.image.load("assets/astronaut.png")
player_img = pygame.transform.scale(player_img, (50, 50))

alien_images = [
    pygame.image.load("assets/alien1.png"),
    pygame.image.load("assets/alien2.png"),
    pygame.image.load("assets/alien3.png"),
]
alien_images = [pygame.transform.scale(img, (50, 50)) for img in alien_images]

bullet_img = pygame.image.load("assets/bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

resources = {
    "food": pygame.image.load("assets/food.png"),
    "oxygen": pygame.image.load("assets/oxygen.png"),
    "energy_drink": pygame.image.load("assets/energy_drink.png"),
}

for resource in resources:
    resources[resource] = pygame.transform.scale(resources[resource], (32, 32))

# Load Sounds
pygame.mixer.init()
pygame.mixer.music.load("sounds/thriller_bg_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop background music

shoot_sound = pygame.mixer.Sound("sounds/laserShoot.wav")
shoot_sound.set_volume(0.7)

level_up_sound = pygame.mixer.Sound("sounds/level_up_beep.wav")
level_up_sound.set_volume(0.7)

game_over_sound = pygame.mixer.Sound("sounds/game_over.mp3")
game_over_sound.set_volume(0.7)
# Player setup
player_rect = player_img.get_rect()
player_rect.topleft = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
player_speed = 7
player_running_speed = 10
player_health = 100
player_energy = 100
bullets = []
bullet_speed = 10
bullet_direction = "up"

# Alien setup
class GameAlien:
    def __init__(self, x, y, speed, damage, health, image):
        self.rect = image.get_rect(topleft=(x, y))
        self.speed = min(2 + speed * 0.1, 4)  # Cap alien speed
        self.damage = damage
        self.health = health
        self.image = image

    def move_towards_player(self):
        if player_rect.x < self.rect.x:
            self.rect.x -= self.speed
        elif player_rect.x > self.rect.x:
            self.rect.x += self.speed
        if player_rect.y < self.rect.y:
            self.rect.y -= self.speed
        elif player_rect.y > self.rect.y:
            self.rect.y += self.speed

    def take_damage(self, damage):
        self.health -= damage

def spawn_alien(level):
    alien = GameAlien(
        random.randint(0, SCREEN_WIDTH - 50),
        random.randint(0, SCREEN_HEIGHT - 50),
        level,
        5 + level,
        3 + level,
        alien_images[level % len(alien_images)]
    )
    return alien

alien = spawn_alien(0)

# Resource setup
resource_positions = {key: (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)) for key in resources}
collected_resources = {key: 0 for key in resources}

# Add custom background
background_img = pygame.image.load("assets/space_bg.png")
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

background_offset = 0

# Game Loop
running = True
level = 0
max_levels = 8  # Limit levels to 8

while running:
    # Draw infinite background
    screen.blit(background_img, (0, background_offset))
    screen.blit(background_img, (0, background_offset - SCREEN_HEIGHT))
    background_offset += 2
    if background_offset >= SCREEN_HEIGHT:
        background_offset = 0

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            shoot_sound.play()  # Play shooting sound
            if bullet_direction == "up":
                bullet_rect = bullet_img.get_rect(center=(player_rect.centerx, player_rect.top))
            elif bullet_direction == "left":
                bullet_rect = bullet_img.get_rect(center=(player_rect.left, player_rect.centery))
            elif bullet_direction == "right":
                bullet_rect = bullet_img.get_rect(center=(player_rect.right, player_rect.centery))
            bullets.append(bullet_rect)

    # Player Movement
    keys = pygame.key.get_pressed()
    speed = player_running_speed if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and player_energy > 0 else player_speed
    if speed == player_running_speed:
        player_energy -= 0.1
    if keys[pygame.K_UP]:
        player_rect.y -= speed
        bullet_direction = "up"
    if keys[pygame.K_DOWN]:
        player_rect.y += speed
        bullet_direction = "up"
    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
        bullet_direction = "left"
    if keys[pygame.K_RIGHT]:
        player_rect.x += speed
        bullet_direction = "right"

    player_rect.clamp_ip(screen.get_rect())
    screen.blit(player_img, player_rect.topleft)

    # Bullet Movement
    for bullet in bullets[:]:
        if bullet_direction == "up":
            bullet.y -= bullet_speed
        elif bullet_direction == "left":
            bullet.x -= bullet_speed
        elif bullet_direction == "right":
            bullet.x += bullet_speed

        screen.blit(bullet_img, bullet)
        if bullet.top < 0 or bullet.left < 0 or bullet.right > SCREEN_WIDTH:
            bullets.remove(bullet)

    # Alien Behavior
    alien.move_towards_player()
    screen.blit(alien.image, alien.rect.topleft)
    if player_rect.colliderect(alien.rect):
        player_health -= alien.damage / FPS

    for bullet in bullets[:]:
        if bullet.colliderect(alien.rect):
            alien.take_damage(10)
            bullets.remove(bullet)
            if alien.health <= 0:
                print(f"Alien defeated! Level {level + 1} complete.")
                level += 1
                if level < max_levels:
                    alien = spawn_alien(level)
                else:
                    print("Congratulations! You completed all levels.")
                    running = False

    # Resource collection
    for resource, pos in resource_positions.items():
        resource_rect = pygame.Rect(pos[0], pos[1], 32, 32)
        screen.blit(resources[resource], resource_rect.topleft)
        if player_rect.colliderect(resource_rect):
            level_up_sound.play()  # Play level-up sound
            collected_resources[resource] += 1
            resource_positions[resource] = (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))
            if resource == "food":
                player_health = min(player_health + 10, 100)
            elif resource == "oxygen":
                player_energy = min(player_energy + 10, 100)
            elif resource == "energy_drink":
                player_speed += 0.1

    # UI
    font = pygame.font.Font(None, 36)
    health_text = font.render(f"Health: {int(player_health)}", True, WHITE)
    energy_text = font.render(f"Energy: {int(player_energy)}", True, WHITE)
    screen.blit(health_text, (10, 10))
    screen.blit(energy_text, (10, 50))

    if player_health <= 0:
        game_over_sound.play()
        pygame.mixer.music.stop()
        print("Game Over! You failed to survive.")
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()