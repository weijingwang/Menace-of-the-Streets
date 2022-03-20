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


x = road_width*4
accel_x = 0
accel_z = 0



class lane:
    def __init__(self,x,width):
        self.x=x
        self.width = width
    def draw(self):
        pygame.draw.line(screen,"white",(focal_point,horizon_line),(self.x,screen_height),5)
        pygame.draw.line(screen,"white",(focal_point,horizon_line),(self.x+road_width,screen_height),5)



move_right = False
move_left = False
current_lane = 0

while not done:
    lanes = [
        [(focal_point,horizon_line),[x-road_width*2,screen_height],[x-road_width*4,screen_height]],
        [(focal_point,horizon_line),[x-road_width*2,screen_height],[x-road_width*3,screen_height]],
        [(focal_point,horizon_line),[x-road_width,screen_height],[x-road_width*2,screen_height]],
        [(focal_point,horizon_line),[x,screen_height],[x-road_width,screen_height]],
        [(focal_point,horizon_line),[x,screen_height],[x+road_width,screen_height]],
        [(focal_point,horizon_line),[x+road_width,screen_height],[x+road_width*2,screen_height]],
        [(focal_point,horizon_line),[x+road_width*2,screen_height],[x+road_width*3,screen_height]],
        [(focal_point,horizon_line),[x+road_width*2,screen_height],[x+road_width*4,screen_height]]
    ]

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                current_lane+=1
                move_right = True
            elif event.key == pygame.K_LEFT:
                current_lane-=1
                move_left = True
            


    if move_right==True:
        x-=800
        move_right=False
    elif move_left==True:
        x+=800
        move_left=False


    print(current_lane)

    screen.fill("black")
    for lane in lanes:
        pygame.gfxdraw.filled_polygon(screen,lane,(lane[2][0]%255,lane[1][0]%255,lane[2][0]%255))


    clock.tick(60)
    pygame.display.update()
    