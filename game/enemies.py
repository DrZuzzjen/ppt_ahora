"""
Enemies module for Mario Sisters game.
Contains satirical gender-swapped versions of classic enemies.
"""
import pygame
import random
from constants import *

class Enemy(pygame.sprite.Sprite):
    """Base class for all enemies"""
    
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.vel_x = 0
        self.vel_y = 0
        self.direction = -1  # -1 left, 1 right
        self.points = 100  # Points awarded for defeat
    
    def update(self, platforms):
        """Update enemy position and check for collisions"""
        # Apply gravity
        self.vel_y += PLAYER_GRAVITY * 0.8
        
        # Update position
        self.rect.x += self.vel_x * self.direction
        self.check_horizontal_collisions(platforms)
        
        self.rect.y += int(self.vel_y)
        self.check_vertical_collisions(platforms)
    
    def check_horizontal_collisions(self, platforms):
        """Check and resolve horizontal collisions"""
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.direction *= -1  # Reverse direction
            
            # Move away from collision
            if self.direction > 0:
                self.rect.left = hits[0].rect.right
            else:
                self.rect.right = hits[0].rect.left
    
    def check_vertical_collisions(self, platforms):
        """Check and resolve vertical collisions"""
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            if self.vel_y > 0:  # Falling
                self.rect.bottom = hits[0].rect.top
                self.vel_y = 0
            else:  # Rising
                self.rect.top = hits[0].rect.bottom
                self.vel_y = 0
    
    def stomp(self):
        """Handle being stomped by player"""
        self.kill()
        return self.points


class Goombetta(Enemy):
    """Female version of Goomba with a bow"""
    
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE, (165, 42, 42))  # Brown
        self.vel_x = 1
        self.points = 100
        self.name = "Goombetta"
    
    def update(self, platforms):
        """Update with simple left-right movement"""
        super().update(platforms)
        
        # Fall off edge detection (smarter movement)
        ahead_x = self.rect.x + self.direction * TILE_SIZE
        ahead_y = self.rect.bottom + 5
        
        # Check if there's ground ahead
        ground_ahead = False
        for platform in platforms:
            if (platform.rect.left <= ahead_x <= platform.rect.right and 
                abs(platform.rect.top - ahead_y) < 10):
                ground_ahead = True
                break
        
        # If no ground ahead, turn around
        if not ground_ahead:
            self.direction *= -1


class Koopette(Enemy):
    """Female Koopa Troopa with a shell"""
    
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE * 1.5, (0, 128, 0))  # Dark green
        self.vel_x = 1.5
        self.points = 200
        self.name = "Koopette"
        self.shell_mode = False
        self.shell_timer = 0
    
    def update(self, platforms):
        """Update with shell transformation ability"""
        if not self.shell_mode:
            super().update(platforms)
        else:
            # Shell mode - faster movement
            self.rect.x += self.vel_x * self.direction * 3
            
            # Check for collisions in shell mode
            hits = pygame.sprite.spritecollide(self, platforms, False)
            if hits:
                self.direction *= -1
            
            # Shell mode timer
            self.shell_timer -= 1
            if self.shell_timer <= 0:
                self.shell_mode = False
                self.image.fill((0, 128, 0))  # Back to green
    
    def stomp(self):
        """When stomped, enter shell mode instead of dying"""
        if not self.shell_mode:
            self.shell_mode = True
            self.shell_timer = 180  # 3 seconds at 60 FPS
            self.image.fill((200, 200, 200))  # Gray shell
            return 50  # Fewer points for just shelling
        else:
            return super().stomp()  # Actually defeat if already in shell


class PiranhaQueenPlant(Enemy):
    """Piranha Plant with a crown"""
    
    def __init__(self, x, y, pipe_top=True):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE * 2, (255, 0, 0))  # Red
        self.pipe_top = pipe_top
        self.points = 200
        self.name = "Piranha Queen"
        self.rise_timer = 0
        self.hidden = False
        
        # Movement pattern
        self.rise_speed = 1
        self.max_rise = TILE_SIZE * 2
        self.current_rise = 0
    
    def update(self, platforms):
        """Piranha plants don't move horizontally but rise from pipes"""
        # Skip standard movement
        
        # Manage rise/hide cycle
        if self.rise_timer > 0:
            self.rise_timer -= 1
        else:
            if self.hidden:
                # Start rising
                self.hidden = False
                self.rise_timer = 120  # Stay visible for 2 seconds
                self.current_rise = 0
            else:
                # Start hiding
                self.hidden = True
                self.rise_timer = 180  # Stay hidden for 3 seconds
        
        # Adjust position based on rise cycle
        if not self.hidden:
            if self.current_rise < self.max_rise:
                self.current_rise += self.rise_speed
                self.rect.y -= self.rise_speed if self.pipe_top else self.rise_speed * -1
        else:
            if self.current_rise > 0:
                self.current_rise -= self.rise_speed
                self.rect.y += self.rise_speed if self.pipe_top else self.rise_speed * -1


class BossetteBowsette(Enemy):
    """The big boss - gender-swapped Bowser"""
    
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE * 3, TILE_SIZE * 4, (255, 165, 0))  # Orange
        self.vel_x = 0.5
        self.points = 5000
        self.name = "Bossette"
        self.health = 5
        self.attack_timer = 180
        self.attack_pattern = 0
        
    def update(self, platforms):
        """Complex movement and attack patterns"""
        super().update(platforms)
        
        # Attack timer
        self.attack_timer -= 1
        if self.attack_timer <= 0:
            self.attack_timer = 180  # 3 seconds between attacks
            self.attack_pattern = random.randint(0, 2)
            self.attack()
    
    def attack(self):
        """Execute one of several attack patterns"""
        if self.attack_pattern == 0:
            # Jump
            self.vel_y = PLAYER_JUMP * 0.7
        elif self.attack_pattern == 1:
            # Charge
            self.vel_x *= 3
        elif self.attack_pattern == 2:
            # Would spawn fireballs in a real implementation
            pass
    
    def stomp(self):
        """Bosses have multiple hit points"""
        self.health -= 1
        if self.health <= 0:
            return super().stomp()
        return 50  # Small points for each hit