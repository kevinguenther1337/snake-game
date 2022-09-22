
import pygame,random

# Colors
BLUE = (0,0,255)
RED = (200,0,0)
GREEN = (0,125,0) # Snake color
BLACK = (0,0,0)
WHITE = (255,255,255)

# Board Stats
BOX_SIZE = 30
BOARD_SIZE = 30
DISPLAY_SIZE = ((BOX_SIZE*BOARD_SIZE),(BOX_SIZE*BOARD_SIZE))


# Option stuff
pygame.init()
clock = pygame.time.Clock()
score_font = pygame.font.SysFont("comicsansms",40)
end_font = pygame.font.SysFont("comicsansms",20)
lose_font = pygame.font.SysFont("comicsansms",60)
display = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption("Snake Game")

# Checks if the player hits wall or himself
def check_collision(snake: list):
    # Check if snake hits wall
    if snake[-1][1] >= DISPLAY_SIZE[1] or snake[-1][1] < 0 or snake[-1][0] >= DISPLAY_SIZE[0] or snake[-1][0] < 0:
        return False
    else:
        # Checks if segment[-1] (Newest body part) hits other body part
        for segment in snake[:-1]:
                if segment == snake[-1]:
                    return False

    return True

# Draws apple to screen
def draw_apple(apples : list, apple_counter : int, amount_of_apples : int):

    while len(apples) < amount_of_apples:
        apple_x = random.randrange(BOX_SIZE,(DISPLAY_SIZE[0]-BOX_SIZE),BOX_SIZE)
        apple_y = random.randrange(BOX_SIZE,(DISPLAY_SIZE[1]-BOX_SIZE),BOX_SIZE)

        # check if apple spawns inside of snake, recurssively draws apple again
        if (apple_x,apple_y) in snake_body:
            draw_apple(apples,apple_counter,amount_of_apples)

        apples.append((apple_x,apple_y))
        apple_counter += 1

    return True

# Checks if the apple has been eaten
def check_apple(snake_body: list, apples: list):
    for apple in apples:
        if (snake_body[-1][0],snake_body[-1][1]) == (apple[0],apple[1]):
            return False
        
    return True

# Draws the current score to screen
def draw_score(score: int):
    value = score_font.render(f"SCORE: {score}", True, BLACK)
    display.blit(value,[0,0])

running = True
try_again = True
while try_again:     

    # Snake starting stats
    snake_length = 5
    snake_speed = 10.0
    speed_change = 0.25
    snake_body = [(BOX_SIZE*BOARD_SIZE/2,BOX_SIZE*BOARD_SIZE/2)] # Starting body 
    x_change = 0
    y_change = -BOX_SIZE #UP

    # Game stats
    score = 0
    displaying_apple = False
    amount_of_apples = 4
    apple_counter = 0
    apples = []

    while running:
        display.fill("white")

        # Key handling
        for event in pygame.event.get():
            if  event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -BOX_SIZE
                    x_change = 0

                elif event.key == pygame.K_DOWN:
                    y_change = BOX_SIZE
                    x_change = 0

                elif event.key == pygame.K_RIGHT:
                    x_change = BOX_SIZE
                    y_change = 0

                elif event.key == pygame.K_LEFT:
                    x_change = -BOX_SIZE
                    y_change = 0

            
        # Main part 
        if running:
            # Append current coordinates to snake body
            snake_body.append((snake_body[-1][0] + x_change,snake_body[-1][1] + y_change))

            # Removes the last part of the body to get body length right
            if len(snake_body) > snake_length:
                snake_body.pop(0)

            # Check if the player hits body / window wall
            running = check_collision(snake_body)

            # Draw snake body
            for segment in snake_body:
                pygame.draw.rect(display, GREEN, [segment[0], segment[1], BOX_SIZE, BOX_SIZE])

            # Checks if apple is on board, if not draws new apple
            if not displaying_apple:
                displaying_apple = draw_apple(apples,apple_counter, amount_of_apples)

            # Check if player eats apple
            displaying_apple = check_apple(snake_body,apples)

            if not displaying_apple:
                snake_speed += speed_change
                snake_length += 1
                score += 1
                apples.remove((snake_body[-1][0],snake_body[-1][1]))

            for apple in apples:
                pygame.draw.rect(display, RED, [apple[0], apple[1], BOX_SIZE, BOX_SIZE])
        
        # Draw current score
        draw_score(score)

        # Update game
        pygame.display.update()
        clock.tick(snake_speed)
    

    value = score_font.render(f"SCORE: {score}", True, BLACK)
    text_rect = value.get_rect(center=(DISPLAY_SIZE[0]/2,(DISPLAY_SIZE[1]/2)-70))
    display.blit(value,text_rect)

    value = lose_font.render(f"YOU LOSE!", True, BLACK)
    text_rect = value.get_rect(center=(DISPLAY_SIZE[0]/2,DISPLAY_SIZE[1]/2))
    display.blit(value,text_rect)

    value = end_font.render(f"PRESS SAPCE TO CONTINUE OR ESACPE TO QUIT!", True, BLACK)
    text_rect = value.get_rect(center=(DISPLAY_SIZE[0]/2,(DISPLAY_SIZE[1]/2)+70))
    display.blit(value,text_rect)
    pygame.display.update()

    while not running and try_again:
        for event in pygame.event.get():
            if  event.type == pygame.QUIT:
                try_again = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = True
                elif event.key == pygame.K_ESCAPE:
                    try_again = False

# Quit game 
pygame.quit()
quit()

