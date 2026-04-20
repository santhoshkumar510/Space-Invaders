# Space Invaders - Python & Pygame

A classic arcade-style Space Invaders game built using Python and the Pygame library. This project demonstrates object-oriented programming (OOP), sprite management, collision detection, and game state logic.

##  Features
* **Player Mechanics:** Smooth spaceship movement and laser firing system with cooldowns.
* **Dynamic Enemies:** Procedurally generated alien fleet with randomized textures and lateral movement.
* **Adaptive Combat:** Aliens fire back at randomized intervals with a capped number of active projectiles.
* **Explosion System:** Multi-sized animated explosions for different impact types (bullets vs. ships).
* **Health System:** Real-time visual health bar that updates as the player takes damage.
* **Game States:** Includes a pre-game countdown and distinct "Win/Loss" screen conditions.
* **Audio:** Integrated sound effects for lasers, explosions, and impacts.

##  Technical Highlights
* **Sprite Groups:** Efficiently manages and updates multiple game objects (bullets, aliens, explosions) using `pygame.sprite.Group`.
* **Collision Masks:** Uses pixel-perfect collision detection (`pygame.mask`) for precise interaction between projectiles and ship hulls.
* **Animation Logic:** Implemented a frame-counter system to handle explosion animations across three different scales.
* **Timing Logic:** Utilizes `pygame.time.get_ticks()` to manage weapon cooldowns and game countdowns without interrupting the main loop.

##  Installation & Running

1. **Prerequisites:** Ensure you have Python installed and the Pygame library:
   ```bash
   pip install pygame
