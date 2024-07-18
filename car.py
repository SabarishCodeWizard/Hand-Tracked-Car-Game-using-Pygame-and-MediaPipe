import pygame
import sys
import random
import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8,
    max_num_hands=1
)
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Load video for background
video_path = "D:\GitHub\Hand-Tracked-Car-Game-using-Pygame-and-MediaPipe-main\stock-footage-racing-game-top-down-view-of-road-with-tree-bit-old-video-game-retro-style-background-seamless.webm"
video = cv2.VideoCapture(video_path)

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load background music
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)

# Screen dimensions
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game")

# Load car image
car_img = pygame.image.load("flycar.png")
car_img = pygame.transform.scale(car_img, (300 ,150))

# Load thunder image
thunder_img = pygame.image.load("thunder.png")
thunder_img = pygame.transform.scale(thunder_img, (200, 200))
thunder = []

# Load spaceship image
space_img = pygame.image.load("spaceship.png")
space_img = pygame.transform.scale(space_img, (50, 100))
space = []

# Load jackpot rock image
jackpot_img = pygame.image.load("jackpot_rock.png")
jackpot_img = pygame.transform.scale(jackpot_img, (50, 50))
jackpot_thunder = []

# Load and resize -up images
power_up_images = {
    'invincibility': pygame.transform.scale(pygame.image.load('invincibility_power_up.png'), (100, 100)),
    'speed_boost': pygame.transform.scale(pygame.image.load('speed_boost_power_up.png'), (100, 100)),
    'extra_points': pygame.transform.scale(pygame.image.load('extra_points_power_up.png'), (100, 100)),
}

# Game variables
speed = 8
thunder_speed = 4
jackpot_thunder_speed = 5
space_speed = 4
obstacle_frequency = 100
score = 0
font = pygame.font.Font(None, 36)
start_time = pygame.time.get_ticks()
speed_increment_interval = 7000
speed_increment = 2

# Power-up variables
power_ups = pygame.sprite.Group()
invincible = False
invincible_timer = 0

# Smoothing variables
smoothing_factor = 0.2
smoothed_x = WIDTH // 2
smoothed_y = HEIGHT - 100

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Define PowerUp class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, image, type, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.type = type
        self.speed = 4  # Adjust speed as needed

    def update(self):
        self.rect.y += self.speed

    def apply_power_up(self, player):
        global speed, score, invincible, invincible_timer
        if self.type == 'invincibility':
            invincible = True
            invincible_timer = pygame.time.get_ticks()
            print("Invincibility power-up collected!")
        elif self.type == 'speed_boost':
            speed += 4  # Increase speed for a duration
            pygame.time.set_timer(pygame.USEREVENT + 1, 2000)  # Reset speed after 2 seconds
            print("Speed boost power-up collected!")
        elif self.type == 'extra_points':
            score += 500  # Increase score immediately
            print("Extra points power-up collected!")

# Define Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)

    def update(self, pos):
        self.rect.center = pos

