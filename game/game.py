"""
Main game module for Mario Sisters.
Handles game states, rendering, and the game loop.
"""
import pygame
import sys
from constants import *
from player import MariaSister, LuigiettaSister, PeachSister, DaisySister
from enemies import Goombetta, Koopette, PiranhaQueenPlant, BossetteBowsette
from platforms import Ground, Brick, QuestionBlock, Pipe, MovingPlatform, FallingPlatform, LevelExit
from items import Coin, HeelShoe, FeatherCap, PurseItem, StarPower, OneUpMushroom

class Game:
    """Main game class for Mario Sisters"""
    
    def __init__(self):
        """Initialize the game"""
        pygame.init()
        pygame.display.set_caption(SCREEN_TITLE)
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = STATE_INTRO
        
        # Font setup
        self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
        self.normal_font = pygame.font.Font(None, NORMAL_FONT_SIZE)
        
        # Load assets
        self.load_assets()
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        
        # Game variables
        self.current_level = 1
        self.score = 0
        self.time_left = 300  # seconds
        self.time_counter = 0
        self.camera_offset_x = 0
        
        # Player selection
        self.available_sisters = ["Maria", "Luigietta", "Peach", "Daisy"]
        self.selected_sister = 0
        
    def load_assets(self):
        """Load game assets like images and sounds"""
        # For now, we're using colored rectangles
        # In a full game, this would load sprites, sounds, etc.
        pass
    
    def new_game(self):
        """Start a new game"""
        # Reset game state
        self.score = 0
        self.time_left = 300
        self.current_level = 1
        self.state = STATE_PLAYING
        
        # Clear sprite groups
        self.all_sprites.empty()
        self.platforms.empty()
        self.enemies.empty()
        self.items.empty()
        self.players.empty()
        
        # Create the player based on selection
        self.create_player()
        
        # Load the first level
        self.load_level(self.current_level)
        
    def create_player(self):
        """Create the player character based on selection"""
        # Starting position
        x, y = 100, 300
        
        # Choose sister based on selection
        if self.available_sisters[self.selected_sister] == "Maria":
            self.player = MariaSister(x, y)
        elif self.available_sisters[self.selected_sister] == "Luigietta":
            self.player = LuigiettaSister(x, y)
        elif self.available_sisters[self.selected_sister] == "Peach":
            self.player = PeachSister(x, y)
        else:  # Daisy
            self.player = DaisySister(x, y)
        
        self.players.add(self.player)
        self.all_sprites.add(self.player)
    
    def load_level(self, level_number):
        """Load a level by its number"""
        # Clear existing level objects
        for sprite in self.all_sprites:
            if sprite != self.player:
                sprite.kill()
        
        # Reset camera
        self.camera_offset_x = 0
        
        # Create level elements based on level number
        if level_number == 1:
            self.create_level_1()
        elif level_number == 2:
            self.create_level_2()
        elif level_number == 3:
            self.create_boss_level()
    
    def create_level_1(self):
        """Create the first level layout"""
        # Ground platforms
        for x in range(0, SCREEN_WIDTH * 3, TILE_SIZE):
            if 700 < x < 900 or 1100 < x < 1300:  # Create some gaps
                continue
            ground = Ground(x, SCREEN_HEIGHT - TILE_SIZE, TILE_SIZE)
            self.platforms.add(ground)
            self.all_sprites.add(ground)
        
        # Add some blocks
        for x in range(300, 500, TILE_SIZE):
            brick = Brick(x, SCREEN_HEIGHT - TILE_SIZE * 4)
            self.platforms.add(brick)
            self.all_sprites.add(brick)
        
        # Question blocks with items
        q_block1 = QuestionBlock(350, SCREEN_HEIGHT - TILE_SIZE * 7, "coin")
        q_block2 = QuestionBlock(450, SCREEN_HEIGHT - TILE_SIZE * 7, "heels")
        self.platforms.add(q_block1, q_block2)
        self.all_sprites.add(q_block1, q_block2)
        
        # Pipes
        pipe1 = Pipe(600, SCREEN_HEIGHT, 2)
        pipe2 = Pipe(1000, SCREEN_HEIGHT, 3)
        self.platforms.add(pipe1, pipe2)
        self.all_sprites.add(pipe1, pipe2)
        
        # Moving platform
        moving_plat = MovingPlatform(800, SCREEN_HEIGHT - TILE_SIZE * 4, 
                                    TILE_SIZE * 3, "horizontal", 200, 1)
        self.platforms.add(moving_plat)
        self.all_sprites.add(moving_plat)
        
        # Enemies
        goombetta1 = Goombetta(400, SCREEN_HEIGHT - TILE_SIZE * 2)
        goombetta2 = Goombetta(800, SCREEN_HEIGHT - TILE_SIZE * 2)
        koopette = Koopette(1200, SCREEN_HEIGHT - TILE_SIZE * 2)
        self.enemies.add(goombetta1, goombetta2, koopette)
        self.all_sprites.add(goombetta1, goombetta2, koopette)
        
        # Items/coins
        for x in range(350, 550, TILE_SIZE):
            coin = Coin(x, SCREEN_HEIGHT - TILE_SIZE * 10)
            self.items.add(coin)
            self.all_sprites.add(coin)
        
        # Level exit
        self.exit = LevelExit(SCREEN_WIDTH * 2.8, SCREEN_HEIGHT)
        self.all_sprites.add(self.exit)
    
    def create_level_2(self):
        """Create the second level layout"""
        # This would have a similar structure to level 1 but with different layout
        # and more complex elements
        # For brevity, we'll just add a placeholder message
        print("Level 2 would be created here")
    
    def create_boss_level(self):
        """Create the final boss level"""
        # This would create a boss arena with the Bossette/Bowsette boss
        # For brevity, we'll just add a placeholder message
        print("Boss level would be created here")
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == STATE_PLAYING:
                        self.state = STATE_PAUSE
                    elif self.state == STATE_PAUSE:
                        self.state = STATE_PLAYING
                
                if self.state == STATE_INTRO:
                    if event.key == pygame.K_UP:
                        self.selected_sister = (self.selected_sister - 1) % len(self.available_sisters)
                    if event.key == pygame.K_DOWN:
                        self.selected_sister = (self.selected_sister + 1) % len(self.available_sisters)
                    if event.key == pygame.K_RETURN:
                        self.new_game()
                
                elif self.state == STATE_PLAYING:
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        self.player.jump()
                    if event.key == pygame.K_z or event.key == pygame.K_LSHIFT:
                        self.player.use_special_ability()
                    # Add direct key handling for left/right movement
                    if event.key == pygame.K_LEFT:
                        self.player.move_left()
                    if event.key == pygame.K_RIGHT:
                        self.player.move_right()
                
                elif self.state == STATE_GAME_OVER or self.state == STATE_WIN:
                    if event.key == pygame.K_RETURN:
                        self.state = STATE_INTRO
    
    def update(self):
        """Update game state"""
        if self.state == STATE_PLAYING:
            # Update time
            self.time_counter += 1
            if self.time_counter >= FPS:  # Every second
                self.time_counter = 0
                self.time_left -= 1
                if self.time_left <= 0:
                    self.game_over()
            
            # Get keyboard input for player movement
            keys = pygame.key.get_pressed()
            # Ensure continuous movement while keys are held down
            if keys[pygame.K_LEFT]:
                self.player.move_left()
            if keys[pygame.K_RIGHT]:
                self.player.move_right()
            
            # Update moving platforms
            for platform in self.platforms:
                if isinstance(platform, MovingPlatform) or isinstance(platform, FallingPlatform):
                    platform.update()
            
            # Update player
            self.player.update(self.platforms)
            
            # Check if player fell off the screen
            if self.player.rect.top > SCREEN_HEIGHT:
                self.player_died()
            
            # Update camera to follow player
            self.update_camera()
            
            # Update enemies
            for enemy in self.enemies:
                enemy.update(self.platforms)
                
                # Check for player collision with enemy
                if pygame.sprite.collide_rect(self.player, enemy):
                    # Check if stomping (player is above and falling)
                    if (self.player.rect.bottom < enemy.rect.centery and 
                        self.player.vel_y > 0):
                        self.score += enemy.stomp()
                        self.player.vel_y = PLAYER_JUMP * 0.5  # Bounce
                    else:
                        # Player gets hit
                        self.player_hit()
            
            # Update items
            for item in self.items:
                item.update(self.platforms)
                
                # Check if player collected item
                if pygame.sprite.collide_rect(self.player, item):
                    if isinstance(item, Coin):
                        self.score += item.value
                        item.kill()
                    else:
                        # Apply power-up effect
                        item.apply_effect(self.player)
                        item.kill()
            
            # Check for level exit
            if pygame.sprite.collide_rect(self.player, self.exit):
                self.exit.touch()
                self.complete_level()
    
    def update_camera(self):
        """Update camera position to follow player"""
        # Simple camera that follows player horizontally
        player_center_x = self.player.rect.centerx
        
        # Only scroll if player is beyond the middle of the screen
        if player_center_x > SCREEN_WIDTH / 2:
            target_offset = -(player_center_x - SCREEN_WIDTH / 2)
            
            # Limit camera to the start of the level
            if target_offset > 0:
                target_offset = 0
                
            # Smooth camera movement
            self.camera_offset_x = target_offset
    
    def player_hit(self):
        """Handle player being hit by an enemy"""
        if not hasattr(self.player, 'invincible') or not self.player.invincible:
            self.player.lives -= 1
            
            # Temporary invincibility after being hit
            self.player.invincible = True
            self.player.invincible_timer = 120  # 2 seconds
            
            # Power down
            if self.player.power_level > 0:
                self.player.power_level -= 1
            
            # Check for game over
            if self.player.lives <= 0:
                self.game_over()
    
    def player_died(self):
        """Handle player death (falling off screen)"""
        self.player.lives -= 1
        
        if self.player.lives <= 0:
            self.game_over()
        else:
            # Respawn at the start of the level
            self.player.rect.x = 100
            self.player.rect.y = 300
            self.player.vel_y = 0
    
    def complete_level(self):
        """Handle level completion"""
        # Add time bonus
        self.score += self.time_left * 10
        
        # Move to next level
        self.current_level += 1
        if self.current_level > 3:  # Assuming 3 levels total
            self.win_game()
        else:
            self.load_level(self.current_level)
    
    def game_over(self):
        """Handle game over state"""
        self.state = STATE_GAME_OVER
    
    def win_game(self):
        """Handle winning the game"""
        self.state = STATE_WIN
    
    def draw(self):
        """Draw everything to the screen"""
        self.screen.fill(SKY_BLUE)  # Sky background
        
        if self.state == STATE_INTRO:
            self.draw_intro()
        elif self.state == STATE_PLAYING:
            self.draw_game()
        elif self.state == STATE_PAUSE:
            self.draw_game()
            self.draw_pause()
        elif self.state == STATE_GAME_OVER:
            self.draw_game_over()
        elif self.state == STATE_WIN:
            self.draw_win()
        
        pygame.display.flip()
    
    def draw_game(self):
        """Draw the main gameplay elements"""
        # Apply camera offset to all sprites
        for sprite in self.all_sprites:
            offset_rect = sprite.rect.copy()
            offset_rect.x += self.camera_offset_x
            
            # Only draw if on screen
            if -TILE_SIZE < offset_rect.x < SCREEN_WIDTH + TILE_SIZE:
                self.screen.blit(sprite.image, offset_rect)
        
        # Draw HUD
        self.draw_hud()
    
    def draw_hud(self):
        """Draw the heads-up display with score, time, etc."""
        # Background for HUD
        hud_bg = pygame.Surface((SCREEN_WIDTH, 30))
        hud_bg.fill(BLACK)
        hud_bg.set_alpha(150)  # Semi-transparent
        self.screen.blit(hud_bg, (0, 0))
        
        # Score
        score_text = self.normal_font.render(f"SCORE: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 5))
        
        # Lives
        lives_text = self.normal_font.render(f"LIVES: {self.player.lives}", True, WHITE)
        self.screen.blit(lives_text, (200, 5))
        
        # Time
        time_text = self.normal_font.render(f"TIME: {self.time_left}", True, WHITE)
        self.screen.blit(time_text, (SCREEN_WIDTH - 150, 5))
        
        # Sister name
        name_text = self.normal_font.render(f"SISTER: {self.player.name}", True, WHITE)
        self.screen.blit(name_text, (SCREEN_WIDTH // 2 - 100, 5))
    
    def draw_intro(self):
        """Draw the intro/title screen"""
        # Title
        title_text = self.title_font.render("MARIO SISTERS", True, RED)
        subtitle_text = self.normal_font.render("A Satirical Adventure", True, WHITE)
        
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4 + 50))
        
        self.screen.blit(title_text, title_rect)
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Character selection
        select_text = self.normal_font.render("Select Your Sister:", True, WHITE)
        select_rect = select_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
        self.screen.blit(select_text, select_rect)
        
        # Display character options
        for i, sister in enumerate(self.available_sisters):
            color = YELLOW if i == self.selected_sister else WHITE
            sister_text = self.normal_font.render(sister, True, color)
            pos_y = SCREEN_HEIGHT//2 + i * 30
            sister_rect = sister_text.get_rect(center=(SCREEN_WIDTH//2, pos_y))
            self.screen.blit(sister_text, sister_rect)
        
        # Instructions
        instr_text = self.normal_font.render("Press UP/DOWN to select, ENTER to start", True, WHITE)
        instr_rect = instr_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100))
        self.screen.blit(instr_text, instr_rect)
        
        # Copyright
        copyright_text = self.normal_font.render("© 2025 Satirical Games Inc.", True, WHITE)
        copyright_rect = copyright_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        self.screen.blit(copyright_text, copyright_rect)
    
    def draw_pause(self):
        """Draw the pause screen overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(150)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.title_font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(pause_text, pause_rect)
        
        # Instructions
        instr_text = self.normal_font.render("Press ESC to resume", True, WHITE)
        instr_rect = instr_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(instr_text, instr_rect)
    
    def draw_game_over(self):
        """Draw the game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(200)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        over_text = self.title_font.render("GAME OVER", True, RED)
        over_rect = over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        self.screen.blit(over_text, over_rect)
        
        # Score
        score_text = self.normal_font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(score_text, score_rect)
        
        # Restart instructions
        restart_text = self.normal_font.render("Press ENTER to return to title screen", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_win(self):
        """Draw the victory screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 100))  # Dark blue
        overlay.set_alpha(200)
        self.screen.blit(overlay, (0, 0))
        
        # Victory text
        win_text = self.title_font.render("YOU WIN!", True, YELLOW)
        win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        self.screen.blit(win_text, win_rect)
        
        # Satirical message
        message_text = self.normal_font.render("The princesses saved themselves!", True, WHITE)
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(message_text, message_rect)
        
        # Score
        score_text = self.normal_font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
        self.screen.blit(score_text, score_rect)
        
        # Return instructions
        return_text = self.normal_font.render("Press ENTER to return to title screen", True, WHITE)
        return_rect = return_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
        self.screen.blit(return_text, return_rect)