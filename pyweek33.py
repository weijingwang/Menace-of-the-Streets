import pygame
import pygame.gfxdraw
import os
import random

class Background(pygame.sprite.Sprite):
    def __init__(self,scroll_speed,direction,x):
        super().__init__()
        self.x = x
        self.pos =[self.x,720/3]
        self.scroll_speed = scroll_speed
        self.image =pygame.image.load("./assets/cityback.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(int(1280/2),int(720/4)))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos
        self.direction = direction
        

    def update(self):
        if self.direction == "right":
            self.pos[0]+=self.scroll_speed
            if self.pos[0]>1280:
                self.pos[0]=self.x
            self.rect = self.image.get_rect(midbottom = self.pos)
        if self.direction =="left":
            self.pos[0]-=self.scroll_speed
            if self.pos[0]<0:
                self.pos[0]=self.x
            self.rect = self.image.get_rect(midbottom = self.pos)

        

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type,my_lane) -> None:
        super().__init__()
        self.my_lane = my_lane
        self.image_link = None
        self.type = type

        self.height_multiplier = 0

        if self.type == 1 or self.type == 2:
            self.image_link = "./assets/car_f.png"

            self.height_multiplier = 0.5

        elif self.type == self.type == 3 or self.type ==4:
            self.image_link = "./assets/car_b.png"
            self.height_multiplier = 0.5

        elif self.type == 0 or self.type == 5:
            self.image_link = ("./assets/house_off.png")
            self.height_multiplier = 3
        elif self.type == 6:
            self.image = "./assets/empty.png"

        self.house_on = pygame.image.load("./assets/house_on.png").convert_alpha()


        self.image = pygame.image.load("./assets/car_b.png").convert_alpha()

        self.scale = 0
        self.image = pygame.image.load(self.image_link).convert_alpha()
        self.original_image = self.image
        self.image = pygame.transform.scale(self.original_image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = 1280/2,720/3

        self.pos = [1280/2,720/3]


        self.speed =0.0001
        self.accel = 0.005
        self.new_accel = 0.005
        # self.z = z


        # self.width = width
        # self.height = height
        self.is_kill = False
        

    def update(self,lane_data,current_lane,remove_this):
        # print(self.my_lane)
        keys = pygame.key.get_pressed()
        if remove_this == self.my_lane:
            print("killed",self.my_lane)
            self.kill()
        if self.scale>800:
            self.is_kill=True
            self.kill()
        if self.scale>800 and self.my_lane == current_lane:
            print("DIE")
            quit()

        if keys[pygame.K_SPACE]:
            self.speed += self.new_accel*5
            self.new_accel+=0.001
        # print(self.new_accel)
            # print("YESSSSSS++++++++++")
        if self.type == 0 or self.type ==5:
            if self.scale<800 and self.scale >100:
                # print("do it now")
                if (self.my_lane == 0 and current_lane ==1) or (self.my_lane == 5 and current_lane ==4):
                    if keys[pygame.K_SPACE]:
                        # self.kill()
                        self.original_image = self.house_on
                        # print("YESSSSSS++++++++++")
        # print(current_lane)
        delta_y_f = 240-720
        delta_x_f = (1280/2)-(((lane_data[self.my_lane][1]-lane_data[self.my_lane][0])/2)+lane_data[self.my_lane][0])
        delta_ratio = delta_x_f/delta_y_f
        delta_y_now = 240-self.pos[1]
        delta_x_now = delta_y_now*delta_ratio
        new_x = (1280/2)-delta_x_now
        #MOVE CAR HERE
        self.pos[1]+=self.speed
        self.speed+=self.accel
        self.pos[0]=new_x

        delta_x_fL = (1280/2)-lane_data[self.my_lane][0]
        delta_x_fR = (1280/2)-lane_data[self.my_lane][1]
        delta_ratioL = delta_x_fL/delta_y_f
        delta_ratioR = delta_x_fR/delta_y_f
        delta_x_nowL = delta_y_now*delta_ratioL
        delta_x_nowR = delta_y_now*delta_ratioR
        new_xL = (1280/2)-delta_x_nowL
        new_xR = (1280/2)-delta_x_nowR
        obst_width = abs(new_xL-new_xR)
        self.scale =int(obst_width)

        self.image = pygame.transform.scale(self.original_image, (self.scale, int(self.scale*self.height_multiplier)))
        self.rect = self.image.get_rect(midbottom = self.pos)

class Game():
    def __init__(self,current_lane,screen):
        #IMAGES
        self.stars_bg = pygame.image.load("./assets/stars.png").convert_alpha()
        self.cityback = pygame.image.load("./assets/cityback.png").convert_alpha()
        self.POV_car_L = pygame.image.load("./assets/POV_car_L.png").convert_alpha()
        self.POV_car_M = pygame.image.load("./assets/POV_car_M.png").convert_alpha()
        self.POV_car_R = pygame.image.load("./assets/POV_car_R.png").convert_alpha()
        self.fog = pygame.image.load("./assets/fog.png").convert_alpha()
        self.evil_twin = pygame.image.load("./assets/evil_twin.png").convert_alpha()
        self.mayor_twin = pygame.image.load("./assets/mayor_twin.png").convert_alpha()

        self.image = self.POV_car_M
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
        self.lane0 = pygame.sprite.Group()
        self.lane1 = pygame.sprite.Group()
        self.lane2 = pygame.sprite.Group()
        self.lane3 = pygame.sprite.Group()
        self.lane4 = pygame.sprite.Group()
        self.lane5 = pygame.sprite.Group()
        self.lane_occupant = [self.lane0,self.lane1,self.lane2,self.lane3,self.lane4,self.lane5]

        self.the_one_who_will_be_removed = 0


    def update_lane(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and self.move_left == False:
                    self.image=self.POV_car_R
                    self.current_lane+=1
                    self.next_x = self.current_lane*-self.road_width
                    self.move_right = True
                elif event.key == pygame.K_LEFT and self.move_right == False:
                    self.image=self.POV_car_L
                    self.current_lane-=1
                    self.next_x = self.current_lane*-self.road_width
                    self.move_left = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    self.image = self.POV_car_M

        if self.move_right==True:
            if self.x>=self.next_x:
                self.x-=self.screen_width*0.04#0.0125
            else:
                self.x=self.next_x
                self.move_right=False
        if self.move_left==True:
            if self.x<=self.next_x:
                self.x+=self.screen_width*0.04
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


        # print(self.lane_data)
    def run(self):
        self.screen.fill((20,24,82))
        self.screen.blit(pygame.transform.scale(self.stars_bg,(screen_width,screen_height)),(0,0))

        pygame.draw.rect(self.screen,(14,47,38),(0,240,1280,480))
        # self.screen.blit(pygame.transform.scale(self.cityback,(screen_width,screen_height)),(0,0))
        # self.background_group.draw(self.screen)
        # self.background_group.update()
        # random_x = randrange(-3,3)
        # random_y = randrange(-3,3)

        for lane in self.lane_array:
            pygame.gfxdraw.filled_polygon(self.screen,[(self.x0,self.y0),[self.x+self.road_width*lane[0],self.screen_height],[self.x+self.road_width*lane[1],self.screen_height]],lane[2])


        self.lane1.draw(self.screen)
        self.lane2.draw(self.screen)
        self.lane3.draw(self.screen)
        self.lane4.draw(self.screen)
        self.screen.blit(pygame.transform.scale(self.fog,(self.screen_width,self.screen_height)),(0,0))
        self.lane0.draw(self.screen)
        self.lane5.draw(self.screen)

        self.lane0.update(self.lane_data,self.current_lane,self.the_one_who_will_be_removed)
        self.lane1.update(self.lane_data,self.current_lane,self.the_one_who_will_be_removed)
        self.lane2.update(self.lane_data,self.current_lane,self.the_one_who_will_be_removed)
        self.lane3.update(self.lane_data,self.current_lane,self.the_one_who_will_be_removed)
        self.lane4.update(self.lane_data,self.current_lane,self.the_one_who_will_be_removed)
        self.lane5.update(self.lane_data,self.current_lane,self.the_one_who_will_be_removed)

        # self.screen.blit(pygame.transform.scale(self.evil_twin,(int(self.screen_width/2),self.screen_height)),(0,0))
        # self.screen.blit(pygame.transform.scale(self.mayor_twin,(int(self.screen_width/2),self.screen_height)),(int(self.screen_width/2),0))

        pygame.draw.rect(self.screen,"black",(0,620,1280,100))
        self.screen.blit(pygame.transform.scale(self.image,(screen_width,screen_height)),(0,0))



    def spawn_obstacles(self):
        current_obstacles = len(self.lane0)+len(self.lane1)+len(self.lane2)+len(self.lane3)+len(self.lane4)+len(self.lane5)
        # print(self.lane_occupant)
        if current_obstacles == 0:
            self.the_one_who_will_be_removed = None
            for count, x in enumerate(range(0,6)):
                # print(count)
                if len(self.lane_occupant[x]) ==0 and random.choice((True,False))==True:
                    test = Obstacle(x,x)
                    self.lane_occupant[x].add(test)
            if len(self.lane_occupant[1]) == 1 and len(self.lane_occupant[2]) == 1 and len(self.lane_occupant[3]) == 1 and len(self.lane_occupant[4]) == 1:
                self.the_one_who_will_be_removed = random.choice((1,2,3,4))
                # print("remove one",self.the_one_who_will_be_removed) 
        

                



pygame.mixer.pre_init()
pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("pyweek33 - Menace of the Streets")
clock= pygame.time.Clock()
done = False
bob=pygame.mixer.music.load("./assets/music/menace of the streets.mp3")
bob=pygame.mixer.music.load("./assets/music/before the disaster.mp3")
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(1)

my_game = Game(4,screen)
while not done:
    my_game.update_lane()
    my_game.spawn_obstacles()
    my_game.run()
    clock.tick(60)
    pygame.display.update()