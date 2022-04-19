import pygame
import time
import random
import directpythonplatform as dpp
 
pygame.init()
 
#converted the colors to HEX values, as needed for vbuffer
#white = (255, 255, 255)
white = 0xFFFFFF
#yellow = (255, 255, 102)
yellow = 0xFFFF00
#black = (0, 0, 0)
black = 0x000000
#red = (213, 50, 80)
red = 0xFF0000
#green = (0, 255, 0)
green = 0x008000
#blue = (50, 153, 213)
blue = 0x0000FF
 
#dis_width = 600
#dis_height = 400
dimensions = [600, 400]
 
#dis = pygame.display.set_mode((dis_width, dis_height))
vb = dpp.VBuffer(dimensions)
dis = dpp.Window(vb, 1)
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 15

 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
        #draw_rectangle(vb, black, x[0], x[1])    #our function, have yet to test it so I commented it out
 
#unchanged
def gameLoop():
    game_over = False
    game_close = False
 
    x1 = dimensions[0] / 2
    y1 = dimensions[1] / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1
 
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
 
    while not game_over:
 
        while game_close == True:
            dis.fill(blue)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
 
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        #draw_rectangle(vb, black, x[0], x[1])   #same as above
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
 
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
 
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 
 
gameLoop()