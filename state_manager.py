
import pygame
from settings import *
from sprites import *

class StateManager:
    def __init__(self):
        self.state = "PREP"
        self.sanity = INITIAL_SANITY
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        
        # PREP State variables
        self.ingredients = pygame.sprite.Group()
        self.spawn_timer = 0
        self.spawn_interval = 2000 # milliseconds

        # TRAUMA State variables
        self.nerve_path = None
        self.deviated = False
        self.deviation_start_time = 0

    def reset_trauma(self):
        self.nerve_path = NervePath()
        self.deviated = False

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

            mouse_pos = pygame.mouse.get_pos()
            distance = self.nerve_path.check_deviation(mouse_pos)

            if distance > NERVE_DEVIATION_LIMIT:
                self.deviated = True
                # Trigger "Injury" - currently just a console log or flag
                print("INJURY! Deviation too high.")
                self.sanity -= 1 # Rapid drain on failure? Or instant fail?
                # For now just drain sanity
            else:
                self.deviated = False
                # Healing mechanic? Or just survive? 
                # If they reach the end, maybe restore sanity to PREP state?
                # Simplified: if x > SCREEN_WIDTH - 50, success
                if mouse_pos[0] > SCREEN_WIDTH - 100:
                    self.sanity = 50 # Restore some sanity
                    self.state = "PREP"
                    self.ingredients.empty()

    def draw(self, surface):
        if self.state == "PREP":
            surface.fill(BLACK) # Kitchen background placeholder
            self.ingredients.draw(surface)
        
        elif self.state == "TRAUMA":
            surface.fill(RADICCHIO_RED)
            if self.nerve_path:
                self.nerve_path.draw(surface)
            
            if self.deviated:
                text_surf = self.font.render("INJURY DETECTED!", True, WHITE)
                surface.blit(text_surf, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))

        # HUD
        sanity_text = self.font.render(f"Sanity: {self.sanity}", True, WHITE)
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(sanity_text, (10, 10))
        surface.blit(score_text, (10, 50))
