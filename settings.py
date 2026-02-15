
# settings.py
import pygame

# --- Screen Settings ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
CAPTION = "Radicchio Kitchens: Employee Training Module"

# --- Colors ---
# Format: (R, G, B)
RADICCHIO_RED = (142, 35, 68)
VEIN_WHITE = (240, 240, 230)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
GREEN = (0, 255, 0)

# --- Gameplay Settings ---
INITIAL_SANITY = 100
TRAUMA_THRESHOLD = 20
SANITY_PENALTY_MISS = 15
NERVE_DEVIATION_LIMIT = 22 # medium restriction
DAMAGE_TICK_INTERVAL = 750 # ms
INGREDIENT_LIFETIME = 10000 # 10 seconds
INGREDIENT_WARNING_TIME = 6000 # 6 seconds

# --- Assets Paths ---
# Create empty folders for:
# assets/images/
# assets/sounds/
ASSET_DIR_IMAGES = "assets/images"
ASSET_DIR_SOUNDS = "assets/sounds"

# --- Image Assets ---
IMG_HAND_RIGHT = "Right Hand.png"
IMG_HAND_LEFT_NORMAL = "Left Hand.png"
IMG_HAND_LEFT_DAMAGED = "Left Hand Damaged.png"
IMG_HAND_LEFT_BADLY_DAMAGED = "Left Hand Badly Damaged.png"
IMG_HANDS_KNIFE = "Hands with knife.png"
IMG_CURSOR_KNIFE = "Knife Cursor.png"

# --- Scaling ---
HAND_SCALE = 0.3
CURSOR_SCALE = 0.08

# --- Minigame Settings ---
GRACE_PERIOD_DURATION = 3000 # ms
START_POINT_RADIUS = 30
PULSE_SPEED = 0.1 # Factor for sine wave speed
