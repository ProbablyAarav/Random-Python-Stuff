import tkinter as tk
import random

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
SPIKE_SIZE = 30
GOAL_SIZE = 30
MAX_PLATFORMS = 10  # Maximum number of platforms per level
MAX_JUMP_DISTANCE = 200  # Maximum horizontal distance the player can jump

# Create the main window
root = tk.Tk()
root.title("Platformer Game")
canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="blue")
canvas.pack()

# Variables
current_level = 0
player_x, player_y = 50, 500
velocity_x, velocity_y = 0, 0
is_jumping = False
gravity = 2
move_speed = 5

# Platforms, Spikes, and Goal
platforms = []
spikes = []
goal = None
running = False  # Variable to control the game loop

# Functions for game mechanics
def create_platform(x, y):
    platform = canvas.create_rectangle(x, y, x + PLATFORM_WIDTH, y + PLATFORM_HEIGHT, fill="green")
    platforms.append(platform)

def create_spike(x, y):
    spike = canvas.create_polygon(x, y, x + SPIKE_SIZE / 2, y - SPIKE_SIZE, x + SPIKE_SIZE, y, fill="red")
    spikes.append(spike)

def create_goal(x, y):
    global goal
    goal = canvas.create_oval(x, y, x + GOAL_SIZE, y + GOAL_SIZE, fill="red")

def reset_player_position():
    global player_x, player_y, velocity_x, velocity_y, is_jumping
    player_x, player_y = canvas.coords(platforms[0])[:2]
    player_x += (PLATFORM_WIDTH - PLAYER_WIDTH) // 2  # Center player on the first platform
    player_y -= PLAYER_HEIGHT
    velocity_x, velocity_y = 0, 0
    is_jumping = False

def move_player():
    global player_x, player_y, velocity_x, velocity_y, is_jumping
    
    # Gravity effect
    velocity_y += gravity
    
    # Update player position
    player_x += velocity_x
    player_y += velocity_y
    
    # Collision with platforms
    for platform in platforms:
        x1, y1, x2, y2 = canvas.coords(platform)
        if player_x + PLAYER_WIDTH > x1 and player_x < x2 and player_y + PLAYER_HEIGHT >= y1 and player_y + PLAYER_HEIGHT <= y2:
            velocity_y = 0
            is_jumping = False
            player_y = y1 - PLAYER_HEIGHT

    # Collision with spikes
    for spike in spikes:
        coords = canvas.coords(spike)
        if player_x + PLAYER_WIDTH > coords[0] and player_x < coords[4] and player_y + PLAYER_HEIGHT >= coords[1]:
            reset_player_position()

    # Collision with goal
    if goal:
        gx1, gy1, gx2, gy2 = canvas.coords(goal)
        if player_x + PLAYER_WIDTH > gx1 and player_x < gx2 and player_y + PLAYER_HEIGHT > gy1 and player_y < gy2:
            go_to_next_level()

    # Collision with window boundaries
    if player_x < 0:
        player_x = 0
    if player_x + PLAYER_WIDTH > WINDOW_WIDTH:
        player_x = WINDOW_WIDTH - PLAYER_WIDTH
    if player_y > WINDOW_HEIGHT:
        reset_player_position()

def update_canvas():
    canvas.delete("player")
    canvas.create_rectangle(player_x, player_y, player_x + PLAYER_WIDTH, player_y + PLAYER_HEIGHT, fill="gray", tags="player")

def start_game(level=1):
    global current_level, running
    current_level = level
    running = True
    load_level(level)
    game_loop()

def load_level(level):
    canvas.delete("all")
    platforms.clear()
    spikes.clear()
    
    if level <= 10:
        generate_predefined_level(level)
    else:
        generate_ai_level(level)
    
    reset_player_position()

