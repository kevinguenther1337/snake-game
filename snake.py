
import random
import pygame

# Colors
APPLE_CL = (180, 0, 0)
SNAKE_CL = (0, 100, 0)  # Snake color
TEXT_CL = (255, 255, 255)


# Board Stats
BLOCK_SIZE = 40  # must be number % 2 = 0
BOARD_SIZE = 24
DISPLAY_SIZE = ((BLOCK_SIZE*BOARD_SIZE), (BLOCK_SIZE*BOARD_SIZE))
AMOUNT_OF_APPLES = 6  # Amount of apples which spawn on the board

# Option stuff
pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption("Snake Game V1.1")
MODE = "DEV"

# Fonts
score_font = pygame.font.SysFont("comicsansms", 40)
end_font = pygame.font.SysFont("comicsansms", 20)
lose_font = pygame.font.SysFont("comicsansms", 60)

#TODO: Add Sound effects, new board design, new features?


# Checks if the player hits wall or himself
def check_collision_with_wall(snake: list):
    # Check if snake hits wall
    if snake[-1][1] >= DISPLAY_SIZE[1] or snake[-1][1] < 0 or\
         snake[-1][0] >= DISPLAY_SIZE[0] or snake[-1][0] < 0:
        return False
    else:
        # Checks if body_part[-1] (Newest body part) hits other body part
        for body_part in snake[:-1]:
            if body_part == snake[-1]:
                return False

    return True


# Creates object on random position
# (Object to create, max amount,
# other coordinate to check pos for)
def create_object(cords: list, am_object: int, other_cords: list):

    while len(cords) < am_object:
        pos_x = random.randrange(BLOCK_SIZE, (
            DISPLAY_SIZE[0]-BLOCK_SIZE), BLOCK_SIZE)
        pos_y = random.randrange(BLOCK_SIZE, (
            DISPLAY_SIZE[1]-BLOCK_SIZE), BLOCK_SIZE)

        # check if apple spawns inside of snake, recurssively draws apple again
        if (pos_x, pos_y) in snake_body or (pos_x, pos_y) in cords or (
                pos_x, pos_y) in other_cords:
            create_object(cords, am_object, other_cords)
        else:
            cords.append((pos_x, pos_y))
            

    return True


# Checks if the object is hit
def colission_with_object(snake_body: list, objects: list):
    for object in objects:
        if (snake_body[-1][0], snake_body[-1][1]) == (object[0], object[1]):
            return False

    return True


# Draws the current score to screen
def draw_score(score: int):
    value = score_font.render(f"SCORE: {score}", True, TEXT_CL)
    display.blit(value, [0, 0])

# Basic view into variables etc.
def draw_dev_info(speed, snake_body: list, apples: list, landmines: list):
    dev_info = end_font.render(
        f"SPEED: {speed}, LENGTH: {len(snake_body)}", True, TEXT_CL)
    display.blit(dev_info, [0, 60])
    dev_info = end_font.render(
        f"APPLES: {len(apples)} LANDMINES: {len(landmines)}", True, TEXT_CL)
    display.blit(dev_info, [0, 80])


# Game options
running = True
try_again = True


def end_screen(running, try_again):
    value = score_font.render(f"SCORE: {score}", True, TEXT_CL)
    text_rect = value.get_rect(center=(
        DISPLAY_SIZE[0]/2, (DISPLAY_SIZE[1]/2)-70))
    display.blit(value, text_rect)

    value = lose_font.render("YOU LOSE!", True, TEXT_CL)
    text_rect = value.get_rect(center=(DISPLAY_SIZE[0]/2, DISPLAY_SIZE[1]/2))
    display.blit(value, text_rect)

    value = end_font.render(
        "PRESS SAPCE TO CONTINUE OR ESACPE TO QUIT!", True, TEXT_CL)
    text_rect = value.get_rect(center=(DISPLAY_SIZE[0]/2, (
        DISPLAY_SIZE[1]/2)+70))
    display.blit(value, text_rect)
    pygame.display.update()

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


