import pygame
import random
import time

# Initialize pygame and mixer for audio
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Disco DJ Button Sequence")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load DJ and button images
dj_image = pygame.image.load('assets/seratoDJ.png')  # You can replace this with any image you want
z_button_image = pygame.image.load('assets/z_but.png')
x_button_image = pygame.image.load('assets/x_but.png')
c_button_image = pygame.image.load('assets/c_but.png')

# Resize images
dj_image = pygame.transform.scale(dj_image, (300, 300))
z_button_image = pygame.transform.scale(z_button_image, (200, 200))
x_button_image = pygame.transform.scale(x_button_image, (200, 200))
c_button_image = pygame.transform.scale(c_button_image, (200, 200))

# Game clock
clock = pygame.time.Clock()

# Button positions on the screen
button_positions = {
    'z': (130, 390),
    'x': (310, 390),
    'c': (480, 390)
}

# Fonts
font = pygame.font.SysFont(None, 55)

# Load background music
pygame.mixer.music.load('assets/bgm.mp3')  # Replace with your own file
pygame.mixer.music.play(-1)  # Play indefinitely

# DJ's x-axis movement range for "dancing" (center area)
dj_x_min = 150  # Left bound of the center area
dj_x_max = 350  # Right bound of the center area
dj_x_position = 260  # Initial x-position for DJ (center)

# Timer for DJ movement to slow down the movement
dj_move_timer = 0
dj_move_interval = 700  # Time in milliseconds between moves (0.7 seconds)

# Score initialization
score = 0

# Display the sequence of buttons pressed by the DJ
def show_sequence(sequence):
    global dj_x_position, dj_move_timer

    # Display each button press symbol with delay
    for btn in sequence:
        screen.fill(BLACK)

        # Draw the score in the top right corner
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 200, 20))

        # Move DJ to a new random x position based on the beat timer
        if pygame.time.get_ticks() - dj_move_timer > dj_move_interval:
            dj_x_position = random.randint(dj_x_min, dj_x_max)
            dj_move_timer = pygame.time.get_ticks()  # Reset the move timer

        screen.blit(dj_image, (dj_x_position, 50))

        # Show the button currently being pressed
        if btn == 'z':
            screen.blit(z_button_image, button_positions['z'])
        elif btn == 'x':
            screen.blit(x_button_image, button_positions['x'])
        elif btn == 'c':
            screen.blit(c_button_image, button_positions['c'])

        pygame.display.update()
        pygame.time.wait(700)  # 0.7 seconds between button presses

    # Short delay after showing the full sequence
    pygame.time.wait(500)


def check_player_input(sequence, player_input):
    return sequence == player_input


# Main game loop
def game_loop():
    global dj_x_position, dj_move_timer, score
    running = True
    dj_sequence = []
    player_sequence = []
    round_active = False
    show_message = False
    message_text = ""

    while running:
        screen.fill(BLACK)

        # Move DJ to a new random x position based on the beat timer
        if pygame.time.get_ticks() - dj_move_timer > dj_move_interval:
            dj_x_position = random.randint(dj_x_min, dj_x_max)
            dj_move_timer = pygame.time.get_ticks()  # Reset the move timer

        # Draw the score in the top right corner
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 200, 20))

        # Display the DJ in the new position
        screen.blit(dj_image, (dj_x_position, 50))

        # Draw the buttons
        screen.blit(z_button_image, button_positions['z'])
        screen.blit(x_button_image, button_positions['x'])
        screen.blit(c_button_image, button_positions['c'])

        # Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if round_active:
                    if event.key == pygame.K_z:
                        player_sequence.append('z')
                    elif event.key == pygame.K_x:
                        player_sequence.append('x')
                    elif event.key == pygame.K_c:
                        player_sequence.append('c')

                    # Once the player's sequence length matches the DJ's, check it
                    if len(player_sequence) == len(dj_sequence):
                        if check_player_input(dj_sequence, player_sequence):
                            show_message = True
                            message_text = "Correct!"
                            score += 1  # Increment score on correct input
                        else:
                            show_message = True
                            message_text = "Wrong!"
                        round_active = False

        # If not in an active round, generate new DJ sequence
        if not round_active and not show_message:
            dj_sequence = [random.choice(['z', 'x', 'c']) for _ in range(3)]
            show_sequence(dj_sequence)
            player_sequence = []
            round_active = True

        # Show the result of the round in the bottom left
        if show_message:
            text_surface = font.render(message_text, True, WHITE)
            screen.blit(text_surface, (20, SCREEN_HEIGHT - 50))
            pygame.display.update()
            pygame.time.wait(2000)  # Pause for 2 seconds
            show_message = False

        # Update the screen
        pygame.display.update()
        clock.tick(30)

    pygame.quit()


# Start the game
game_loop()