def generate_predefined_level(level):
    # Generate predefined levels 1-10
    num_platforms = max(2, MAX_PLATFORMS - level)  # Fewer platforms as level increases
    platform_gap = WINDOW_HEIGHT // (num_platforms + 1)  # Space between platforms
    
    last_x, last_y = 50, platform_gap  # Start with the first platform near the player
    create_platform(last_x, last_y)
    
    for i in range(1, num_platforms):
        platform_x = random.randint(max(0, last_x - MAX_JUMP_DISTANCE), min(WINDOW_WIDTH - PLATFORM_WIDTH, last_x + MAX_JUMP_DISTANCE))
        platform_y = platform_gap * (i + 1)
        create_platform(platform_x, platform_y)
        last_x, last_y = platform_x, platform_y
    
    # Add spikes based on level
    if level >= 5:
        num_spikes = min(level - 4, num_platforms)  # Increase number of spikes with difficulty
        for _ in range(num_spikes):
            spike_x = random.randint(0, WINDOW_WIDTH - SPIKE_SIZE)
            spike_y = random.randint(0, WINDOW_HEIGHT - SPIKE_SIZE)
            create_spike(spike_x, spike_y)
    
    # Place the goal at a random location on the last platform
    last_platform_coords = canvas.coords(platforms[-1])
    goal_x = last_platform_coords[0] + random.randint(0, PLATFORM_WIDTH - GOAL_SIZE)
    goal_y = last_platform_coords[1] - GOAL_SIZE
    create_goal(goal_x, goal_y)

def generate_ai_level(level):
    # Procedurally generate levels beyond level 10
    difficulty = level - 10  # Increase difficulty with each new AI-generated level
    
    num_platforms = max(2, MAX_PLATFORMS - difficulty)  # Fewer platforms as difficulty increases
    platform_gap = WINDOW_HEIGHT // (num_platforms + 1)  # Space between platforms
    
    last_x, last_y = 50, platform_gap  # Start with the first platform near the player
    create_platform(last_x, last_y)
    
    for i in range(1, num_platforms):
        platform_x = random.randint(max(0, last_x - MAX_JUMP_DISTANCE), min(WINDOW_WIDTH - PLATFORM_WIDTH, last_x + MAX_JUMP_DISTANCE))
        platform_y = platform_gap * (i + 1)
        create_platform(platform_x, platform_y)
        last_x, last_y = platform_x, platform_y
    
    # Add spikes based on difficulty
    num_spikes = min(difficulty, num_platforms)  # Increase number of spikes with difficulty
    for _ in range(num_spikes):
        spike_x = random.randint(0, WINDOW_WIDTH - SPIKE_SIZE)
        spike_y = random.randint(0, WINDOW_HEIGHT - SPIKE_SIZE)
        create_spike(spike_x, spike_y)
    
    # Place the goal at a random location on the last platform
    last_platform_coords = canvas.coords(platforms[-1])
    goal_x = last_platform_coords[0] + random.randint(0, PLATFORM_WIDTH - GOAL_SIZE)
    goal_y = last_platform_coords[1] - GOAL_SIZE
    create_goal(goal_x, goal_y)

def go_to_next_level():
    global current_level
    current_level += 1
    load_level(current_level)

def on_key_press(event):
    global velocity_x, velocity_y, is_jumping
    if event.keysym in ("a", "Left"):
        velocity_x = -move_speed
    elif event.keysym in ("d", "Right"):
        velocity_x = move_speed
    elif event.keysym in ("w", "Up"):
        if not is_jumping:
            velocity_y = -20
            is_jumping = True

def on_key_release(event):
    global velocity_x
    if event.keysym in ("a", "Left", "d", "Right"):
        velocity_x = 0

# Home screen and level select
def show_home_screen():
    global running
    running = False
    canvas.delete("all")
    start_button = tk.Button(root, text="Start Game", command=lambda: start_game(1))
    select_button = tk.Button(root, text="Select Level", command=show_level_select)
    canvas.create_window(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 30, window=start_button)
    canvas.create_window(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 30, window=select_button)

def show_level_select():
    global running
    running = False
    canvas.delete("all")
    buttons = []
    for i in range(1, 11):
        button = tk.Button(root, text=f"Level {i}", command=lambda i=i: start_game(i))
        buttons.append(button)
        canvas.create_window(WINDOW_WIDTH / 2, 50 + i * 40, window=button)

# Main game loop
def game_loop():
    if running:
        move_player()
        update_canvas()
        root.after(16, game_loop)

# Bind the keys
root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)

# Start the game at the home screen
show_home_screen()
root.mainloop()
