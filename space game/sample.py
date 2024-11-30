import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Explorer - Cat-astrophe Quest")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load assets
player_img = pygame.image.load("spaceship.png")
player_img = pygame.transform.scale(player_img, (50, 50))

cat_img = pygame.image.load("alien4.png")
cat_img = pygame.transform.scale(cat_img, (40, 40))

background_img = pygame.image.load("space_bg2.png")
background_img = pygame.transform.scale(background_img, (800, 600))
# Game variables
player = pygame.Rect(WIDTH // 2, HEIGHT // 2, 50, 50)
player_speed = 5

cat = pygame.Rect(random.randint(0, WIDTH - 40), random.randint(0, HEIGHT - 40), 40, 40)
cat_velocity = [random.choice([-2, 2]), random.choice([-2, 2])]  # Random drift in zero gravity

rescued = False

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Functions
def draw_window():
    screen.blit(background_img, (0, 0))
    screen.blit(player_img, (player.x, player.y))

    if not rescued:
        screen.blit(cat_img, (cat.x, cat.y))

    # Draw game status
    if rescued:
        rescue_text = font.render("You rescued the space cat! Mission Complete!", True, WHITE)
        screen.blit(rescue_text, (WIDTH // 2 - rescue_text.get_width() // 2, HEIGHT // 2 - 20))
    else:
        quest_text = font.render("Rescue the space cat!", True, WHITE)
        screen.blit(quest_text, (10, 10))

    pygame.display.update()

def handle_movement(keys):
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.x < WIDTH - player.width:
        player.x += player_speed
    if keys[pygame.K_UP] and player.y > 0:
        player.y -= player_speed
    if keys[pygame.K_DOWN] and player.y < HEIGHT - player.height:
        player.y += player_speed

def update_cat():
    cat.x += cat_velocity[0]
    cat.y += cat_velocity[1]

    # Bounce off walls
    if cat.x <= 0 or cat.x >= WIDTH - cat.width:
        cat_velocity[0] *= -1
    if cat.y <= 0 or cat.y >= HEIGHT - cat.height:
        cat_velocity[1] *= -1

# Main loop
def main():
    global rescued
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        handle_movement(keys)

        if not rescued:
            update_cat()
            if player.colliderect(cat):
                rescued = True

        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()