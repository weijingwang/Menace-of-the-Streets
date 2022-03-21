from ast import AsyncFunctionDef
import pygame
import pygame.gfxdraw
import os
from random import randrange
class Obstacle(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.width = 300
        self.height = 300
        self.image = pygame.transform.scale(pygame.image.load("./assets/car_f.png"), (self.width, self.height))
        self.rect = self.image.get_rect()
        
    def update(self):
        if self.rect[0]>300:
            self.kill()
        # self.rect.right+=10
        # self.rect.bottom+=1
        self.width+=1
        self.height+=1
        print(self.image,self.rect,self.width,self.height)
        




class Game():
    def __init__(self,current_lane,screen):
        self.lane_array = [
            [0,1,(33,83,33)],
            [1,2,(66,66,66)],
            [2,3,(99,99,99)],
            [3,4,(132,132,132)],
            [4,5,(165,165,165)],
            [5,6,(198,248,198)]
        ]
        self.current_lane =current_lane
        self.screen_height = 720
        self.screen_width = 1280
        self.y0 = self.screen_height/3
        self.x0 = self.screen_width/2
        self.road_width=self.screen_width
        self.move_left = False
        self.move_right= False
        self.x = self.current_lane*-self.road_width
        self.next_x = self.current_lane*-self.road_width
        self.screen = screen

        self.test_obst = Obstacle()
        self.obstacle_group = pygame.sprite.Group()
        self.obstacle_group.add(self.test_obst)


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

        # print(self.current_lane,self.x,self.next_x)
    def run(self):
        # random_x = randrange(-3,3)
        # random_y = randrange(-3,3)
        for lane in self.lane_array:
            pygame.gfxdraw.filled_polygon(self.screen,[(self.x0,self.y0),[self.x+self.road_width*lane[0],self.screen_height],[self.x+self.road_width*lane[1],self.screen_height]],lane[2])
        self.screen.blit(pygame.transform.scale(fog,(screen_width,screen_height)),(0,0))
        pygame.draw.rect(self.screen,"black",(0,620,1280,100))
        self.screen.blit(pygame.transform.scale(POV_car,(screen_width,screen_height)),(0,0))
        self.obstacle_group.draw(self.screen)
        self.obstacle_group.update()




pygame.mixer.pre_init()
pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
clock= pygame.time.Clock()
 
POV_car = pygame.image.load("./assets/POV_car.png").convert_alpha()
fog = pygame.image.load("./assets/fog.png").convert_alpha()
done = False

pygame.mixer.music.load("./assets/i drivin and they hatin.mp3")
pygame.mixer.music.play(-1,0.0)

my_game = Game(4,screen)
while not done:
    my_game.update_lane()
    screen.fill("black")
    my_game.run()
    clock.tick(60)
    pygame.display.update()
