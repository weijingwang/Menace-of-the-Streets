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
next_x = current_lane*-road_width

while not done:
    lanes = [
        [(focal_point,horizon_line),[x,screen_height],[x+road_width,screen_height]],
        [(focal_point,horizon_line),[x+road_width,screen_height],[x+road_width*2,screen_height]],
        [(focal_point,horizon_line),[x+road_width*2,screen_height],[x+road_width*3,screen_height]],
        [(focal_point,horizon_line),[x+road_width*3,screen_height],[x+road_width*4,screen_height]],
        [(focal_point,horizon_line),[x+road_width*4,screen_height],[x+road_width*5,screen_height]],
        [(focal_point,horizon_line),[x+road_width*5,screen_height],[x+road_width*6,screen_height]],
        [(focal_point,horizon_line),[x+road_width*6,screen_height],[x+road_width*7,screen_height]],
        [(focal_point,horizon_line),[x+road_width*7,screen_height],[x+road_width*8,screen_height]]
    ]

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                current_lane+=1
                next_x = current_lane*-road_width
                move_right = True
            elif event.key == pygame.K_LEFT:
                current_lane-=1
                next_x = current_lane*-road_width
                move_left = True
            
    # if current_lane<0:
    #     current_lane=0
    # elif current_lane>7:
    #     current_lane=7

    if move_right==True:
        if x>=next_x:
            x-=10
        else:
            x=next_x
            move_right=False

    if move_left==True:
        if x<=next_x:
            x+=10
        else:
            x=next_x
            move_left=False

    print(current_lane,next_x)

    # print(current_lane)

    screen.fill("black")
    for lane in lanes:
        pygame.gfxdraw.filled_polygon(screen,lane,(lane[2][0]%255,lane[1][0]%255,lane[2][0]%255))


    clock.tick(60)
    pygame.display.update()