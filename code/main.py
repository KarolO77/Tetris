from settings import *
from sys import exit

# components
from start import Start
from game import Game
from score import Score
from preview import Preview
from pause import Pause

from random import choice

class Main:
    def __init__(self):

        # general
        pygame.init()
        pygame.display.set_caption("Tetris")
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.started = False

        # shapes
        self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]

        # components
        self.start = Start(self.update_settings)
        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()
        self.pause = Pause(self.display_surface)

    def update_settings(self, settings):
        self.game.player_settings = settings

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(TETROMINOS.keys())))
        return next_shape

    def display_pause(self, score, ended):
        self.pause.run(score, ended)

        if self.pause.paused == False:
            self.game.paused = False
            self.pause.paused = True

        if self.pause.restart == True:
            self.game.restart()

            self.game.paused = False
            self.pause.restart = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            if not self.started:

                # display
                self.display_surface.fill(GRAY)

                # components
                self.start.run()
                self.started = self.start.started

            if self.started:

                # display
                self.display_surface.fill(BLACK)
                
                # components
                self.game.run()
                self.score.run()
                self.preview.run(self.next_shapes)

                # will display pause screen only if game is paused
                if self.game.paused: self.display_pause(self.game.current_score, self.game.ended)

            #updating the game
            pygame.display.update()
            self.clock.tick(120)

if __name__ == "__main__":
    main = Main()
    main.run()