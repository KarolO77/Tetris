from settings import *
from timer import Timer

from random import choice


class Game:
    def __init__(self, get_next_shape, update_score):

        # general
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(PADDING, PADDING))
        self.sprites = pygame.sprite.Group()

        # game connection
        self.get_next_shape = get_next_shape
        self.update_score = update_score

        # settings
        self.player_settings = None
        self.set_settings = False

        # frame
        self.frame_surface = pygame.Surface(
            (GAME_WIDTH + THICK_FRAME * 2, GAME_HEIGHT + THICK_FRAME * 2)
        )
        self.frame_rect = self.frame_surface.get_rect(
            topleft=(PADDING - THICK_FRAME, PADDING - THICK_FRAME)
        )

        # tetromino
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.tetromino = Tetromino(
            choice(list(TETROMINOS.keys())),
            self.sprites,
            self.create_new_tetromino,
            self.field_data,
        )

        # timer
        self.down_speed = UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False
        self.timers = {
            "vertical move": Timer(UPDATE_START_SPEED, True, self.move_down),
            "horizontal_move": Timer(MOVE_WAIT_TIME),
            "rotate": Timer(ROTATE_WAIT_TIME),
            "pause": Timer(PAUSE_WAIT_TIME),
            "mouse": Timer(MOUSE_WAIT_TIME),
        }
        self.timers["vertical move"].activate()

        # pause
        self.paused = False
        self.ended = False

        # score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0

    def calibrate_settings(self):
        if not self.set_settings and self.player_settings:
            self.k_left = getattr(pygame, self.player_settings["Left"])
            self.k_right = getattr(pygame, self.player_settings["Right"])
            self.k_down = getattr(pygame, self.player_settings["Down"])
            self.k_rotate = getattr(pygame, self.player_settings["Rotate"])
            self.k_pause = getattr(pygame, self.player_settings["Pause"])
            self.set_settings = True

    def restart(self):
        self.sprites.empty()
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.tetromino = Tetromino(
            choice(list(TETROMINOS.keys())),
            self.sprites,
            self.create_new_tetromino,
            self.field_data,
        )

        self.down_speed = UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.3
        self.timers["vertical move"].duration = self.down_speed

        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0
        self.update_score(self.current_lines, self.current_score, self.current_level)

    def calculate_score(self, num_lines):
        self.current_lines += num_lines
        self.current_score += SCORE_DATA[num_lines] * self.current_level

        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
            self.down_speed *= 0.8
            self.down_speed_faster = self.down_speed * 0.3
            self.timers["vertical move"].duration = self.down_speed

        self.update_score(self.current_lines, self.current_score, self.current_level)

    def check_game_over(self):
        for block in self.tetromino.blocks:
            if block.pos.y < 0:
                self.paused = True
                self.ended = True

    def create_new_tetromino(self):

        self.check_game_over()
        self.check_finished_rows()
        self.tetromino = Tetromino(
            self.get_next_shape(),
            self.sprites,
            self.create_new_tetromino,
            self.field_data,
        )

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        if not self.paused:
            self.tetromino.move_down()

    def draw_grid(self):

        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(
                self.surface, LINE_COLOR, (x, 0), (x, self.surface.get_height()), 1
            )

        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(
                self.surface, LINE_COLOR, (0, y), (self.surface.get_width(), y)
            )

        pygame.draw.rect(
            self.display_surface, FRAME_COLOR, self.frame_rect, THICK_FRAME, 3
        )

    def pressed_keys(self):
        keys = pygame.key.get_pressed()

        if not self.paused:

            # check horizontal movement
            if not self.timers["horizontal_move"].active:
                if keys[self.k_left]:
                    self.tetromino.move_horizontal(-1)
                    self.timers["horizontal_move"].activate()

                if keys[self.k_right]:
                    self.tetromino.move_horizontal(1)
                    self.timers["horizontal_move"].activate()

            # check rotation
            if not self.timers["rotate"].active:
                if keys[self.k_rotate]:
                    self.tetromino.rotate()
                    self.timers["rotate"].activate()

            # down speedup
            if not self.down_pressed and keys[self.k_down]:
                self.down_pressed = True
                self.timers["vertical move"].duration = self.down_speed_faster

            if self.down_pressed and not keys[self.k_down]:
                self.down_pressed = False
                self.timers["vertical move"].duration = self.down_speed

            # pause
            if not self.timers["pause"].active and keys[self.k_pause]:
                self.paused = True
                self.timers["pause"].activate()

        if self.paused and not self.ended:
            if not self.timers["pause"].active and keys[self.k_pause]:
                self.paused = False
                self.timers["pause"].activate()

    def check_finished_rows(self):
        # get the full row indexes
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)

        if delete_rows:
            for delete_row in delete_rows:

                # delete full rows
                for block in self.field_data[delete_row]:
                    block.kill()

                # move down blocks
                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1

            # rebuild the field data
            self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

            # update_score
            self.calculate_score(len(delete_rows))

    def run(self):
        self.calibrate_settings()  # checks only once when game is started

        # update
        self.pressed_keys()
        self.timer_update()
        self.sprites.update()

        # drawing
        self.surface.fill(BOARD_COLOR)
        self.sprites.draw(self.surface)

        # grid
        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))


class Tetromino:
    def __init__(self, shape, group, create_new_tetromino, field_data):
        self.shape = shape
        self.block_positions = TETROMINOS[shape]["shape"]
        self.color = TETROMINOS[shape]["color"]
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data

        # create blocks
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

    # collisions
    def next_move_horizontal_collide(self, blocks, amount):
        collision_list = [
            block.horizontal_collide(int(block.pos.x + amount), self.field_data)
            for block in self.blocks
        ]
        return True if any(collision_list) else False

    def next_move_vertical_collide(self, blocks, amount):
        collision_list = [
            block.vertical_collide(int(block.pos.y + amount), self.field_data)
            for block in self.blocks
        ]
        return True if any(collision_list) else False

    # movement
    def move_horizontal(self, amount):
        if not self.next_move_horizontal_collide(self.blocks, amount):
            for block in self.blocks:
                block.pos.x += amount

    def move_down(self):
        if not self.next_move_vertical_collide(self.blocks, 1):
            for block in self.blocks:
                block.pos.y += 1
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.create_new_tetromino()

    def rotate(self):
        if self.shape != "O":

            pivot_pos = self.blocks[0].pos
            new_block_pos = [block.rotate(pivot_pos) for block in self.blocks]

            for pos in new_block_pos:
                if pos.x < 0 or pos.x >= COLUMNS:
                    return

                if self.field_data[int(pos.y)][int(pos.x)]:
                    return

                if pos.y > ROWS:
                    return

            for index, block in enumerate(self.blocks):
                block.pos = new_block_pos[index]


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):

        # general
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        # position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft=self.pos * CELL_SIZE)

    def rotate(self, pivot_pos):
        return pivot_pos + (self.pos - pivot_pos).rotate(90)

    def horizontal_collide(self, x, field_data):
        if not 0 <= x < COLUMNS:
            return True

        if field_data[int(self.pos.y)][x]:
            return True

    def vertical_collide(self, y, field_data):
        if y >= ROWS:
            return True

        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True

    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE
