from settings import *
from timer import Timer
from button import Button

from os import path
import string

class Start:
	def __init__(self, update_settings):

		# general
		self.surface = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.display_surface = pygame.display.get_surface()

		self.stopped = False
		self.started = False
		self.in_settings = False

		self.update_settings = update_settings

		# font
		self.font = pygame.font.Font(path.join('..','fonts','nocontinue.ttf'), 35)

		# settings
		self.assign_keys = [f'K_{i}' for i in 
							list(string.ascii_lowercase)+
							[str(i) for i in range(10)]+
							"MINUS,SPACE,PERIOD,SLASH,COMMA,SEMICOLON,EQUALS,LEFTBRACKET,RIGHTBRACKET,QUOTE".split(',')]
		self.factory_settings = {
			'Left' : 'K_LEFT',
			'Right' : 'K_RIGHT',
			'Down' : 'K_DOWN',
			'Rotate' : 'K_UP',
			'Pause' : 'K_ESCAPE'
		}

		# visuals
		self.button_image = pygame.image.load(path.join('..','visuals','CUSTOM_BUTTON.jpg'))
		self.b_height = self.button_image.get_height()
		self.b_width = self.button_image.get_width()

		self.interspace = (WINDOW_WIDTH - 4*self.b_width) / 3

		self.logo = pygame.image.load(path.join('..','visuals', 'Logo.jpg'))
		self.logo_pos = self.logo.get_rect(topleft = (WINDOW_WIDTH/4,WINDOW_HEIGHT/4))

		self.keyboard = pygame.image.load(path.join('..','visuals', 'KEYBOARD.jpg'))
		self.keyboard = pygame.transform.scale(self.keyboard, (self.keyboard.get_width()*0.85, self.keyboard.get_height()*0.85))
		self.keyboard_pos = self.keyboard.get_rect(topleft = (6.5*self.interspace,150+self.b_height))

		# buttons
		self.buttons = {
			'start' : Button((WINDOW_WIDTH/4, WINDOW_HEIGHT/2), self.button_image, "START"),
			'go_back' : Button((PADDING,PADDING), pygame.image.load(path.join('..','visuals', 'GO_BACK_BUTTON.jpg'))),
			'go_settings' : Button((WINDOW_WIDTH/4+self.b_width*1.5, WINDOW_HEIGHT/2), self.button_image, "SETTINGS"),
			'save' : Button((WINDOW_WIDTH/2-self.b_width/2, WINDOW_HEIGHT - 3*self.b_height), self.button_image, "SAVE"),
			'settings' : {
				'left' : Button((self.interspace+self.b_width, 150), self.button_image, 'Left'),
				'right' : Button((self.interspace+self.b_width, 150+self.b_height), self.button_image, 'Right'),
				'down' : Button((self.interspace+self.b_width, 150+2*self.b_height), self.button_image, 'Down'),
				'rotate' : Button((self.interspace+self.b_width, 150+3*self.b_height), self.button_image, 'Rotate'),
				'pause' : Button((self.interspace+self.b_width, 150+4*self.b_height), self.button_image, 'Pause')
			}
		}

		# timer
		self.timers = {
			'mouse' : Timer(MOUSE_WAIT_TIME),
			'assign_keys' : Timer(PAUSE_WAIT_TIME)
		}

	def get_mouse(self):
		self.mouse_pos = pygame.mouse.get_pos()

	def timer_update(self):
		for timer in self.timers.values():
			timer.update()

	def display_text(self, pos, text):
		text_surface = self.font.render(text, True, 'black')
		text_rect = text_surface.get_rect(center = pos)
		self.surface.blit(text_surface, text_rect)

	# start
	def display_start_visuals(self):

		# buttons
		self.surface.blit(self.buttons['start'].image, self.buttons['start'].pos)
		self.display_text(self.buttons['start'].text_pos, self.buttons['start'].text)

		self.surface.blit(self.buttons['go_settings'].image, self.buttons['go_settings'].pos)
		self.display_text(self.buttons['go_settings'].text_pos, self.buttons['go_settings'].text)

		# logo
		self.surface.blit(self.logo, self.logo_pos)

	def check_start_buttons(self):

		if not self.timers['mouse'].active:
			if self.buttons['start'].clicked(self.mouse_pos):
				self.save_settings()
				self.started = True
				self.timers['mouse'].activate()

			if self.buttons['go_settings'].clicked(self.mouse_pos):
				self.in_settings = True
				self.timers['mouse'].activate()

	# settings
	def display_settings_visuals(self):

		# keyboard
		self.surface.blit(self.keyboard, self.keyboard_pos)

		# go back
		self.surface.blit(self.buttons['go_back'].image, self.buttons['go_back'].pos)

		# save
		self.surface.blit(self.buttons['save'].image, self.buttons['save'].pos)
		self.display_text(self.buttons['save'].text_pos, self.buttons['save'].text)

		# display describe and assign buttons
		for button in self.buttons['settings'].values():
			# describe_b
			self.surface.blit(button.image, (self.interspace, button.pos[1]))
			self.display_text((self.interspace+self.b_width/2, button.pos[1]+self.b_height/2), button.key)

			# assign_b
			self.surface.blit(button.image, button.pos)
			self.display_text(button.text_pos, button.text)

			# draws frame when collides with mouse
			if button.rect.collidepoint(self.mouse_pos) and not self.stopped:
				pygame.draw.rect(self.display_surface,RED,button.rect,3)

	def check_settings_buttons(self):
		if not self.stopped:

			if not self.timers['mouse'].active:
				if self.buttons['go_back'].clicked(self.mouse_pos):
					self.in_settings = False
					self.timers['mouse'].activate()

				if self.buttons['save'].clicked(self.mouse_pos):
					self.save_settings()
					self.timers['mouse'].activate()

				for button in self.buttons['settings'].values():
					if button.clicked(self.mouse_pos):
						self.assign_button = button
						self.stopped = True
						self.timers['mouse'].activate()

	def assign_key(self, button):
		pygame.draw.rect(self.display_surface,RED,button.rect,3)
		keys = pygame.key.get_pressed()

		if not self.timers['assign_keys'].active:
			for key in self.assign_keys:
				if keys[getattr(pygame,key)] and (key not in self.factory_settings.values()):
					self.factory_settings[button.key] = key
					button.text = pygame.key.name(getattr(pygame,key))
					self.stopped = False
					self.timers['assign_keys'].activate()
	
	def save_settings(self):
		self.update_settings(self.factory_settings)

	# run
	def run(self):

		# update
		self.get_mouse()
		self.timer_update()

		# draw
		self.display_surface.blit(self.surface, (0,0))
		self.surface.fill(BLACK)

		if not self.in_settings:

			self.display_start_visuals()
			self.check_start_buttons()

		if self.in_settings:

			self.display_settings_visuals()
			self.check_settings_buttons()

			if self.stopped: self.assign_key(self.assign_button)