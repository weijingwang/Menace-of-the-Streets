import pygame
import pygame.gfxdraw
import os
import random
class Text(pygame.sprite.Sprite):
    def __init__(self,screen,message,pos,size,bottom) -> None:
        super().__init__()
        self.screen = screen
        self.pos = pos
        self.size = size
        self.bottom = bottom
        self.original_size = self.size
        self.color=(200,200,200)
        self.myFont = pygame.font.Font("./assets/font/TanoheSans-Medium.ttf", self.size)
        self.message = message
        self.image = self.myFont.render(self.message, 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        
    def update(self,on):
        self.rect.center = self.pos
        if on==True:
            self.color = (130,115,250)
        elif on==False:
            self.color = (70,67,78)
        if self.bottom == True:
            self.color = (100,97,108)
        self.image = self.myFont.render(self.message, 1, self.color)

class realText(pygame.sprite.Sprite):
    def __init__(self,screen,pos,size) -> None:
        super().__init__()
        self.screen = screen
        self.pos = pos
        self.size = size
        self.original_size = self.size
        self.color=(200,200,200)
        self.myFont = pygame.font.Font("./assets/font/TanoheSans-Medium.ttf", self.size)
        self.image = self.myFont.render("_", 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        
    def update(self,message):
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        # if on==True:
        #     self.color = (130,115,250)
        # elif on==False:
        #     self.color = (70,67,78)
        # if self.bottom == True:
        #     self.color = (100,97,108)
        self.image = self.myFont.render(message, 1, self.color)

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
            self.image_link = ("./assets/empty.png")

        self.house_on = pygame.image.load("./assets/house_on.png").convert_alpha()

        self.image = pygame.image.load(self.image_link).convert_alpha()
        self.original_image = self.image
        self.image = pygame.transform.scale(self.original_image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = 1280/2,720/3

    def update(self,pos,scale,is_alive,turn_house_on):
        if is_alive==0:
            self.kill()
        if turn_house_on==1:
            self.original_image = self.house_on

        self.image = pygame.transform.scale(self.original_image, (int(scale), int(scale*self.height_multiplier)))
        self.rect = self.image.get_rect(midbottom = pos)

class Game():
    def __init__(self,current_lane,screen,game_type):
        self.game_type = game_type
        #IMAGES
        self.stars_bg = pygame.image.load("./assets/stars.png").convert_alpha()
        self.POV_car_L = pygame.image.load("./assets/POV_car_L.png").convert_alpha()
        self.POV_car_M = pygame.image.load("./assets/POV_car_M.png").convert_alpha()
        self.POV_car_R = pygame.image.load("./assets/POV_car_R.png").convert_alpha()
        self.fog = pygame.image.load("./assets/fog.png").convert_alpha()
        self.lose_image = pygame.image.load("./assets/death.png").convert_alpha()
        self.image = self.POV_car_M
        #MUSIC
        self.play_music = True
        #SOUND
        self.channel1 = pygame.mixer.Channel(1)
        self.channel2 = pygame.mixer.Channel(2)
        self.channel3 = pygame.mixer.Channel(3)
        self.channel1.set_volume(0.75)
        self.channel2.set_volume(0.25)
        self.channel3.set_volume(2)
        self.sound_car_rev = pygame.mixer.Sound("./assets/sound/car_rev.ogg")
        self.sound_car_rev_loops = 0
        self.sound_elaphant = pygame.mixer.Sound("./assets/sound/dog.ogg")
        self.crash_small = pygame.mixer.Sound("./assets/sound/crash_small.ogg")

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

        self.my_score = 0
        
        self.obst_pos = [[1280/2,720/3],[1280/2,720/3],[1280/2,720/3],[1280/2,720/3],[1280/2,720/3],[1280/2,720/3]]
        self.obst_scale = [0,0,0,0,0,0]
        self.obst_speed=[0.0001,0.0001,0.0001,0.0001,0.0001,0.0001]
        self.obst_accel=[0.005,0.005,0.005,0.005,0.005,0.005]
        self.obst_new_accel=[0.01,0.01,0.01,0.01,0.01,0.01]
        #=========================
        self.obst_delta_y_f = [0,0,0,0,0,0]
        self.obst_delta_x_f = [0,0,0,0,0,0]
        self.obst_delta_ratio = [0,0,0,0,0,0]
        self.obst_delta_y_now = [0,0,0,0,0,0]
        self.obst_delta_x_now = [0,0,0,0,0,0]
        self.obst_new_x = [0,0,0,0,0,0]

        self.obst_delta_x_fL = [0,0,0,0,0,0]
        self.obst_delta_x_fR = [0,0,0,0,0,0]
        self.obst_delta_ratioL = [0,0,0,0,0,0]
        self.obst_delta_ratioR = [0,0,0,0,0,0]
        self.obst_delta_x_nowL = [0,0,0,0,0,0]
        self.obst_delta_x_nowR = [0,0,0,0,0,0]
        self.obst_new_xL = [0,0,0,0,0,0]
        self.obst_new_xR = [0,0,0,0,0,0]
        self.obst_width = [0,0,0,0,0,0]

        self.obst_is_alive = [0,0,0,0,0,0]
        self.obst_house_on = [0,0,0,0,0,0]
        self.obst_can_turn_house_on = [1,1,1,1,1,1]

        self.obst_speed_og=0.0001
        self.obst_accel_og=0.005
        self.obst_new_accel_og=0.03

        #TEXT
        self.scoreFont = pygame.font.Font(None, 50)
        self.scoreText = self.scoreFont.render("score is: "+str(self.my_score), True,("white"))

        self.lose = False
        self.retry_ok = False
        self.lose_text1 = realText(self.screen,[1280/2,720/4],40)
        self.lose_text_group1 = pygame.sprite.Group()
        self.lose_text2 = realText(self.screen,[1280/2,720/2],40)
        self.lose_text_group2 = pygame.sprite.Group()
        self.lose_text3 = realText(self.screen,[1280/2,(720*3)/4],40)
        self.lose_text_group3 = pygame.sprite.Group()
        self.lose_text_group1.add(self.lose_text1)
        self.lose_text_group2.add(self.lose_text2)
        self.lose_text_group3.add(self.lose_text3)

        self.game_done = False
    def update_lane(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RETURN and self.game_type==1:
                    self.game_done=True
                if event.key == pygame.K_RIGHT and self.move_left == False and self.current_lane!=5:
                    self.image=self.POV_car_R
                    self.current_lane+=1
                    self.next_x = self.current_lane*-self.road_width
                    self.move_right = True
                elif event.key == pygame.K_LEFT and self.move_right == False and self.current_lane!=0:
                    self.image=self.POV_car_L
                    self.current_lane-=1
                    self.next_x = self.current_lane*-self.road_width
                    self.move_left = True
                if event.key == pygame.K_UP:
                    self.sound_car_rev_loops = -1
                    self.channel1.play(self.sound_car_rev,self.sound_car_rev_loops)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    self.image = self.POV_car_M
                elif event.key == pygame.K_UP:
                    self.channel1.fadeout(100)
                    # self.channel1.stop()
                    self.sound_car_rev_loops = 0

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
        # if self.current_lane==-1 or self.current_lane ==6:
        #     self.lose = False

        self.lane_data = [
            [self.x+self.road_width*self.lane_array[0][0],self.x+self.road_width*self.lane_array[0][1]],
            [self.x+self.road_width*self.lane_array[1][0],self.x+self.road_width*self.lane_array[1][1]],
            [self.x+self.road_width*self.lane_array[2][0],self.x+self.road_width*self.lane_array[2][1]],
            [self.x+self.road_width*self.lane_array[3][0],self.x+self.road_width*self.lane_array[3][1]],
            [self.x+self.road_width*self.lane_array[4][0],self.x+self.road_width*self.lane_array[4][1]],
            [self.x+self.road_width*self.lane_array[5][0],self.x+self.road_width*self.lane_array[5][1]]
        ]
    def draw(self):
        if self.play_music==True and self.game_type!=2:
            pygame.mixer.music.load("./assets/music/i drivin and they hatin.mp3")
            pygame.mixer.music.play(-1,0.0)
            pygame.mixer.music.set_volume(1)
            self.play_music=False
        self.screen.fill((20,24,82))
        self.screen.blit(pygame.transform.scale(self.stars_bg,(screen_width,screen_height)),(0,0))

        pygame.draw.rect(self.screen,(14,47,38),(0,240,1280,480))

        for lane in self.lane_array:
            pygame.gfxdraw.filled_polygon(self.screen,[(self.x0,self.y0),[self.x+self.road_width*lane[0],self.screen_height],[self.x+self.road_width*lane[1],self.screen_height]],lane[2])


        self.lane1.draw(self.screen)
        self.lane2.draw(self.screen)
        self.lane3.draw(self.screen)
        self.lane4.draw(self.screen)
        self.screen.blit(pygame.transform.scale(self.fog,(self.screen_width,self.screen_height)),(0,0))
        self.lane0.draw(self.screen)
        self.lane5.draw(self.screen)

        self.lane0.update(self.obst_pos[0],self.obst_scale[0],self.obst_is_alive[0],self.obst_house_on[0])
        self.lane1.update(self.obst_pos[1],self.obst_scale[1],self.obst_is_alive[1],self.obst_house_on[1])
        self.lane2.update(self.obst_pos[2],self.obst_scale[2],self.obst_is_alive[2],self.obst_house_on[2])
        self.lane3.update(self.obst_pos[3],self.obst_scale[3],self.obst_is_alive[3],self.obst_house_on[3])
        self.lane4.update(self.obst_pos[4],self.obst_scale[4],self.obst_is_alive[4],self.obst_house_on[4])
        self.lane5.update(self.obst_pos[5],self.obst_scale[5],self.obst_is_alive[5],self.obst_house_on[5])

        # self.screen.blit(pygame.transform.scale(self.evil_twin,(int(self.screen_width/2),self.screen_height)),(0,0))
        # self.screen.blit(pygame.transform.scale(self.mayor_twin,(int(self.screen_width/2),self.screen_height)),(int(self.screen_width/2),0))

        pygame.draw.rect(self.screen,"black",(0,620,1280,100))
        self.screen.blit(pygame.transform.scale(self.image,(screen_width,screen_height)),(0,0))
    def calculate_obstacle_pos(self):
        for x in range(0,6):
            keys = pygame.key.get_pressed()
            if self.obst_scale[x]>900:#kill sprite. RESET
                self.obst_pos[x] = [1280/2,720/3]
                self.obst_scale[x] = 0
                self.obst_speed[x]=self.obst_speed_og
                self.obst_accel[x]=self.obst_accel_og
                self.obst_new_accel[x]=self.obst_new_accel_og
                self.obst_is_alive[x]=0
                self.obst_can_turn_house_on[x]=1
                self.obst_house_on[x]=0
            if self.the_one_who_will_be_removed == x:#prevent 4 cars in a row on road by removing one random one
                self.obst_is_alive[x]=0
            if self.obst_is_alive[x]:
                if self.obst_scale[x]>800 and x == self.current_lane:
                    print("music stopped")
                    self.channel3.play(self.crash_small)
                    self.lose = True

            if keys[pygame.K_UP]:
                self.obst_speed[x] += self.obst_new_accel[x]*5
                self.obst_new_accel[x]+=0.001

            self.obst_delta_y_f[x] = 240-720
            self.obst_delta_x_f[x] = (1280/2)-(((self.lane_data[x][1]-self.lane_data[x][0])/2)+self.lane_data[x][0])
            self.obst_delta_ratio[x] = self.obst_delta_x_f[x]/self.obst_delta_y_f[x]
            self.obst_delta_y_now[x] = 240-self.obst_pos[x][1]
            self.obst_delta_x_now[x] = self.obst_delta_y_now[x]*self.obst_delta_ratio[x]
            self.obst_new_x[x] = (1280/2)-self.obst_delta_x_now[x]
            #MOVE CAR HERE
            self.obst_pos[x][1]+=self.obst_speed[x]#==============================================================================
            self.obst_speed[x]+=self.obst_accel[x]
            self.obst_pos[x][0]=self.obst_new_x[x]#======================================================================================

            self.obst_delta_x_fL[x] = (1280/2)-self.lane_data[x][0]
            self.obst_delta_x_fR[x] = (1280/2)-self.lane_data[x][1]
            self.obst_delta_ratioL[x] = self.obst_delta_x_fL[x]/self.obst_delta_y_f[x]
            self.obst_delta_ratioR[x] = self.obst_delta_x_fR[x]/self.obst_delta_y_f[x]
            self.obst_delta_x_nowL[x] = self.obst_delta_y_now[x]*self.obst_delta_ratioL[x]
            self.obst_delta_x_nowR[x] = self.obst_delta_y_now[x]*self.obst_delta_ratioR[x]
            self.obst_new_xL[x] = (1280/2)-self.obst_delta_x_nowL[x]
            self.obst_new_xR[x] = (1280/2)-self.obst_delta_x_nowR[x]
            self.obst_width[x] = abs(self.obst_new_xL[x]-self.obst_new_xR[x])
            self.obst_scale[x] =self.obst_width[x]#======================================================================================
            # print(self.obst_is_alive)
            # self.image = pygame.transform.scale(original_image, (scale, int(scale*height_multiplier)))
            # self.rect = self.image.get_rect(midbottom = pos)
            if self.obst_is_alive[x]:
                if x == 0 or x ==5:
                    if self.obst_scale[x]<900 and self.obst_scale[x] >100:# and can_turn_house_on == True:
                        # print("do it now")
                        if (x == 0 and self.current_lane ==1) or (x == 5 and self.current_lane ==4):
                            if keys[pygame.K_UP]:
                                # print("yes")
                                if self.obst_can_turn_house_on[x]==1:
                                    self.obst_house_on[x]=1
                                    self.obst_can_turn_house_on[x]=0
                                    self.channel2.play(self.sound_elaphant)
                                    # self.channel2.fadeout(0)
                                    self.my_score+=1
    def spawn_obstacles(self):
        # print(self.obst_scale)
        current_obstacles = len(self.lane0)+len(self.lane1)+len(self.lane2)+len(self.lane3)+len(self.lane4)+len(self.lane5)
        self.calculate_obstacle_pos()
        self.obst_accel_og+=0.00001
        if self.game_type == 1:
            if current_obstacles == 0:
                self.the_one_who_will_be_removed = None
                for x in range(0,6):

                    if len(self.lane_occupant[x]) ==0 and random.choice((True,False))==True:
                        if x == 0 or x==5 or x==1:
                        # print(self.obst_pos[x])
                            test = Obstacle(x,x)
                            self.obst_is_alive[x]=1
                            self.lane_occupant[x].add(test)

        else:
            if current_obstacles == 0:
                self.the_one_who_will_be_removed = None
                for x in range(0,6):

                    if len(self.lane_occupant[x]) ==0 and random.choice((True,False))==True:
                        # print(self.obst_pos[x])
                        test = Obstacle(x,x)
                        self.obst_is_alive[x]=1
                        self.lane_occupant[x].add(test)
                        
                if len(self.lane_occupant[1]) == 1 and len(self.lane_occupant[2]) == 1 and len(self.lane_occupant[3]) == 1 and len(self.lane_occupant[4]) == 1:
                    self.the_one_who_will_be_removed = random.choice((1,2,3,4))

     
    def draw_score(self):
        if self.game_type==1:#TUTORIAL
            self.scoreText = self.scoreFont.render('Mind simulation (tutorial)', True,("white"))
            self.tutorial_text1 = self.scoreFont.render('press UP to to speed up and disturb homes if you are in the adjacent lane ', True,("white"))
            self.tutorial_text2 = self.scoreFont.render('press LEFT or RIGHT ONCE to change ONE lane', True,("white"))
            self.tutorial_text3 = self.scoreFont.render('if you CRASH you DIE', True,("white"))
            self.tutorial_text4 = self.scoreFont.render('press ENTER to start game', True,("white"))
            self.screen.blit(self.scoreText,(800,50))
            self.screen.blit(self.tutorial_text1,(50,500))
            self.screen.blit(self.tutorial_text2,(250,550))
            self.screen.blit(self.tutorial_text3,(450,600))
            self.screen.blit(self.tutorial_text4,(400,650))
        elif self.game_type==2:#GAME
            self.scoreText = self.scoreFont.render(str(self.my_score)+"/5"+" homes disturbed", True,("white"))
            self.screen.blit(self.scoreText,(900,50))
        elif self.game_type==0:#CHALLENGE
            self.scoreText = self.scoreFont.render(str(self.my_score)+" homes disturbed", True,("white"))
            self.screen.blit(self.scoreText,(900,50))


    def go_to_ending(self):
        if self.game_type == 2 and self.my_score >= 5:
            self.channel1.stop()
            self.channel2.stop()
            self.channel3.stop()
            pygame.mixer.music.stop()
            return(True)
    def tutorial_to_game(self):
        return(self.game_done)

    def show_lose(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.retry_ok = True
            if event.type == pygame.KEYUP and self.retry_ok==True and event.key == pygame.K_SPACE:
                self.my_score = 0
                self.obst_pos = [[1280/2,720/3],[1280/2,720/3],[1280/2,720/3],[1280/2,720/3],[1280/2,720/3],[1280/2,720/3]]
                self.obst_scale = [0,0,0,0,0,0]
                self.obst_speed=[0.0001,0.0001,0.0001,0.0001,0.0001,0.0001]
                self.obst_accel=[0.005,0.005,0.005,0.005,0.005,0.005]
                self.obst_new_accel=[0.01,0.01,0.01,0.01,0.01,0.01]
                self.obst_is_alive = [0,0,0,0,0,0]
                self.obst_house_on = [0,0,0,0,0,0]
                self.obst_can_turn_house_on = [1,1,1,1,1,1]
                self.play_music = True
                self.lose = False
                self.retry_ok = False
        # print(self.retry_ok)
                    
        # pygame.mixer.music.stop()
        self.channel1.fadeout(100)
        self.screen.blit(self.lose_image,(0,0))
        self.lose_text_group1.update("HOBBY is when you buy a NEW car")
        self.lose_text_group1.draw(self.screen)
        self.lose_text_group2.update("PASSION is when you keep the old one RUNNING")
        self.lose_text_group2.draw(self.screen)
        self.lose_text_group3.update("Press Space to retry...")
        self.lose_text_group3.draw(self.screen)
        
    def run(self):
        if self.lose == True:
            self.show_lose()
        else:
            self.update_lane()
            self.spawn_obstacles()
            self.draw()
            self.draw_score()

class GameTitle():
    def __init__(self,screen):
        self.screen = screen
        self.image = pygame.image.load("./assets/title.png").convert_alpha()
        self.title_fog = pygame.image.load("./assets/title_fog.png").convert_alpha()
        self.title_fog = pygame.transform.scale(self.title_fog, (1280, 720))
        # pygame.mixer.music.load("./assets/music/before the disaster.mp3")
        # pygame.mixer.music.play(-1,0.0)
        # pygame.mixer.music.set_volume(1)
        self.title_text = Text(self.screen,"Menace of the Street",(1280/2,720-720/5-720/20),100,False)
        self.text_group = pygame.sprite.Group()
        self.text_group.add(self.title_text)

        self.text_story = Text(self.screen,"Story",(1280/4,720-720/15-720/30),50,False)
        self.text_challenge = Text(self.screen,"Challenge",(1280/2,720-720/15-720/30),50,False)
        self.text_about = Text(self.screen,"About",(1280/4+1280/2,720-720/15-720/30),50,False)
        self.group0 = pygame.sprite.Group()
        self.group1 = pygame.sprite.Group()
        self.group2 = pygame.sprite.Group()
        self.group0.add(self.text_story)
        self.group1.add(self.text_challenge)
        self.group2.add(self.text_about)

        self.select = 0
        self.light_0 = True
        self.light_1 = False
        self.light_2 = False

        self.move_text_pos=[1280/2,10]
        self.instructions = Text(self.screen,"Press Left or Right to select. Press Space to continue.",self.move_text_pos,20,True)
        self.moving_text_group = pygame.sprite.Group()
        self.moving_text_group.add(self.instructions)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.select +=1
                elif event.key == pygame.K_LEFT:
                    self.select -=1
                if event.key ==pygame.K_SPACE:
                    if self.select==0:
                        return(0)

                    elif self.select==1:
                        return(1)
                    elif self.select==2:
                        return(2)
        if self.select >= 2:
            self.select=2
        if self.select <= 0:
            self.select=0
        if self.select == 0:
            self.light_0 = True
        else:
            self.light_0=False
        if self.select == 1:
            self.light_1 = True
        else:
            self.light_1=False
        if self.select == 2:
            self.light_2 = True
        else:
            self.light_2=False
        # print(self.select,self.light_0,self.light_1,self.light_2)    
        self.screen.blit(self.image,(0,0))
        self.text_group.draw(self.screen)
        self.group0.draw(self.screen)
        self.group1.draw(self.screen)
        self.group2.draw(self.screen)
        self.group0.update(self.light_0)
        self.group1.update(self.light_1)
        self.group2.update(self.light_2)

        self.moving_text_group.draw(self.screen)
        self.moving_text_group.update(False)
        self.screen.blit(self.title_fog,(0,0))

class Story():
    def __init__(self,screen):
        self.screen = screen
        self.music = "./assets/music/before the disaster.mp3"
        self.music_played=True
        self.music_can_switch =True
        self.play_music = True


        self.sound_car_rev = pygame.mixer.Sound("./assets/sound/car_rev.ogg")



        self.clock = pygame.time.Clock()
        self.count = 0
        self.empty = pygame.image.load("./assets/empty.png").convert_alpha()
        self.evil_twin = pygame.image.load("./assets/evil_twin.png").convert_alpha()
        self.mayor_twin = pygame.image.load("./assets/mayor_twin.png").convert_alpha()
        self.lamps = pygame.image.load("./assets/lamps.png").convert_alpha()
        self.mayor_twin =pygame.transform.scale(self.mayor_twin, (int(720*0.5625), 720))
        # self.evil_twin =pygame.transform.scale(self.evil_twin, (int(720*0.5625), 720))

        self.lamps = pygame.transform.scale(self.lamps, (int(720*0.5625), 720))


        self.intro_town0 = pygame.image.load("./assets/intro_town0.png").convert_alpha()
        self.intro_town0 = pygame.transform.scale(self.intro_town0, (1280, 720))
        self.intro_town = pygame.image.load("./assets/intro_town.png").convert_alpha()
        self.intro_town = pygame.transform.scale(self.intro_town, (3840, 720))
        self.intro_town_all = [self.intro_town0,self.intro_town0]
        self.intro_town_pos = [[-1280,0],[0,0],[-3840,0]]
        self.fibbari_car_pos = [800,340]
        self.fibbari_car = pygame.image.load("./assets/fibbari_car.png").convert_alpha()
        self.intro_town_stop = False
        self.intro_town_done = False
        self.fib_accel = 2


        self.text_bg = pygame.image.load("./assets/text_bg.png").convert_alpha()
        self.text_bg = pygame.transform.scale(self.text_bg, (1280, int(720/4)))
        self.speaker_text= realText(self.screen,[1280/2,600],40)
        self.message_text= realText(self.screen,[1280/2,670],25)
        self.text_speaker_group = pygame.sprite.Group()
        self.message_group = pygame.sprite.Group()
        self.text_speaker_group.add(self.speaker_text)
        self.message_group.add(self.message_text)
        self.current_text = [
            ["","Press Space to continue"],
            ["","It was just like any other peaceful and quiet night in Mr. Mayor's city..."],
            [" ","and the dear subjects who are true and loyal are about sleep. But not before Mr. Mayor finishes talking!"],
            ["Mr. Mayor","Dear my true and loyal subjects if you will."],
            ["Mr. Mayor","You may spam space to skip me, but please. I implore you to lend me an ear..."],#INDEX 4

            ["Mr. Mayor","As many of you should know, today is my birthday..."],
            ["loyal subjects","mr. mayor, that is so great. happy birthday mr mayor. we appreciate you"],
            ["Mr. Mayor","...Thank you thank you. Now let us end this evening with a toast..."],

            ["Mr. Mayor",'There once was a mother who has asked her son: "Anton, am I a bad mother?"'],
            ["Mr. Mayor",'The son replied, "Dear mother, my name is Paul..."'],
            ["Mr. Mayor","My name is Mr. Mayor"],
            ["loyal subjects","We love you Mr. Mayor"],
            ["loyal subjects","You are such a good mayor. And a good person"],
            ["Mr. Mayor","Why thank you my dear and loyalest citizens of my city. I would like to wish you all a good night"],
            [" ","meanwhile on the ouskirts of Mr. Mayor's city..."],#index 11+3 =14
            ["TWIN MAYOR","mr mayor, you will not be having a good night sleep this night..."],#INDEX 12+3 = 15
            ["TWIN MAYOR","99% of the PEOPLE in this world live by SOCIETY's rules, obligations and socially ACCEPTED behavior"],
            ["TWIN MAYOR", "1% do NOT. they are OUTLAWS. ####### THE world"],
            [" "," "],#INDEX 15+3
            ['','']#INDEX 16+3
        ]
        self.check_keydown = False

        self.subject1 = self.empty
        self.subject2 = self.empty
        self.subject1_pos = [0,0]
        self.subject2_pos = [0,0]

        self.alphaSurface = pygame.Surface((1280,720))
        self.alphaSurface.set_alpha(0)
        self.alph_count = 0

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # self.intro_town_stop = True
                self.check_keydown = True

            if event.type == pygame.KEYUP and self.check_keydown == True and self.count<18 and event.key == pygame.K_SPACE:
                self.count+=1
                self.check_keydown=False
            # print(str(self.count)+" is the storty count")
    def see_city(self):
        if self.count >= 1 and self.count<14:
            for x in range(0,2):
                self.intro_town_pos[x][0]+=10
                if self.intro_town_pos[x][0]>=1280:
                    self.intro_town_pos[x][0]=1280
            if self.intro_town_pos[2][0]<=0:
                self.intro_town_pos[2][0]+=10#-self.intro_town_accel

        else:
            for x in range(0,2):
                self.intro_town_pos[x][0]+=10
                if self.intro_town_pos[x][0]>=1280 and x==0:
                        self.intro_town_pos[x][0]=-1280
                elif self.intro_town_pos[x][0]>=1280 and x==1:
                        self.intro_town_pos[x][0]=-1280

    def update(self):
        if self.count ==0:
            print(self.count)

        elif self.count >=1 and self.count <14:
            self.subject1 = self.mayor_twin
            self.subject2 = self.lamps
            self.subject1_pos[0]=self.intro_town_pos[2][0]+100  
            self.subject2_pos[0]=self.intro_town_pos[2][0]+700
        elif self.count ==14:


            self.subject1 = self.empty
            self.subject2 = self.fibbari_car
            self.subject1_pos[0]=0  
            self.subject2_pos=self.fibbari_car_pos
            self.intro_town = self.empty
            # pygame.mixer.music.stop()
            # pygame.mixer.music.unload()
            # self.music_played=False
            if self.music_can_switch == True:
                self.music="./assets/music/menace of the streets.mp3"
                pygame.mixer.music.load(self.music)
                pygame.mixer.music.play(-1,0.0)
                pygame.mixer.music.set_volume(0.75)
                self.music_played=False
        elif self.count ==15:
            self.subject1 = self.evil_twin
            self.subject1_pos[0]=0  
        elif self.count ==18:
            # pygame.mixer.Sound.play(self.sound_car_rev)
            pygame.mixer.music.fadeout(3000)
            self.subject1 = self.empty
            self.subject2_pos[0]-=5-self.fib_accel
            self.fib_accel-=0.1
            self.alphaSurface.blit(pygame.transform.scale(self.text_bg,(1280,720)),(0,0))
            self.alph_count+=1
            self.alphaSurface.set_alpha(self.alph_count)

    def run(self):
        if self.play_music==True:
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1,0.0)
            pygame.mixer.music.set_volume(0.75)
            self.play_music = False
        self.update()
        self.get_input()
        self.see_city()
        # self.begin()
        self.screen.blit(self.intro_town_all[0],self.intro_town_pos[0])
        self.screen.blit(self.intro_town_all[1],self.intro_town_pos[1])
        self.screen.blit(self.intro_town,self.intro_town_pos[2])
        # self.screen.blit(self.fibbari_car,self.fibbari_car_pos)
        # self.screen.blit(self.begin_town,[self.begin_town_pos,0])


        self.screen.blit(self.subject1,self.subject1_pos)
        self.screen.blit(self.subject2,self.subject2_pos)

        self.screen.blit(self.text_bg,(0,720-720/4))
        self.text_speaker_group.update(self.current_text[self.count][0])
        self.message_group.update(self.current_text[self.count][1])
        self.text_speaker_group.draw(self.screen)
        self.message_group.draw(self.screen)
        self.screen.blit(self.alphaSurface,(0,0))
        # self.screen.blit(self.evil_twin,(0,0))
        # self.clock.tick(60)
    def intro_finished(self):
        if self.alph_count>=300:
            return(True)

class Ending():
    def __init__(self,screen):
        self.screen = screen
        self.music = "./assets/music/menace of the streets.mp3"
        self.music_played=True
        self.music_can_switch =True
        self.play_music = True

        self.sound_crash_big = pygame.mixer.Sound("./assets/sound/crash_big.ogg")

        self.count = 0
        self.empty = pygame.image.load("./assets/empty.png").convert_alpha()
        self.evil_twin = pygame.image.load("./assets/evil_twin.png").convert_alpha()
        self.mayor_twin = pygame.image.load("./assets/mayor_twin.png").convert_alpha()
        self.mayor_twin =pygame.transform.scale(self.mayor_twin, (int(720*0.5625), 720))
        self.evil_twin =pygame.transform.scale(self.evil_twin, (int(720*0.5625), 720))

        self.scene1 = pygame.image.load("./assets/e_scene1.png").convert_alpha()

        self.intro_town0 = pygame.image.load("./assets/end_town0.png").convert_alpha()
        self.intro_town0 = pygame.transform.scale(self.intro_town0, (1280, 720))
        self.intro_town = pygame.image.load("./assets/end_town.png").convert_alpha()
        self.intro_town = pygame.transform.scale(self.intro_town, (3840, 720))
        self.intro_town_all = [self.intro_town0,self.intro_town0]
        self.intro_town_pos = [[-1280,0],[0,0],[-3840,0]]
        self.fibbari_car_pos = [800,340]
        self.fibbari_car = pygame.image.load("./assets/fibbari_car.png").convert_alpha()
        self.intro_town_stop = False
        self.intro_town_done = False
        self.fib_accel = 2


        self.text_bg = pygame.image.load("./assets/text_bg.png").convert_alpha()
        self.text_bg = pygame.transform.scale(self.text_bg, (1280, int(720/4)))
        self.speaker_text= realText(self.screen,[1280/2,600],40)
        self.message_text= realText(self.screen,[1280/2,670],25)
        self.text_speaker_group = pygame.sprite.Group()
        self.message_group = pygame.sprite.Group()
        self.text_speaker_group.add(self.speaker_text)
        self.message_group.add(self.message_text)
        self.current_text = [
            ["TWIN MAYOR","I do believe that I have sufficiently exercised my rights of driving ..."],
            ["TWIN MAYOR","its time for me to go"],#INDEX 1
            ["TWIN MAYOR","oops"],#INDEX 2
            ['',''],#index 3
            ['Mr. Mayor','My dear home! Today is my birthday!'],
            ["TWIN MAYOR","I never say sorry"],
            ["Mr. Mayor","you must pay for this young man! You may not leave"],
            ["TWIN MAYOR","Hi Mr. Mayor. I am your twin. I am TWIN MAYOR"],#7
            ["Mr. Mayor","TWIN MAYOR, I will have you pay for the damages you have caused on this night."],
            ["TWIN MAYOR","sorry man I'm broke"]#9
        ]

        self.check_keydown = False

        self.subject1 = self.empty
        self.subject2 = self.empty
        self.subject1_pos = [0,0]
        self.subject2_pos = [0,0]

        self.alphaSurface = pygame.Surface((1280,720))
        self.alphaSurface.set_alpha(0)
        self.alph_count = 0

        self.can_crash = True
        self.can_go_next = True

    def get_input(self):
        print(self.count)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.can_go_next==True:
                # self.intro_town_stop = True
                self.check_keydown = True

            if event.type == pygame.KEYUP and self.check_keydown == True and self.count<9 and event.key == pygame.K_SPACE and self.can_go_next==True:
                self.count+=1
                self.check_keydown=False
            # print(str(self.count)+" is the storty count")
    def see_city(self):
        if self.count == 3:
            for x in range(0,2):
                self.intro_town_pos[x][0]+=30
                if self.intro_town_pos[x][0]>=1280:
                    self.intro_town_pos[x][0]=1280
            if self.intro_town_pos[2][0]<=350:
                self.intro_town_pos[2][0]+=30#-self.intro_town_accel
            if self.fibbari_car_pos[0]>=550:
                self.fibbari_car_pos[0]-=3

        else:
            for x in range(0,2):
                self.intro_town_pos[x][0]+=10
                if self.intro_town_pos[x][0]>=1280 and x==0:
                        self.intro_town_pos[x][0]=-1280
                elif self.intro_town_pos[x][0]>=1280 and x==1:
                        self.intro_town_pos[x][0]=-1280

    def update(self):
        if self.count ==0:
            self.subject1 = self.evil_twin
            self.subject2 = self.fibbari_car
            self.subject1_pos[0]=100
            self.subject2_pos=self.fibbari_car_pos
        elif self.count ==3:
            self.subject1=self.empty
            if self.intro_town_pos[2][0]>=350 and self.fibbari_car_pos[0]<=550:
                if self.can_crash==True:
                    self.can_go_next=True
                    pygame.mixer.Sound.play(self.sound_crash_big)
                    print("play sound")
                    self.intro_town_pos[2][0]=1280
                    self.fibbari_car_pos[0]=-500
                    self.can_crash=False
            else:
                self.can_go_next=False
        elif self.count ==4:
            self.subject1 = self.mayor_twin
            self.subject2 = self.evil_twin
            self.subject2_pos=[750,0]
        # print(self.intro_town_pos[2][0])
            # pygame.mixer.music.fadeout(3000)
            # self.subject1 = self.empty
            # self.subject2_pos[0]-=5-self.fib_accel
            # self.fib_accel-=0.1
            # self.alphaSurface.blit(pygame.transform.scale(self.text_bg,(1280,720)),(0,0))
            # self.alph_count+=1
            # self.alphaSurface.set_alpha(self.alph_count)

    def run(self):
        if self.play_music==True:
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1,0.0)
            pygame.mixer.music.set_volume(0.75)
            self.play_music = False
        self.update()
        self.get_input()
        self.see_city()
        # self.begin()
        self.screen.blit(self.intro_town_all[0],self.intro_town_pos[0])
        self.screen.blit(self.intro_town_all[1],self.intro_town_pos[1])
        if self.can_crash==False:
            self.screen.blit(self.scene1,(0,0))
        self.screen.blit(self.intro_town,self.intro_town_pos[2])
        # self.screen.blit(self.fibbari_car,self.fibbari_car_pos)
        # self.screen.blit(self.begin_town,[self.begin_town_pos,0])


        self.screen.blit(self.subject1,self.subject1_pos)
        self.screen.blit(self.subject2,self.subject2_pos)

        self.screen.blit(self.text_bg,(0,720-720/4))
        self.text_speaker_group.update(self.current_text[self.count][0])
        self.message_group.update(self.current_text[self.count][1])
        self.text_speaker_group.draw(self.screen)
        self.message_group.draw(self.screen)
        self.screen.blit(self.alphaSurface,(0,0))
        # self.screen.blit(self.evil_twin,(0,0))
        # self.clock.tick(60)
    def intro_finished(self):
        if self.alph_count>=300:
            return(True)

pygame.mixer.pre_init()
pygame.init()
screen_width = 1280
screen_height = 720
pygame.mixer.music.load("./assets/music/menace of the streets.mp3")
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(1)

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("pyweek33--Menace of the Streets")
fibbari_car = pygame.image.load("./assets/fibbari_car.png").convert_alpha()
fibbari_car = pygame.transform.scale(fibbari_car, (1280, 720))
stars = pygame.image.load("./assets/stars.png").convert_alpha()
stars = pygame.transform.scale(stars, (1280, 720))
about = pygame.image.load("./assets/about.png").convert_alpha()
lose_image = pygame.image.load("./assets/death.png").convert_alpha()
#SOUND
crash_small = pygame.mixer.Sound("./assets/sound/crash_small.ogg")

clock= pygame.time.Clock()
title_done = False
about_done = True
challenge_done = True

intro_done = True
tutorial_done = True
game_done = True
end_done = True

my_title = GameTitle(screen)
intro = Story(screen)
challenge = Game(4,screen,0)
tutorial = Game(4,screen,1)
game = Game(4,screen,2)
end = Ending(screen)

done_0 = False
while not done_0:
    while not title_done:
        check_event = my_title.run()
        if check_event ==0:
            intro_done = False
            title_done = True
            done_0 = True
        elif check_event ==1:
            challenge_done = False
            title_done = True
            done_0 = True
        elif check_event ==2:
            about_done = False
            title_done = True
        clock.tick(60)
        pygame.display.update()
    while not about_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                about_done = True
                title_done = False
        screen.fill("black")
        screen.blit(fibbari_car,(0,0))
        screen.blit(stars,(0,0))
        screen.blit(about,(0,0))
        clock.tick(60)
        pygame.display.update()

while not challenge_done:
    challenge.run()
    clock.tick(60)
    pygame.display.update()

while not intro_done:
    intro.run()
    if intro.intro_finished() == True:
        tutorial_done=False
        intro_done = True
    clock.tick(60)
    pygame.display.update()

while not tutorial_done:
    if tutorial.tutorial_to_game()==True:
        game_done=False
        tutorial_done=True
    tutorial.run()
    clock.tick(60)
    pygame.display.update()

while not game_done:
    if game.go_to_ending()==True:
        end_done=False
        game_done=True
    game.run()
    clock.tick(60)
    pygame.display.update()

while not end_done:
    end.run()
    if end.intro_finished() == True:
        end = True
    clock.tick(60)
    pygame.display.update()

        


