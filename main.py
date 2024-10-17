import pygame
import random
import time


pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Disco DJ Button Sequence")

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#load sprites and images
title_image = pygame.image.load('assets/title.png')
background_image = pygame.image.load('assets/disco.png')
dj_image = pygame.image.load('assets/seratoDJ.png')
z_button_image = pygame.image.load('assets/z_but.png')
x_button_image = pygame.image.load('assets/x_but.png')
c_button_image = pygame.image.load('assets/c_but.png')

#load sound effects
beat_sound = pygame.mixer.Sound('assets/beat.mp3')
press_sound = pygame.mixer.Sound('assets/fx.mp3')

#scale assets
title_image = pygame.transform.scale(title_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
dj_image = pygame.transform.scale(dj_image, (300, 300))
z_button_image = pygame.transform.scale(z_button_image, (200, 200))
x_button_image = pygame.transform.scale(x_button_image, (200, 200))
c_button_image = pygame.transform.scale(c_button_image, (200, 200))


clock = pygame.time.Clock()


button_positions = {
    'z': (130, 390),
    'x': (310, 390),
    'c': (480, 390)
}

#py font
font = pygame.font.SysFont(None, 55)

#load music
pygame.mixer.music.load('assets/bgm.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#set sir serato's dancing area
dj_x_min = 150
dj_x_max = 350
dj_x_position = 260

dj_move_timer = 0
dj_move_interval = 700


score = 0

#sequence display
def show_sequence(sequence):
    global dj_x_position, dj_move_timer

    #display button sequence for every start of round
    for btn in sequence:
        screen.blit(background_image, (0, 0))

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 200, 20))

        #make serato dance
        if pygame.time.get_ticks() - dj_move_timer > dj_move_interval:
            dj_x_position = random.randint(dj_x_min, dj_x_max)
            dj_move_timer = pygame.time.get_ticks()

        screen.blit(dj_image, (dj_x_position, 80))

        #button sound on press mechanic
        if btn == 'z':
            screen.blit(z_button_image, button_positions['z'])
            beat_sound.play()
        elif btn == 'x':
            screen.blit(x_button_image, button_positions['x'])
            beat_sound.play()
        elif btn == 'c':
            screen.blit(c_button_image, button_positions['c'])
            beat_sound.play()

        pygame.display.update()
        pygame.time.wait(700)


    pygame.time.wait(500)


def check_player_input(sequence, player_input):
    return sequence == player_input


#main game loop
def game_loop():
    global dj_x_position, dj_move_timer, score
    running = True
    dj_sequence = []
    player_sequence = []
    round_active = False
    show_message = False
    message_text = ""

    #title screen display
    screen.blit(title_image, (0, 0))
    pygame.display.update()
    pygame.time.wait(5000)

    while running:
        screen.blit(background_image, (0, 0))

        #move serato to a random position on the dance floor
        if pygame.time.get_ticks() - dj_move_timer > dj_move_interval:
            dj_x_position = random.randint(dj_x_min, dj_x_max)
            dj_move_timer = pygame.time.get_ticks()


        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 200, 20))


        screen.blit(dj_image, (dj_x_position, 80))

        #draw buttons on screem
        screen.blit(z_button_image, button_positions['z'])
        screen.blit(x_button_image, button_positions['x'])
        screen.blit(c_button_image, button_positions['c'])

        #event checker
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if round_active:
                    if event.key == pygame.K_z:
                        player_sequence.append('z')
                        press_sound.play()
                    elif event.key == pygame.K_x:
                        player_sequence.append('x')
                        press_sound.play()
                    elif event.key == pygame.K_c:
                        player_sequence.append('c')
                        press_sound.play()

                    #check if players sequence matches
                    if len(player_sequence) == len(dj_sequence):
                        if check_player_input(dj_sequence, player_sequence):
                            show_message = True
                            message_text = "Correct!"
                            score += 1
                        else:
                            show_message = True
                            message_text = "Wrong!"
                        round_active = False

        #serato dance
        if not round_active and not show_message:
            dj_sequence = [random.choice(['z', 'x', 'c']) for _ in range(3)]
            show_sequence(dj_sequence)
            player_sequence = []
            round_active = True

        #game update result
        if show_message:
            text_surface = font.render(message_text, True, WHITE)
            screen.blit(text_surface, (20, SCREEN_HEIGHT - 50))
            pygame.display.update()
            pygame.time.wait(2000)
            show_message = False


        pygame.display.update()
        clock.tick(30)

    pygame.quit()


#start
game_loop()
