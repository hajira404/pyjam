import pygame
import random
from PIL import Image

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
def fix_image(file_path):
    img = Image.open(file_path)
    img.save(file_path)

# Fix images to remove incorrect ICC profiles
fix_image("assets/astronaut.png")
fix_image("assets/alien3.png")
fix_image("assets/space_bg.png")
fix_image("assets/planet.png")
fix_image("assets/food.png")
fix_image("assets/oxygen.png")
fix_image("assets/energy_drink.png")
#fix_image("assets/special_item.png")

# Re-load images after fixing ICC profiles
player_img = pygame.image.load("assets/astronaut.png")
player_img = pygame.transform.scale(player_img, (50, 50))

alien_img = pygame.image.load("assets/alien3.png")
alien_img = pygame.transform.scale(alien_img, (50, 50))

bullet_img = pygame.image.load("assets/bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

planet_bg = pygame.image.load("assets/planet.png")
planet_bg = pygame.transform.scale(planet_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

space_bg = pygame.image.load("assets/space_bg.png")
space_bg = pygame.transform.scale(space_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

resources = {
    "food": pygame.image.load("assets/food.png"),
    "oxygen": pygame.image.load("assets/oxygen.png"),
    "energy_drink": pygame.image.load("assets/energy_drink.png"),
    #"special_item": pygame.image.load("assets/special_item.png"),
}

for resource in resources:
    resources[resource] = pygame.transform.scale(resources[resource], (32, 32))

# Player setup
player_rect = player_img.get_rect()
player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
player_speed = 5
player_running_speed = 8
player_health = 100
player_energy = 100
bullets = []
bullet_speed = 10

# Alien setup
class GameAlien:
    def __init__(self, x, y, speed, damage):
        self.rect = alien_img.get_rect(topleft=(x, y))
        self.speed = speed
        self.damage = damage
        self.health = 3  # Each alien takes 3 hits

    def move_towards_player(self):
        if player_rect.x < self.rect.x:
            self.rect.x -= self.speed
        elif player_rect.x > self.rect.x:
            self.rect.x += self.speed
        if player_rect.y < self.rect.y:
            self.rect.y -= self.speed
        elif player_rect.y > self.rect.y:
            self.rect.y += self.speed

    def take_damage(self):
        self.health -= 1

aliens = []

# Game variables
collected_resources = {"food": 0, "oxygen": 0, "energy_drink": 0, "special_item": 0}
current_bg = space_bg
inside_planet = False
planet_resources = []
planet_aliens = []
found_planet = False

def spawn_aliens(count, speed, damage):
    return [GameAlien(random.randint(50, SCREEN_WIDTH - 100), 
                      random.randint(50, SCREEN_HEIGHT - 100), 
                      speed, damage) for _ in range(count)]

def spawn_resources():
    positions = []
    for _ in range(4):  # Spawn 4 random resources
        positions.append(pygame.Rect(random.randint(50, SCREEN_WIDTH - 50),
                                     random.randint(50, SCREEN_HEIGHT - 50),
                                     32, 32))
    return positions

# Main Game Loop
running = True
while running:
    screen.blit(current_bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and inside_planet:
            bullet_rect = bullet_img.get_rect(midtop=player_rect.midtop)  # Create a Rect for the bullet
            bullets.append(bullet_rect)  # Add the bullet to the list

    # Movement
    keys = pygame.key.get_pressed()
    speed = player_running_speed if keys[pygame.K_LSHIFT] else player_speed
    if keys[pygame.K_UP]:
        player_rect.y -= speed
    if keys[pygame.K_DOWN]:
        player_rect.y += speed
    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += speed
    player_rect.clamp_ip(screen.get_rect())

    # Bullets
    for bullet in bullets[:]:
        bullet = bullet.move(0, -bullet_speed)  # Move the bullet upwards
        screen.blit(bullet_img, bullet)  # Draw the bullet
        bullets = [b for b in bullets if b.top > 0]  # Remove bullets that go off-screen

    # Alien movement
    for alien in aliens:
        alien.move_towards_player()
        screen.blit(alien_img, alien.rect.topleft)

    # Planet landing
    if not inside_planet and not found_planet:
        # Simulate finding a planet
        found_planet = player_rect.y < 50

    if found_planet and not inside_planet:
        current_bg = planet_bg
        inside_planet = True
        planet_aliens = spawn_aliens(5, 2, 10)
        planet_resources = spawn_resources()
        print("Planet found!")

    if inside_planet:
        for resource in planet_resources:
            screen.blit(resources["food"], resource.topleft)

    # Draw player
    screen.blit(player_img, player_rect.topleft)

    # Draw aliens
    for alien in aliens:
        alien.move_towards_player()
        screen.blit(alien_img, alien.rect.topleft)

    # Draw resources if inside planet
    if inside_planet:
        for resource in planet_resources:
            screen.blit(resources["food"], resource.topleft)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()