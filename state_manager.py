
import pygame
from settings import *
from sprites import *

class StateManager:
    def __init__(self):
        self.state = "PREP"
        self.sanity = INITIAL_SANITY
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 100) # For countdown
        
        # PREP State variables
        self.ingredients = pygame.sprite.Group()
        self.spawn_timer = 0
        self.spawn_interval = 2000 # milliseconds

        # TRAUMA State variables
        self.nerve_path = None
        self.deviated = False
        self.trauma_start_time = 0
        self.is_grace_period = False
        self.pulse_timer = 0
        self.deviation_timer = 0
        self.last_frame_time = 0
        self.damage_flash_timer = 0

    def reset_trauma(self):
        self.nerve_path = NervePath()
        self.deviated = False
        self.trauma_start_time = pygame.time.get_ticks()
        self.is_grace_period = True
        self.deviation_timer = 0
        self.last_frame_time = pygame.time.get_ticks()
        self.damage_flash_timer = 0

    def handle_input(self, event):
        if self.state == "PREP":
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_ingredient = None
                for ingredient in self.ingredients:
                    if ingredient.rect.collidepoint(event.pos):
                        clicked_ingredient = ingredient
                        break
                
                if clicked_ingredient:
                    self.score += 1
                    clicked_ingredient.kill()
                else:
                    self.sanity -= SANITY_PENALTY_MISS
        
        elif self.state == "TRAUMA":
            # Input handling for trauma mostly happens in update via mouse pos
            pass

    def update(self):
        if self.state == "PREP":
            # Sanity Check
            if self.sanity <= TRAUMA_THRESHOLD:
                self.state = "TRAUMA"
                self.reset_trauma()
                return

            # Spawn Ingredients
            now = pygame.time.get_ticks()
            if now - self.spawn_timer > self.spawn_interval:
                self.ingredients.add(Ingredient())
                self.spawn_timer = now

            self.ingredients.update()

        elif self.state == "TRAUMA":
            if not self.nerve_path:
                self.reset_trauma()

            now = pygame.time.get_ticks()
            elapsed = now - self.trauma_start_time
            
            if self.is_grace_period:
                if elapsed >= GRACE_PERIOD_DURATION:
                    self.is_grace_period = False
                else:
                    # In grace period, just update pulse timer and return
                    self.pulse_timer += 1
                    return

            # Active Game Logic (Post Grace Period)
            mouse_pos = pygame.mouse.get_pos()
            distance = self.nerve_path.check_deviation(mouse_pos)
            
            dt = now - self.last_frame_time
            self.last_frame_time = now

            if distance > NERVE_DEVIATION_LIMIT:
                self.deviated = True
                
                # Damage tick logic
                self.deviation_timer += dt
                if self.deviation_timer >= DAMAGE_TICK_INTERVAL:
                    print("INJURY! Deviation too high.")
                    self.sanity -= 1 
                    self.deviation_timer = 0 # Reset after damage
                    self.damage_flash_timer = 150 # Flash for 150ms
            else:
                self.deviated = False
                self.deviation_timer = 0 # Reset if safe
                
                # Healing mechanic? Or just survive? 
                # If they reach the end, maybe restore sanity to PREP state?
                # Simplified: if x > SCREEN_WIDTH - 50, success
                if mouse_pos[0] > SCREEN_WIDTH - 100:
                    self.sanity = 50 # Restore some sanity
                    self.state = "PREP"
                    self.ingredients.empty()
            
            if self.damage_flash_timer > 0:
                self.damage_flash_timer -= dt

    def draw(self, surface):
        if self.state == "PREP":
            surface.fill(BLACK) # Kitchen background placeholder
            self.ingredients.draw(surface)
        
        elif self.state == "TRAUMA":
            # Background
            if self.is_grace_period:
                # Pulsating Red
                import math
                pulse = (math.sin(self.pulse_timer * PULSE_SPEED) + 1) / 2 # 0 to 1
                # Interpolate between BLACK and RADICCHIO_RED
                # Dark: (0, 0, 0), Bright: RADICCHIO_RED (142, 35, 68)
                r = int(0 + (RADICCHIO_RED[0] - 0) * pulse)
                g = int(0 + (RADICCHIO_RED[1] - 0) * pulse)
                b = int(0 + (RADICCHIO_RED[2] - 0) * pulse)
                surface.fill((r, g, b))
            elif self.damage_flash_timer > 0:
                 # Flash White (same as countdown)
                 surface.fill(WHITE)
            else:
                surface.fill(RADICCHIO_RED)

            if self.nerve_path:
                self.nerve_path.draw(surface)
                
                # Highlight Start Point during grace period
                if self.is_grace_period:
                    start_pos = self.nerve_path.start_point
                    # Draw glowing green circle
                    pygame.draw.circle(surface, GREEN, (int(start_pos[0]), int(start_pos[1])), START_POINT_RADIUS, 3)
                    
                    # Draw Countdown
                    remaining = max(0, GRACE_PERIOD_DURATION - (pygame.time.get_ticks() - self.trauma_start_time))
                    seconds = (remaining // 1000) + 1
                    timer_text = self.large_font.render(str(seconds), True, WHITE)
                    text_rect = timer_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                    surface.blit(timer_text, text_rect)
            
            # Removed Text Blit

        # HUD
        sanity_text = self.font.render(f"Sanity: {self.sanity}", True, WHITE)
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(sanity_text, (10, 10))
        surface.blit(score_text, (10, 50))
