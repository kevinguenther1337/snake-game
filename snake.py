import random
import pygame

# Colors
APPLE_CL = (180, 0, 0)
SNAKE_CL = (0, 100, 0)
TEXT_CL = (255, 255, 255)
COLOR_LIST = [(0, 0, 255), (0,127,255), (0, 0, 255), (255, 128, 0), (255, 0 , 255), (0, 255, 0), (255, 0, 0),   ]

# Board Stats
MAX_SPEED = 18.0
BLOCK_SIZE = 34 # must be number % 2 = 0
BOARD_SIZE = 22
DISPLAY_SIZE = ((BLOCK_SIZE*BOARD_SIZE), (BLOCK_SIZE*BOARD_SIZE))
AMOUNT_OF_APPLES =  4 # Amount of apples which spawn on the board
COLOR_MODE = True
 
# Option stuff
pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode(DISPLAY_SIZE, 0, 0, 0, 144)
pygame.display.set_caption("Snake Game V1.2")
running = True
try_again = True

# Fonts
FONT_NAME = "Arial Black"
score_font = pygame.font.SysFont(FONT_NAME, 30)
end_font = pygame.font.SysFont(FONT_NAME, 20)
lose_font = pygame.font.SysFont(FONT_NAME, 60)


# Checks if the player hits wall or himself
def check_snake_collision(snake: list):
    # Check if snake hits wall
    if snake[-1][1] >= DISPLAY_SIZE[1] or snake[-1][1] < 0 or\
            snake[-1][0] >= DISPLAY_SIZE[0] or snake[-1][0] < 0:
        return False
    else:
        # Check if snake hits body part
        return False if snake[-1] in snake[:-1] else True


# Creates new object at random position
def create_object(cords: list, am_object: int, other_cords: list):

    while len(cords) < am_object:
        new_cords = (
            random.randrange(BLOCK_SIZE, (
                DISPLAY_SIZE[0]-BLOCK_SIZE), BLOCK_SIZE),
            random.randrange(BLOCK_SIZE, (
                DISPLAY_SIZE[0]-BLOCK_SIZE), BLOCK_SIZE))

        # check if apple spawns inside of snake, recurssively creates new cords
        if new_cords in snake_body or new_cords in cords or\
                new_cords in other_cords:
            create_object(cords, am_object, other_cords)
        else:
            cords.append(new_cords)
    return True


# Checks if object is hit by snake
def colission_with_object(snake_body: list, objects: list):
    return not snake_body[-1] in objects


# Draws score
def draw_score(score: int):
    value = score_font.render(f"SCORE: {score}", True, TEXT_CL)
    display.blit(value, [0, 0])


def end_screen(running, try_again):
    value = score_font.render(f"SCORE: {score}", True, TEXT_CL)
    text_rect = value.get_rect(center=(
        DISPLAY_SIZE[0]/2, (DISPLAY_SIZE[1]/2)-40))
    display.blit(value, text_rect)

    value = lose_font.render("YOU LOSE!", True, TEXT_CL)
    text_rect = value.get_rect(center=(DISPLAY_SIZE[0]/2, DISPLAY_SIZE[1]/2))
    display.blit(value, text_rect)

    value = end_font.render(
        "PRESS SPACE TO CONTINUE OR ESACPE TO QUIT!", True, TEXT_CL)
    text_rect = value.get_rect(center=(DISPLAY_SIZE[0]/2, (
        DISPLAY_SIZE[1]/2)+40))
    display.blit(value, text_rect)
    pygame.display.update()

    # Get user input
    while not running and try_again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try_again = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = True
                elif event.key == pygame.K_ESCAPE:
                    try_again = False

    return running, try_again


