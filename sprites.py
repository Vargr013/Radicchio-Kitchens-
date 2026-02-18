
import pygame
import random
import math
from settings import *

import os

class ChefHand(pygame.sprite.Sprite):
    """
    Represents the chef's hands on the screen.
    Handles loading, positioning, and rendering of hand sprites, including state changes based on damage.
    """
    def __init__(self):
        super().__init__()
        self.load_images()
        
        # Base surface for composition
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        
        # State
        self.left_hand_state = "normal" # "normal", "damaged", "badly_damaged"
        self.is_attacking = False
        
        self.update_visuals()

    def load_images(self):
        def load(name):
            path = os.path.join(ASSET_DIR_IMAGES, name)
            try:
                img = pygame.image.load(path).convert_alpha()
                # Scale by factor
                new_size = (int(img.get_width() * HAND_SCALE), int(img.get_height() * HAND_SCALE))
                return pygame.transform.smoothscale(img, new_size)
            except Exception as e:
                print(f"Error loading {name}: {e}")
                s = pygame.Surface((100, 100))
                s.fill((255, 0, 255))
                return s

        self.img_right = load(IMG_HAND_RIGHT)
        self.img_left_normal = load(IMG_HAND_LEFT_NORMAL)
        self.img_left_damaged = load(IMG_HAND_LEFT_DAMAGED)
        self.img_left_badly = load(IMG_HAND_LEFT_BADLY_DAMAGED)
        self.img_attack = load(IMG_HANDS_KNIFE)

    def update_visuals(self, angle_right=0, angle_left=0):
        self.image.fill((0, 0, 0, 0)) # Clear
        
        offset = SCREEN_WIDTH // 5

        # Helper to center image with optional x offset and rotation
        def blit_centered(img, offset_x=0, rotation_angle=0):
            if rotation_angle != 0:
                # Rotate around center
                # Logic assumes pivot is roughly center of image for simplicity
                img_rotated = pygame.transform.rotate(img, rotation_angle)
                
                # Calculate center of where standard sprite sits
                base_x = (SCREEN_WIDTH - img.get_width()) // 2 + offset_x
                base_y = SCREEN_HEIGHT - img.get_height()
                center = (base_x + img.get_width() // 2, base_y + img.get_height() // 2)
                
                rect = img_rotated.get_rect(center=center)
                self.image.blit(img_rotated, rect.topleft)
            else:
                x = (SCREEN_WIDTH - img.get_width()) // 2 + offset_x
                y = SCREEN_HEIGHT - img.get_height() # Align bottom
                self.image.blit(img, (x, y))

        if self.is_attacking:
            blit_centered(self.img_attack)
        else:
            # Draw Right Hand (offset to right, rotated)
            blit_centered(self.img_right, offset, angle_right)
            
            # Draw Left Hand based on state (offset to left, rotated)
            img_left = None
            if self.left_hand_state == "normal":
                img_left = self.img_left_normal
            elif self.left_hand_state == "damaged":
                img_left = self.img_left_damaged
            elif self.left_hand_state == "badly_damaged":
                img_left = self.img_left_badly
            
            if img_left:
                blit_centered(img_left, -offset, angle_left)

    def update(self):
        mx, my = pygame.mouse.get_pos()
        offset = SCREEN_WIDTH // 5
        
        # --- Right Hand Calculation ---
        w_r, h_r = self.img_right.get_size()
        cx_r = (SCREEN_WIDTH - w_r) // 2 + offset + w_r // 2
        cy_r = SCREEN_HEIGHT - h_r // 2
        
        dx_r = mx - cx_r
        dy_r = my - cy_r
        
        angle_r = -math.degrees(math.atan2(dy_r, dx_r)) - 90
        # Clamp Right: -30 to 0 (Right/Clockwise only)
        angle_r = max(-30, min(0, angle_r))
        
        # --- Left Hand Calculation ---
        # Assuming Left Hand is roughly same size/position logic mirrored
        w_l, h_l = self.img_left_normal.get_size()
        cx_l = (SCREEN_WIDTH - w_l) // 2 - offset + w_l // 2
        cy_l = SCREEN_HEIGHT - h_l // 2
        
        dx_l = mx - cx_l
        dy_l = my - cy_l
        
        angle_l = -math.degrees(math.atan2(dy_l, dx_l)) - 90
        # Clamp Left: 0 to 30 (Left/CCW only)
        angle_l = max(0, min(30, angle_l))
        
        self.update_visuals(angle_r, angle_l)

    def set_hand_stage(self, stage):
        """
        Sets the visual stage of the left hand based on damage level.
        0 = Normal
        1 = Damaged
        2+ = Badly Damaged
        """
        if stage == 0:
            self.left_hand_state = "normal"
        elif stage == 1:
            self.left_hand_state = "damaged"
        else:
            self.left_hand_state = "badly_damaged"
        
        self.update_visuals()

    def set_attack(self, attacking):
        if self.is_attacking != attacking:
            self.is_attacking = attacking
            self.update_visuals()

class Cursor(pygame.sprite.Sprite):
    """
    Represents the player's cursor (aiming point) in the game.
    Follows the mouse position.
    """
    def __init__(self):
        super().__init__()
        path = os.path.join(ASSET_DIR_IMAGES, IMG_CURSOR_KNIFE)
        try:
            img = pygame.image.load(path).convert_alpha()
            new_size = (int(img.get_width() * CURSOR_SCALE), int(img.get_height() * CURSOR_SCALE))
            self.image = pygame.transform.smoothscale(img, new_size)
        except:
            self.image = pygame.Surface((20, 20))
            self.image.fill(RADICCHIO_RED)
            
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Ingredient(pygame.sprite.Sprite):
    """
    Represents a sliceable ingredient in the PREP phrase.
    Handles random spawning, rotation, and blinking before expiry.
    """
    def __init__(self):
        super().__init__()
        # Placeholder for ingredient image.
        # Ideally: self.image = pygame.image.load(os.path.join(ASSET_DIR_IMAGES, 'radicchio.png')).convert_alpha()
        
        # Base surface
        base_size = 64
        self.image = pygame.Surface((base_size, base_size), pygame.SRCALPHA)
        self.image.fill(GREEN)
        
        # Draw a visual "cut line" (Horizontal Center)
        # This represents 0 degrees rotation
        mid_y = base_size // 2
        pygame.draw.line(self.image, VEIN_WHITE, (0, mid_y), (base_size, mid_y), 3)
        
        # Random Rotation
        self.angle = random.randint(0, 360)
        self.image = pygame.transform.rotate(self.image, self.angle)
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        # Limit spawning to the top 1/3 of the screen
        max_y = SCREEN_HEIGHT // 3 - self.rect.height
        self.rect.y = random.randrange(0, max(1, max_y)) 
        self.creation_time = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.creation_time
        
        # Blinking effect if warning time passed
        if elapsed > INGREDIENT_WARNING_TIME:
            # Blink interval: 200ms
            if (now // 200) % 2 == 0:
                self.image.set_alpha(50) # Dim
            else:
                self.image.set_alpha(255) # Bright
        else:
            self.image.set_alpha(255) # Ensure normal alpha otherwise

class NervePath:
    """
    Represents the path for the TRAUMA minigame.
    Generates a random jagged path and handles collision detection for deviation.
    """
    def __init__(self):
        self.points = self.generate_path()
        self.start_point = self.points[0]
        self.end_point = self.points[-1]
        self.width = 30 # Thickness of the "safe zone" is implied, visual line thickness might be different

    def generate_path(self):
        # Generate a random jagged line across the screen
        points = []
        start_x = 50
        start_y = SCREEN_HEIGHT // 2
        points.append((start_x, start_y))

        current_x = start_x
        current_y = start_y

        while current_x < SCREEN_WIDTH - 50:
            current_x += random.randint(30, 80)
            current_y += random.randint(-50, 50)
            # Clamp Y
            # Limit to top 1/3 of screen to avoid hand obstruction
            max_y = SCREEN_HEIGHT // 3
            current_y = max(50, min(max_y, current_y))
            points.append((current_x, current_y))
        
        return points

    def draw(self, surface):
        if len(self.points) > 1:
            pygame.draw.lines(surface, VEIN_WHITE, False, self.points, 5)

    def get_distance_to_segment(self, point, segment_start, segment_end):
        # Calculate distance from point to line segment
        px, py = point
        x1, y1 = segment_start
        x2, y2 = segment_end

        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == 0:
            return math.hypot(px - x1, py - y1)

        t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
        t = max(0, min(1, t)) # Clamp to segment

        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        return math.hypot(px - closest_x, py - closest_y)

    def check_deviation(self, mouse_pos):
        # Check if mouse is too far from ALL segments (simplified collision)
        # In a real game, you might track progress along the path.
        # Here we just check if the player is close to ANY part of the line.
        min_dist = float('inf')
        for i in range(len(self.points) - 1):
            dist = self.get_distance_to_segment(mouse_pos, self.points[i], self.points[i+1])
            if dist < min_dist:
                min_dist = dist
        
        return min_dist
