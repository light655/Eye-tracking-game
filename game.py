import cv2
from GazeTracking.gaze_tracking import GazeTracking
import matplotlib.pyplot as plt
import numpy as np
import pygame

# gaze tracking setup
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# initial condition of motion of ball
ball_pos_vec = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_v_mag = screen.get_height() / 2.0    # speed of ball is half the height of the screen per second
ball_v_ang = np.pi / 8.0                  # initial moving angle of 22.5 degrees

# function to bounce the ball back when it hit the wall
def bounce(pos_vec, v_ang):
    if pos_vec.x >= screen.get_width() or pos_vec.x <= 0.0:
        v_ang = np.pi - v_ang
        if v_ang > np.pi: 
            v_ang -= 2 * np.pi
    elif pos_vec.y >= screen.get_height() or pos_vec.y <= 0.0:
        v_ang *= -1

    return pos_vec, v_ang

# data arrays
i = 0
n_frame = 300
v_eye = np.zeros(n_frame)
h_eye = np.zeros(n_frame)
v_ball = np.zeros(n_frame)
h_ball = np.zeros(n_frame)

# game loop
while running and i < n_frame:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update gaze tracking
    _, frame = webcam.read()        # read a frame from webcam
    gaze.refresh(frame)             # analyse frame with gaze tracker
    v_eye[i] = gaze.vertical_ratio()    # store eye gaze direction to array
    h_eye[i] = gaze.horizontal_ratio()

    # update ball's position on screen
    ball_pos_vec, ball_v_ang = bounce(ball_pos_vec, ball_v_ang)
    ball_pos_vec += ball_v_mag * pygame.Vector2(np.cos(ball_v_ang), -np.sin(ball_v_ang)) * dt
        # the negative sign for y-axis is required due to the left-handed coordinates
    h_ball[i] = ball_pos_vec.x      # store ball position to array
    v_ball[i] = ball_pos_vec.y

    screen.fill("purple")
    pygame.draw.circle(screen, "red", ball_pos_vec, 40)
    pygame.display.flip()           # update screen frame

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    i += 1

pygame.quit()   # close game window

def standardise(arr):
    return (arr - np.mean(arr)) / np.std(arr)

# standardise the position of the ball and the eyes
v_eye = standardise(v_eye)
h_eye = standardise(h_eye) * -1
v_ball = standardise(v_ball)
h_ball = standardise(h_ball)

n_frames = np.arange(n_frame)

fig, (ax1, ax2) = plt.subplots(2, 1, layout="constrained")
ax1.plot(n_frames, v_ball, n_frames, v_eye)
ax1.set_ylim(-3, 3)
ax1.set_xlabel("Frame")
ax1.set_ylabel("Vertical Position")
ax2.plot(h_ball, n_frames, h_eye, n_frames)
ax2.set_xlim(-3, 3)
ax2.set_xlabel("Horizontal Position")
ax2.set_ylabel("Frame")
plt.show()