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





class lane:
    def __init__(self,x,width):
        self.x=x
        self.width = width
    def draw(self):
        pygame.draw.line(screen,"white",(focal_point,horizon_line),(self.x,screen_height),5)
        pygame.draw.line(screen,"white",(focal_point,horizon_line),(self.x+road_width,screen_height),5)



lanes = [
    [(focal_point,horizon_line),[x,screen_height],[x+road_width,screen_height]],
    [(focal_point,horizon_line),[x,screen_height],[x-road_width,screen_height]]
]




while not done:
    lanes = [
        [(focal_point,horizon_line),[x,screen_height],[x+road_width,screen_height]],
        [(focal_point,horizon_line),[x,screen_height],[x-road_width,screen_height]],
        [(focal_point,horizon_line),[x+road_width,screen_height],[x+road_width*2,screen_height]],
        [(focal_point,horizon_line),[x+road_width*2,screen_height],[x+road_width*3,screen_height]],
        [(focal_point,horizon_line),[x-road_width,screen_height],[x-road_width*2,screen_height]],
        [(focal_point,horizon_line),[x-road_width*2,screen_height],[x-road_width*3,screen_height]]
        
    ]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                accel_x = 0
            elif event.key == pygame.K_LEFT:
                accel_x = 0

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_RIGHT]: 
        accel_x+=0.1
        x -= 10+accel_x
    if pressed[pygame.K_LEFT]:
        accel_x+=0.1
        x += 10+accel_x


    screen.fill("black")
    for lane in lanes:
        pygame.gfxdraw.filled_polygon(screen,lane,(lane[2][0]%255,lane[1][0]%255,lane[2][0]%255))
    # pygame.draw.line(screen,"white",(focal_point,horizon_line),(x,screen_height),5)
    # pygame.draw.line(screen,"white",(focal_point,horizon_line),(x+road_width,screen_height),5)
    # pygame.draw.line(screen,"white",(focal_point,horizon_line),(x-road_width,screen_height),5)
    # pygame.draw.line(screen,"white",(focal_point,horizon_line),(x+road_width*2,screen_height),5)
    # pygame.draw.line(screen,"white",(focal_point,horizon_line),(x-road_width*2,screen_height),5)
    # pygame.draw.line(screen,"white",(focal_point,horizon_line),(x+road_width*3,screen_height),5)
    # pygame.draw.line(screen,"white",(focal_point,horizon_line),(x-road_width*3,screen_height),5)
    # pygame.draw.line(screen,"white",(focal_point,horizon_line),(x+road_width*4,screen_height),5)
    # pygame.draw.line(screen,"white",(focal_point,horizon_line),(x-road_width*4,screen_height),5)   

    clock.tick(60)
    pygame.display.update()
    