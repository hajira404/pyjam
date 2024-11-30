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
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Clock for controlling FPS
clock = pygame.time.Clock()
FPS = 60

# Load and Resize Images
player_img = pygame.image.load("assets/astronaut.png")
player_img = pygame.transform.scale(player_img, (50, 50))  # Resizing the player image

alien_images = [
    pygame.image.load("assets/alien1.png"),  # Add new alien images here
    pygame.image.load("assets/alien2.png"),
    pygame.image.load("assets/alien3.png"),
]

# Rescale alien images
alien_images = [pygame.transform.scale(img, (50, 50)) for img in alien_images]

bullet_img = pygame.image.load("assets/bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (10, 20))  # Resizing bullet image

resources = {
    "food": pygame.image.load("assets/food.png"),
    "oxygen": pygame.image.load("assets/oxygen.png"),
    "energy_drink": pygame.image.load("assets/energy_drink.png"),
}

for resource in resources:
    resources[resource] = pygame.transform.scale(resources[resource], (32, 32))  # Resizing resource icons

# Player setup
player_rect = player_img.get_rect()
player_rect.topleft = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
player_speed = 7
player_running_speed = 10
player_health = 10000
player_energy = 100
weapon_equipped = None

# Bullet setup
bullets = []
bullet_speed = 10
bullet_direction = "up"  # Default shooting direction is upwards

# Alien setup
class GameAlien:
    def __init__(self, x, y, speed, damage, health, image):
        self.rect = image.get_rect(topleft=(x, y))
        self.speed = speed
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

# Initialize alien (only one per level)
def spawn_alien(level):
    alien = GameAlien(
        random.randint(0, SCREEN_WIDTH - 50),
        random.randint(0, SCREEN_HEIGHT - 50),
        random.randint(1 + level, 3 + level),  # Increased speed with each level
        random.randint(5, 10),
        3 + level,  # Increased health with each level
        alien_images[level % len(alien_images)]  # Change alien image per level
    )
    return alien

alien = spawn_alien(0)  # Start with level 0 alien

# Resource setup
resource_positions = {
    "food": (
        random.randint(50, SCREEN_WIDTH - 50),
        random.randint(50, SCREEN_HEIGHT - 50),
    ),
    "oxygen": (
        random.randint(50, SCREEN_WIDTH - 50),
        random.randint(50, SCREEN_HEIGHT - 50),
    ),
    "energy_drink": (
        random.randint(50, SCREEN_WIDTH - 50),
        random.randint(50, SCREEN_HEIGHT - 50),
    ),
}
collected_resources = {"food": 0, "oxygen": 0, "energy_drink": 0}

# Multiverse setup
universes = ["Retro Area", "Car World", "Alien Wasteland"]
current_universe = 0
universe_cooldown = 300  # Cooldown in frames (~5 seconds)
universe_timer = 0

# Infinite space background setup
background_img = pygame.image.load("assets/space_bg.png")
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

background_offset = 0  # Used for moving background infinitely

# Game Loop
running = True
level = 0  # Start at level 0
while running:
    screen.fill(BLACK)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Shooting bullet based on movement direction
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
        bullet_direction = "up"  # Shooting up
    if keys[pygame.K_DOWN]:
        player_rect.y += speed
        bullet_direction = "up"  # Shooting up
    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
        bullet_direction = "left"  # Shooting left
    if keys[pygame.K_RIGHT]:
        player_rect.x += speed
        bullet_direction = "right"  # Shooting right

    # Prevent player from going out of bounds
    player_rect.clamp_ip(screen.get_rect())

    # Draw Player
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

    # Alien-Player Collision (Attack)
    if player_rect.colliderect(alien.rect):
        player_health -= alien.damage / FPS  # Damage applied gradually

    # Bullet-Alien Collision
    for bullet in bullets[:]:
        if bullet.colliderect(alien.rect):
            alien.take_damage(10)  # Bullet damage
            bullets.remove(bullet)
            if alien.health <= 0:
                print(f"Alien defeated! Level {level + 1} complete.")
                level += 1
                alien = spawn_alien(level)  # Spawn new alien for the next level

    # Resource collection
    for resource, pos in resource_positions.items():
        resource_rect = pygame.Rect(pos[0], pos[1], 32, 32)
        screen.blit(resources[resource], resource_rect.topleft)
        if player_rect.colliderect(resource_rect):
            collected_resources[resource] += 1
            resource_positions[resource] = (
                random.randint(50, SCREEN_WIDTH - 50),
                random.randint(50, SCREEN_HEIGHT - 50),
            )
            if resource == "food":
                player_health = min(player_health + 10, 10000)
            elif resource == "oxygen":
                player_energy = min(player_energy + 10, 100)
            elif resource == "energy_drink":
                player_speed += 1  # Increase player speed

    # Update the infinite space background (scrolling effect)
    background_offset += 1
    if background_offset >= SCREEN_WIDTH:
        background_offset = 0

    # Draw Resources and UI
    font = pygame.font.Font(None, 36)
    health_text = font.render(f"Health: {int(player_health)}", True, WHITE)
    energy_text = font.render(f"Energy: {int(player_energy)}", True, WHITE)
    screen.blit(health_text, (10, 10))
    screen.blit(energy_text, (10, 50))

    resource_text = font.render(
        f"Food: {collected_resources['food']} | Oxygen: {collected_resources['oxygen']} | Energy: {collected_resources['energy_drink']}",
        True,
        WHITE,
    )
    screen.blit(resource_text, (10, 90))

    # Check for Game Over
    if player_health <= 0:
        print("Game Over! You failed to survive.")
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()