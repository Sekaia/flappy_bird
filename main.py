# TODO:
# Random color pipes
# random bird each time
import pygame, sys, random, bird


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


def create_pipe():
    random_pipe_position = random.choice(pipe_height)
    bottom_pipe = green_pipe_surface.get_rect(midtop = (700, random_pipe_position))
    top_pipe = green_pipe_surface.get_rect(midbottom = (700, random_pipe_position - 300))
    return bottom_pipe, top_pipe


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(green_pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(red_pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes


def check_collision(pipes):
    global can_score

    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        can_score = True
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(state):
    if state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)
    if state == 'game_start' or state == 'game_over':
        score_surface = game_font.render(f'Score: {(int(score))}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {(int(high_score))}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)


def update_score(current, high):
    if current > high:
        high = current
    return high


def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True


pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)

# Game Variables
gravity = 0.25
bird_movement = 0
game_state = "game_start" # game_start, game_active, game_over
score = 0
high_score = 0
can_score = True

# Background
day_bg_surface = pygame.transform.scale2x(pygame.image.load('assets/background-day.png').convert())
night_bg_surface = pygame.transform.scale2x(pygame.image.load('assets/background-night.png').convert())

# Floor
floor_surface = pygame.transform.scale2x(pygame.image.load('assets/base.png').convert())
floor_x_pos = 0

# Bird Animations
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 512))
# Timer for animation
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Pipes
green_pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png').convert())
red_pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe-red.png').convert())
pipe_list = []
# Timer for pipe spawns
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

# Day/night timer
DAYNIGHT = pygame.USEREVENT + 2
pygame.time.set_timer(DAYNIGHT, 10000)
day_or_night = "day"

# Game start screen
game_start_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_start_rect = game_start_surface.get_rect(center = (288, 512))

# Game over screen
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/gameover.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288, 512))

# Sounds
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')


# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state == "game_active":
                bird_movement = 0
                bird_movement -= 10
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_state == "game_start":
                game_state = "game_active"
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0
            if event.key == pygame.K_SPACE and game_state == "game_over":
                game_state = "game_start"
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()
        if event.type == DAYNIGHT:
            if day_or_night == "day":
                day_or_night = "night"
            else:
                day_or_night = "day"

    if day_or_night == "day":
        screen.blit(day_bg_surface, (0, 0))
    else:
        screen.blit(night_bg_surface, (0, 0))

    if game_state == "game_active":
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        if not check_collision(pipe_list):
            game_state = "game_over"

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        pipe_score_check()
        score_display('main_game')

    elif game_state == "game_start":
        screen.blit(game_start_surface, game_start_rect)
        high_score = update_score(score, high_score)
        score_display('game_start')

    elif game_state == "game_over":
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
