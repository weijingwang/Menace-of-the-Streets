
import pygame
import pygame.gfxdraw
import os
import random
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,current_lane,lane_data,my_lane,z) -> None:
        super().__init__()

        self.scale = 0
        self.image = pygame.image.load("./assets/car_b.png").convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.midbottom = 1280/2,720/3

        self.current_lane = current_lane
        self.lane_data = lane_data
        self.my_lane = my_lane

        self.pos = [1280/2,720/3]


        self.speed =0.5
        self.z = z


        # self.width = width
        # self.height = height
        
    def update(self,lane_data):
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     self.pos[1]+=100
        # print(self.rect.x)
        if self.scale>1000:
            self.kill()


        delta_y_f = 240-720
        delta_x_f = (1280/2)-(((lane_data[self.my_lane][1]-lane_data[self.my_lane][0])/2)+lane_data[self.my_lane][0])
        delta_ratio = delta_x_f/delta_y_f
        delta_y_now = 240-self.pos[1]
        delta_x_now = delta_y_now*delta_ratio
        new_x = (1280/2)-delta_x_now
        #MOVE CAR HERE
        self.pos[1]+=self.speed
        self.pos[0]=new_x


        delta_y_fO = 240-720
        delta_x_fL = (1280/2)-lane_data[self.my_lane][0]
        delta_x_fR = (1280/2)-lane_data[self.my_lane][1]
        delta_ratioL = delta_x_fL/delta_y_f
        delta_ratioR = delta_x_fR/delta_y_f
        delta_y_nowO = 240-self.pos[1]
        delta_x_nowL = delta_y_now*delta_ratioL
        delta_x_nowR = delta_y_now*delta_ratioR
        new_xL = (1280/2)-delta_x_nowL
        new_xR = (1280/2)-delta_x_nowR
        obst_width = abs(new_xL-new_xR)
        # print(obst_width)
        self.scale =int(obst_width)

        self.image = pygame.transform.scale(self.original_image, (self.scale, int(self.scale/2)))
        self.rect = self.image.get_rect(midbottom = self.pos)
        # print(self.rect)


class Game():
    def __init__(self,current_lane,screen):
        #IMAGES
        self.stars_bg = pygame.image.load("./assets/stars.png").convert_alpha()
        self.POV_car = pygame.image.load("./assets/POV_car.png").convert_alpha()
        self.fog = pygame.image.load("./assets/fog.png").convert_alpha()
        #BASIC
        self.screen = screen
        self.screen_height = 720
        self.screen_width = 1280
        self.y0 = self.screen_height/3
        self.x0 = self.screen_width/2
        self.road_width=self.screen_width
        self.z = 0


        #LANES
        self.current_lane =current_lane
        self.move_left = False
        self.move_right= False
        self.x = self.current_lane*-self.road_width
        self.next_x = self.current_lane*-self.road_width

        self.lane_array = [
            [0,1,(33,83,33)],
            [1,2,(66,66,66)],
            [2,3,(99,99,99)],
            [3,4,(132,132,132)],
            [4,5,(165,165,165)],
            [5,6,(198,248,198)]
        ]


        # pygame.gfxdraw.filled_polygon(self.screen,[(self.x0,self.y0),[self.x+self.road_width*lane[0],self.screen_height],[self.x+self.road_width*lane[1],self.screen_height]],lane[2])
        self.lane_data = [
            [self.x+self.road_width*self.lane_array[0][0],self.x+self.road_width*self.lane_array[0][1]],
            [self.x+self.road_width*self.lane_array[1][0],self.x+self.road_width*self.lane_array[1][1]],
            [self.x+self.road_width*self.lane_array[2][0],self.x+self.road_width*self.lane_array[2][1]],
            [self.x+self.road_width*self.lane_array[3][0],self.x+self.road_width*self.lane_array[3][1]],
            [self.x+self.road_width*self.lane_array[4][0],self.x+self.road_width*self.lane_array[4][1]],
            [self.x+self.road_width*self.lane_array[5][0],self.x+self.road_width*self.lane_array[5][1]]
        ]



        #OBSTACLES
        self.obstacle_group = pygame.sprite.Group()


    def update_lane(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.current_lane+=1
                    self.next_x = self.current_lane*-self.road_width
                    self.move_right = True
                elif event.key == pygame.K_LEFT:
                    self.current_lane-=1
                    self.next_x = self.current_lane*-self.road_width
                    self.move_left = True
        if self.move_right==True:
            if self.x>=self.next_x:
                self.x-=self.screen_width*0.0125
            else:
                self.x=self.next_x
                self.move_right=False
        if self.move_left==True:
            if self.x<=self.next_x:
                self.x+=self.screen_width*0.0125
            else:
                self.x=self.next_x
                self.move_left=False
        if self.current_lane==-1 or self.current_lane ==6:
            print("YOU DIE")
        # print(self.lane_data)
        self.lane_data = [
            [self.x+self.road_width*self.lane_array[0][0],self.x+self.road_width*self.lane_array[0][1]],
            [self.x+self.road_width*self.lane_array[1][0],self.x+self.road_width*self.lane_array[1][1]],
            [self.x+self.road_width*self.lane_array[2][0],self.x+self.road_width*self.lane_array[2][1]],
            [self.x+self.road_width*self.lane_array[3][0],self.x+self.road_width*self.lane_array[3][1]],
            [self.x+self.road_width*self.lane_array[4][0],self.x+self.road_width*self.lane_array[4][1]],
            [self.x+self.road_width*self.lane_array[5][0],self.x+self.road_width*self.lane_array[5][1]]
        ]
        # print(self.lane_data)
        self.obstacle_group.update(self.lane_data)

        # print(self.lane_data)
    def run(self):
        screen.fill((20,24,82))
        self.screen.blit(pygame.transform.scale(self.stars_bg,(screen_width,screen_height)),(0,0))

        pygame.draw.rect(self.screen,(14,47,38),(0,240,1280,480))
        # random_x = randrange(-3,3)
        # random_y = randrange(-3,3)

        for lane in self.lane_array:
            pygame.gfxdraw.filled_polygon(self.screen,[(self.x0,self.y0),[self.x+self.road_width*lane[0],self.screen_height],[self.x+self.road_width*lane[1],self.screen_height]],lane[2])


        self.obstacle_group.draw(self.screen)
        self.obstacle_group.update(self.lane_data)


        self.screen.blit(pygame.transform.scale(self.fog,(self.screen_width,self.screen_height)),(0,0))
        pygame.draw.rect(self.screen,"black",(0,620,1280,100))
        self.screen.blit(pygame.transform.scale(self.POV_car,(screen_width,screen_height)),(0,0))

    def move_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.z+=1

    def spawn_obstacles(self):
        enemy_count=random.randrange(0,4)
        
        if self.z>=40:
            for x in range(0,enemy_count):
                x = Obstacle(self.current_lane,self.lane_data,random.randrange(1,5),self.z)
                self.obstacle_group.add(x)
            self.z=0
        print(self.z)
                






pygame.mixer.pre_init()
pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
clock= pygame.time.Clock()
done = False
bob=pygame.mixer.music.load("./assets/i drivin and they hatin.mp3")
# bob=pygame.mixer.music.load("./assets/menace of the streets.mp3")
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(1)
print(bob)
my_game = Game(4,screen)
while not done:
    my_game.move_player()
    my_game.update_lane()
    my_game.spawn_obstacles()
    my_game.run()
    clock.tick(60)
    pygame.display.update()