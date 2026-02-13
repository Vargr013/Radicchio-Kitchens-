
import pygame
import sys
from settings import *
from state_manager import StateManager
from sprites import ChefHand, Cursor

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()
    
    # Load custom cursor or use ChefHand sprite
    pygame.mouse.set_visible(False) 
    
    # Initialize Game Components
    state_manager = StateManager()
    hand = ChefHand()
    cursor = Cursor()
    all_sprites = pygame.sprite.Group(hand, cursor)

    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Pass events to state manager
            state_manager.handle_input(event)

        # 2. Update
        state_manager.update()
        all_sprites.update()

        # 3. Draw
        screen.fill(BLACK) # Clear screen
        
        # State Manager handles drawing game state
        state_manager.draw(screen)
        
        # Draw hand on top
        all_sprites.draw(screen)

        # 4. Refresh Display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
