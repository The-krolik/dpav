from directpythonplatform import *
from utility import draw_rectangle
import random
clock = pygame.time.Clock()



def our_snake(snake_block, snake_list):
    for x in snake_list:
        pt1 = (int(x[0]),int(x[1]))
        pt2 = (int(x[0] + snake_block),int(x[1] + snake_block))
        draw_rectangle(window.vbuffer,white,pt1,pt2)

def newFood():
        window.vbuffer[:] = black
        foodx = round(random.randrange(0, x_dim - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, y_dim - snake_block) / 10.0) * 10.0
        pt1 = (int(foodx),int(foody))
        pt2 = (int(foodx + snake_block),int(foody + snake_block))
        draw_rectangle(window.vbuffer,red,pt1,pt2)
        

white = 0xffffff
black = 0x000000
red = 0xFF0000
    
x_dim = 600
y_dim = 400

window = Window(VBuffer((x_dim,y_dim)))
game_over = False
game_close = False

x1 = x_dim / 2
y1 = y_dim / 2

count = 1
x1_change = 0
y1_change = 0

snake_block = 10
snake_speed = 15

snake_List = []
Length_of_snake = 1

window.open()
gotFood = False
move = True

window.vbuffer[:] = black
foodx = round(random.randrange(0, x_dim - snake_block) / 10.0) * 10.0
foody = round(random.randrange(0, y_dim - snake_block) / 10.0) * 10.0
pt1 = (int(foodx),int(foody))
pt2 = (int(foodx + snake_block),int(foody + snake_block))
draw_rectangle(window.vbuffer,red,pt1,pt2)

while window.is_open():
    
    if 'q' in window.eventq:
        game_over = True
        game_close = False
        quit()
    elif 'w' in window.eventq: #up
        x1_change = 0
        y1_change = -snake_block
    elif 'a' in window.eventq: #left
        x1_change = -snake_block
        y1_change = 0
    elif 's' in window.eventq: #down
        x1_change = 0
        y1_change = snake_block
    elif 'd' in window.eventq: #right
        x1_change = snake_block
        y1_change = 0
    
    x1 += x1_change
    y1 += y1_change
    
    window.vbuffer[:] = black
    if gotFood == True:
        newFood()
        gotFood = False


    
    snake_Head = [x1, y1]
    snake_List.append(snake_Head)
    
    snake_Head = snake_List[0]
    
    
    if len(snake_List) > Length_of_snake:
        del snake_List[0]
    
    if len(snake_List) > 1:
        if snake_Head in snake_List[1:]:
            print(snake_Head)
            print(snake_List[0:])
            quit()

    if snake_Head[0] == x_dim + 1 or snake_Head[0] == -1 or snake_Head[1] == y_dim + 1 or snake_Head[1] == -1:
        quit()
        
    for x in snake_List[:-1]:
        if x == snake_Head:
            game_close = True
            
    our_snake(snake_block,snake_List)
    
    clock.tick(snake_speed)

    if x1 == foodx and y1 == foody:
        gotFood = True
        foodx = round(random.randrange(0, x_dim - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, y_dim - snake_block) / 10.0) * 10.0
        Length_of_snake += 1

