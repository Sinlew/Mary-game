import pygame, sys
from addons.settings import *
from map.level import Level


class Game:
    def __init__(self) -> None:
        
        # setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        
        pygame.display.set_caption("Pyzel")
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.level.hero_is_dead():
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.level.toggle_menu()
                
                    


            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()