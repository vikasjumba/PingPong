__author__ = 'Windows'

# Implementation of classic arcade game Pong

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random
# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
# paddle1_pos and paddle2_pos represent the top vertical position of paddles
# and initial positions are at exact half the width of game.
paddle1_pos = 0
paddle2_pos = 0
paddle1_vel = 0
paddle2_vel = 0
# initialize ball_pos and ball_vel for new bal in middle of table
# The initial values of ball position and velocity will be assigned in spawn_ball().
ball_pos = [0,0]
ball_vel = [0,0]
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_vel[0] = random.randrange(120,240) / 60
    ball_vel[1] = -random.randrange(60,180)  / 60
    ball_pos[0] = WIDTH / 2
    ball_pos[1] = HEIGHT / 2
    if direction == LEFT:
        ball_vel[0] = -ball_vel[0]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT / 2 - PAD_HEIGHT / 2
    paddle2_pos = HEIGHT / 2 - PAD_HEIGHT / 2
    spawn_ball(RIGHT)


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # draw ball
    canvas.draw_circle((ball_pos[0], ball_pos[1]), BALL_RADIUS, 12, 'White','White')
    # update paddle's vertical position, keep paddle on the screen

    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    paddle1_pos  = min(paddle1_pos, HEIGHT - PAD_HEIGHT)
    paddle2_pos  = min(paddle2_pos, HEIGHT - PAD_HEIGHT)
    paddle1_pos  = max(paddle1_pos, 0)
    paddle2_pos  = max(paddle2_pos, 0)

    # draw paddles
    canvas.draw_line([4, paddle1_pos], [4, paddle1_pos + PAD_HEIGHT], PAD_WIDTH, 'White')
    canvas.draw_line([WIDTH - PAD_WIDTH + 4, paddle2_pos], \
    [WIDTH - PAD_WIDTH + 4, paddle2_pos + PAD_HEIGHT], PAD_WIDTH, 'White')
    # determine whether paddle and ball collide
    # Bouncing condition for up and down wall
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
# bound parameters, hardcoded values are added for smooth game experience
    leftBound = BALL_RADIUS - PAD_WIDTH + 23
    rightBound = WIDTH - BALL_RADIUS - PAD_WIDTH - 7
    p1UpBound = paddle1_pos - BALL_RADIUS
    p1LowBound = paddle1_pos + PAD_HEIGHT + BALL_RADIUS
    p2UpBound = paddle2_pos - BALL_RADIUS
    p2LowBound = paddle2_pos + PAD_HEIGHT + BALL_RADIUS
# Bouncing condition for left and right wall without gutters
    if (ball_pos[0] <= leftBound and p1UpBound <= ball_pos[1] <= p1LowBound) or \
    (ball_pos[0] >= rightBound and p2UpBound <= ball_pos[1] <= p2LowBound):
        ball_vel[0] = -ball_vel[0]
    # increase the ball velocity by 10%
        ball_vel[0] += 0.1*ball_vel[0]
        ball_vel[1] += 0.1*ball_vel[1]
    elif ball_pos[0] <= leftBound:  # respawning conditions
        score2 += 1
        spawn_ball(RIGHT)
    elif ball_pos[0] >= rightBound:
        score1 += 1
        spawn_ball(LEFT)
    # draw scores
    canvas.draw_text(str(score1), [WIDTH / 2 - 120, 100], 80, 'White')
    canvas.draw_text(str(score2), [WIDTH / 2 + 50, 100], 80, 'White')
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -180.0 / 60
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 180.0 / 60
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -180.0 / 60
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 180.0 / 60

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
def restart():
    new_game()
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_canvas_background('Maroon')
frame.add_button('Restart', restart, 100)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
new_game()
frame.start()

