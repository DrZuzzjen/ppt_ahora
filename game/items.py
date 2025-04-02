"""
Items module for Mario Sisters game.
Contains collectibles, power-ups, and other items.
"""
import pygame
import random
from constants import *

class Item(pygame.sprite.Sprite):
    """Base class for all collectible items"""
    
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.vel_x = 0
        self.vel_y = 0
        
    def update(self, platforms):
        """Update item position and apply physics"""
        # Apply gravity
        self.vel_y += PLAYER_GRAVITY * 0.5
        
        # Update position
        self.rect.x += int(self.vel_x)
        self.rect.y += int(self.vel_y)
        
        # Check for collisions with platforms
        self.check_collisions(platforms)
    
    def check_collisions(self, platforms):
        """Basic collision detection"""
        # Vertical collisions
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            if self.vel_y > 0:  # Falling
                self.rect.bottom = hits[0].rect.top
                self.vel_y = 0
                
        # Horizontal collisions
        for platform in hits:
            if self.vel_x > 0:  # Moving right
                if self.rect.right > platform.rect.left and self.rect.right < platform.rect.right:
                    self.rect.right = platform.rect.left
                    self.vel_x *= -1  # Bounce
            elif self.vel_x < 0:  # Moving left
                if self.rect.left < platform.rect.right and self.rect.left > platform.rect.left:
                    self.rect.left = platform.rect.right
                    self.vel_x *= -1  # Bounce


class Coin(Item):
    """Basic collectible coin"""
    
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE//2, TILE_SIZE//2, YELLOW)
        self.value = 100
        
        # Animation variables
        self.bobbing = True
        self.bob_height = 5
        self.bob_speed = 0.1
        self.bob_direction = 1
        self.start_y = y
        self.current_bob = 0
    
    def update(self, platforms=None):
        """Coins don't fall, they bob up and down"""
        if self.bobbing:
            self.current_bob += self.bob_speed * self.bob_direction
            if abs(self.current_bob) >= self.bob_height:
                self.bob_direction *= -1
                
            self.rect.y = self.start_y + self.current_bob


class FeatherCap(Item):
    """Power-up that grants cape abilities"""
    
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE, YELLOW)
        self.vel_x = 2  # Moves horizontally
        self.power_type = "cape"
    
    def apply_effect(self, player):
        """Apply the cape power to the player"""
        player.power_level = 2
        # In a real implementation, would change player's sprite and add abilities


class HeelShoe(Item):
    """Power-up that grants stomp abilities"""
    
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE, RED)
        self.vel_x = 2  # Moves horizontally
        self.power_type = "heels"
    
    def apply_effect(self, player):
        """Apply the heel power to the player"""
        player.power_level = 1
        # In a real implementation, would change player's sprite and add abilities


class PurseItem(Item):
    """Power-up that grants throwing abilities"""
    
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE, PINK)
        self.vel_x = 2  # Moves horizontally
        self.power_type = "purse"
    
    def apply_effect(self, player):
        """Apply the purse power to the player"""
        player.power_level = 3
        # In a real implementation, would change player's sprite and add abilities


class StarPower(Item):
    """Temporary invincibility star"""
    
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE, (255, 215, 0))  # Gold
        self.vel_x = 3
        self.vel_y = -5  # Initial bounce
        self.power_type = "star"
        
        # Animation variables
        self.colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        self.color_index = 0
        self.color_timer = 0
    
    def update(self, platforms):
        """Stars bounce around the level"""
        super().update(platforms)
        
        # Stars bounce when they hit the ground
        if self.vel_y == 0:
            self.vel_y = -10
        
        # Color cycling animation
        self.color_timer += 1
        if self.color_timer >= 5:
            self.color_timer = 0
            self.color_index = (self.color_index + 1) % len(self.colors)
            self.image.fill(self.colors[self.color_index])
    
    def apply_effect(self, player):
        """Apply temporary invincibility"""
        player.invincible = True
        player.invincible_timer = 600  # 10 seconds at 60 FPS


class OneUpMushroom(Item):
    """Extra life item"""
    
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE, (50, 205, 50))  # Lime green
        self.vel_x = 2
        self.power_type = "1up"
    
    def apply_effect(self, player):
        """Grant an extra life"""
        player.lives += 1