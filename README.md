# Multiverse Survival Game

## Overview

The **Multiverse Survival Game** is an action-packed game where players take on the role of an astronaut navigating through a multiverse filled with alien enemies, collecting resources, and facing challenges to survive. The player must defeat aliens, collect resources, and survive multiple levels while avoiding collisions with alien creatures and other obstacles.

---

## Features

- **Multiple Levels**: The game has multiple levels, each increasing in difficulty.
- **Alien Enemies**: Different types of aliens appear on each level, each with unique behaviors and health.
- **Bullet Types**: The player can use different types of bullets based on the current level, including fire, ice, and gravity bullets.
- **Resource Collection**: Collect resources like food and energy drinks to survive and improve player stats.
- **Hearts**: Player starts with a certain number of hearts and loses them when they collide with aliens.
- **Level Transitions**: As the player defeats aliens, they move to the next level with increasing difficulty.
- **Scoreboard**: After the game ends, a scoreboard displays the player's performance, including the number of aliens defeated, food collected, and energy potions consumed.

---

## Installation

To play the game, follow the steps below:

1. **Clone or Download the Repository**:
   - Download the entire project or clone it using Git:
   ```bash
   git clone <repository-url>
## Game Instructions

### Movement:
- Use the arrow keys to move the astronaut (Up, Down, Left, Right).
- Hold **Shift** to move faster.

### Shooting:
- Press the **Spacebar** to shoot bullets. The bullet type depends on the current level.

### Objective:
- Defeat aliens to progress through levels.
- Collect resources like food and energy drinks to restore hearts and energy.

### Game Over:
- If you lose all hearts or fail to defeat the aliens in time, the game will end and a scoreboard will be displayed.

## Game Logic

### Game Loop:
The game follows a continuous loop that:
- Handles events such as key presses and mouse clicks.
- Updates the player's position and actions.
- Checks for collisions between the player, bullets, and aliens.
- Spawns new aliens as the level progresses.
- Draws the player, bullets, aliens, and resources on the screen.

### Levels:
- The game progresses through different levels, with each level introducing harder aliens.
- Each level has its own bullet type (e.g., fire bullets for Level 1, ice bullets for Level 2).
- The player collects resources to stay alive and heal.

### Bullets:
The game supports different bullet types:
- Fire Bullets
- Ice Bullets
- Gravity Bullets

The bullet type is set based on the current level.

### Scoreboard:
After finishing the game, the scoreboard shows:
- Total number of food collected.
- Total number of energy potions collected.
- Total number of aliens defeated.

## Future Enhancements
- **Power-ups**: Add more power-ups and upgrades for the player.
- **More Levels**: Introduce more levels with different alien types and challenges.
- **Online Leaderboard**: Track high scores globally.

