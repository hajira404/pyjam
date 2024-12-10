import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Multiverse Survival Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock for controlling FPS
clock = pygame.time.Clock()
FPS = 60

# Load Fonts
font = pygame.font.Font(pygame.font.match_font('pixel', bold=True), 48)

# Load Background Image
background_img = pygame.image.load("assets/space_bg.png")
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load and Resize Images
player_img = pygame.image.load("assets/astronaut/astronaut1.png")
player_img = pygame.transform.scale(player_img, (50, 50))

# Update the alien images and properties
alien_images = [
    pygame.image.load("assets/aliens/lev1[1].png"),  # Level 1 Alien
    pygame.image.load("assets/aliens/lev1[2].png"),  # Level 2 Alien
    pygame.image.load("assets/aliens/lev2[1].png"),  # Level 2 Alien
    pygame.image.load("assets/aliens/lev2[2].png"),  # Level 2 Alien

]
alien_images = [pygame.transform.scale(img, (50, 50)) for img in alien_images]

# Load Bullet Images (Different types of bullets)

bullet_img = pygame.image.load("assets/guns and bullets/fire_bullet1.png")
bullet_img = pygame.transform.scale(bullet_img, (50, 50))
    
# Heart Image
heart_img = pygame.image.load("assets/heart.png")
heart_img = pygame.transform.scale(heart_img, (40, 40))

# Resources setup
resources = {
    "food": pygame.image.load("assets/resources/food.png"),
    "energy_drink": pygame.image.load("assets/resources/red_energy.png"),
}

# Resize resources
resource_size = (50, 50)
for resource in resources:
    resources[resource] = pygame.transform.scale(resources[resource], resource_size)

resource_positions = {
    key: (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))
    for key in resources
}
collected_resources = {key: 0 for key in resources}

# Load Sounds
pygame.mixer.init()
pygame.mixer.music.load("sounds/thriller_bg_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop background music

shoot_sound = pygame.mixer.Sound("sounds/laserShoot.wav")
shoot_sound.set_volume(0.7)

level_up_sound = pygame.mixer.Sound("sounds/level_up_beep.wav")
level_up_sound.set_volume(0.7)

def opening_scene():
    background_offset = 1
    pygame.mixer.music.play(-1)
    running = True
    while running:
        # Draw infinite scrolling background
        screen.blit(background_img, (0, background_offset))
        screen.blit(background_img, (0, background_offset - SCREEN_HEIGHT))
        background_offset += 1  # Reduced speed
        if background_offset >= SCREEN_HEIGHT:
            background_offset = 0

        # Game Title
        title_text = font.render("Multiverse Survival Game", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)

        # Options
        play_text = font.render("Play", True, WHITE)
        play_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        quit_text = font.render("Quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))

        # Check if the mouse is hovering over the buttons
        mouse_pos = pygame.mouse.get_pos()
        if play_rect.collidepoint(mouse_pos):
            play_text = font.render("Play ", True, (255, 0, 0))  # Highlight in red
        if quit_rect.collidepoint(mouse_pos):
            quit_text = font.render("Quit", True, (255, 0, 0))  # Highlight in red

        screen.blit(play_text, play_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):
                    running = False
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

# Call the opening scene
opening_scene()
# Player setup
player_rect = player_img.get_rect()
player_rect.topleft = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
player_speed = 7
player_running_speed = 10
player_energy = 100
bullets = []
bullet_speed = 10
bullet_direction = "up"
hearts = 5  # Total hearts
max_hearts = 5
hit_cooldown = 0  # Cooldown after losing a heart

# Alien setup
class GameAlien:
    def __init__(self, x, y, speed, damage, health, image):
        self.rect = image.get_rect(topleft=(x, y))
        self.speed = min(2 + speed * 0.1, 4)  # Cap alien speed
        self.damage = damage
        self.health = health
        self.image = image
        self.shots_taken = 0  # Track shots taken by the alien

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
        self.shots_taken += 1
        if self.shots_taken >= 3:  # After 3 shots, the alien dies
            self.health = 0

def spawn_alien(level):
    # Define properties for aliens based on level
    alien_speed = level * 0.5  # Alien speed increases with each level
    alien_damage = 5 + level  # Alien damage increases with each level
    alien_health = 3 + level  # Alien health increases with each level
    
    # Spawn the alien with the appropriate properties
    alien = GameAlien(
        random.randint(0, SCREEN_WIDTH - 50),
        random.randint(0, SCREEN_HEIGHT - 50),
        alien_speed,
        alien_damage,
        alien_health,
        alien_images[level % len(alien_images)]  # Select alien image based on level
    )
    return alien

alien = spawn_alien(0)

# Add custom background
background_img = pygame.image.load("assets/space_bg.png")
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

background_offset = 0
background_speed = 1

# Font setup
font = pygame.font.Font(None, 36)  # Default system font

def draw_text_with_border(text, font, color, border_color, x, y, center=False):
    """Renders text with a border."""
    text_surface = font.render(text, True, color)
    border_surfaces = [
        font.render(text, True, border_color)
        for _ in range(8)
    ]
    offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]

    for border_surface, offset in zip(border_surfaces, offsets):
        screen.blit(border_surface, (x + offset[0], y + offset[1]))

    text_rect = text_surface.get_rect(center=(x, y)) if center else (x, y)
    screen.blit(text_surface, text_rect)

# Game Loop
running = True
level = 1
max_levels = 8  # Limit levels to 8

def display_message(text, duration, fade_out=False):
    """Displays a message in the center of the screen with optional fade-out effect."""
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < duration:
        screen.blit(background_img, (0, background_offset))
        screen.blit(background_img, (0, background_offset - SCREEN_HEIGHT))
        alpha = max(255 - int((pygame.time.get_ticks() - start_time) / duration * 255), 0) if fade_out else 255
        draw_text_with_border(
            text,
            font,
            WHITE,
            (0, 0, 0),  # Black border
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            center=True
        )
        pygame.display.flip()
        clock.tick(FPS)

# Function to display a message on the screen
def display_message_game_over(text, duration, fade_out=False):
    message = font.render(text, True, WHITE)
    message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    screen.blit(message, message_rect)
    pygame.display.flip()

    if fade_out:
        fade_duration = 2000  # 2 seconds fade-out duration
        fade_step = 255 / fade_duration * FPS
        alpha = 255
        
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < fade_duration:
            screen.fill(BLACK)
            alpha -= fade_step
            if alpha < 0:
                alpha = 0
            message.set_alpha(alpha)
            screen.blit(message, message_rect)
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)
    
    pygame.time.delay(duration)

