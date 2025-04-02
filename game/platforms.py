"""
Platforms module for Mario Sisters game.
Contains terrain elements like blocks, pipes, and platforms.
"""
import pygame
from constants import *

class Platform(pygame.sprite.Sprite):
    """Base class for all platform objects"""
    
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.solid = True  # Can be collided with


class Ground(Platform):
    """Basic ground platform"""
    
    def __init__(self, x, y, width):
        super().__init__(x, y, width, TILE_SIZE, (150, 75, 0))  # Brown


class Brick(Platform):
    """Breakable brick block"""
    
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE, (210, 105, 30))  # Dark orange
        self.hit_count = 0
        self.breakable = True
        self.contains_item = False
        self.item_type = None
    
    def hit(self):
        """Handle being hit from below by player"""
        if self.contains_item:
            # Logic to spawn item would go here
            self.contains_item = False
            self.image.fill((210, 180, 140))  # Lighter color after item is out
            return True
        
        if self.breakable:
            self.hit_count += 1
            if self.hit_count >= 1:
                self.kill()  # Remove the brick
                return True
        return False


class QuestionBlock(Platform):
    """Question mark block with hidden items"""
    
    def __init__(self, x, y, item_type="coin"):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE, (255, 255, 0))  # Yellow
        self.active = True
        self.item_type = item_type
    
    def hit(self):
        """Spawn an item when hit from below"""
        if self.active:
            self.active = False
            self.image.fill((128, 128, 128))  # Gray after being hit
            # Spawning item logic would go here
            return True
        return False


class Pipe(Platform):
    """Warp pipe"""
    
    def __init__(self, x, y, height=2):
        # Create pipe with specified height (in tiles)
        pipe_height = TILE_SIZE * height
        super().__init__(x, y - pipe_height + TILE_SIZE, TILE_SIZE * 2, pipe_height, (0, 200, 0))  # Green
        self.warp_destination = None
        self.has_enemy = False
    
    def set_destination(self, level_name, x, y):
        """Set the warp destination for this pipe"""
        self.warp_destination = (level_name, x, y)
    
    def warp(self):
        """Warp a player to the destination"""
        if self.warp_destination:
            return self.warp_destination
        return None


class MovingPlatform(Platform):
    """Platform that moves along a path"""
    
    def __init__(self, x, y, width, movement_type="horizontal", distance=128, speed=1):
        super().__init__(x, y, width, TILE_SIZE, (200, 200, 200))  # Gray
        
        self.start_x = x
        self.start_y = y
        self.movement_type = movement_type
        self.distance = distance
        self.speed = speed
        self.direction = 1
        self.move_counter = 0
    
    def update(self):
        """Move the platform along its path"""
        if self.movement_type == "horizontal":
            self.rect.x += self.speed * self.direction
            self.move_counter += self.speed
            
            if self.move_counter >= self.distance:
                self.direction *= -1
                self.move_counter = 0
                
        elif self.movement_type == "vertical":
            self.rect.y += self.speed * self.direction
            self.move_counter += self.speed
            
            if self.move_counter >= self.distance:
                self.direction *= -1
                self.move_counter = 0


class FallingPlatform(Platform):
    """Platform that falls after being stepped on"""
    
    def __init__(self, x, y, width):
        super().__init__(x, y, width, TILE_SIZE, (150, 150, 150))  # Light gray
        self.triggered = False
        self.fall_delay = 30  # Half second delay at 60 FPS
        self.fall_speed = 0
    
    def update(self):
        """Handle falling behavior"""
        if self.triggered:
            if self.fall_delay > 0:
                self.fall_delay -= 1
            else:
                self.fall_speed += PLAYER_GRAVITY
                self.rect.y += int(self.fall_speed)
                
                # Remove if off screen
                if self.rect.top > SCREEN_HEIGHT:
                    self.kill()
    
    def trigger(self):
        """Trigger the platform to start falling"""
        self.triggered = True


class LevelExit(Platform):
    """Flag pole or other level exit"""
    
    def __init__(self, x, y):
        super().__init__(x, y - TILE_SIZE * 5, TILE_SIZE, TILE_SIZE * 5, (255, 215, 0))  # Gold
        self.solid = False  # Can pass through
        self.reached = False
    
    def touch(self):
        """Handle player touching the exit"""
        self.reached = True
        return True