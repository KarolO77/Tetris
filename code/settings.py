import pygame

# game size
COLUMNS = 12
ROWS = 20
CELL_SIZE = 45
THICK_FRAME = 4
GAME_WIDTH, GAME_HEIGHT = COLUMNS * CELL_SIZE, ROWS * CELL_SIZE

# side bar size
SIDE_BAR_WIDTH = 225
PREVIEW_HEIGHT_FRACTION = 0.7
SCORE_HEIGHT_FRACTION = 1 - PREVIEW_HEIGHT_FRACTION

# window
PADDING = 20
WINDOW_WIDTH = GAME_WIDTH + SIDE_BAR_WIDTH + PADDING * 3
WINDOW_HEIGHT = GAME_HEIGHT + PADDING * 2

# game behaviour
UPDATE_START_SPEED = 300
MOVE_WAIT_TIME = 150
ROTATE_WAIT_TIME = 150
PAUSE_WAIT_TIME = 300
MOUSE_WAIT_TIME = 400
BLOCK_OFFSET = pygame.Vector2(COLUMNS // 2 , -1)

# colors
CYAN = '#33FFFF'
BLUE = '#0000FF'
ORANGE = '#FF8000'
YELLOW = '#FFFF33'
GREEN = '#33FF33'
PURPLE = '#9933FF'
RED = '#FF0000'
GRAY = '#606060'
BLACK = '#111111'
BOARD_COLOR = '#202020'
LINE_COLOR = '#303030'
FRAME_COLOR = '#D0D0D0'
PAUSE_BOARD_COLOR = (100,0,0,40)

# shapes
TETROMINOS = {
    'I' : {'shape' : [(0,0),(0,1),(0,-1),(0,-2)], 'color' :  CYAN},
    'J' : {'shape' : [(0,0),(-1,1),(0,1),(0,-1)], 'color' :  BLUE},
    'L' : {'shape' : [(0,0),(0,-1),(0,1),(1,1)], 'color' :  ORANGE},
    'O' : {'shape' : [(0,0),(1,-1),(0,-1),(1,0)], 'color' :  YELLOW},
    'S' : {'shape' : [(0,0),(-1,0),(0,-1),(1,-1)], 'color' :  GREEN},
    'T' : {'shape' : [(0,0),(1,0),(0,-1),(-1,0)], 'color' :  PURPLE},
    'Z' : {'shape' : [(0,0),(-1,-1),(0,-1),(1,0)], 'color' :  RED}
    }

SCORE_DATA = {
    1 : 20, 
    2 : 60,
    3 : 100,
    4 : 200
    }