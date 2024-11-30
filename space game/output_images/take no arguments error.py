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

alien_img = pygame.image.load("assets/alien1.png")
alien_img = pygame.transform.scale(alien_img, (50, 50))  # Resizing the alien image

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
player_speed = 5
player_running_speed = 8
player_health = 100
player_energy = 100
weapon_equipped = None

# Alien setup
class GameAlien:
    def _init_(self, x, y, speed, damage):
        self.rect = alien_img.get_rect(topleft=(x, y))
        self.speed = speed
        self.damage = damage

    def move_towards_player(self):
        if player_rect.x < self.rect.x:
            self.rect.x -= self.speed
        elif player_rect.x > self.rect.x:
            self.rect.x += self.speed
        if player_rect.y < self.rect.y:
            self.rect.y -= self.speed
        elif player_rect.y > self.rect.y:
            self.rect.y += self.speed

aliens = [GameAlien(random.randint(0, SCREEN_WIDTH - 50), 
                    random.randint(0, SCREEN_HEIGHT - 50), 
                    random.randint(1, 3), 
                    random.randint(5, 10)) for _ in range(5)]

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

# Game Loop
running = True
while running:
    screen.fill(BLACK)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player Movement
    keys = pygame.key.get_pressed()
    speed = player_running_speed if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and player_energy > 0 else player_speed
    if speed == player_running_speed:
        player_energy -= 0.1
    if keys[pygame.K_UP]:
        player_rect.y -= speed
    if keys[pygame.K_DOWN]:
        player_rect.y += speed
    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += speed

    # Prevent player from going out of bounds
    player_rect.clamp_ip(screen.get_rect())

    # Draw Player
    screen.blit(player_img, player_rect.topleft)

    # Alien Behavior
    for alien in aliens:
        alien.move_towards_player()
        screen.blit(alien_img, alien.rect.topleft)

        # Alien-Player Collision (Attack)
        if player_rect.colliderect(alien.rect):
            player_health -= alien.damage / FPS  # Damage applied gradually

    # Draw Resources and collect
    for resource, pos in resource_positions.items():
        screen.blit(resources[resource], pos)
        resource_rect = pygame.Rect(pos[0], pos[1], 32, 32)  # Assuming 32x32 resource icons
        if player_rect.colliderect(resource_rect):
            collected_resources[resource] += 1
            resource_positions[resource] = (
                random.randint(50, SCREEN_WIDTH - 50),
                random.randint(50, SCREEN_HEIGHT - 50),
            )
            if resource == "food":
                player_health = min(player_health + 10, 100)
            elif resource == "oxygen":
                player_energy = min(player_energy + 10, 100)

    # Multiverse Switch
    if keys[pygame.K_m] and universe_timer == 0:
        current_universe = (current_universe + 1) % len(universes)
        universe_timer = universe_cooldown
        print(f"Switched to: {universes[current_universe]}")

    if universe_timer > 0:
        universe_timer -= 1

    # UI: Health, Energy, and Resources
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

    universe_text = font.render(f"Current Universe: {universes[current_universe]}", True, GREEN)
    screen.blit(universe_text, (10, 130))

    # Check for Game Over
    if player_health <= 0:
        print("Game Over! You failed to survive.")
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()