while try_again:

    # == Default settings ==
    speed_change = 0.125
    snake_body = [(BLOCK_SIZE*BOARD_SIZE/2, BLOCK_SIZE*BOARD_SIZE/2)]  # Snake starting position
    displaying_apple = False
    displaying_landmines = False
    landmines = True # Adds landmines to the game

    # Inital movement => up
    x_change = 0
    y_change = -BLOCK_SIZE

    # Game settings
    score = 0
    snake_length = 3  # Starting length of snake
    speed = 12

    # Object stats
    apples = []
    landmine_cords = []

    while running:
        display.fill("BLACK")  # Background color

        # Key handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:  # if key is pressed
                if (event.key == pygame.K_UP or event.key == pygame.K_w) \
                    and not (y_change == BLOCK_SIZE and x_change == 0):
                    y_change = -BLOCK_SIZE
                    x_change = 0

                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) \
                    and not (y_change == -BLOCK_SIZE and x_change == 0):
                    y_change = BLOCK_SIZE
                    x_change = 0
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) \
                    and not (y_change == 0 and x_change == -BLOCK_SIZE):
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) \
                    and not (y_change == 0 and x_change == BLOCK_SIZE):
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_p:
                    paused = True
                    # Pause game
                    while paused:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            elif event.type == pygame.KEYDOWN:
                                paused = False if event.key == pygame.K_p or event.key == pygame.K_SPACE else True
                                quit() if event.key == pygame.K_ESCAPE else None
                        clock.tick(144)
                elif event.key == pygame.K_ESCAPE:
                    quit()

        # Main part
        if running:
            # Adding the new body part at newest position
            snake_body.append(
                (snake_body[-1][0] + x_change, snake_body[-1][1] + y_change))

            # Removes the last part of the body to get body length right
            snake_body.pop(0) if len(snake_body) > snake_length else None

            # Check if the player hits end of board
            running = check_snake_collision(snake_body)

            if landmines and running:
                running = colission_with_object(snake_body, landmine_cords)

            # Draw snake body
            for part in snake_body:
                pygame.draw.rect(
                    display, (0, 60, 0),
                    [part[0], part[1], BLOCK_SIZE, BLOCK_SIZE])
                if COLOR_MODE:
                    pygame.draw.rect(
                        display, random.choice(COLOR_LIST),
                        [part[0], part[1], BLOCK_SIZE-2, BLOCK_SIZE-2])
                else:
                    pygame.draw.rect(
                        display, (0, 130, 0),
                        [part[0], part[1], BLOCK_SIZE-2, BLOCK_SIZE-2])

            # Checks if apple is on board, if not draws new apple
            if not displaying_apple:
                displaying_apple = create_object(
                    apples, AMOUNT_OF_APPLES, landmine_cords)

            # Check if player eats apple
            displaying_apple = colission_with_object(snake_body, apples)

            if not displaying_apple:
                # Adds speed_change to the current speed if snake_speed
                # is lower than MAX_SPEED
                speed += speed_change if speed < MAX_SPEED else 0.02
                snake_length += 1
                score += 1

                # Adds one landmine to the game every x eaten apple
                if landmines and (score % 5 == 0):
                    displaying_landmines = create_object(
                        landmine_cords, len(landmine_cords) + 1, apples)

                # Removes the eaten apple from game
                apples.remove((snake_body[-1][0], snake_body[-1][1]))

            if landmines and not displaying_landmines:
                displaying_landmines = create_object(
                    landmine_cords, len(landmine_cords), apples)

                # Replacing every x mines position for more randomness
                if len(landmine_cords) % 5 == 0 and len(landmine_cords) != 0:
                    landmine_cords.pop(random.randrange(0,len(landmine_cords)))
                    displaying_landmines = create_object(
                        landmine_cords, len(landmine_cords), apples)

            # Draws apples to board
            for apple in apples:
                pygame.draw.rect(
                    display, (140, 0, 0),
                    [apple[0], apple[1], BLOCK_SIZE, BLOCK_SIZE])
                pygame.draw.rect(
                    display, APPLE_CL,
                    [apple[0], apple[1], BLOCK_SIZE-2, BLOCK_SIZE-2])

            # Draws landmines to board
            if landmines:
                for landmine in landmine_cords:
                    pygame.draw.rect(
                        display, (100, 100, 100), [
                            landmine[0], landmine[1], BLOCK_SIZE, BLOCK_SIZE])
                    pygame.draw.rect(
                        display, (128, 128, 128), [
                            landmine[0], landmine[1],
                            BLOCK_SIZE-2, BLOCK_SIZE-2])

        # Update game
        draw_score(score)
        pygame.display.update()
        clock.tick(speed)

    # Try again part or quit
    running, try_again = end_screen(running, try_again)

# Quit game
pygame.quit()
quit()
