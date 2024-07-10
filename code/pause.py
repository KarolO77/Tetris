from settings import *
from timer import Timer
from button import Button

from os.path import join

class Pause:
    def __init__(self, surface):

        # general
        self.paused = True
        self.ended = False
        self.restart = False

        self.display_surface = surface
        self.pause_rect = self.display_surface.get_rect(topleft = (0,0))

        # font
        self.font = pygame.font.Font(join('..','fonts','nocontinue.ttf'), 50)

        # buttons
        self.restart_game_image = pygame.image.load(join('..','visuals', 'RESTART_BUTTON.jpg'))
        self.restart_game_image = pygame.transform.scale(self.restart_game_image, (96,96))
        self.restart_game_button = Button((WINDOW_WIDTH/2-self.restart_game_image.get_width()-30, WINDOW_HEIGHT/2), self.restart_game_image)

        self.resume_game_image = pygame.image.load(join('..','visuals', 'RESUME_BUTTON.jpg'))
        self.resume_game_button = Button((WINDOW_WIDTH/2+30, WINDOW_HEIGHT/2), self.resume_game_image)

        # timer
        self.mouse_timer = Timer(MOUSE_WAIT_TIME)

    def update_mouse(self):
        self.mouse_pos = pygame.mouse.get_pos()

    def timer_update(self):
        self.mouse_timer.update()

    def display_text(self, score):
        text_surface = self.font.render(f"SCORE: {score}", True, 'white')
        text_rect = text_surface.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2-70))
        self.display_surface.blit(text_surface, text_rect)

    def display_elements(self, ended):
        pygame.draw.rect(self.display_surface, PAUSE_BOARD_COLOR, self.pause_rect,50)
        pygame.draw.circle(self.display_surface, PAUSE_BOARD_COLOR, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2), WINDOW_WIDTH/5)
        
        # buttons
        if not ended:
            self.display_surface.blit(self.resume_game_button.image, self.resume_game_button.pos)
            self.restart_game_button.pos = (WINDOW_WIDTH/2-self.restart_game_image.get_width()-30, self.restart_game_button.pos[1])
            self.restart_game_button.rect = self.restart_game_image.get_rect(center = self.restart_game_button.pos)
            self.display_surface.blit(self.restart_game_button.image, self.restart_game_button.pos)
        else:
            self.restart_game_button.pos = (WINDOW_WIDTH/2-self.restart_game_image.get_width()/2, self.restart_game_button.pos[1])
            self.restart_game_button.rect = self.restart_game_image.get_rect(center = self.restart_game_button.pos)
            self.display_surface.blit(self.restart_game_button.image, self.restart_game_button.pos)

    def check_buttons(self, ended):

        if not self.mouse_timer.active:
            if self.restart_game_button.clicked(self.mouse_pos):
                self.restart = True
                self.mouse_timer.activate()

            if self.resume_game_button.clicked(self.mouse_pos) and not ended:
                self.paused = False
                self.mouse_timer.activate()

    def run(self, score, ended):
        # update
        self.update_mouse()
        self.timer_update()

        # rest
        self.display_elements(ended)
        self.check_buttons(ended)
        self.display_text(score)