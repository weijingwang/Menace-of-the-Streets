import pygame
import random

WIDTH = 900
HEIGHT = 700
ROWS = 20
COLUMNS = 20
TILE_SIZE = int(WIDTH / COLUMNS), int(HEIGHT / ROWS)
TILE_W, TILE_H = int(TILE_SIZE)
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

TURN = "TeamOne"

# some functions to translate grid <-> screen coordinates
def posToScreen(pos):
    column, row = pos
    return column * TILE_W, row * TILE_H

def screenToPos(pos):
    column, row = pos
    return column / TILE_W, row / TILE_H    

def draw_grid(screen):
    for i in range(1, int(HEIGHT), int(TILE_H)):
        pygame.draw.line(screen, GREEN, (1,i) ,(WIDTH,i), 2)

    for j in range(1, WIDTH, TILE_W):
        pygame.draw.line(screen, GREEN, (j,1) ,(j,HEIGHT), 2)

# a class that handles selecting units
class Cursor(pygame.sprite.Sprite):
    def __init__(self, units, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)

        # group of the units that can be controlled
        self.units = units

        # we create two images
        # to indicate if we are selecting or moving
        self.image = pygame.Surface(TILE_SIZE)
        self.image.set_colorkey((43,43,43))
        self.image.fill((43,43,43))
        self.rect = self.image.get_rect()
        self.selected_image = self.image.copy()
        pygame.draw.rect(self.image, pygame.Color('red'), self.image.get_rect(), 4)
        pygame.draw.rect(self.selected_image, pygame.Color('purple'), self.image.get_rect(), 4)
        self.base_image = self.image

        self.selected = None

    def update(self):
        # let's draw the rect on the grid, based on the mouse position
        pos = pygame.mouse.get_pos()
        self.rect.topleft = posToScreen(screenToPos(pos))

    def handle_click(self, pos):
        if not self.selected:
            # if we have not selected a unit, do it now
            for s in pygame.sprite.spritecollide(self, self.units, False):
                self.selected = s
                self.image = self.selected_image
        else:
            # if we have a unit selected, just set its target attribute, so it will move on its own
            self.selected.target = posToScreen(screenToPos(pos))
            self.image = self.base_image
            self.selected = None

class TeamOne(pygame.sprite.Sprite):
    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = pygame.Surface(TILE_SIZE)
        self.image.fill(GREEN)
        self.pos = random.randint(0, COLUMNS), random.randint(0, ROWS)
        self.rect = self.image.get_rect(topleft = posToScreen(self.pos))
        self.target = None

    def update(self):
        # do nothing until target is set
        # (maybe unset it if we reached our target)
        if self.target:
            if self.rect.x < self.target[0]:
                self.rect.move_ip(1, 0)
            elif self.rect.x > self.target[0]:
                self.rect.move_ip(-1, 0)
            elif self.rect.y < self.target[1]:
                self.rect.move_ip(0, 1)
            elif self.rect.y > self.target[1]:
                self.rect.move_ip(0, -1)
        self.pos = screenToPos(self.rect.topleft)

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A Game")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.LayeredUpdates()
    team_ones = pygame.sprite.Group()
    for i in range(5):
        TeamOne(all_sprites, team_ones)
    cursor = Cursor(team_ones, all_sprites)

    # a nice, simple, clean main loop
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # we could also pass all events to all sprites
            # so we would not need this special clause for the cursor...
            if event.type == pygame.MOUSEBUTTONDOWN:
                cursor.handle_click(event.pos)

        all_sprites.update()
        screen.fill(BLACK)
        draw_grid(screen)
        all_sprites.draw(screen)

        pygame.display.flip()

if __name__ == '__main__':
    main()