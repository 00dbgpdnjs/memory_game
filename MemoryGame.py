import pygame  
from random import * 

# set by level
def setup(level):
    # how long do i show numbers before hiding it by rect
    global display_time
    display_time = 5 - (level // 3)
    display_time = max(display_time, 1) # display_time < 1 -> 1
    # how many number do users have to memory?
    number_count = (level // 3) + 5
    number_count = min(number_count, 20) # max of number

    # dispose number randomly to gid form at screen
    shuffle_grid(number_count)

# Shuffle number (the most important part)
def shuffle_grid(number_count):
    rows = 5
    columns = 9

    cell_size = 130 # width, height size each grid cell
    button_size = 110 # the size of the button that will actually be drawn within grid cell
    screen_left_margin = 55
    screen_top_margin = 20

    # [[0, 0, 0, 0, 0, 0, 0, 5, 0],
    #  [0, 0, 0, 0, 0, 4, 0, 0, 0],
    #  [0, 1, 0, 0, 0, 0, 2, 0, 0],
    #  [0, 0, 0, 0, 3, 0, 0, 0, 0],
    #  [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    grid = [[0 for col in range(columns)] for row in range(rows)] # 5 * 9 grid, all values is 0

    number = 1 # depose from 1 to number_count
    while number <= number_count:
        row_idx = randrange(0, rows) # y-coordinate/ line 2; select randomly among 0 ~ 5 
        col_idx = randrange(0, columns) # select X-coordinate randomly among 0 ~ 8

        # fill the number in the x, y coordinates when the value is 0: because overlapping causes some numbers to disappear
        if grid[row_idx][col_idx] == 0: # []: double list access
            grid[row_idx][col_idx] = number # Number(v)
            number += 1 

            # Calculate x, y coordinates of current grid cell pos
            center_x = screen_left_margin + (col_idx * cell_size) + (cell_size / 2)
            center_y = screen_top_margin + (row_idx * cell_size) + (cell_size / 2)

            # Make number button
            button = pygame.Rect(0, 0, button_size, button_size)
            button.center = (center_x, center_y)

            number_buttons.append(button) # Append btn to number_btn var list

    # Check random number deposed
    # print(grid) # in terminal

def display_start_screen():
    pygame.draw.circle(screen, WHITE, start_button.center, 60, 5) # (,,, Radius, thickness)

    # Show their current level at 'start screen'
    msg = game_font.render(f"{curr_level}", True, WHITE) # render(text, antialias, color, background=None)
    msg_rect = msg.get_rect(center=start_button.center) # get_rect(): Get msg to rect
    screen.blit(msg, msg_rect) # (what, where)

def display_game_screen():
    global hidden

    if not hidden:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # current time (Time goes on and on.) - "start_button click" time
    #print("Game Start") # '/1000': millisec -> sec
        if elapsed_time > display_time:
            hidden = True
    for idx, rect in enumerate(number_buttons, start=1): # bring the list values one by one from number_btns list to rect, Put the index number in idx
        if hidden:
            pygame.draw.rect(screen, WHITE, rect) # Draw rect to hide numbers
        else:
            # number text
            cell_text = game_font.render(str(idx), True, WHITE) # value of text, The 2nd factor is antalias
            text_rect = cell_text.get_rect(center=rect.center) # where
            screen.blit(cell_text, text_rect) # draw by blit func: (what, where)

# Check if coordinates clicked(=pos) are in 'start button'
def check_buttons(pos): 
    global start, start_ticks # when value of glovar var is changed 
    if start:
        check_number_buttons(pos) # Check order of clicked number
    elif start_button.collidepoint(pos): # if 'pos' are in 'start_button'
        start = True 
        start_ticks = pygame.time.get_ticks() # Store current time 

def check_number_buttons(pos):
    global start, hidden, curr_level

    for button in number_buttons: # in order  of list
        if button.collidepoint(pos): # area of 'button' is included in 'pos'?
            if button == number_buttons[0]:
                # print("Correct") 
                del number_buttons[0] # Delete So second become first 
                if not hidden:
                    hidden = True 
            else: # a user clicked a wrong order
                game_over()
                # print("Wrong")
            break 

    # If a user pass each level, level up and go back to the start_screen again
    if len(number_buttons) == 0:
        start = False # display_start_screen()
        hidden = False
        curr_level += 1
        setup(curr_level) # Run setup() again acoording to the next level 

# game over and show a msg
def game_over():
    global running
    running = False # to escape 'game loop'

    msg = game_font.render(f"Your level is {curr_level}", True, WHITE) # render(text, antialias, color, background=None)
    msg_rect = msg.get_rect(center=(screen_width/2, screen_height/2)) 

    screen.fill(BLACK) # not to overlap with game screen 
    screen.blit(msg, msg_rect) # (what, where)

pygame.init() # reset(necessary)
screen_width = 1280 
screen_height = 720 
screen = pygame.display.set_mode((screen_width, screen_height)) 
pygame.display.set_caption("Memory Game") 
game_font = pygame.font.Font(None, 120) 
# (the font type is none (=default font), size)

start_button = pygame.Rect(0, 0, 120, 120) 
start_button.center = (120, screen_height - 120) 

BLACK = (0, 0, 0) 
WHITE = (250, 250, 250)
GRAY = (50, 50, 50)

number_buttons = [] # list about buttons to play
curr_level = 1 
display_time = None # time to display numbers before hiding it by rect
start_ticks = None # (*Search 'tick') Store current time when a user click start_button So put this var in 'def check_buttons'

# game start status var
start = False 
# when a user click 1, hide all numbers
hidden = False

# Perform setup func before game start 
setup(curr_level) 

# game loop 
running = True 
while running:
    click_pos = None 

    # event(=keyboard or mouse) loop
    for event in pygame.event.get(): # Which event 
        if event.type == pygame.QUIT: 
            running = False 
        elif event.type == pygame.MOUSEBUTTONUP: 
            click_pos = pygame.mouse.get_pos() # Stores 'click pos'
            # print(click_pos) 

    screen.fill(BLACK) 

    if start:
        display_game_screen()
    else:
        display_start_screen() 

    if click_pos: # Run when click_pos is and Check if coordinates clicked are in 'start button'
        check_buttons(click_pos)

    # necessary after screen work; to display a new screen
    pygame.display.update() # blank screen -> display_start_screen()

# to give a user 5 sec to check own level before closing the game
pygame.time.delay(5000)

# End game
pygame.quit()