# ====(MAIN PART OF GAME)====
while try_again:

    # == Setting default settings ==
    snake_length = 5  # Starting length of snake
    speed = 13.0
    MAX_SPEED = 16.0
    speed_change = 0.125
    snake_body = [(BLOCK_SIZE*BOARD_SIZE/2, BLOCK_SIZE*BOARD_SIZE/2)]
    x_change = 0
    y_change = -BLOCK_SIZE  # UP

    # Game stats
    score = 0
    displaying_apple = False
    displaying_landmines = False

    # Object stats
    apple_counter = 0
    landmines = True  # Set counter to at least 1 to play with landmines
    amount_of_landmines = 0
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
                if event.key == pygame.K_UP:
                    y_change = -BLOCK_SIZE
                    x_change = 0

                elif event.key == pygame.K_DOWN:
                    y_change = BLOCK_SIZE
                    x_change = 0

                elif event.key == pygame.K_RIGHT:
                    x_change = BLOCK_SIZE
                    y_change = 0

                elif event.key == pygame.K_LEFT:
                    x_change = -BLOCK_SIZE
                    y_change = 0

        # Main part
        if running:
            # Adding the new body part at newest position
            snake_body.append(
                (snake_body[-1][0] + x_change, snake_body[-1][1] + y_change))

            # Removes the last part of the body to get body length right
            snake_body.pop(0) if len(snake_body) > snake_length else None

            # Check if the player hits end of board
            running = check_collision_with_wall(snake_body)

            if running:
                # Check if snake hits landmine
                running = colission_with_object(snake_body, landmine_cords)

            # Draw snake body
            for part in snake_body:
                pygame.draw.rect(
                    display, (0,60,0), [part[0], part[1], BLOCK_SIZE, BLOCK_SIZE])
                pygame.draw.rect(
                    display, SNAKE_CL, [part[0], part[1], BLOCK_SIZE-2, BLOCK_SIZE-2])

            # Checks if apple is on board, if not draws new apple
            if not displaying_apple:
                displaying_apple = create_object(
                    apples, AMOUNT_OF_APPLES, landmine_cords)

            # Check if player eats apple
            displaying_apple = colission_with_object(snake_body, apples)

            if not displaying_apple:
                # Adds speed_change to the current speed if snake_speed
                # is lower than SNAKE_MAX_SPEED
                speed += speed_change if speed < MAX_SPEED else 0
                snake_length += 1
                score += 1
                # Adds one landmine to the game every 5th eaten apple
                if landmines == True and score % 5 == 0:
                    amount_of_landmines += 1
                    displaying_landmines = False

                # Removes the eaten apple from game
                apples.remove((snake_body[-1][0], snake_body[-1][1]))

            if landmines == True and not displaying_landmines:
                displaying_landmines = create_object(
                    landmine_cords, amount_of_landmines, apples)

            # Draws apples to board
            for apple in apples:
                pygame.draw.rect(
                    display, (140,0,0), [apple[0], apple[1], BLOCK_SIZE, BLOCK_SIZE])
                pygame.draw.rect(
                    display, APPLE_CL, [apple[0], apple[1], BLOCK_SIZE-2, BLOCK_SIZE-2])

            # Draws landmines to board
            for landmine in landmine_cords:
                pygame.draw.rect(
                    display, (200, 200, 200), [
                        landmine[0], landmine[1], BLOCK_SIZE, BLOCK_SIZE])
                pygame.draw.rect(
                    display, (255, 255, 255), [
                        landmine[0], landmine[1], BLOCK_SIZE-2, BLOCK_SIZE-2])

        # Draw current score
        draw_score(score)
        if MODE == "DEV":  # Dev / else
            draw_dev_info(speed, snake_body, apples, landmine_cords)
        # Update game
        pygame.display.update()
        clock.tick(speed)

    # Try again part or quit
    running, try_again = end_screen(running, try_again)

# Quit game
pygame.quit()
quit()
