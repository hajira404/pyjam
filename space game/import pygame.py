import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stranded Astronaut Survival")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock
clock = pygame.time.Clock()

# Player setup
player_size = 50
player = pygame.Rect(WIDTH // 2, HEIGHT // 2, player_size, player_size)
player_speed = 5

# World properties
tile_size = 800  # Chunk size for the infinite map
world_offset = [0, 0]  # Camera position
chunks = {}  # Stores generated chunks
inventory = 0
health = 100

# Resources and aliens
def generate_objects(center_x, center_y):
    resources = []
    aliens = []
    for _ in range(10):  # Generate 10 resources
        rx = random.randint(center_x - tile_size // 2, center_x + tile_size // 2)
        ry = random.randint(center_y - tile_size // 2, center_y + tile_size // 2)
        resources.append(pygame.Rect(rx, ry, 20, 20))
    for _ in range(3):  # Generate 3 aliens
        ax = random.randint(center_x - tile_size // 2, center_x + tile_size // 2)
        ay = random.randint(center_y - tile_size // 2, center_y + tile_size // 2)
        aliens.append(pygame.Rect(ax, ay, 30, 30))
    return resources, aliens

# Load initial chunk
starting_chunk = (0, 0)
chunks[starting_chunk] = generate_objects(0, 0)

# Font
font = pygame.font.Font(None, 36)

# Draw the game elements
def draw_game():
    screen.fill(BLACK)
    
    # Visible chunks
    visible_chunks = []
    for cx in range(-1, 2):
        for cy in range(-1, 2):
            chunk_key = (cx + world_offset[0] // tile_size, cy + world_offset[1] // tile_size)
            if chunk_key not in chunks:
                chunks[chunk_key] = generate_objects(chunk_key[0] * tile_size, chunk_key[1] * tile_size)
            visible_chunks.append(chunk_key)
            resources, aliens = chunks[chunk_key]
            for resource in resources:
                pygame.draw.rect(screen, GREEN, resource.move(-world_offset[0], -world_offset[1]))
            for alien in aliens:
                pygame.draw.rect(screen, RED, alien.move(-world_offset[0], -world_offset[1]))
    
    # Draw the player
    pygame.draw.rect(screen, BLUE, player)
    
    # Display inventory and health
    inventory_text = font.render(f"Resources: {inventory}", True, WHITE)
    health_text = font.render(f"Health: {health}", True, WHITE)
    screen.blit(inventory_text, (10, 10))
    screen.blit(health_text, (10, 50))

    return visible_chunks

# Handle collisions
def handle_collisions(visible_chunks):
    global inventory, health
    
    for chunk_key in visible_chunks:
        resources, aliens = chunks[chunk_key]
        
        # Resource collection
        for resource in resources[:]:
            if player.colliderect(resource.move(-world_offset[0], -world_offset[1])):
                resources.remove(resource)
                inventory += 1
        
        # Alien damage
        for alien in aliens:
            if player.colliderect(alien.move(-world_offset[0], -world_offset[1])):
                health -= 1  # Damage on collision

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Movement controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        world_offset[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        world_offset[0] += player_speed
    if keys[pygame.K_UP]:
        world_offset[1] -= player_speed
    if keys[pygame.K_DOWN]:
        world_offset[1] += player_speed

    # Draw the game and handle collisions
    visible_chunks = draw_game()
    handle_collisions(visible_chunks)
    
    # End game if health is zero
    if health <= 0:
        print("Game Over! You survived by collecting", inventory, "resources.")
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()