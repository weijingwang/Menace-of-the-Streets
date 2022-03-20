from doctest import DONT_ACCEPT_BLANKLINE
import pygame
import pygame.gfxdraw

pygame.init()
done = False

screen_width = 800
screen_height = 600
horizon_line = screen_height/3
focal_point = screen_width/2
road_width = screen_width


screen = pygame.display.set_mode((screen_width,screen_height))
clock= pygame.time.Clock()


x = 0
accel_x = 0
accel_z = 0



move_right = False
move_left = False
current_lane = 0

while not done:
    lanes = [
<<<<<<< HEAD
<<<<<<< HEAD
        [(focal_point,horizon_line),[x,screen_height],[x+road_width,screen_height]],
        [(focal_point,horizon_line),[x+road_width,screen_height],[x+road_width*2,screen_height]],
        [(focal_point,horizon_line),[x+road_width*2,screen_height],[x+road_width*3,screen_height]],
        [(focal_point,horizon_line),[x+road_width*3,screen_height],[x+road_width*4,screen_height]],
        [(focal_point,horizon_line),[x+road_width*4,screen_height],[x+road_width*5,screen_height]],
        [(focal_point,horizon_line),[x+road_width*5,screen_height],[x+road_width*6,screen_height]],
        [(focal_point,horizon_line),[x+road_width*6,screen_height],[x+road_width*7,screen_height]],
        [(focal_point,horizon_line),[x+road_width*7,screen_height],[x+road_width*8,screen_height]]
=======
=======
>>>>>>> parent of 5761411 (proper order for lanes)
        [(focal_point,horizon_line),[x-road_width*2,screen_height],[x-road_width*3,screen_height]],
        [(focal_point,horizon_line),[x-road_width,screen_height],[x-road_width*2,screen_height]],
        [(focal_point,horizon_line),[x,screen_height],[x-road_width,screen_height]],
        [(focal_point,horizon_line),[x,screen_height],[x+road_width,screen_height]],
        [(focal_point,horizon_line),[x+road_width,screen_height],[x+road_width*2,screen_height]],
        [(focal_point,horizon_line),[x+road_width*2,screen_height],[x+road_width*3,screen_height]]
<<<<<<< HEAD
>>>>>>> parent of 5761411 (proper order for lanes)
=======
>>>>>>> parent of 5761411 (proper order for lanes)
    ]

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_LEFT:
                move_left = True
            


    if move_right==True:
        if -road_width*current_lane-road_width<=x:
            print(road_width*current_lane,x,current_lane)
            x-=10
        else:
            move_right=False
            current_lane-=1
    elif move_left==True:
        x+=800
        move_left=False
        current_lane+=1


    print(current_lane)

    screen.fill("black")
    for lane in lanes:
        pygame.gfxdraw.filled_polygon(screen,lane,(lane[2][0]%255,lane[1][0]%255,lane[2][0]%255))


    clock.tick(60)
    pygame.display.update()
    