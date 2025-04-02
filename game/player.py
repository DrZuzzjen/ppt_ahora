"""
Player module for Mario Sisters game.
Contains the Sister characters with their unique abilities.
"""
import pygame
from constants import *

class Sister(pygame.sprite.Sprite):
    """Base class for all sister characters"""
    
    def __init__(self, x, y, color, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        
        # Physics
        self.vel_x = 0
        self.vel_y = 0
        self.acc_x = 0
        self.acc_y = 0
        self.direction = 1  # 1 for right, -1 for left
        self.jumping = False
        self.on_ground = False
        
        # Game stats
        self.score = 0
        self.lives = 3
        self.power_level = 0
        
        # Special ability cooldown
        self.ability_cooldown = 0
        self.ability_active = False
    
    def update(self, platforms):
        """Update the sister's position and status"""
        self.acc_x = 0
        self.acc_y = PLAYER_GRAVITY
        
        # Apply friction
        self.acc_x += self.vel_x * PLAYER_FRICTION
        
        # Update velocity
        self.vel_x += self.acc_x
        self.vel_y += self.acc_y
        
        # Limit velocity for better control
        if abs(self.vel_x) < 0.1:
            self.vel_x = 0
            
        # Update position
        self.rect.x += int(self.vel_x)
        self.check_horizontal_collisions(platforms)
        
        self.rect.y += int(self.vel_y)
        self.check_vertical_collisions(platforms)
        
        # Update ability cooldown
        if self.ability_cooldown > 0:
            self.ability_cooldown -= 1
            if self.ability_cooldown <= 0:
                self.ability_active = False
    
    def check_horizontal_collisions(self, platforms):
        """Check and resolve horizontal collisions"""
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            if self.vel_x > 0:  # Moving right
                self.rect.right = hits[0].rect.left
            else:  # Moving left
                self.rect.left = hits[0].rect.right
            self.vel_x = 0
    
    def check_vertical_collisions(self, platforms):
        """Check and resolve vertical collisions"""
        self.on_ground = False
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            if self.vel_y > 0:  # Falling
                self.rect.bottom = hits[0].rect.top
                self.on_ground = True
                self.vel_y = 0
                self.jumping = False
            else:  # Rising and hit head
                self.rect.top = hits[0].rect.bottom
                self.vel_y = 0
    
    def jump(self):
        """Make the sister jump if on ground"""
        if self.on_ground and not self.jumping:
            self.jumping = True
            self.vel_y = PLAYER_JUMP
    
    def move_left(self):
        """Move sister to the left"""
        self.acc_x = -PLAYER_ACC
        self.direction = -1
    
    def move_right(self):
        """Move sister to the right"""
        self.acc_x = PLAYER_ACC
        self.direction = 1
    
    def use_special_ability(self):
        """Use the sister's special ability if cooldown is over"""
        if self.ability_cooldown <= 0:
            self.ability_active = True
            self.ability_cooldown = 120  # 2 seconds at 60 FPS
            return True
        return False
    
    def draw_status(self, screen):
        """Draw character status like lives and power"""
        font = pygame.font.Font(None, SMALL_FONT_SIZE)
        text = font.render(f"{self.name}: {self.lives} Lives", True, WHITE)
        return text


class LuigiettaSister(Sister):
    """The high-jumping green sister"""
    
    def __init__(self, x, y):
        super().__init__(x, y, GREEN, "Luigietta")
        self.jump_power = PLAYER_JUMP * 1.5
    
    def jump(self):
        """Luigietta jumps higher than her sister"""
        if self.on_ground and not self.jumping:
            self.jumping = True
            self.vel_y = self.jump_power
    
    def use_special_ability(self):
        """Flutter jump that slows descent"""
        if super().use_special_ability():
            # Slow down falling
            if self.vel_y > 0:
                self.vel_y *= 0.5
            return True
        return False


class MariaSister(Sister):
    """The balanced red sister with fireball ability"""
    
    def __init__(self, x, y):
        super().__init__(x, y, RED, "Maria")
        self.fireballs = pygame.sprite.Group()
    
    def use_special_ability(self):
        """Throw a fireball in the direction facing"""
        if super().use_special_ability():
            # Create fireball logic would go here
            print(f"Maria throws fireball {self.direction}")
            return True
        return False


class PeachSister(Sister):
    """The floating pink sister"""
    
    def __init__(self, x, y):
        super().__init__(x, y, PINK, "Peach")
    
    def use_special_ability(self):
        """Float gracefully for a short time"""
        if super().use_special_ability():
            # Floating logic - almost zero gravity
            self.vel_y = 0.5
            return True
        return False


class DaisySister(Sister):
    """The ground-pound yellow sister"""
    
    def __init__(self, x, y):
        super().__init__(x, y, YELLOW, "Daisy")
    
    def use_special_ability(self):
        """Ground pound that stuns enemies"""
        if super().use_special_ability() and not self.on_ground:
            # Fast downward acceleration
            self.vel_y = 15
            return True
        return False