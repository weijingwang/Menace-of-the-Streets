import pygame
pygame.init()
screen_h = 720
screen_w = 1280
screen = pygame.display.set_mode((screen_w,screen_h))
clock= pygame.time.Clock()
done = False

class lane(pygame.sprite.Sprite):
    def __init__(self,display,x,y):
        super().__init__()
        self.display=display
        self.image = pygame.draw.polygon(self.display,(50,100,200),[[10,10],[720,20+x],[720,20+x]])
        # self.rect = self.image.get_rect()
        self.x=x
        self.y=y  

#lane group
mlane = lane(screen,20,30)
lane_group = pygame.sprite.Group()
lane_group.add(mlane)


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    screen.fill("black")
    lane_group.draw(screen)
    clock.tick(60)
    pygame.display.update()