# Initialize player
player = Player(car_img, (WIDTH // 2, HEIGHT - 100))
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Define road boundaries
road_width = int(WIDTH * 0.6)
road_left = (WIDTH - road_width) // 2
road_right = road_left + road_width

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT + 1:
            speed -= 4

    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame to fit within the game window
    frame = cv2.resize(frame, (WIDTH//3, HEIGHT//3))

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and find hands
    result = hands.process(rgb_frame)

    # Extract hand landmarks
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            for landmark in mp_hands.HandLandmark:
                landmark_px = int(hand_landmarks.landmark[landmark].x * frame.shape[1])
                landmark_py = int(hand_landmarks.landmark[landmark].y * frame.shape[0])
                cv2.circle(frame, (landmark_px, landmark_py), 5, (255, 0, 0), -1)

            x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
            y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            x = int(x * WIDTH)
            y = int(y * HEIGHT)
            smoothed_x = int(smoothing_factor * x + (1 - smoothing_factor) * smoothed_x)
            smoothed_y = int(smoothing_factor * y + (1 - smoothing_factor) * smoothed_y)
            player.update((smoothed_x, smoothed_y))
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the webcam frame
    cv2.imshow('Hand Tracking', frame)

    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > WIDTH:
        player.rect.right = WIDTH
    if player.rect.top < 0:
        player.rect.top = 0
    if player.rect.bottom > HEIGHT:
        player.rect.bottom = HEIGHT

    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time > speed_increment_interval:
        speed += speed_increment
        thunder_speed += speed_increment
        space_speed += speed_increment
        jackpot_thunder_speed += speed_increment
        start_time = pygame.time.get_ticks()

    if random.randint(1, obstacle_frequency) == 1:
        rock_rect = thunder_img.get_rect(center=(random.randint(road_left + 50, road_right - 50), -50))
        thunder.append(rock_rect)
    for rock_rect in thunder:
        rock_rect.y += thunder_speed
        if rock_rect.top > HEIGHT:
            thunder.remove(rock_rect)

    if random.randint(1, 500) == 1:
        jackpot_rock_rect = jackpot_img.get_rect(center=(random.randint(road_left + 50, road_right - 50), -50))
        jackpot_thunder.append(jackpot_rock_rect)
    for jackpot_rock_rect in jackpot_thunder:
        jackpot_rock_rect.y += jackpot_thunder_speed
        if jackpot_rock_rect.top > HEIGHT:
            jackpot_thunder.remove(jackpot_rock_rect)

    if random.randint(1, obstacle_frequency) == 1:
        truck_rect = space_img.get_rect(center=(random.randint(road_left + 50, road_right - 50), -50))
        space.append(truck_rect)
    for truck_rect in space:
        truck_rect.x -= space_speed
        if truck_rect.right < 0:
            space.remove(truck_rect)

    if random.randint(1, 100) == 1:
        power_up_type = random.choice(['invincibility', 'speed_boost', 'extra_points'])
        power_up_img = power_up_images[power_up_type]
        power_up_rect = power_up_img.get_rect(center=(random.randint(road_left + 50, road_right - 50), -50))
        power_up = PowerUp(power_up_img, power_up_type, power_up_rect.center)
        power_ups.add(power_up)

    power_ups.update()

    collided_power_ups = pygame.sprite.spritecollide(player, power_ups, True)
    for power_up in collided_power_ups:
        power_up.apply_power_up(player)

    collision_rect = player.rect.inflate(-player.rect.width * 0.3, -player.rect.height * 0.3)
    for rock_rect in thunder:
        if collision_rect.colliderect(rock_rect):
            if not invincible:
                running = False

    for truck_rect in space:
        if collision_rect.colliderect(truck_rect):
            if not invincible:
                running = False
    
    for jackpot_rock_rect in jackpot_thunder:
        if collision_rect.colliderect(jackpot_rock_rect):
            score += 500
            jackpot_thunder.remove(jackpot_rock_rect)

    if invincible and (pygame.time.get_ticks() - invincible_timer) > 5000:
        invincible = False

    # Extract and process video frame for background
    ret, background_frame = video.read()
    if not ret:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop video if it ends
        ret, background_frame = video.read()

    background_frame = cv2.resize(background_frame, (WIDTH, HEIGHT))
    background_frame = cv2.cvtColor(background_frame, cv2.COLOR_BGR2RGB)
    background_frame = np.rot90(background_frame)  # Rotate if needed
    background_surface = pygame.surfarray.make_surface(background_frame)

    # Draw background frame
    screen.blit(background_surface, (0, 0))

    # Draw everything else on top of the background
    screen.blit(player.image, player.rect)
    for rock_rect in thunder:
        screen.blit(thunder_img, rock_rect)
    for jackpot_rock_rect in jackpot_thunder:
        screen.blit(jackpot_img, jackpot_rock_rect)
    for truck_rect in space:
        screen.blit(space_img, truck_rect)
    for power_up in power_ups:
        screen.blit(power_up.image, power_up.rect)

    # Draw score on the right side
    draw_text(f"Score: {score}", font, pygame.Color('white'), screen, WIDTH - 150, 10)

    pygame.display.flip()
    score += 1
    clock.tick(60)

screen.fill((0, 0, 0))
draw_text("Game Over", font, pygame.Color('white'), screen, WIDTH//2 - 100, HEIGHT//2 - 50)
draw_text(f"Final Score: {score}", font, pygame.Color('white'), screen, WIDTH//2 - 100, HEIGHT//2 + 50)
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
sys.exit()
