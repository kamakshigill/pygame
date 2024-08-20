import pygame
import random

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")


bird_sprites = pygame.image.load("assets/bird_sprites.jpeg").convert_alpha()
background_image = pygame.image.load("assets/background.jpeg").convert_alpha()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
pipe_image = pygame.image.load("assets/pipe.jpeg").convert_alpha()
pipe_image = pygame.transform.scale(pipe_image, (70, SCREEN_HEIGHT))
flap_sound = pygame.mixer.Sound("assets/flap-101soundboards.mp3")
hit_sound = pygame.mixer.Sound("assets/flappy-bird-hit-sound-101soundboards.mp3")


bird_frames = [
    bird_sprites.subsurface(pygame.Rect(0, 0, 50, 50)),
    bird_sprites.subsurface(pygame.Rect(50, 0, 50, 50)),
    bird_sprites.subsurface(pygame.Rect(100, 0, 50, 50)),
]


new_width = 25
new_height = 25
bird_frames = [pygame.transform.scale(frame, (new_width, new_height)) for frame in bird_frames]

bird_frame_index = 0
bird_frame_countdown = 5


bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
gravity = 0.5
flap_strength = -10
downward_force = 10
bird_width, bird_height = 25, 25

pipe_width = 70
pipe_gap = 200
pipe_velocity = -5

pipes = []

def create_pipe():
    pipe_height = random.randint(150, 400)
    pipe_top = pygame.Rect(SCREEN_WIDTH, 0, pipe_width, pipe_height)
    pipe_bottom = pygame.Rect(SCREEN_WIDTH, pipe_height + pipe_gap, pipe_width, SCREEN_HEIGHT - pipe_height - pipe_gap)
    return pipe_top, pipe_bottom

pipes.append(create_pipe())

score = 0
high_score = 0
font = pygame.font.Font(None, 36)

def reset_game():
    global bird_y, bird_velocity, pipes, score, bird_frame_index
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    pipes = [create_pipe()]
    score = 0
    bird_frame_index = 0

def update_high_score():
    global high_score, score
    if score > high_score:
        high_score = score

def check_collision(bird_rect, pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
            return True
    return False

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):  # Flap with SPACE, W, or UP_ARROW
                bird_velocity = flap_strength
                flap_sound.play()
            elif event.key in (pygame.K_s, pygame.K_DOWN):  # Fall faster with S or DOWN_ARROW
                bird_velocity += downward_force


    bird_velocity += gravity


    bird_y += bird_velocity


    if bird_y > SCREEN_HEIGHT - bird_height:
        bird_y = SCREEN_HEIGHT - bird_height
        bird_velocity = 0
    if bird_y < 0:
        bird_y = 0
        bird_velocity = 0


    bird_frame_countdown -= 1
    if bird_frame_countdown <= 0:
        bird_frame_index = (bird_frame_index + 1) % len(bird_frames)
        bird_frame_countdown = 5

    bird_image = bird_frames[bird_frame_index]


    for pipe in pipes:
        pipe[0].x += pipe_velocity
        pipe[1].x += pipe_velocity

    if pipes[-1][0].x < SCREEN_WIDTH // 2:
        pipes.append(create_pipe())

    if pipes[0][0].x < -pipe_width:
        pipes.pop(0)
        score += 1


    bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
    if bird_y > SCREEN_HEIGHT - bird_height or bird_y < 0:
        hit_sound.play()
        pygame.time.delay(1000)
        update_high_score()
        reset_game()

    if check_collision(bird_rect, pipes):
        hit_sound.play()
        pygame.time.delay(1000)
        update_high_score()
        reset_game()


    screen.blit(bird_image, (bird_x, bird_y))
    for pipe in pipes:
        screen.blit(pipe_image, pipe[0].topleft, (0, 0, pipe_width, pipe[0].height))
        screen.blit(pipe_image, pipe[1].topleft, (0, SCREEN_HEIGHT - pipe[1].height, pipe_width, pipe[1].height))


    score_text = font.render(f"Score: {score}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))

    pygame.display.flip()
    clock.tick(30)


pygame.quit()