# Scoreboard Variables
collected_food = 0
collected_energy_potions = 0
defeated_aliens = 0

def display_scoreboard():
    background_offset = 1
    pygame.mixer.music.play(-1)
    running = True
    while running:
        # Draw infinite scrolling background
        screen.blit(background_img, (0, background_offset))
        screen.blit(background_img, (0, background_offset - SCREEN_HEIGHT))
        background_offset += 1  # Reduced speed
        if background_offset >= SCREEN_HEIGHT:
            background_offset = 0

        # Create a larger font for the scoreboard title
        title_font = pygame.font.Font(pygame.font.match_font('pixel', bold=True), 72)  # Larger font size

        # Display Scoreboard Title
        scoreboard_title = title_font.render("Game Over - Scoreboard", True, WHITE)
        scoreboard_title_rect = scoreboard_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(scoreboard_title, scoreboard_title_rect)

        # Display collected food, energy drinks, and defeated aliens
        food_text = font.render(f"Food Collected: {collected_food}", True, WHITE)
        food_text_rect = food_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        screen.blit(food_text, food_text_rect)

        energy_text = font.render(f"Energy Potions: {collected_energy_potions}", True, WHITE)
        energy_text_rect = energy_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(energy_text, energy_text_rect)

        alien_text = font.render(f"Aliens Defeated: {defeated_aliens}", True, WHITE)
        alien_text_rect = alien_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        screen.blit(alien_text, alien_text_rect)

        play_text = font.render("Play Again", True, WHITE)
        play_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        quit_text = font.render("Quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 180))

        # Check if the mouse is hovering over the buttons
        mouse_pos = pygame.mouse.get_pos()
        if play_rect.collidepoint(mouse_pos):
            play_text = font.render("Play Again", True, (255, 0, 0))  # Highlight in red
        if quit_rect.collidepoint(mouse_pos):
            quit_text = font.render("Quit", True, (255, 0, 0))  # Highlight in red

        # Draw the buttons
        screen.blit(play_text, play_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        # Wait for player's choice (Play Again or Quit)
        waiting = True
        while waiting:
           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if play_rect.collidepoint(mouse_pos):
                        return "play"
                    elif quit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        exit()

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
            # Bullet Movement
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

    # Draw Player with Flashing Effect if on Cooldown
    if hit_cooldown > pygame.time.get_ticks():
        if (pygame.time.get_ticks() // 200) % 2 == 0:  # Flash every 200ms
            screen.blit(player_img, player_rect.topleft)
    else:
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

    # Check Player-Alien Collision
    if player_rect.colliderect(alien.rect):
        if pygame.time.get_ticks() > hit_cooldown:
            hearts -= 1
            print(f"Hit! Hearts remaining: {hearts}")
            hit_cooldown = pygame.time.get_ticks() + 1000  # 1-second cooldown
            if hearts <= 0:
                pygame.mixer.music.stop()
                print("Game Over! You failed to survive.")
                result = display_scoreboard()  # Show scoreboard when the player loses

                if result == "play":
                # Reset the game state if the player chooses to play again
                    level = 0
                    hearts = max_hearts
                    collected_food = 0
                    collected_energy_potions = 0
                    defeated_aliens = 0
                    player_energy = 100
                    player_rect.topleft = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    alien = spawn_alien(level)
                    pygame.mixer.music.play(-1)  # Restart background music
                    running = True  # Restart the game loop
                else:
                # Player chose to quit, exit the game
                    pygame.quit()
                    exit()

    # Check for Alien Defeat
    for bullet in bullets[:]:
        if bullet.colliderect(alien.rect):
            alien.take_damage()  # Register a shot
            bullets.remove(bullet)
            if alien.health <= 0:
                level_up_sound.play()  # Play level-up sound
                defeated_aliens += 1
                print(f"Alien defeated! Level {level + 1} complete.")
                level += 1
                hearts = max_hearts  # Refresh hearts to full
                if level < max_levels:
                    # Display the level transition message
                    display_message(f"Alien Defeated!! Level {level}", 1000, fade_out=True)
                    alien = spawn_alien(level)  # Reset alien for the new level
                    alien.health = 3 + level   # Reset alien health based on the new level
                else:
                    result = display_scoreboard()
                    if result == "play":
                    # Reset the game state if the player chooses to play again
                        level = 0
                        hearts = max_hearts
                        collected_food = 0
                        collected_energy_potions = 0
                        defeated_aliens = 0
                        player_energy = 100
                        player_rect.topleft = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                        alien = spawn_alien(level)
                        pygame.mixer.music.play(-1)  # Restart background music
                        running = True  # Restart the game loop
                    else:
                    # Player chose to quit, exit the game
                        pygame.quit()
                        exit()
                    


    # Resource collection (slow rotation and subtle movement)
    for resource, pos in resource_positions.items():
        float_x = math.sin(pygame.time.get_ticks() * 0.001) * 0.5
        float_y = math.cos(pygame.time.get_ticks() * 0.001) * 0.5
        new_pos = (pos[0] + float_x, pos[1] + float_y)
        
        resource_surface = pygame.transform.rotate(resources[resource], pygame.time.get_ticks() * 0.05)  # Slow rotation
        resource_rect = resource_surface.get_rect(center=new_pos)
        screen.blit(resource_surface, resource_rect.topleft)
        
        if player_rect.colliderect(resource_rect):
            collected_resources[resource] += 1
            resource_positions[resource] = (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))
            if resource == "food":
                hearts = min(hearts + 1, max_hearts)  # Regain one heart
                collected_food += 1
            elif resource == "energy_drink":
                player_speed += 0.1
                collected_energy_potions += 1

    # Draw Hearts
    for i in range(hearts):
        screen.blit(heart_img, (10 + i * 50, 10))
    # Draw Collected Resources Below Hearts
    food_text = f"Food: {collected_resources['food']}"
    energy_text = f"Energy: {collected_resources['energy_drink']}"
    draw_text_with_border(food_text, font, WHITE, BLACK, 10, 60)
    draw_text_with_border(energy_text, font, WHITE, BLACK, 10, 100)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()